from django.db import models

# Create your models here.

class Usuarios(models.Model):
    idUsuario = models.IntegerField(primary_key=True, db_column="IdUsuario")
    nomUsuario = models.CharField(max_length=200, db_column="NomUsuario")
    idRol = models.IntegerField(db_column="IdRol")
    clave = models.CharField(max_length=200, db_column="Clave")
    nomUsu = models.CharField(max_length=100, db_column="NomUsu")
    apeUsu = models.CharField(max_length=100, db_column="ApeUsu")
    tipoUsuario = models.CharField(max_length=100, db_column="TipoUsuario")
    
    class Meta:
        managed: False
        db_table = "[Biometrico].[dbo].[TbUsuarios]"


class Empleados(models.Model):
    idEmpleado = models.IntegerField(primary_key=True, db_column="UserId")
    documentoEmpleado = models.CharField(max_length=20, db_column="UserCode")
    nombreEmpleado = models.CharField(max_length=200, db_column="Name")
    cargoEmpleado = models.CharField(max_length=100, db_column="IdCargo")
    fechaIngresoEmpleado = models.DateField(db_column="EmployDate")
    fechaRetiroEmpleado = models.DateField(db_column="FechaRetiro")
    CumpleanosEmpleado =models.DateField(db_column="Birthday")
    evaluacionTipo = models.IntegerField(db_column="TipoEvaluacion")
    class Meta:
        managed: False
        db_table = "[Biometrico].[dbo].[Userinfo]"    