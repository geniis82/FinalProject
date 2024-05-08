from odoo import models,fields,api
from odoo.exceptions import ValidationError
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

class UsuarioModel(models.Model):
    _name ='final_project.usuariomodel'
    _description='Usuario Model'
    _sql_constraints=[
        ('_dni_uniq',
        'UNIQUE (dni)',
        'No pueden existir 2 usuarios con el mismo DNI'),    
    ]

    dni = fields.Char(string="DNI", required=True, size=9)
    name = fields.Char(string="Name", required=True, index=True)
    surname = fields.Char(string="Surname", required=True, index=True)
    tlf = fields.Char(size=9, required=True, string="Phone")
    photoUsu = fields.Binary()
    dateBirth = fields.Date(required=True)
    email = fields.Char(string="email", required=True)
    password=fields.Char(default="isca2024.")
    vehiculos = fields.One2many('final_project.vehiculosmodel', 'usuario', string="Vehiculos",ondelete='cascade')
    polizas = fields.One2many('final_project.polizamodel', 'usuario', string='Polizas',readonly=True,ondelete='cascade')
    isClient=fields.Boolean(default=True)
    partes=fields.One2many('final_project.partesmodel','client1',string='Partes',ondelete="cascade")

    def set_dni(self,dni):
        self.dni=dni

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
    
    @api.constrains("dni")
    def _check_dni(self):
        if len(self.dni)!=9:
            raise ValidationError("La longitud del DNI es incorrecta")
        else:
            if not self.dni[:8].isdigit():
                raise ValidationError("El formato del DNI es incorrecto")
            if not self.dni[-1].isalpha():
                raise ValidationError("El formato del DNI es incorrecto")
            
            letraDni="TRWAGMYFPDXBNJZSQVHLCKE"
            numDni=int(self.dni[:-1])
            letraCal=letraDni[numDni % 23]
            letra_usuario = self.dni[-1]

            if letra_usuario.isupper():
                if letraCal != letra_usuario:
                    raise ValidationError("La letra del DNI es incorrecta")
            else:
                dni_corregido = str(numDni) + letra_usuario.upper()
                self.set_dni(dni_corregido)
                letra=dni_corregido[-1]
                if letraCal != letra:
                    raise ValidationError("La letra del DNI es incorrecta")
        return True
    

    @api.constrains("tlf")
    def _check_tlf(self):
        if len(self.tlf)!=9:
            raise ValidationError("La longitud del telefono es incorrecta")
        else:
            for char in self.tlf:
                if not char.isdigit():
                    raise ValidationError("El formato del telefono es incorrecto")
                    break
        return True
    
    @api.constrains("email")
    def _checkEmail(self):
        patron_correo = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if patron_correo.match(self.email):
            return True
        else:
            raise ValidationError("El formato del correo electrónico es incorrecto")
        

    @api.constrains("dateBirth")
    def checkYears(self):
        edad = relativedelta(datetime.now(), self.dateBirth)
        if edad.years < 18:
            raise ValidationError("El usuario debe tener almenos 18 años")