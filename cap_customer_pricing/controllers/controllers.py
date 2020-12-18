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

    @http.route('/customer_pricing/submitted', type="http", auth='public', methods=['POST'] website=True)
    def pricing_submitted(self, **kwargs):
        if int(kwargs['num_users']) > 50:
            return request.redirect('/customer_pricing/contact_us')

        pricing = {
            'name': kwargs['company_name'],
            'company_name': kwargs['company_name'],
            'phone_number': kwargs['phone_number'],
            'email': kwargs['email'],
            'num_users': kwargs['num_users'],
        }

        pricing_saved = request.env['cap_customer_pricing.pricing'].sudo(
                ).create(pricing)

        for value in kwargs:
            if value.startswith('module'):
                estimate_line = {
                    'estimate_id': pricing_saved.id,
                    'module_id': kwargs[value],
                }
                request.env['cap_customer_pricing.line'].sudo().create(
                    estimate_line)

        return request.redirect('/customer_pricing/results/%d' % (pricing_saved.id))

    @http.route('/customer_pricing/contact_us', type="http", auth='public', website=True)
    def pricing_contact(self):
        return http.request.render('cap_customer_pricing.contact_us', {})

    @http.route('/customer_pricing/results/<int:pricing_id>', type="http", auth='public', website=True)
    def pricing_result(self, pricing_id):

        return request.render('cap_customer_pricing.results', {
            'pricing': pricing_id
        })