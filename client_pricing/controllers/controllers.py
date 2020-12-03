# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class ClientPricingWeb(http.Controller):

    @http.route('/client_pricing', type="http", auth='public', website=True)
    def pricing_webform(self, **kw):
        Modules = http.request.env['client_pricing.module']
        return http.request.render('client_pricing.pricing_template', {
            'modules': Modules.sudo().search([])
        })

    @http.route('/client_pricing/submitted', type="http", auth='public',
        website=True)
    def pricing_submitted(self, **kw):
        if int(kw['num_users']) > 50:
            return request.redirect('/client_pricing/contact_us')

        pricing = {
            'name': kw['company_name'],
            'company_name': kw['company_name'],
            'phone_number': kw['phone_number'],
            'email': kw['email'],
            'num_users': kw['num_users'],
        }

        pricing_saved = request.env['client_pricing.pricing'].sudo(
                ).create(pricing)

        for value in kw:
            if value.startswith('module'):
                estimate_line = {
                    'estimate_id': pricing_saved.id,
                    'module_id': kw[value],
                }
                request.env['client_pricing.line'].sudo().create(
                    estimate_line)

        return request.render('client_pricing.submitted', {
            'pricing': request.env['client_pricing.pricing'].sudo().browse(
                pricing_saved.id)
        })

    @http.route('/client_pricing/contact_us', type="http", auth='public',
        website=True)
    def pricing_contact(self, **kw):
        return http.request.render('client_pricing.contact_us', {})
