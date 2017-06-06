# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request


class Payment_Receipt(http.Controller):
    
    @http.route(['/website_invoice/print/<model("account.invoice"):invoice>'],
            type='http', auth="public", website=True)
    def print_invoice(self, invoice):
        if invoice:
            pdf = request.env['report'].sudo().get_pdf(
                [invoice.id],
                'invoice_payment_receipt.invoice_payment_receipt_report_id'
            )
            pdfhttpheaders = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(pdf))
            ]
            return request.make_response(pdf, headers=pdfhttpheaders)
