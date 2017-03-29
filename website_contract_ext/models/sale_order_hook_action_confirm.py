# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api
from odoo.addons.website_contract.models.sale_order import SaleOrder


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.one
    def assign_contract_template(self):
        stl_obj = self.env['sale.subscription.template.line']
        st_obj = self.env['sale.subscription.template']
        product_id = self.order_line[0].product_id
        active_st_ids = [r.id for r in st_obj.search([('active', '=', True)])]
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


class SaleOrderHookActionConfirm(models.AbstractModel):
    _name = 'sale.order.hook.action.confirm'
    _description = 'Provide hook point for action_confirm method'

    def _register_hook(self):
        SaleOrder.action_confirm = action_confirm
        return super(SaleOrderHookActionConfirm, self)._register_hook()
