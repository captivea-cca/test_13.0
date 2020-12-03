# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID


class Task(models.Model):
    _inherit = "project.task"

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)
