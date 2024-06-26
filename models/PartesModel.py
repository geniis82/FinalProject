from odoo import models,fields,api
from datetime import datetime
from odoo.exceptions import ValidationError
import re
from dateutil.relativedelta import relativedelta
import base64
import requests

class PartesModel(models.Model):
    _name ='final_project.partesmodel'
    _description='Partes Model'

    name = fields.Integer(string='Poliza ID', default=lambda self: self.setRef(),readonly=True)
    descripcion=fields.Text(required=True,string="Descripción del Accidente",index=True)
    dataParte = fields.Date(string="Fecha del Parte", default=lambda self: datetime.today(),readonly=True,index=True)
    photo=fields.Binary()
    
    location=fields.Char(required=True,string="Localidad",index=True)
    addres=fields.Char(required=True,string="Dirección",index=True)

    client1= fields.Many2one('final_project.usuariomodel',string="Usuario 1",required=True,domain="[('polizas', '!=', False)]",ondelete="cascade")
    client2= fields.Many2one('final_project.usuariomodel',string="Usuario 2",domain="[('polizas', '!=', False),('id', '!=', client1)]",ondelete="cascade")
    #Usuario 1 parte
    dni = fields.Char(related='client1.dni', readonly=True)
    nameCliente = fields.Char(related='client1.name', readonly=True)
    surname = fields.Char(related='client1.surname', readonly=True)
    tlf = fields.Char(related='client1.tlf', readonly=True)
    dateBirth = fields.Date(related='client1.dateBirth', readonly=True)
    email = fields.Char(related='client1.email', readonly=True, string="Email")
    
    vehiculo = fields.Many2one('final_project.vehiculosmodel', string="Vehiculo", domain="[('usuario', '=', client1)]",required=True,ondelete='cascade')
    vehiculo2 = fields.Many2one('final_project.vehiculosmodel', string="Vehiculo", domain="[('usuario', '=', client2)]",ondelete='cascade')

    #Vehiculo 1 parte
    matricula=fields.Char(string="Matricula" ,related='vehiculo.name',size=7)
    marca=fields.Char(string="Marca",related='vehiculo.marca',index=True)
    modelo =fields.Char(string="Modelo",related='vehiculo.modelo',index=True)

    #Aseguradora 1 parte
    nameAseguradora=fields.Char(related='client1.vehiculos.poliza_id.aseguradora_id.name', readonly=True, string="Nombre Aseguradora")
    numPoliza = fields.Char(related='client1.vehiculos.poliza_id.name', readonly=True, string="Número de Póliza")

    isClient=fields.Boolean(default=False,related='client2.isClient')

    #Usuario 2 parte
    dni2 = fields.Char(related='client2.dni', readonly=True, string="DNI Usuario 2")
    nameCliente2 = fields.Char(related='client2.name', readonly=True, string="Nombre Usuario 2")
    surname2 = fields.Char(related='client2.surname', readonly=True, string="Apellidos Usuario 2")
    tlf2 = fields.Char(related='client2.tlf', readonly=True, string="Teléfono Usuario 2")
    dateBirth2 = fields.Date(related='client2.dateBirth', readonly=True, string="Fecha de Nacimiento Usuario 2")
    email2 = fields.Char(related='client2.email', readonly=True, string="Email Usuario 2")


    #Vehiculo 2 parte
    matricula2 = fields.Char(related='client2.vehiculos.name', readonly=True, string="Matricula Vehículo 2")
    marca2 = fields.Char(related='client2.vehiculos.marca', readonly=True, string="Marca Vehículo 2")
    modelo2 = fields.Char(related='client2.vehiculos.modelo', readonly=True, string="Modelo Vehículo 2")

    #Aseguradora 2 parte
    nameAseguradora2=fields.Char(related='client2.vehiculos.poliza_id.aseguradora_id.name', readonly=True, string="Nombre Aseguradora")
    numPoliza2 = fields.Char(related='client2.vehiculos.poliza_id.name', readonly=True, string="Número de Póliza")


    nameAsegurNoClien=fields.Char(string="Nombre Aseguradora")
    numPoliNoClien=fields.Char(string="Número de Póliza")

    def set_dni2(self,dni):
        self.dni2=dni

    @api.onchange('nameAseguradora2', 'numPoliza2')
    def _onchange_nameAseguradora2_numPoliza2(self):
        if self.nameAseguradora2 == False:
            self.nameAseguradora2 = self.nameAsegurNoClien
        if self.numPoliza2 == False:
            self.numPoliza2 = self.numPoliNoClien

    @api.onchange('client1')
    def onchange_client(self):
        if not self.client1:
            self.vehiculo = False
        else:
            self.dni = self.client1.dni
            self.nameCliente = self.client1.name
            self.surname = self.client1.surname
            self.tlf = self.client1.tlf
            self.dateBirth = self.client1.dateBirth
            self.email = self.client1.email
            self.vehiculo = False  
            self.matricula=False
            self.marca=False
            self.modelo=False
            self.nameAseguradora=False
            self.numPoliza=False
            #Limpia fields client2
            self.client2=False
            self.dni2 = False
            self.nameCliente2 = False
            self.surname2 = False
            self.tlf2 = False
            self.dateBirth2 = False
            self.email2 = False
            self.vehiculo2 = False  
            self.matricula2=False
            self.marca2=False
            self.modelo2=False
            self.nameAseguradora2=False
            self.numPoliza2=False

    @api.onchange('client2')
    def onchange_client2(self):
        if not self.client2:
            self.vehiculo = False
        else:
            self.dni2 = self.client2.dni
            self.nameCliente2 = self.client2.name
            self.surname2 = self.client2.surname
            self.tlf2 = self.client2.tlf
            self.dateBirth2 = self.client2.dateBirth
            self.email2 = self.client2.email
            self.vehiculo2 = False  
            self.matricula2=False
            self.marca2=False
            self.modelo2=False
            self.nameAseguradora2=False
            self.numPoliza2=False

    @api.onchange('vehiculo')
    def onchange_vehiculo(self):
        if self.vehiculo:
            self.matricula = self.vehiculo.name
            self.marca = self.vehiculo.marca
            self.modelo = self.vehiculo.modelo
            # Obtener la primera póliza asociada al vehículo seleccionado
            poliza = self.vehiculo.poliza_ids
            if poliza:
                self.nameAseguradora = poliza.aseguradora_id.name
                self.numPoliza = poliza.name

    @api.onchange('vehiculo2')
    def onchange_vehiculo2(self):
        if self.vehiculo2:
            self.matricula2 = self.vehiculo2.name
            self.marca2 = self.vehiculo2.marca
            self.modelo2 = self.vehiculo2.modelo
            # Obtener la primera póliza asociada al vehículo seleccionado
            poliza = self.vehiculo2.poliza_ids
            if poliza:
                self.nameAseguradora2 = poliza.aseguradora_id.name
                self.numPoliza2 = poliza.name

    def setRef(self):
        result = self.env['final_project.partesmodel'].search_read([])
        if len(result) == 0:
            return 1
        else:
            return result[-1]["name"] + 1
        
    
    @api.constrains("dni2")
    def _check_dni(self):
        if len(self.dni2)!=9:
            raise ValidationError("La longitud del DNI del usuario 2 es incorrecta")
        else:
            if not self.dni2[:8].isdigit():
                raise ValidationError("El formato del DNI del usuario 2 es incorrecto")
            if not self.dni2[-1].isalpha():
                raise ValidationError("El formato del DNI del usuario 2 es incorrecto")
            
            letraDni="TRWAGMYFPDXBNJZSQVHLCKE"
            numDni=int(self.dni2[:-1])
            letraCal=letraDni[numDni % 23]
            letra_usuario = self.dni2[-1]

            if letra_usuario.isupper():
                if letraCal != letra_usuario:
                    raise ValidationError("La letra del DNI del usuario 2 es incorrecta")
            else:
                dni_corregido = str(numDni) + letra_usuario.upper()
                self.set_dni2(dni_corregido)
                letra=dni_corregido[-1]
                if letraCal != letra:
                    raise ValidationError("La letra del DNI del usuario 2 es incorrecta")
        return True

    @api.constrains("tlf2")
    def _check_tlf(self):
        if len(self.tlf2)!=9:
            raise ValidationError("La longitud del numero del usaurio 2 debe de ser de 9 numeros")
        else:
            for char in self.tlf2:
                if not char.isdigit():
                    raise ValidationError("El formato del telefono del usaurio 2 es incorrecto")
                    break
        return True
    
    @api.constrains("email2")
    def _checkEmail(self):
        patron_correo = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if patron_correo.match(self.email2):
            return True
        else:
            raise ValidationError("El formato del correo electronico del usuario 2 es incorrecto")
        
        
    @api.constrains("dateBirth2")
    def checkYears(self):
        edad = relativedelta(datetime.now(), self.dateBirth2)
        if edad.years < 18:
            raise ValidationError("El usuario 2 debe tener 18 años")
        
    @api.constrains("matricula2")
    def _check_matricula_format(self):
        for vehiculo in self:
            pattern1 = r'^\d{4}[A-Z]{3}$'
            pattern2 = r'^[A-Z]\d{4}[A-Z]{2}$'
            pattern3 = r'^[A-Z]{2}\d{4}[A-Z]{2}$'
            if not (re.match(pattern1, vehiculo.matricula2) or re.match(pattern2, vehiculo.matricula2) or re.match(pattern3, vehiculo.matricula2)):
                raise ValidationError("El formato de la matrícula del usuario 2 es incorrecto. Debe ser 0000XXX, X0000XX o XX0000XX.")
