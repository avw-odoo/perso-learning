# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging


logger = logging.getLogger(__name__)


class PropertyType(models.Model):
    """ The type of property """
    _name = 'property.type'

    name = fields.Char('Type', required=True)
    meta_type = fields.Char('Kind of type', required=True)
    description = fields.Text('Description')
        


class Property(models.Model):
    """ Property for sale """
    _name = 'property'
    _description = 'Property for sale'
    _inherit = ['mail.thread']

    name = fields.Char('Reference', required=True, track_visibility='onchange')
    street = fields.Char(track_visibility='onchange')
    street2 = fields.Char(track_visibility='onchange')
    zip = fields.Char(change_default=True, track_visibility='onchange')
    city = fields.Char(track_visibility='onchange')
    state_id = fields.Many2one("res.country.state", string='State', track_visibility='onchange', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', track_visibility='onchange', ondelete='restrict')
    active = fields.Boolean(default=True, track_visibility='onchange')
    attachment_number = fields.Integer(compute='_get_attachment_number', string="Number of Attachments")
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'property')], string='Attachments')
    property_type_id = fields.Many2one('property.type', string='Property type', help='The type of property', required=True)


    @api.multi
    def _address_as_string(self):
        self.ensure_one()
        addr = []
        if self.street:
            addr.append(self.street)
        if self.street2:
            addr.append(self.street2)
        if self.city:
            addr.append(self.city)
        if self.state_id:
            addr.append(self.state_id.name)
        if self.country_id:
            addr.append(self.country_id.name)
        if not addr:
            raise UserError(_("Address missing on partner '%s'.") % self.name)
        return ' '.join(addr)

    @api.model
    def _prepare_url(self, url, replace):
        assert url, 'Missing URL'
        for key, value in replace.iteritems():
            if not isinstance(value, (str, unicode)):
                # for latitude and longitude which are floats
                value = unicode(value)
            url = url.replace(key, value)
        logger.debug('Final URL: %s', url)
        return url

    @api.multi
    def open_map(self):
        self.ensure_one()
        map_website = self.env.user.context_map_website_id
        if not map_website:
            raise UserError(
                _('Missing map provider: '
                  'you should set it in your preferences.'))
        if (map_website.lat_lon_url and hasattr(self, 'partner_latitude') and
                self.partner_latitude and self.partner_longitude):
            url = self._prepare_url(
                map_website.lat_lon_url, {
                    '{LATITUDE}': self.partner_latitude,
                    '{LONGITUDE}': self.partner_longitude})
        else:
            if not map_website.address_url:
                raise UserError(
                    _("Missing parameter 'URL that uses the address' "
                      "for map website '%s'.") % map_website.name)
            url = self._prepare_url(
                map_website.address_url,
                {'{ADDRESS}': self._address_as_string()})
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    @api.multi
    def open_route_map(self):
        self.ensure_one()
        if not self.env.user.context_route_map_website_id:
            raise UserError(
                _('Missing route map website: '
                  'you should set it in your preferences.'))
        map_website = self.env.user.context_route_map_website_id
        if not self.env.user.context_route_start_partner_id:
            raise UserError(
                _('Missing start address for route map: '
                  'you should set it in your preferences.'))
        start_partner = self.env.user.context_route_start_partner_id
        if (map_website.route_lat_lon_url and
                hasattr(self, 'partner_latitude') and
                self.partner_latitude and self.partner_longitude and
                start_partner.partner_latitude and
                start_partner.partner_longitude):
            url = self._prepare_url(  # pragma: no cover
                map_website.route_lat_lon_url, {
                    '{START_LATITUDE}': start_partner.partner_latitude,
                    '{START_LONGITUDE}': start_partner.partner_longitude,
                    '{DEST_LATITUDE}': self.partner_latitude,
                    '{DEST_LONGITUDE}': self.partner_longitude})
        else:
            if not map_website.route_address_url:
                raise UserError(
                    _("Missing route URL that uses the addresses "
                        "for the map website '%s'") % map_website.name)
            url = self._prepare_url(
                map_website.route_address_url, {
                    '{START_ADDRESS}': start_partner._address_as_string(),
                    '{DEST_ADDRESS}': self._address_as_string()})
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    @api.multi
    def _get_attachment_number(self):
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'property'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attach_data = dict((res['res_id'], res['res_id_count']) for res in read_group_res)
        for record in self:
            record.attachment_number = attach_data.get(record.id, 0)

    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        return action