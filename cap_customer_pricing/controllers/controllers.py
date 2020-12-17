# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class ClientPricingWeb(http.Controller):

    @http.route('/customer_pricing', type="http", auth='public', website=True)
    def pricing_webform(self):
        Modules = http.request.env['cap_customer_pricing.module']
        return http.request.render('cap_customer_pricing.pricing_template', {
            'modules': Modules.sudo().search([])
        })

    @http.route('/customer_pricing/submitted', type="http", auth='public', website=True)
    def pricing_submitted(self, **kw):
        if int(kw['num_users']) > 50:
            return request.redirect('/customer_pricing/contact_us')

        pricing = {
            'name': kw['company_name'],
            'company_name': kw['company_name'],
            'phone_number': kw['phone_number'],
            'email': kw['email'],
            'num_users': kw['num_users'],
        }

        pricing_saved = request.env['cap_customer_pricing.pricing'].sudo(
                ).create(pricing)

        for value in kw:
            if value.startswith('module'):
                estimate_line = {
                    'estimate_id': pricing_saved.id,
                    'module_id': kw[value],
                }
                request.env['cap_customer_pricing.line'].sudo().create(
                    estimate_line)

        return request.redirect('/customer_pricing/results')

    @http.route('/customer_pricing/contact_us', type="http", auth='public', website=True)
    def pricing_contact(self, **kw):
        return http.request.render('cap_customer_pricing.contact_us', {})

    @http.route('/customer_pricing/customer_pricing/results', type="http", auth='public', website=True)
    def pricing_result(self, pricing_saved_id):

        return request.render('cap_customer_pricing.results', {
            'pricing': pricing_saved_id
        })