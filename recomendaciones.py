#Maria Fernanda Argueta, Javier Mombiela, Javier Valle
#Proyecto Sistema de  Recomendaciones 
#Seccion 10
#Grupo 8

#importando clases externas
import pandas as pd
import numpy as np
import matplotlib as plt
from py2neo import Graph
from neo4j import GraphDatabase

"""
Empezamos el programa estableciendo conexion entre Python y 
nuestro grafo de neo4j para despues poder obtener toda la 
informacion del grafo y almacenarla en listas aca en el
programa. 
"""

#establecer conexion con el uri, usuario y contrasena correctos
graphdp = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","password"))

#iniciando la sesion
session = graphdp.session()

#crear = "CREATE (p:Genero {titulo:'Ciencia Ficcion'})"
#cre = session.run(crear)

#defininiendo los nombres de usuarios y metiendolos a una lista
def obtenerPersona(grapho):
    nombresUsuario = grapho.run("MATCH(p:Usuario) return p.titulo")
    lista = [nodo["p.titulo"] for nodo in nombresUsuario]
    return lista

#definiendo la lista de los usuarios
listaUs = obtenerPersona(session)    

#defininiendo los nombres de las peliculas y metiendolas a una lista
def obtenerPersona(grapho):
    nombresPelis = grapho.run("MATCH(p:Pelicula) return p.titulo")
    lista = [nodo["p.titulo"] for nodo in nombresPelis]
    return lista

#definiendo la lista de los usuarios
listaPel = obtenerPersona(session)   

#defininiendo los nombres de los generos y metiendolos a una lista
def obtenerPersona(grapho):
    nombresGeneros = grapho.run("MATCH(p:Genero) return p.titulo")
    lista = [nodo["p.titulo"] for nodo in nombresGeneros]
    return lista

#definiendo la lista de los usuarios
listaGen = obtenerPersona(session) 

#persona = session.read_transaction(obtenerPersona)

"""
Ya que tenemos toda la informacion del grafo almacenada en listas,
podemos seguir con la interaccion del usuario y utilizar la informacion
obtenida anteriormente para dar recomendaciones.
"""

#pidiendo nombre de usuario
nom_usuario = input("\nIngrese su nombre de usuario: ")

#if para ver si el nombre de usuario ya es parta de la base de datos o no
if nom_usuario in listaUs:
    print("\nBienvendio de nuevo", nom_usuario,"!")
else:
    crearUs = session.run("CREATE (p:Usuario {titulo:'"+nom_usuario+"'})") #agregando el nombre de usuario al nodo
    print("\nBienvenido a la familia", nom_usuario,", ahora mismo te agregamos a la base de datos!")

opcion = 0
#iniciar ciclo infinito con un while con las 3 opciones disponibles
while True:
    opciones = False
    while not opciones:
        try:
            print("\nMenu \n1. Recomendar \n2. Recomiendeme \n3. salir \n")
            opcion = int(input("Opcion> "))
        #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
        except ValueError:
            print('\nIngrese solo numeros!\n')
        #usar un if para asegurarnos que el usuario solo ponga un numero del 1-3  
        if opcion >=1 and opcion <=3:
            opciones = True
        else:
            print('\nIngrese valores solamente entre 1 y 3.\n')

#empezando las opciones

    #empezando opcion1
    if opcion==1:
        print("\nSeleccione el genero que contiene la pelicula a recomendar:")
        for number, genero in enumerate(listaGen): #imprimiendo los generos como listado
            print(number+1, genero)

    #haciendo un while para asegurar que se elija la opcion correcta
        op = 0
        ops = False
        while not ops:
            try:
                op = int(input("\nGenero> "))
            #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
            except ValueError:
                print('\nIngrese solo numeros!\n')
            #usar un if para asegurarnos que el usuario solo ponga un numero del 1-5    
            if op >=1 and op <=5:
                ops = True
            else:
                print('\nIngrese valores solamente entre 1 y 5.\n')

        print(listaGen[op-1])
        #creando un listado de las peliculas correspondientes al genero
        pelisPorGen = session.run("MATCH (a:Pelicula)-[:es_genero]->(b:Genero {titulo:'"+listaGen[op-1]+"'}) return a.titulo")
        listaPelisPorGen = [nodo["a.titulo"] for nodo in pelisPorGen]
        print(listaPelisPorGen)

    #empezando opcion2
    if opcion==2:
        print("adios")

    #iniciar opcion 3
    if opcion==3:
        #imprimir un par de mensajes
        print("\nGracias por utilizar nuestro servicio, vuelva pronto!")
        print("Finalizando Programa...")
        print("Programa Finalizado\n")
        #salir del ciclo
        break