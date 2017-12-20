# -*- coding: utf-8 -*-
# Copyright 2017 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Print Invoice Payment Receipt - Portal',
    'summary': 'Allows customers to print invoice receipts from portal page.',
    'version':'10.0.1.0.1',
    'license': 'LGPL-3',
    'category':'Website',
    'description': """
This module allows your customers to print invoice receipts from portal page.
This module depends on invoice_payment_receipt - a private module by Probuse
Consulting Service Pvt. Ltd.
            """,
    'author' : 'Quartile Limited',
    'website': 'https://www.odoo-asia.com',
    'depends': [
        'website_portal_sale',
        'invoice_payment_receipt',
    ],
    'data':[
        'views/website_portal_sale_templates.xml',
    ],
    'installable': True,
    'application': False,
}
