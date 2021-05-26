"""
Maria Fernanda Argueta, Javier Mombiela, Javier Valle
Proyecto Sistema de  Recomendaciones 
Seccion 10
Grupo 8

La funcion de este proyecto es poder hacer una conexion entre neo4j y python
para asi poder extraer datos de neo4j y tambien poder meterle datos y modificarlos.
"""
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

#iniciando la sesion de neo4j
session = graphdp.session()

#leer los archivos csv con pandas
catalogo = pd.read_csv("Peliculas.csv")
simis = pd.read_csv("Similitudes.csv")
rates = pd.read_csv("Ratings.csv")

""" Este es el codigo que se utilizo solo una vez para poder pasar los datos de los csv a neo4j

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
"""

#defininiendo los nombres de usuarios y metiendolos a una lista
def obtenerPersona(grapho):
    nombresUsuario = grapho.run("MATCH(p:Usuario) return p.titulo")
    lista = [nodo["p.titulo"] for nodo in nombresUsuario]
    return lista

#definiendo la lista de los usuarios y sortenado
listaUs = obtenerPersona(session)    
listaUs = sorted(listaUs)

#defininiendo los nombres de las peliculas y metiendolas a una lista
def obtenerPersona(grapho):
    nombresPelis = grapho.run("MATCH(p:Pelicula) return p.titulo")
    lista = [nodo["p.titulo"] for nodo in nombresPelis]
    return lista

#definiendo la lista de las peliculas y sortenado
listaPel = obtenerPersona(session)  
listaPel = sorted(listaPel) 

#defininiendo los nombres de los generos y metiendolos a una lista
def obtenerPersona(grapho):
    nombresGeneros = grapho.run("MATCH(p:Genero) return p.titulo")
    lista = [nodo["p.titulo"] for nodo in nombresGeneros]
    return lista

#definiendo la lista de los generos y sortenado
listaGen = obtenerPersona(session) 
listaGen =sorted(listaGen)

#definir el metodo de promedio
def Promedio(lst):
    return sum(lst) / len(lst)


"""
Ya que tenemos toda la informacion del grafo almacenada en listas,
podemos seguir con la interaccion del usuario y utilizar la informacion
obtenida anteriormente para dar recomendaciones.
"""

print("\n---------------Bienvenido a PelRec-----------------")
print("Somos una comunidad, en la que juntos nos apoyamos\npara poder tener las mejores recomendaciones de\npeliculas para cada uno de nuestros usarios.")
print("----------------------------------------------------- \n")

#pidiendo nombre de usuario
nom_usuario = input("\nPara iniciar, ingrese su nombre de usuario: ")

#if para ver si el nombre de usuario ya es parta de la base de datos o no
if nom_usuario in listaUs:
    print("\nBienvendi@ de nuevo", nom_usuario+"!")
else:
    crearUs = session.run("CREATE (p:Usuario {titulo:'"+nom_usuario+"'})") #agregando el nombre de usuario al nodo
    print("\nBienvenid@ a la familia", nom_usuario,", ahora mismo te agregamos a la base de datos!")

opcion = 0

