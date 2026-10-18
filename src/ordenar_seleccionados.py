# -*- coding: utf-8 -*-
"""
Ordenar selección · herramienta de secuencia de comandos para ArcGIS Pro

Marca con 1 las entidades seleccionadas de una capa y con 0 el resto, en un
campo indicador de la tabla de atributos. Ordenando ese campo de forma
descendente, todas las entidades seleccionadas quedan agrupadas al principio
de la tabla.

Parámetros de la herramienta
  0  Capa de entrada               Capa      Requerido  Entrada
  1  Nombre del campo indicador    Cadena    Opcional   Entrada  (por defecto: "seleccion")

Autor: Jacinto Domínguez Morales · Máster en TIG (UCM), 2025
"""

import arcpy


def ordenar_seleccionados():
    capa = arcpy.GetParameterAsText(0)
    campo = arcpy.GetParameterAsText(1) or "seleccion"

    # Describir la capa y obtener el campo de identificador (OBJECTID, FID...)
    desc = arcpy.Describe(capa)
    oid_field = desc.OIDFieldName

    # FIDSet devuelve los OID seleccionados como cadena "20;23;24;25"
    fidset = desc.FIDSet
    seleccionados = [int(x) for x in fidset.split(";")] if fidset else []

    # Crear el campo indicador (SHORT) si no existe
    campos = [f.name for f in arcpy.ListFields(capa)]
    if campo not in campos:
        arcpy.AddField_management(capa, campo, "SHORT")

    # Escribir 1 en las entidades seleccionadas y 0 en el resto,
    # comparando por OID para no depender del orden de las filas
    with arcpy.da.UpdateCursor(capa, [oid_field, campo]) as cursor:
        for oid, _ in cursor:
            valor = 1 if oid in seleccionados else 0
            cursor.updateRow((oid, valor))

    arcpy.AddMessage(f"Marcadas {len(seleccionados)} entidades como seleccionadas.")


if __name__ == "__main__":
    ordenar_seleccionados()
