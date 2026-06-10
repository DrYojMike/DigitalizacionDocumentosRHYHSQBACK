from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from urllib.parse import quote
from django.http import FileResponse, Http404
import os
import mimetypes

# Create your views here.

@api_view(['GET'])
def FormatoEvaluacion(request, tipo):

    if not tipo:
        return Response({
            "message": "Error: Se requiere el Parametro tipo",
            "data": []
        })

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    A.IdEvaArea,
                    A.NomEvaArea,
                    C.IdEvaCompetencia,
                    C.NomEvaCompetencia,
                    C.DesEvaCompetencia,
                    IG.IdEvaIndicadorGestion,
                    IG.NomEvaIndicadorGestion
                FROM [Biometrico].[dbo].[TbEvaluacionArea] A
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionCompetencia] C ON C.IdAreaCompetencia = A.IdEvaArea 
                    AND C.ForEvaCompetencia IN (0, %s)
                INNER JOIN [Biometrico].[dbo].[TbEvaluacionIndicadorGestion] IG ON IG.IdCompetenciaIndicadorGestion = C.IdEvaCompetencia 
                    AND ForEvaIndicadorGestion IN (0, %s)
                ORDER BY A.IdEvaArea, C.IdEvaCompetencia
            """, [tipo, tipo])

            rows = cursor.fetchall()

        data = {}

        for row in rows:
            area_id = row[0]
            area_name = row[1]
            comp_id = row[2]
            comp_name = row[3]
            comp_desc = row[4]
            ind_id = row[5]
            ind_name = row[6]

            # AREA
            if area_id not in data:
                data[area_id] = {
                    "area": area_name,
                    "competencias": {}
                }

            # COMPETENCIA
            if comp_id not in data[area_id]["competencias"]:
                data[area_id]["competencias"][comp_id] = {
                    "nombre": comp_name,
                    "descripcion": comp_desc,
                    "indicadores": []
                }

            # INDICADOR
            data[area_id]["competencias"][comp_id]["indicadores"].append({
                "id": ind_id,
                "nombre": ind_name
            })

        # convertir a lista final
        result = []
        for area in data.values():
            area["competencias"] = list(area["competencias"].values())
            result.append(area)

        return Response({
            "message": "OK",
            "data": result
        })

    except Exception as e:
        return Response({
            "message": f"Error: {str(e)}",
            "data": []
        })