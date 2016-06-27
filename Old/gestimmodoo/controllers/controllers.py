# -*- coding: utf-8 -*-
from openerp import http

class Gestimmodoo(http.Controller):
    @http.route('/gestimmodoo/gestimmodoo/', auth='public', website=True)
    def index(self, **kw):
        return "Hello, world"

    @http.route('/gestimmodoo/gestimmodoo/objects/', auth='public', website=True)
    def list(self, **kw):
        return http.request.render('gestimmodoo.listing', {
            'root': '/gestimmodoo/gestimmodoo',
            'objects': http.request.env['gestimmodoo.gestimmodoo'].search([]),
        })

    @http.route('/gestimmodoo/gestimmodoo/objects/<model("gestimmodoo.gestimmodoo"):obj>/', auth='public', website=True)
    def object(self, obj, **kw):
        return http.request.render('gestimmodoo.object', {
            'object': obj
        })