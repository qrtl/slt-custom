# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # def _get_default_contract_template_id(self):
    #     # res = 0
    #     ct_obj = self.env['sale.subscription.template']
    #     ct_recs = ct_obj.search([('name','=','Odoo Quarterly')])
    #     if ct_recs:
    #         return ct_recs[0].id
    #     # return res
    #     # return self.env.ref('website_quote.website_quote_template_default', raise_if_not_found=False)
    #
    # # template_id = fields.Many2one(
    # #     'sale.quote.template', 'Quotation Template',
    # #     default=_get_default_template_id, readonly=True,
    # #     states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    #
    #
    # contract_template = fields.Many2one(
    #     'sale.subscription.template',
    #     'Contract Template',
    #     default=_get_default_contract_template_id,
    #     help="If set, all recurring products in this Sales Order will be "
    #          "included in a new Subscription with the selected template"
    # )


    @api.one
    def assign_contract_template(self):
        stl_obj = self.env['sale.subscription.template.line']
        product_id = self.order_line[0].product_id
        st_obj = self.env['sale.subscription.template']
        active_st_recs = st_obj.search([
            ('active', '=', True)
        ])
        active_st_ids = [rec.id for rec in active_st_recs]
        stl_recs = stl_obj.search([
            ('product_id', '=', product_id.id),
            ('subscription_template_id', 'in', active_st_ids),
        ])
        if stl_recs:
            self.contract_template = stl_recs[0].subscription_template_id.id

    @api.one
    def action_confirm(self):
        if self.subscription_id and any(
                self.order_line.mapped('product_id').mapped('recurring_invoice')):
            lines = self.order_line.filtered(
                lambda s: s.product_id.recurring_invoice)
            msg_body = self.env.ref(
                'website_contract.chatter_add_paid_option').render(
                values={'lines': lines})
            # done as sudo since salesman may not have write rights on subscriptions
            self.subscription_id.sudo().message_post(body=msg_body,
                                                     author_id=self.env.user.partner_id.id)

        self.assign_contract_template()  # OSCG add

        sub = self.create_contract()
        return super(SaleOrder,
                     self.with_context(create_contract=bool(sub))).action_confirm()
