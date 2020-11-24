# -*- coding: utf-8 -*-

from odoo import fields, models, api
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ControlEmployeesHorario(models.Model):
    _name = 'controlemployees.horario'
    _description = 'Horario'
    _order = 'name asc'
    name = fields.Char(string= 'Codigo', required= True, size=150)
    horaInicio = fields.Char(string='Hora inicio', required=True, size=150)
    horaFin = fields.Char(string='Hora fin', required=True, size=150)
    horasXsemana = fields.Char(string='Hora por semana', required=True, size=150)
    descripcion = fields.Char(string='Descripcion', size=150)
    _sql_constraints = {('horario_uniq', 'unique(codigo)', 'El codigo del usuario debe ser unico')}

class ControlEmployeesEmpleado(models.Model):
    _name = 'controlemployees.empleado'  # nombre del modelo
    _description = 'Empleado'  # describe los datos
    _order = 'name asc'  # ordenar
    name = fields.Char(string='Nombre', required=True, size=150, index=True)
    cedula = fields.Char(string='Cedula', required=True, size=150, index=True)
    genero = fields.Char(string='Genero', required=True, size=150, index=True)
    edad = fields.Char(string='Edad', required=True, size=150, index=True)
    # Relación una a muchas
    horario_id =  fields.Many2one('controlemployees.horario', 'Horario', required=True)
    _sql_constraints = {('empleado_uniq', 'unique(cedula)', 'La cedula del empleado debe ser unica')}
    # Con esto se crea el estado de un modelo, luego se debe pasar el view.xml para acomodar las vistas
    state = fields.Selection([
        ('habilitado', 'Habilitado'),
        ('registrado', 'Usuario registrado'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', required=True, index=True, track_visibility='onchange', track_sequence=1,
        default='habilitado')
    #Despues de crear el boton paso a crear el metodo con el mismo nombre del boton
    #Si un metodo no funciona se puede probar como lo hace el profe.
    #@apipuntomulti sobre la funcion y estando importado
    @api.multi
    def registrar_usuario(self):
        #Desarrollar la comunicacion hacia la raspberry
        self.write({'state':'registrado'})
    #Aca se esta utilizando sin el @apimulti y tambien funciona
    def habilitar_usuario(self):
        #Desarrollar la comunicacion hacia la raspberry
        self.write({'state':'habilitado'})


     #para hacer la peticion al la raspberry debo importar request y json
    #Esta funcion no se esta utilizando ya que fue un modelo para hacer prueba con request inspector
    def prender_sensorDos(self):
        #_logger.info("json enviado {0}".format(json.dumps({"cedula":self.cedula})))
        headers = {"Content-Type":"application/json"}
        payload = {"nombre":self.name, "cedula":self.cedula}
        datajson = json.dumps(payload)
        #Esta url es de request inspector para probar
        url= "https://requestinspector.comhe/inspect/01epvfmpqdk41wzm23b4f6ekn0"
        response = requests.request("POST",url,data=datajson, headers=headers)
        if response.status_code == 200:
            pass
        #se coloca esto si quiero guardar la respuesta, debo adicionar un campo en el modelo llamado respuesta
        #self.write({'respuesta':str(response.content)})

    def prender_sensor(self):
        #_logger.info("json enviado {0}".format(json.dumps({"cedula":self.cedula})))
        api_endpoint= "https://lintiest-gar-5907.dataplicity.io/auth"
        headerToken= {"Content-Type": "application/json"}
        dataToken = {"username":"yohn@gmail.com","password":"123"}
        dataTokenJson= json.dumps(dataToken)
        response = requests.request("POST", api_endpoint, data=dataTokenJson, headers=headerToken)
        token= response.json()['access_token']

        headers = {"Content-Type": "application/json"}
        headers['Authorization']= "JWT {0}".format(token)

        payload = {"state": 1}
        datajson = json.dumps(payload)
        # Esta url es de request inspector para probar
        url = "https://lintiest-gar-5907.dataplicity.io/led/green/"
        response = requests.request("POST", url, data=datajson, headers=headers)
        if response.status_code == 200:
            pass

        #Esta url es de request inspector para probar



    def apagar_sensor(self):
        #_logger.info("json enviado {0}".format(json.dumps({"cedula":self.cedula})))

        api_endpoint = "https://lintiest-gar-5907.dataplicity.io/auth"
        headerToken = {"Content-Type": "application/json"}
        dataToken = {"username": "yohn@gmail.com", "password": "123"}
        dataTokenJson = json.dumps(dataToken)
        response = requests.request("POST", api_endpoint, data=dataTokenJson, headers=headerToken)
        token = response.json()['access_token']

        headers = {"Content-Type": "application/json"}
        headers['Authorization'] = "JWT {0}".format(token)


        payload = {"state":0}
        datajson = json.dumps(payload)
        #Esta url es de request inspector para probar
        url= "https://lintiest-gar-5907.dataplicity.io/led/green/"
        response = requests.request("POST",url,data=datajson, headers=headers)
        if response.status_code == 200:
            pass

class ControlEmployeesRegistro(models.Model):
    _name = 'controlemployees.registro'  # nombre del modelo
    _description = 'Registro'  # describe los datos
    _order = 'name asc'  # ordenar
    name = fields.Char(string='Nombre', required=True)
    fecha = fields.Date(string='Fecha', required=True)
    tipo = fields.Char(string='Tipo', required=True, size=150, index=True)
    codigoRegristro = fields.Char(string='Codigo', required=True, size=150, index=True)
    # Relación una a muchas
    empleado_id =  fields.Many2one('controlemployees.empleado', 'Empleado', required=True)
    _sql_constraints = {('registro_uniq', 'unique(codigoRegistro)', 'El codigo del registro debe ser unico')}