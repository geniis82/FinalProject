from odoo import models,fields,api
from odoo.exceptions import ValidationError
import re

class VehiculosModel(models.Model):
    _name ='final_project.vehiculosmodel'
    _description='Vehiculos Model'
    _sql_constraints=[
        ('_mat_uniq',
        'UNIQUE (name)',
        'No se pueden guardar 2 vehiculos con la misma matricula'),    
        
    ]

    name=fields.Char(string="Matricula",required=True)
    marca=fields.Char(string="Marca",required=True,index=True)
    modelo =fields.Char(string="Modelo",required=True,index=True)
    usuario=fields.Many2one('final_project.usuariomodel',string="Propietario")

    poliza_id=fields.Many2one('final_project.polizamodel',compute='compute_poliza',inverse='poliza_inverse',ondelete='cascade')
    poliza_ids=fields.One2many('final_project.polizamodel','vehiculo_id',ondelete='cascade')


    def set_matricula(self,matricula):
        self.name=matricula

    @api.depends('poliza_ids')
    def compute_poliza(self):
        if len(self.poliza_ids) > 0:
            self.poliza_id = self.poliza_ids[0]


    def poliza_inverse(self):
        if len(self.poliza_ids) > 0:
            # delete previous reference
            asset = self.env['final_project.polizamodel'].browse(self.poliza_ids[0].id)
            asset.vehicle_id = False
        # set new reference
        self.poliza_id.vehicle_id = self


    @api.constrains("name")
    def _check_matricula_format(self):
        for vehiculo in self:
            pattern1 = r'^\d{4}[A-Z]{3}$'
            pattern2 = r'^[A-Z]\d{4}[A-Z]{2}$'
            pattern3 = r'^[A-Z]{2}\d{4}[A-Z]{2}$'
            if not (re.match(pattern1, vehiculo.name) or re.match(pattern2, vehiculo.name) or re.match(pattern3, vehiculo.name)):
                raise ValidationError("El formato de la matrícula es incorrecto. Debe ser 0000XXX, X0000XX o XX0000XX.")