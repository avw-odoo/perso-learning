# -*- coding: utf-8 -*-

from openerp import models, fields, api

class gestimmodoo(models.Model):
    """Properties management for real estate. Property
    is based on partner model.

    """
    _name = 'gestimmodoo.gestimmodoo'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherits = {'res.partner': 'partner_id'}

    
    @api.model # Find the tag 'property' (partner category_id) based on it's XML id
    def _default_category_id(self):
        return [self.env.ref('gestimmodoo.res_partner_category_property').id]


    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete="cascade")
    composition_ids = fields.One2many('composition.composition', 'composition_id', string='Room composition')
    property_kind = fields.Selection(selection=[('villa', 'Villa'),('house', 'House'),('apartment', 'Apartment'),('land', 'Land')], required=True, string='Property kind', help="Specify the property kind")
    account_manager = fields.Many2one('res.users', string='Account manager', index=True, track_visibility='onchange', default=lambda self: self.env.user)


    _defaults = {
        'is_company': True,
        'company_type': 'company',
        # Another deprecated solution to fill default tag on partner --> 'category_id': lambda self, cr, uid, *args, **kwargs: [self.pool.get('ir.model.data').xmlid_to_res_id(cr, uid, 'gestimmodoo.res_partner_category_property')],
        'category_id': _default_category_id,
    }


class composition(models.Model):
    """Composition is to Specify the rooms of a property.

    """
    _description = 'room composition'
    _name = 'composition.composition'


    name = fields.Char(string='Room description')
    room_type = fields.Selection(selection=[('hall', 'Hall'),('kitchen', 'Kitchen'),('bedroom', 'Bedroom'),('miam', 'Miam miam room'),('other', 'Other')], required=True, string='Room kind', help="Some help please")
    surface = fields.Float(string='Room surface (m2)')
    composition_id = fields.Many2one('gestimmodoo.gestimmodoo', required=True, ondelete="cascade")