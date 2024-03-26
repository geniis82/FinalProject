from odoo import models,fields,api

class VehiculosModel(models.Model):
    _name ='final_project.vehiculosmodel'
    _description='Vehiculos Model'

    name=fields.Char(string="Matricula",required=True,size=7)
    marca=fields.Char(string="Marca",required=True,index=True)
    modelo =fields.Char(string="Modelo",required=True,index=True)
    usuario=fields.Many2one('final_project.usuariomodel',string="Propietario")

    poliza_id=fields.Many2one('final_project.polizamodel',compute='compute_poliza',inverse='poliza_inverse')
    poliza_ids=fields.One2many('final_project.polizamodel','vehiculo_id')



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