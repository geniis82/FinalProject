from odoo import models,fields,api
from datetime import datetime
from odoo.exceptions import ValidationError
import re
from dateutil.relativedelta import relativedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class PartesModel(models.Model):
    _name ='final_project.partesmodel'
    _description='Partes Model'

    name = fields.Integer(string='Poliza ID', default=lambda self: self.setRef(),readonly=True)
    descripcion=fields.Text(required=True,string="Descripción del Accidente",index=True)
    dataParte = fields.Date(string="Fecha del Parte", default=lambda self: datetime.today(),readonly=True,index=True)
    photo=fields.Binary(string="Foto del accidente",index=True)
    location=fields.Char(required=True,string="Localidad",index=True)
    addres=fields.Char(required=True,string="Dirección",index=True)

    client1= fields.Many2one('final_project.usuariomodel',string="Usuario 1",required=True,domain="[('polizas', '!=', False)]",ondelete="cascade")
    client2= fields.Many2one('final_project.usuariomodel',string="Usuario 2",domain="[('polizas', '!=', False),('id', '!=', client1)]",ondelete="cascade")
    #Usuario 1 parte
    dni = fields.Char(string="DNI", size=9)
    nameCliente = fields.Char(string="Nombre",  index=True)                                                      
    surname = fields.Char(string="Apellidos",  index=True)
    tlf = fields.Char(size=9, string="Telefono")
    dateBirth = fields.Date(string='Fecha de Nacimineto')
    email = fields.Char(string="Email",)

    vehiculo = fields.Many2one('final_project.vehiculosmodel', string="Vehiculo", domain="[('usuario', '=', client1)]",required=True,ondelete='cascade')
    vehiculo2 = fields.Many2one('final_project.vehiculosmodel', string="Vehiculo", domain="[('usuario', '=', client2)]",ondelete='cascade')

    #Vehiculo 1 parte
    matricula=fields.Char(string="Matricula",size=7)
    marca=fields.Char(string="Marca",index=True)
    modelo =fields.Char(string="Modelo",index=True)

    #Aseguradora 1 parte
    nameAseguradora=fields.Char(string="Nombre de la Aseguradora")
    numPoliza=fields.Char(string="Numero de Poliza")

    isClient=fields.Boolean(default=False)

    #Usuario 2 parte
    dni2 = fields.Char(string="DNI", size=9)
    nameCliente2 = fields.Char(string="Nombre",  index=True)
    surname2 = fields.Char(string="Apellidos",  index=True)
    tlf2 = fields.Char(size=9, string="Telefono")
    dateBirth2 = fields.Date(string='Fecha de Nacimineto')
    email2 = fields.Char(string="Email")

    #Vehiculo 2 parte
    matricula2=fields.Char(string="Matricula",size=7)
    marca2=fields.Char(string="Marca",index=True)
    modelo2 =fields.Char(string="Modelo",index=True)

    #Aseguradora 2 parte
    nameAseguradora2=fields.Char(string="Nombre de la Aseguradora")
    numPoliza2=fields.Char(string="Numero de Poliza")

    def set_dni2(self,dni):
        self.dni2=dni

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
            


    # @api.model
    # def create(self, vals):
    #     # Crea el parte
    #     new_parte = super(PartesModel, self).create(vals)
        
    #     # Envía correo electrónico
    #     self.send_email('Nuevo parte de accidente', f'Se ha generado un nuevo parte de accidente con ID: {new_parte.name}', 'josgenpas@alu.edu.gva.es')
        
    #     return new_parte
    

    @api.model
    def send_email(self, subject, message, to_email):
        from_email = 'lgp398@gmail.com'  # Cambiar al correo del remitente
        password = '1998Valencia.xdxd'  # Cambiar a la contraseña del remitente

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
