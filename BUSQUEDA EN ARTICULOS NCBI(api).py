# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 20:26:12 2023

@author: GUILLERMO FERRER SÁNCHEZ DE MOVELLÁN
"""

### Codigo para buscar articulos en la API Entrez del NCBI 




#   LIBRERIAS A USAR

import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import pandas as pd


#####   PRIMERA PARTE:
    
#####   CONSULTA USANDO ESearch:
#####   Aqui se introduciran los terminos a buscar, si se quiere buscar solo en el titulo
#####   y el numero de resultados a obtener.  Devuelve la id de los articulos que tengan esos terminos.





#   URL base, y definicion o peticion de entrada  de los parametros.   

base_url_parteuno = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
database = "pubmed"
query  = input ("inserte los terminos a buscar")
buscartitulo = input ("¿Buscar solo en el titulo? (si/no)")
resultados = input ("numero de resultados a mostrar (MAXIMO 200)")

if int(resultados) > 200:
    print ("el numero de resultados no puede ser mayor de 200")
    input("Presione Enter para salir...")
    quit()
    
# Reemplazar los espacios en query por "+" (necesario en Entrez)
query = query.replace(" ", "+")


# Creacion de un diccionario con los parametros dados. 
params_parteuno =  {"db": database, "term": query, "retmax": resultados }

if buscartitulo.lower() == "si":  # Convertir a minúsculas para asegurar comparación correcta
    params_parteuno["field"] = "title"



# Montar URL definitiva, y la prueba. (no deberia haber error, pero por si acaso)

url_parteuno= base_url_parteuno + urllib.parse.urlencode (params_parteuno)    
    



# preparamos una lista en blanco para las ID, cogemos la URL, la leemos, y montamos los arboles
# vamos a a las hojas "./IdList/Id".  obtenemos la id, y la añadimos a la lista


ListaID =[]
try:
    print("Consultando la web ", url_parteuno, ". Espere, por favor.")
    with urllib.request.urlopen(url_parteuno) as response:
        consulta_parteuno = response.read ()
        arboles= ET.fromstring (consulta_parteuno)
        hojas = arboles.findall ("./IdList/Id")
        print ("numero de articulos encontrados",len(hojas))
# aqui capturamos la id de cada uno de los articulos 
        
        for hoja in hojas:
            pubmedID = hoja.text
            direccionweb= "https://pubmed.ncbi.nlm.nih.gov/" + pubmedID   
            ListaID.append(pubmedID)
            
except Exception as error_parteuno:
    print(f"Hubo un error al realizar la solicitud:  {error_parteuno}")
    input("Presione Enter para salir...")

ListaID = ",".join(ListaID)    
    
#####   SEGUNDA PARTE:
    
#####   CONSULTA USANDO ESummary:
#####   Aqui el programa usara los ID obtenidos para hacer con ellos una busqueda usando ESummary
#####   Con ello lograremos los datos del articulo



# Consulta a esummary para obtener títulos y otros detalles
base_url_partedos = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
database = "pubmed"

params_partedos =  {"db": database, "id": ListaID, "retmode": "xml" }


url_partedos= base_url_partedos + urllib.parse.urlencode (params_partedos)


#  Preparamos una tabla en blanco para los datos. Cogemos la URL, la leemos y montamos el arbol.
#  Aqui cada "hoja" sera un <DocSum>, que dentro se subdivide un monton de informacion sobre cada articulo.
#  metemos esa informacion en variables, la añadimos como fila a la tabla, y pasamos al siguiente 


Tabla_datos = []
try:
    with urllib.request.urlopen(url_partedos) as response:
        consulta_partedos =  response.read()
        arboles_partedos= ET.fromstring (consulta_partedos)
        

    for hojas in arboles_partedos.findall("./DocSum"):
        Pubmed_id = hojas.find("./Id").text
        Titulo = hojas.find("./Item[@Name='Title']").text
        Autores = [author.text for author in hojas.findall("./Item[@Name='AuthorList']/Item")]
        Publicacion = hojas.find("./Item[@Name='Source']").text
        Fecha =  hojas.find("./Item[@Name='PubDate']").text
        Citas_en_PMC = hojas.find("./Item[@Name='PmcRefCount']").text
        Web_pubmed = "https://pubmed.ncbi.nlm.nih.gov/" + Pubmed_id 
        
        
        # Agregar los datos del artículo a la lista
        Tabla_datos.append([Pubmed_id, Titulo, ', '.join(Autores), Publicacion, Fecha, Citas_en_PMC, Web_pubmed])
        
      
except Exception as error_partedos:
     print(f"Hubo un error al realizar la solicitud:  {error_partedos}")
     input("Presione Enter para salir...")

if Tabla_datos == []:
    print ("no se encontraron resultados para su busqueda. Intente modificar los terminos introducidos")
    input("Presione Enter para salir...")
    quit()

    
    
# Crear un DataFrame de pandas con los datos
data_frame = pd.DataFrame(Tabla_datos, columns=["PubMed ID", "Título", "Autores", "Publicación", "Fecha", "Citas en PMC","Web pubmed"])   
    
directorio = input("Inserte el directorio donde se va a guardar el archivo\n(por ejemplo, C:/Usuarios/TuUsuario/Documentos): ").strip()
nombre_archivo = input("Inserte el nombre del archivo (sin la extensión .xlsx): ").strip()

# Añadir la extensión .xlsx automáticamente
nombre_archivo += ".xlsx"

ruta_completa = ruta_completa = directorio + "/" + nombre_archivo
data_frame.to_excel(ruta_completa, index=False, engine='openpyxl')

input("Archivo guardado con exito. Presione Enter para salir...")
