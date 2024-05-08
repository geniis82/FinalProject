from odoo import models,fields,api

class AseguradoraModel(models.Model):
    _name ='final_project.aseguradoramodel'
    _description='Aseguradora Model'

    name=fields.Char(string="Nombre",required=True,index=True)
    photoAs=fields.Binary(string="Logo")

    polizas=fields.One2many('final_project.polizamodel','aseguradora_id',string='Polizas',readonly=True)