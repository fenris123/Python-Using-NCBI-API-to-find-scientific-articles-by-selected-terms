# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:26:12 2023

@author: GUILLERMO FERRER SÁNCHEZ DE MOVELLÁN
"""

### Codigo buscar en la API  del NCBI 




#   Librerias a usar

import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET



#   URL base, y definicion o peticion de entrada  de los parametros   

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
database = "pubmed"
query  = input ("inserte los terminos a buscar")
titulo = input ("¿Buscar solo en el titulo? (si/no)")
resultados = input ("numero de resultados a mostrar")

# Reemplazar los espacios en query por "+"
query = query.replace(" ", "+")


#    Diccionario con los parametros dados. Tantos los fijos como los a introducir
params =  {"db": database, "term": query, "retmax": resultados }

if titulo.lower() == "si":  # Convertir a minúsculas para asegurar comparación correcta
    params["field"] = "title"




#   ESTO MONTA LA URL DEFINITIVA A CONSULTAR Y LA PRUEBA

try:
    url= base_url + urllib.parse.urlencode (params)    
    
except:
    print("hubo algun tipo de error al consultar la pagina")
    quit()    



#   ESTO COGE LA URL, LA LEE, USA ET PARA FORMAR LOS ARBOLES, Y 
#   VOY A LAS HOJAS "RECORDS/RECORD"

try:
    print("Consultando la web ", url, ". Espere, por favor.")
    with urllib.request.urlopen(url) as response:
        consulta = response.read ()
        arboles= ET.fromstring (consulta)
        hojas = arboles.findall ("./IdList/Id")

#   AQUI YA, VOY PASANDO POR TODAS LAS HOJAS Y COGIENDO DATOS.
        
        for hoja in hojas:
            pubmedID = hoja.text
            direccionweb= "https://pubmed.ncbi.nlm.nih.gov/" + pubmedID
            print (pubmedID, direccionweb)
        
except:
    print("Hubo un error al realizar la solicitud")
    

