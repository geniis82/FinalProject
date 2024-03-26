from odoo import models,fields,api

class UsuarioModel(models.Model):
    _name ='final_project.usuariomodel'
    _description='Usuario Model'

    dni = fields.Char(string="DNI", required=True, size=9)
    name = fields.Char(string="Name", required=True, index=True)
    surname = fields.Char(string="Surname", required=True, index=True)
    tlf = fields.Char(size=9, required=True, string="Phone")
    photo = fields.Binary()
    dateBirth = fields.Date(required=True)
    email = fields.Char(string="email", required=True)

    vehiculos = fields.One2many('final_project.vehiculosmodel', 'usuario', string="Vehiculos")
    polizas = fields.One2many('final_project.polizamodel', 'usuario', string='Polizas',readonly=True)


    def name_get(self):
        result = []
        for user in self:
            result.append((user.id, '{} - {} {}'.format(user.dni, user.name, user.surname)))
        return result