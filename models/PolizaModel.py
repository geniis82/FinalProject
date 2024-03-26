from odoo import models,fields,api
from datetime import datetime

class PolizaModel(models.Model):
    _name ='final_project.polizamodel'
    _description='Poliza Model'

    name = fields.Integer(string='Poliza ID', default=lambda self: self.setRef(),readonly=True)
    data = fields.Date(string='Invoice Date', default=lambda self: datetime.today(),readonly=True)
    vehiculo_id = fields.Many2one('final_project.vehiculosmodel', string="Vehículo Asociado")
    usuario= fields.Many2one('final_project.usuariomodel',string="Usuario Asociado")
    aseguradora_id=fields.Many2one('final_project.aseguradoramodel',string='Aseguradora Asociada')

    used_vehicles = fields.Many2many('final_project.vehiculosmodel', string="Vehículos con Póliza")
    
    @api.onchange('usuario')
    def _onchange_usuario(self):
        if self.usuario:
            # Calcular los vehículos utilizados
            used_vehicles = self.env['final_project.polizamodel'].search([('usuario', '=', self.usuario.id)]).mapped('vehiculo_id.id')
            self.used_vehicles = [(6, 0, used_vehicles)]

    def setRef(self):
        result = self.env['final_project.polizamodel'].search_read([])
        if len(result) == 0:
            return 1
        else:
            return result[-1]["name"] + 1