#iniciar ciclo infinito con un while con las 3 opciones disponibles
while True:

    #vaciando el csv de recomendaciones en cada corrida para poder dar nuevas recomendaciones
    with open("Recomendaciones.csv", 'r+') as recomend:
        recomend.readline() # leyendo solo primera fila para dejar los titulos de las colunas
        recomend.truncate(recomend.tell()) # eliminando todo lo demas

    #agregnado encabezados al csv de recomendar
    #Reccomend = pd.read_csv("Recomendaciones.csv")

    opciones = False
    while not opciones:
        print("\nMenu")
        print("----------------------------")
        print("[1] Quiero Calificar       |")
        print("----------------------------")
        print("[2] Quiero Recomendaciones |")
        print("----------------------------")
        print("[3] Quiero Editar Datos    |")
        print("----------------------------")
        print("[4] Quiero Salir           |")
        print("----------------------------")
        try:
            opcion = int(input("Opcion> "))
        #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
        except ValueError:
            print('\nIngrese solo numeros!\n')
        #usar un if para asegurarnos que el usuario solo ponga un numero del 1-3  
        if opcion >=1 and opcion <=4:
            opciones = True
        else:
            print('\nIngrese valores solamente entre 1 y 4.\n')

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
            if op >=1 and op <=len(listaGen):
                ops = True
            else:
                print('\nIngrese valores solamente entre 1 y 5.\n')

        print("\n"+listaGen[op-1]+":")
        #creando un listado de las peliculas correspondientes al genero
        pelisPorGen = session.run("MATCH (a:Pelicula)-[r:es_genero]->(b:Genero {titulo:'"+listaGen[op-1]+"'}) return a.titulo")
        listaPelisPorGen = [nodo["a.titulo"] for nodo in pelisPorGen]
        listaPelisPorGen = sorted(listaPelisPorGen)
        
        for number, pelicula in enumerate(listaPelisPorGen): #imprimiendo los generos como listado
            print(number+1, pelicula)
        print("\nSeleccione la pelicula a recomendar:")


        #haciendo un while para asegurar que se elija la opcion correcta
        op1 = 0
        ops1 = False
        while not ops1:
            try:
                op1 = int(input("Pelicula> "))
            #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
            except ValueError:
                print('\nIngrese solo numeros!\n')
            #usar un if para asegurarnos que el usuario solo ponga un numero del 1-tamano de la lista   
            if op1 >=1 and op1 <=len(listaPelisPorGen):
                ops1 = True
            else:
                print('\nNumero fuera de Rango.\n')

        print("\nHa seleccionado la pelicula: "+listaPelisPorGen[op1-1]+", que rating le da (1-5):")


        op2 = 0
        ops2 = False
        while not ops2:
            try:
                op2 = int(input("Rating> "))
            #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
            except ValueError:
                print('\nIngrese solo numeros enteros!\n')
            #usar un if para asegurarnos que el usuario solo ponga un numero del 1-5    
            if op2 >=1 and op2 <=5:
                ops2 = True
            else:
                print('\nIngrese valores solamente entre 1 y 5.\n')

        print("\nLe has dado un rating de "+str(op2)+", a "+listaPelisPorGen[op1-1]+".")
        
        #haciendo el rating en neo4j
        darRating = session.run("MATCH (a:Usuario {titulo:'"+nom_usuario+"'}), (b:Pelicula {titulo:'"+listaPelisPorGen[op1-1]+"'}) MERGE (a)-[r:has_rated{rating:'"+str(op2)+"'}]->(b)")

        #viendo cuantos ratings tiene la peli para sacar un promedio
        ratingsPorPeli = session.run("MATCH (a:Usuario)-[r:has_rated]->(b:Pelicula {titulo:'"+listaPelisPorGen[op1-1]+"'}) return r.rating")
        listaRatingsPorPeli = [nodo["r.rating"] for nodo in ratingsPorPeli] 

        #conviertiendo todos los elementos a float
        listaRatingsPorPeli = [float(item) for item in listaRatingsPorPeli]
        

        #encontrar promedio de la lista utilizando el metodo definido anteriormente
        promedio = Promedio(listaRatingsPorPeli)


        nuevoRating = session.run("MATCH (p:Pelicula {titulo:'"+listaPelisPorGen[op1-1]+"'}) set p.rating = '"+str(promedio)+"'")
        print("\nEl nuevo rating de "+listaPelisPorGen[op1-1]+" es de: " +str(promedio)+".")
        print("Gracias por tu rating, esto nos sirve mucho!")

    #empezando opcion2
    if opcion==2:
        print("adios")

    if opcion==3:
        
        op3 = 0
        ops3 = False
        while not ops3:
            print("\nQue quiere editar?")
            print("---------------------------------")
            print("[1] Quiero Agregar Una Pelicula |")
            print("---------------------------------")
            print("[2] Quiero Eliminar Datos       |")
            print("---------------------------------")
            try:
                opcion = int(input("Opcion> "))
            #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
            except ValueError:
                print('\nIngrese solo numeros!\n')
            #usar un if para asegurarnos que el usuario solo ponga un numero del 1-3  
            if opcion >=1 and opcion <=2:
                ops3 = True
            else:
                print('\nIngrese valores solamente entre 1 y 2.\n')

        if op3 ==1:
            tituloPeli = ""
            yaEsta = False
            while not yaEsta:
                try:
                    tituloPeli = input("\nIngrese el titulo de la pelicula a agregar:")
                except ValueError:
                    print("Ya esta en la base!")
                if tituloPeli in listaPel:
                    yaEsta = True
                else:
                    print("\nEse titulo ya esta en la base de datos!\n")


        if op3 ==2:
            print("hola")

    #iniciar opcion 3
    if opcion==4:
        #imprimir un par de mensajes
        print("\nGracias por utilizar PelRec, vuelve pronto!")
        print("Finalizando Programa...")
        print("Programa Finalizado\n")
        #salir del ciclo
        break
