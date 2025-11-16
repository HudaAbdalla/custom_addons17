# -*- coding: utf-8 -*-
# from odoo import http


# class CleopatraHospital(http.Controller):
#     @http.route('/cleopatra_hospital/cleopatra_hospital', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cleopatra_hospital/cleopatra_hospital/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cleopatra_hospital.listing', {
#             'root': '/cleopatra_hospital/cleopatra_hospital',
#             'objects': http.request.env['cleopatra_hospital.cleopatra_hospital'].search([]),
#         })

#     @http.route('/cleopatra_hospital/cleopatra_hospital/objects/<model("cleopatra_hospital.cleopatra_hospital"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cleopatra_hospital.object', {
#             'object': obj
#         })

