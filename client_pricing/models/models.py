# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)



class ClientPricing(models.Model):
    _name = 'client_pricing.pricing'

    name = fields.Char('Name')
    company_name = fields.Char('Company Name')
    phone_number = fields.Char('Phone Number')
    email = fields.Char('Email')
    num_users = fields.Integer('Number of Users')
    estimate_lines = fields.One2many('client_pricing.line', 'estimate_id', string='Estimate Lines')
    module_hours = fields.Integer('Module Hours', compute='_compute_hours', store=True)
    license_cost = fields.Integer('License Cost', compute='_compute_costs', store=True)
    implemen_cost = fields.Integer('Implementation Cost')
    mainte_cost = fields.Integer('Maintenance Cost')
    year_1_cost = fields.Integer('Year 1 Cost')
    year_2_cost = fields.Integer('Year 2 Cost')


    @api.depends('estimate_lines.price')
    def _compute_hours(self):
        for record in self:
            lines = record.estimate_lines
            total = 0
            for line in lines:
                total += line.price
                # _logger.warning(' ##########')
                # _logger.warning(line.price)
            record.module_hours = total

    @api.depends('module_hours')
    def _compute_costs(self):
        for record in self:
            record.implemen_cost = record.num_users * 125
            record.mainte_cost = record.implemen_cost * 0.2
            record.license_cost = (record.num_users * 24 * 12) + record.module_hours
            record.year_1_cost = record.license_cost + record.implemen_cost
            record.year_2_cost = record.license_cost + record.mainte_cost
            #self.to_opp()

    def to_opp(self):
        # partner = self.env['res.partner'].create({
        #     'name': 'self.company_name',
        # })
        self.env['crm.lead'].create({
                'name': self.company_name,
                'type': 'lead',
                'email_from': self.email,
                })


class ClientPricingLines(models.Model):
    _name = 'client_pricing.line'

    estimate_id = fields.Many2one('client_pricing.pricing', string='Estimate id')
    module_id = fields.Many2one('client_pricing.module', string='modules')
    price = fields.Integer(compute='_compute_price')

    @api.depends('estimate_id.num_users', 'module_id.est_user_range')
    def _compute_price(self):
        for record in self:
            num_users = record.estimate_id.num_users
            user_ranges = record.module_id.est_user_range
            price = 0

            _logger.warning('####USER_RANGE####')
            _logger.warning(user_ranges.ids)
            for user_range in user_ranges:
                if num_users >= user_range.num_users:
                    price = user_range.num_hours
            _logger.warning('####PRICE#####')
            _logger.warning(price)
            record.price = price


class ClientModule(models.Model):
    _name = 'client_pricing.module'

    est_user_range = fields.One2many('client_pricing.user_range', 'module_id', string='module id')
    name = fields.Char()



class ClientUserRange(models.Model):
    _name = 'client_pricing.user_range'

    module_id = fields.Many2one('client_pricing.module', string='Estimate module')
    num_users = fields.Integer()
    num_hours = fields.Integer()
