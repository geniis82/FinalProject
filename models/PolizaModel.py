from odoo import models,fields,api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class PolizaModel(models.Model):
    _name ='final_project.polizamodel'
    _description='Poliza Model'

    name = fields.Integer(string='Poliza ID', default=lambda self: self.setRef(),readonly=True)
    dataInicio = fields.Date(string='Fecha de inicio', default=lambda self: datetime.today(),readonly=True)
    dataFinal = fields.Date(string='Fecha de finalización', compute='_compute_fecha_final', store=True)

    vehiculo_id = fields.Many2one('final_project.vehiculosmodel', string="Vehículo Asociado",ondelete='cascade')
    usuario= fields.Many2one('final_project.usuariomodel',string="Usuario Asociado",ondelete='cascade')
    aseguradora_id=fields.Many2one('final_project.aseguradoramodel',string='Aseguradora Asociada')

    used_vehicles = fields.Many2many('final_project.vehiculosmodel', string="Vehículos con Póliza")
    usuarios_disponibles_para_poliza_ids = fields.Many2many('final_project.usuariomodel', compute='_compute_usuarios_disponibles_para_poliza')


    @api.depends('vehiculo_id')
    def _compute_usuarios_disponibles_para_poliza(self):
        vehiculos_sin_poliza = self.env['final_project.vehiculosmodel'].search([('poliza_ids', '=', False)])
        self.usuarios_disponibles_para_poliza_ids = vehiculos_sin_poliza.mapped('usuario.id')

    @api.onchange('usuario')
    def _onchange_usuario(self):
        if self.usuario:
            # Calcular los vehículos utilizados
            used_vehicles = self.env['final_project.polizamodel'].search([('usuario', '=', self.usuario.id)]).mapped('vehiculo_id.id')
            self.used_vehicles = [(6, 0, used_vehicles)]

    @api.depends('dataInicio')
    def _compute_fecha_final(self):
        for record in self:
            # Agregar un año a la fecha de inicio
            fecha_final = fields.Date.from_string(record.dataInicio) + relativedelta(years=1)
            record.dataFinal = fecha_final

    def setRef(self):
        result = self.env['final_project.polizamodel'].search_read([])
        if len(result) == 0:
            return 1
        else:
            return result[-1]["name"] + 1