# -*- coding: utf-8 -*-

from openerp import api, fields, models




class Lead(models.Model):
    _inherit = 'crm.lead'


    property_id = fields.Many2one('orealestate.realestate', string='Property', help='Linked property.')
    mandate = fields.Boolean('Is a mandate', readonly=True)
    property_account_manager = fields.Many2one(related='property_id.user_id', string='Account manager')




class realestate(models.Model):
    """Real Estate property description."""


    _description = 'Property'
    _name = 'orealestate.realestate'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherits = {'crm.lead': 'opportunity_id'}


    def open_map(self, cr, uid, ids, context=None):
        """Open new tab in google maps to show the property in the map."""
        if context is None:
            context = {}
        partner = self.browse(cr, uid, ids, context=context)[0]
        url="http://maps.google.com/maps?oi=map&q="
        if partner.street:
            url+=partner.street.replace(' ','+')
        if partner.city:
            url+='+'+partner.city.replace(' ','+')
        if partner.country_id:
            url+='+'+partner.country_id.name.replace(' ','+')
        if partner.zip:
            url+='+'+partner.zip.replace(' ','+')
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new'
        }


    def open_journey(self, cr, uid, ids, context=None):
        """New ininerance on google maps."""
        if context is None:
            context = {}
        user_obj = self.pool.get('res.users')
        company = user_obj.browse(cr, uid,uid, context=context).company_id
        partner = self.browse(cr, uid, ids, context=context)[0]
        url="http://maps.google.com/maps?saddr="
        if company.street:
            url+=company.street.replace(' ','+')
        if company.city:
            url+='+'+company.city.replace(' ','+')
        if company.country_id:
            url+='+'+company.country_id.name.replace(' ','+')
        if company.zip:
            url+='+'+company.zip.replace(' ','+')
        url+="&daddr="
        if partner.street:
            url+=partner.street.replace(' ','+')
        if partner.city:
            url+='+'+partner.city.replace(' ','+')
        if partner.country_id:
            url+='+'+partner.country_id.name.replace(' ','+')
        if partner.zip:
            url+='+'+partner.zip.replace(' ','+')
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new'
        }


    @api.multi
    def _compute_opportunity_count(self):
        for record in self:
            record.opportunity_count = len(record.opportunity_ids)


    id = fields.Integer('ID', readonly=True)
    opportunity_id = fields.Many2one('crm.lead', 'Related mandate', readonly=True, required=True, ondelete="cascade")
    internal_note = fields.Text(string='Internal note')
    opportunity_ids = fields.One2many('crm.lead', 'property_id', string='Opportunities', readonly=True)
    opportunity_count = fields.Integer('opportunity count', compute = '_compute_opportunity_count')
    composition_ids = fields.One2many('orealestate.composition', 'composition_id', string='Property composition', help='Describe each room of the property and their total area.')
    realestate_id = fields.Many2one('orealestate.property', string='Property kind', help='What kind of property is it?', required=True)
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High')],'Priority', default='0')
    living_area = fields.Integer('Living area (m²)', help='What is the total surface area of the property?')
    land_area = fields.Integer('Land area (m²)', help='What is the total area of the land?')
    room_number = fields.Integer('Number of rooms', help='How many rooms there are in this property?')
    residence = fields.Char()
    sign = fields.Boolean('Sign ?')
    keys = fields.Boolean('Keys ?')

    _defaults = {
        'mandate': True,
        'team_id': api.model(lambda self: self.env.ref('orealestate.orealestate_mandate_team').id),        
    }




class composition(models.Model):
    """Composition is to Specify the rooms of a property."""


    _description = 'Room description'
    _name = 'orealestate.composition'


    name = fields.Char(string='Area description', required=True)
    area_id = fields.Many2one('orealestate.area', string='Area', required=True)
    surface = fields.Integer(string='Area size (m2)')
    composition_id = fields.Many2one('orealestate.realestate', required=True, ondelete="cascade")




class area(models.Model):
    """Types of areas"""


    _name = 'orealestate.area'
    _order = 'name'


    name = fields.Char(string='Area', required=True, translate=True)


    _sql_constraints = [
               ('name_uniq',
                'UNIQUE (name)',
                'Area name must be unique!')
    ]




class property(models.Model):
    """Property kind. The name of this object is not perfect.. """


    _name = "orealestate.property"


    name = fields.Char(string='property kind', required=True, translate=True)
