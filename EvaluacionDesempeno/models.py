from django.db import models

# Create your models here.
class EvaluationArea(models.Model):
    idEvaArea = models.IntegerField(db_column="IdEvaArea",primary_key=True)
    nomEvaArea = models.CharField(db_column="NomEvaArea",max_length=100)
    class Meta:
        managed = False
        db_table = "TbEvaluacionArea"
        

class EvaluationCompetence(models.Model):
    idEvaCompetencia = models.IntegerField(db_column="IdEvaCompetencia", primary_key=True)
    nomEvaCompetencia = models.CharField( db_column="NomEvaCompetencia",max_length=200)
    desEvaCompetencia = models.CharField(db_column="DesEvaCompetencia",max_length=500)
    idAreaCompetencia = models.IntegerField(db_column="IdAreaCompetencia")
    forEvaCompetencia = models.IntegerField(db_column="ForEvaCompetencia")
    class Meta:
        managed = False
        db_table = "TbEvaluacionCompetencia"


class EvaluationIndicator(models.Model):
    idEvaIndicadorGestion = models.IntegerField(db_column="IdEvaIndicadorGestion",primary_key=True)
    nomEvaIndicadorGestion = models.CharField(db_column="NomEvaIndicadorGestion",max_length=200)
    idCompetenciaIndicadorGestion = models.IntegerField(db_column="IdCompetenciaIndicadorGestion")
    class Meta:
        managed = False
        db_table = "TbEvaluacionIndicadorGestion"