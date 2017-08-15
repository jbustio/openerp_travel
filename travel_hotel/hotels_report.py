# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010, 2014 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo.osv import fields
import odoo.osv as osv
from odoo.tools.translate import _
from odoo import tools


class hotels_report(osv.osv.osv):
    _name = "hotels.report"
    _auto = False
    _description = "Hotels Report"

    _columns = {
        'name': fields.Char(_('Name')),
        'start_date': fields.Date(_('Start Date'), readonly=True),
        'end_date': fields.Date(_('End Date'), readonly=True),
        'room': fields.Many2one('option.value', _('Room'),
                                domain="[('option_type_id.code', '=', 'rt')]"),
        'plan': fields.Many2one('option.value', _('Plan'),
                                domain="[('option_type_id.code', '=', 'mp')]"),
        'simple': fields.Float(_('Simple'), readonly=True),
        'double': fields.Float(_('Double'), readonly=True),
        'supplier': fields.Many2one('res.partner', _('Supplier'), readonly=True),
        'triple': fields.Float(_('Triple'), readonly=True),
        'extra_adult': fields.Float(_('Extra Adult'), readonly=True),
        'child': fields.Float(_('Child'), readonly=True),
        'second_child': fields.Float(_('Second Child'), readonly=True)
    }
    _order = 'start_date asc'

    def _select(self):
        select_str = """
             SELECT min(p.id) as id,
              r.start_date as start_date,
              pt.name as name,
             r.end_date as end_date,
             r.room_type_id as room,
             r.meal_plan_id as plan,
             r.simple as simple,
             r.triple as triple,
             r.extra_adult as extra_adult,
             r.child as child,
             r.second_child as second_child,
             l.name as supplier,
             p.price as double
        """
        return select_str

    def _from(self):
        from_str = """
                product_hotel h join product_product pp on (pp.id=h.product_id)
                join product_template pt on (pt.id=pp.product_tmpl_id)
                 join (product_supplierinfo l join pricelist_partnerinfo p on (p.suppinfo_id=l.id)
                join product_rate r on(p.product_rate_id=r.id))
                on (pt.id=l.product_tmpl_id)
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                r.start_date,
                pt.name,
                r.end_date,
                r.room_type_id,
                r.meal_plan_id,
                r.simple,
                r.triple,
                r.extra_adult,
                r.child,
                r.second_child,
                l.name,
                p.price
        """
        return group_by_str

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
