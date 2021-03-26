# -*- coding: utf-8 -*-
# from odoo import http


# class WiInvoiceDue(http.Controller):
#     @http.route('/wi_invoice_due/wi_invoice_due/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wi_invoice_due/wi_invoice_due/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wi_invoice_due.listing', {
#             'root': '/wi_invoice_due/wi_invoice_due',
#             'objects': http.request.env['wi_invoice_due.wi_invoice_due'].search([]),
#         })

#     @http.route('/wi_invoice_due/wi_invoice_due/objects/<model("wi_invoice_due.wi_invoice_due"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wi_invoice_due.object', {
#             'object': obj
#         })
