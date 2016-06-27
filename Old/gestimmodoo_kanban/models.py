from openerp import models, fields

class gestimmodoo(models.Model):
  _inherit = 'gestimmodoo.gestimmodoo'
  priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High')],'Priority', default='0')
  kanban_state = fields.Selection([('normal', 'In Progress'),('blocked', 'Blocked'),('done', 'Ready for next stage')],'Kanban State', default='normal')