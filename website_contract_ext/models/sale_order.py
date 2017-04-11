# -*- coding: utf-8 -*-
# Copyright 2017 Rooms For (Hong Kong) Limited T/A OSCG
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


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

    @api.multi
    def action_confirm(self):
        for order in self:
            order.assign_contract_template()
        return super(SaleOrder, self).action_confirm()
