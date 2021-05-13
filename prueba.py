#Maria Fernanda Argueta, Javier Mombiela, Javier Valle
#Proyecto Sistema de  Recomendaciones 
#Seccion 10
#Grupo 8

import pandas as pd
import numpy as np
import matplotlib as plt
from py2neo import Graph
from neo4j import GraphDatabase

#establecer conexion con el uri, usuario y contrasena correctos
graphdp = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","password"))

#iniciando la sesion
session = graphdp.session()

#crear = "CREATE (p:Genero {titulo:'Ciencia Ficcion'})"
#cre = session.run(crear)

#utilizando la operacion de retornar todos los nodos
opRetornar="MATCH (p) return p"
todos = session.run(opRetornar)

#foreach para poder imprimir todos los nods
for node in todos:
    print(node)

#utilizando la operacion para solo retornar peliculas
opPeliculas = "MATCH (p:Pelicula) return p.titulo"
peliculas = session.run(opPeliculas)
peliculass = []
for node in peliculas:
    peliculass.append(node)
    print(node)

#empezando interaccion con el usuario
nom_usuario = input("\nIngrese su nombre de usuario: ")

print("\nBienvendio de vuelta", nom_usuario)

opcion = 0
#iniciar ciclo infinito con un while con las 5 opciones disponibles
while True:
    opciones = False
    while not opciones:
        try:
            print("\nMenu \n1. Recomendar \n2. Recomiendeme \n3. salir \n")
            opcion = int(input("Opcion> "))
        #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
        except ValueError:
            print('\nIngrese solo numeros!\n')
        #usar un if para asegurarnos que el usuario solo ponga un numero del 1-5    
        if opcion >=1 and opcion <=3:
            opciones = True
        else:
            print('\nIngrese valores entre 1 y 3.\n')

#empezando las opciones

    #empezando opcion1
    if opcion==1:
        print("hola")

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
