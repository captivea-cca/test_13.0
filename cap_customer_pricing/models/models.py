# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class CustomerPricing(models.Model):
    _name = 'cap_customer_pricing.pricing'

    name = fields.Char('Name')
    company_name = fields.Char('Company Name')
    phone_number = fields.Char('Phone Number')
    email = fields.Char('Email')
    num_users = fields.Integer('Number of Users')
    line_ids = fields.One2many('cap_customer_pricing.line', 'estimate_id', string='Estimate Lines')
    module_hours = fields.Integer('Module Hours', compute='_compute_hours', store=True)
    license_cost = fields.Integer('License Cost', compute='_compute_costs', store=True)
    implemen_cost = fields.Integer('Implementation Cost')
    mainte_cost = fields.Integer('Maintenance Cost')
    year_1_cost = fields.Integer('Year 1 Cost')
    year_2_cost = fields.Integer('Year 2 Cost')


    @api.depends('line_ids.price')
    def _compute_hours(self):
        for record in self:
            lines = record.line_ids
            total = 0
            _logger.warning("Outside line for loop")
            _logger.warning(lines)

            for line in lines:
                _logger.warning("Inside line for loop")
                _logger.warning(line.price)
                total += line.price
            record.module_hours = total

    @api.depends('module_hours')
    def _compute_costs(self):
        for record in self:
            record.implemen_cost = record.num_users * 125
            record.mainte_cost = record.implemen_cost * 0.2
            record.license_cost = (record.num_users * 24 * 12) + record.module_hours
            record.year_1_cost = record.license_cost + record.implemen_cost
            record.year_2_cost = record.license_cost + record.mainte_cost

    def to_opp(self):
        self.env['crm.lead'].create({
                'name': self.company_name,
                'type': 'lead',
                'email_from': self.email,
                })


class CustomerPricingLines(models.Model):
    _name = 'cap_customer_pricing.line'

    estimate_id = fields.Many2one('cap_customer_pricing.pricing', string='Estimate id')
    module_id = fields.Many2one('cap_customer_pricing.module', string='modules')
    price = fields.Integer(compute='_compute_price')

    @api.depends('estimate_id.num_users', 'module_id.user_range_ids')
    def _compute_price(self):
        for record in self:
            num_users = record.estimate_id.num_users
            user_ranges = record.module_id.user_range_ids
            price = 0
            _logger.warning("Outside user range for loop")
            for user_range in user_ranges:
                _logger.warning("Inside user range for loop")
                _logger.warning(user_ranges)
                _logger.warning(user_range.num_hours)
                _logger.warning("End of user range for loop")
                if num_users >= user_range.num_users:
                    price = user_range.num_hours
            record.price = price


class CustomerModule(models.Model):
    _name = 'cap_customer_pricing.module'

    user_range_ids = fields.One2many('cap_customer_pricing.user_range', 'module_id', string='module id')
    name = fields.Char()



class CustomerUserRange(models.Model):
    _name = 'cap_customer_pricing.user_range'

    module_id = fields.Many2one('cap_customer_pricing.module', string='Estimate module')
    num_users = fields.Integer()
    num_hours = fields.Integer()
