from odoo import models,fields,api

class AseguradoraModel(models.Model):
    _name ='final_project.aseguradoramodel'
    _description='Aseguradora Model'

    name=fields.Char(string="Name",required=True,index=True)
    photo=fields.Binary()

    polizas=fields.One2many('final_project.polizamodel','aseguradora_id',string='Polizas',readonly=True)