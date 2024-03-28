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


    @api.model
    def create(self, vals):
        # Crear el usuario en Odoo
        user_vals = {
            'name': '{} {}'.format(vals.get('name', ''), vals.get('surname', '')),
            'login': vals.get('email', ''),
            'password': 'isca2024.',
            'email': vals.get('email', ''),
        }
        user = self.env['res.users'].create(user_vals)
        # Continuar con la creación del usuario en el modelo
        return super(UsuarioModel, self).create(vals)

    def unlink(self):
        # Eliminar el usuario de res.users
        self.env['res.users'].search([('login', '=', self.email)]).unlink()
        # Continuar con la eliminación del usuario en el modelo
        return super(UsuarioModel, self).unlink()
    
    def name_get(self):
        result = []
        for user in self:
            result.append((user.id, '{} - {} {}'.format(user.dni, user.name, user.surname)))
        return result