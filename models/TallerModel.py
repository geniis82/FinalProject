from odoo import models,fields,api

class TallerModel(models.Model):
    _name ='final_project.tallermodel'
    _description='Taller Model'

    name=fields.Char(string="Name",required=True,index=True)
    Localidad=fields.Char(string='Localidad',required=True)

