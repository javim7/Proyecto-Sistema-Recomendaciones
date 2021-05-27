#importando clases externas
import pandas as pd
import numpy as np
import matplotlib as plt
from py2neo import Graph
from neo4j import GraphDatabase


#establecer conexion con el uri, usuario y contrasena correctos
graphdp = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","1234"))

#iniciando la sesion de neo4j
session = graphdp.session()

#leer los archivos csv con pandas
catalogo = pd.read_csv("Peliculas.csv")
simis = pd.read_csv("Similitudes.csv")
rates = pd.read_csv("Ratings.csv")

#Creando generos.
generos = ["Action","Ciencia Ficcion", "Comedy", "Drama","Horror","Romance"]

for genero in generos:
    session.run("CREATE (p:Genero {titulo:'"+genero+"'})")

#obteniendo elementos de catalogo y metiendolos a listas
titulos = []
titulos.extend(catalogo['Titulo'].tolist())
duras = []
duras.extend(catalogo['Duración'].tolist())
anos = []
anos.extend(catalogo['Año'].tolist())
ratings = []
ratings.extend(catalogo['Rating'].tolist())
generos = []
generos.extend(catalogo['Genero'].tolist())

#for loop para poder crear todas las peliculas en neo4j y la relaciones con su generos
for row in range(len(titulos)):
    titulo = titulos[row]
    dura = str(duras[row])
    ano = str(anos[row])
    rating = str(ratings[row])
    genero = generos[row]
    session.run("CREATE (p:Pelicula {titulo:'"+titulo+"', duracion:'"+dura+"', año:'"+ano+"', rating:'"+rating+"'})")
    session.run("MATCH (a:Pelicula{titulo:'"+titulo+"'}),(b:Genero{titulo:'"+genero+"'}) MERGE (a)-[r:es_genero]->(b)")

#obteniendo elementos de ratings y metiendolos a listas
usuarios = []
usuarios.extend(rates['Usuario'].tolist())
peliculas = []
peliculas.extend(rates['Pelicula'].tolist())
ratings2 = []
ratings2.extend(rates['Rating'].tolist())

#for loop para poder crear todos los usuarios y hacer relacion de rating con peliculas
for row in range(len(usuarios)):
    usuario = usuarios[row]
    pelicula = peliculas[row]
    rating2 = str(ratings2[row])
    session.run("CREATE (p:Usuario {titulo:'"+usuario+"'})")
    session.run("MATCH (a:Usuario {titulo:'"+usuario+"'}), (b:Pelicula {titulo:'"+pelicula+"'}) MERGE (a)-[r:has_rated{rating:'"+rating2+"'}]->(b)")

#obteniendo elementos de similitudes y metiendolas a listas
pelis1 = []
pelis1.extend(simis['Pelicula1'].tolist())
pelis2 = []
pelis2.extend(simis['Pelicula2'].tolist())

#for loop para poder crear las relaciones entre peliculas similares de diferentes generos
for row in range(len(pelis1)):
    pelicula1 = pelis1[row]
    pelicula2 = pelis2[row]
    session.run("MATCH (a:Pelicula{titulo:'"+pelicula1+"'}),(b:Pelicula{titulo:'"+pelicula2+"'}) MERGE (a)-[r:similar]->(b)")
