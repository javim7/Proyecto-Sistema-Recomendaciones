"""
Maria Fernanda Argueta, Javier Mombiela, Javier Valle
Proyecto Sistema de  Recomendaciones 
Seccion 10
Grupo 8

La funcion de este proyecto es poder hacer una conexion entre neo4j y python
para asi poder extraer datos de neo4j y tambien poder meterle datos y modificarlos.
"""
#importando clases externas
import random
import numpy as np
import pandas as pd
from py2neo import Graph
import matplotlib as plt
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

generos = ["Action","Ciencia Ficcion", "Comedy", "Drama","Horror","Romance"]

for genero in generos:
    session.run("CREATE (p:Usuario {titulo:'"+generos[genero]+"'})")



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
        print("Gracias por tu rating "+nom_usuario+", esto nos sirve mucho!")

    #empezando opcion2
    if opcion==2:
        
        opsent = 0
        opsents = False
        while not opsents: #while para asegurar que ingresen una opcion valida
            print("\nComo te sientes hoy?")
            print("--------------")
            print("[1] Feliz    |")
            print("--------------")
            print("[2] Enojado  |")
            print("--------------")
            print("[3] Triste   |")
            print("--------------")
            try:
                opsent = int(input("Mood> "))
            #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
            except ValueError:
                print('\nIngrese solo numeros!\n')
            #usar un if para asegurarnos que el usuario solo ponga un numero del 1-3  
            if opsent >=1 and opsent <=3:
                opsents = True
            else:
                print('\nIngrese valores solamente entre 1 y 3.\n') 

        #pasando la info de la lista a otra lista para poder editarla
        listagen2 = []

        #for loop para recorrer toda la lista
        for genero in listaGen:
            listagen2.append(genero)

        #preguntando cual es el genero favorito
        print("\nEscoge tu genero favorito:")
        for number, genero in enumerate(listagen2): #imprimiendo los generos como listado
            print(number+1, genero)

        op4 = 0
        ops4 = False
        while not ops4:
            try:
                op4 = int(input("\nGenero> "))
            #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
            except ValueError:
                print('\nIngrese solo numeros!\n')
            #usar un if para asegurarnos que el usuario solo ponga un numero del 1-5    
            if op4 >=1 and op4 <=len(listagen2):
                ops4 = True
            else:
                print('\nIngrese valores solamente entre 1 y 5.\n')

        genero1 = listagen2[op4-1]
        #eliminando ese genero de la lista
        listagen2.remove(genero1)

        #preguntando por otro genero
        print("\nAhora escoge tu segundo genero favorito:")
        for number, genero in enumerate(listagen2): #imprimiendo los generos como listado
            print(number+1, genero)

        op5 = 0
        ops5 = False
        while not ops5:
            try:
                op5 = int(input("\nGenero> "))
            #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
            except ValueError:
                print('\nIngrese solo numeros!\n')
            #usar un if para asegurarnos que el usuario solo ponga un numero del 1-5    
            if op5 >=1 and op5 <=len(listagen2):
                ops5 = True
            else:
                print('\nIngrese valores solamente entre 1 y 5.\n')

        genero2 = listagen2[op5-1]
        #eliminando ese genero de la lista
        listagen2.remove(genero2)

        #meter las peliculas del primer genero a una lista 
        pelisgen1 = session.run("MATCH (a:Pelicula)-[r:es_genero]->(b:Genero {titulo:'"+genero1+"'}) return a.titulo")
        listapelisgen1 = [nodo["a.titulo"] for nodo in pelisgen1]

        randomgen1 = []
        generos1 = []
        #for para obtener 7 pelicula aleatorias y agregarlas a una nueva lista
        for i in range (9):
            peli = random.choice(listapelisgen1)
            randomgen1.append(peli)
            listapelisgen1.remove(peli)
            generos1.append(genero1)

        #creando listas para todas las propiedades de las peliculas
        titulos1 = []
        anos1 = []
        duras1 = []
        ratings1 = []
        #for para poder obtener la informacion de la pelicula 
        for pelicula in randomgen1:
            titulo1 = pelicula
            titulos1.append(titulo1)

            ano1 = session.run("MATCH (p:Pelicula {titulo:'"+pelicula+"'}) return p.año")
            anos2 = [nodo["p.año"] for nodo in ano1]
            anon = anos2.pop(0)
            anos1.append(anon)

            dura1 = session.run("MATCH (p:Pelicula {titulo:'"+pelicula+"'}) return p.duracion")
            duras2 = [nodo["p.duracion"] for nodo in dura1]
            durax = duras2.pop(0)
            duras1.append(durax)

            rating1 = session.run("MATCH (p:Pelicula {titulo:'"+pelicula+"'}) return p.rating")
            ratings2 = [nodo["p.rating"] for nodo in rating1]
            rat = ratings2.pop(0)
            ratings1.append(rat)  

        pelisgen2 = session.run("MATCH (a:Pelicula)-[r:es_genero]->(b:Genero {titulo:'"+genero2+"'}) return a.titulo")
        listapelisgen2 = [nodo["a.titulo"] for nodo in pelisgen2]

        randomgen2 = []
        generos2 = []
        #for para obtener 7 pelicula aleatorias y agregarlas a una nueva lista
        for i in range (7):
            peli = random.choice(listapelisgen2)
            randomgen2.append(peli)
            listapelisgen2.remove(peli)
            generos2.append(genero2)

            #creando listas para todas las propiedades de las peliculas
        titulos22 = []
        anos22 = []
        duras22 = []
        ratings22 = []
        #for para poder obtener la informacion de la pelicula 
        for pelicula in randomgen2:
            titulo22 = pelicula
            titulos22.append(titulo22)

            ano22 = session.run("MATCH (p:Pelicula {titulo:'"+pelicula+"'}) return p.año")
            anos3 = [nodo["p.año"] for nodo in ano22]
            anon = anos3.pop(0)
            anos22.append(anon)

            dura22 = session.run("MATCH (p:Pelicula {titulo:'"+pelicula+"'}) return p.duracion")
            duras3 = [nodo["p.duracion"] for nodo in dura22]
            durax = duras3.pop(0)
            duras22.append(durax)

            rating22 = session.run("MATCH (p:Pelicula {titulo:'"+pelicula+"'}) return p.rating")
            ratings3 = [nodo["p.rating"] for nodo in rating22]
            rat = ratings3.pop(0)
            ratings22.append(rat)

        #serie de ifs para ver cual sera el tercer genero basado en el estado de animo del usuario
        if opsent ==1:
            genero3 = "Comedy"

        if opsent ==2:
            genero3 = "Action"

        if opsent ==3:
            genero3 = "Romance"

        pelisgen3 = session.run("MATCH (a:Pelicula)-[r:es_genero]->(b:Genero {titulo:'"+genero3+"'}) return a.titulo")
        listapelisgen3 = [nodo["a.titulo"] for nodo in pelisgen3]

        randomgen3 = []
        generos3 = []
        #for para obtener 7 pelicula aleatorias y agregarlas a una nueva lista
        for i in range (5):
            peli = random.choice(listapelisgen3)
            randomgen3.append(peli)
            listapelisgen3.remove(peli)
            generos3.append(genero3)

            #creando listas para todas las propiedades de las peliculas
        titulos33 = []
        anos33 = []
        duras33 = []
        ratings33 = []
        #for para poder obtener la informacion de la pelicula 
        for pelicula in randomgen3:
            titulo33 = pelicula
            titulos33.append(titulo33)

            ano33 = session.run("MATCH (p:Pelicula {titulo:'"+pelicula+"'}) return p.año")
            anos4 = [nodo["p.año"] for nodo in ano33]
            anon = anos4.pop(0)
            anos33.append(anon)

            dura33 = session.run("MATCH (p:Pelicula {titulo:'"+pelicula+"'}) return p.duracion")
            duras4 = [nodo["p.duracion"] for nodo in dura33]
            durax = duras4.pop(0)
            duras33.append(durax)

            rating33 = session.run("MATCH (p:Pelicula {titulo:'"+pelicula+"'}) return p.rating")
            ratings4 = [nodo["p.rating"] for nodo in rating33]
            rat = ratings4.pop(0)
            ratings33.append(rat)

        #creando listas vacias para poder combinar ambos generos y recomendar al usuario
        tits = []
        ans = []
        durs = []
        rats = []
        gens = []
        for i in range(len(titulos1)):  #for para agregar toda la info del primer genero a sus listas
            tits.append(titulos1[i])
            ans.append(anos1[i])
            durs.append(duras1[i])
            rats.append(ratings1[i])
            gens.append(generos1[i])

        for i in range(len(titulos22)):  #for para agregar toda la info del segundo genero a sus listas
            tits.append(titulos22[i])
            ans.append(anos22[i])
            durs.append(duras22[i])
            rats.append(ratings22[i])
            gens.append(generos2[i])

        for i in range(len(titulos33)):  #for para agregar toda la info del segundo genero a sus listas
            tits.append(titulos33[i])
            ans.append(anos33[i])
            durs.append(duras33[i])
            rats.append(ratings33[i])
            gens.append(generos3[i])
                

        #rec = pd.read_csv("Recomendaciones.csv")
        #agregando diccionario de listas para poder agregar al csv
        recos = { 'Titulo': tits,
        'Año': ans,
        'Duración': durs,
        'Rating': rats,
        'Genero': gens
        }

        #escribiendo encabezados del csv
        df = pd.DataFrame(recos)

        #pasando toda la info al archivo sorteado dependiendo del rating
        df = df.sort_values(by=["Rating"], ascending=False)
        df.to_csv("Recomendaciones.csv",index=False)

        #imrpimiendo csv
        print("\n\nEstas son las top recomendaciones para usted: ")
        print(pd.read_csv("Recomendaciones.csv"))

        #eliminando datos del csv para poder tener el archivo siempre limpio
        with open("Recomendaciones.csv", 'r+') as recomend:
            recomend.readline() # leyendo solo primera fila para dejar los titulos de las colunas
            recomend.truncate(recomend.tell()) # eliminando todo lo demas
                        

    if opcion==3:
        
        op3 = 0
        ops3 = False
        while not ops3: #while para asegurar que ingresen una opcion valida
            print("\nQue quiere editar?")
            print("---------------------------------")
            print("[1] Quiero Agregar Una Pelicula |")
            print("---------------------------------")
            print("[2] Quiero Eliminar Datos       |")
            print("---------------------------------")
            try:
                op3 = int(input("Opcion> "))
            #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
            except ValueError:
                print('\nIngrese solo numeros!\n')
            #usar un if para asegurarnos que el usuario solo ponga un numero del 1-3  
            if op3 >=1 and op3 <=2:
                ops3 = True
            else:
                print('\nIngrese valores solamente entre 1 y 2.\n')

        if op3 ==1:

            tituloPeli = "" #inicializando el nombre de la peli como vacio para despues poder usarlo
            yaEsta = False
            #while para que ingrese el nombre de una pelicula que no este en la base de datos
            while not yaEsta:
                try:
                    tituloPeli = input("\nIngrese el titulo de la pelicula a agregar: ")
                except ValueError:
                    print("ya esta en la base!")
                if tituloPeli not in listaPel: #viendo si la pelicula ya esta en la base de datos ono
                    yaEsta = True
                else:
                    print("\nEse titulo ya esta en la base de datos!")

            #continuando con la pedida de los datos de la pelicula
            anoPel=""
            #while para que solo ingresen digitos y no strings
            siEs = False
            while not siEs:
                try:
                    anoPel = int(input("\nIngrese el año en el que salio la pelicula: "))
                    it_is = True
                except ValueError: #error por si se ingresa algun tipo de dato
                    it_is = False
                if it_is == True:
                    siEs = True #saliendo del loop
                else:
                    print("\nSolo se aceptan numeros!")

            duraPel = ""
            #while para que solo ingresen digitos y no strings
            siEs2 = False
            while not siEs2:
                try:
                    duraPel = int(input("\nIngrese la duración de la pelicula sin signos (ej. 1:32 seria solo 132): "))
                    it_is = True
                except ValueError: #error por si se ingresa algun tipo de dato
                    it_is = False
                if it_is == True:
                    siEs2 = True #saliendo del loop
                else:
                    print("\nSolo se aceptan numeros!")

            ratingPel = ""
            #while para que solo ingresen digitos y no strings
            siEs3 = False
            while not siEs3:
                try:
                    ratingPel = float(input("\nIngrese el rating de la pelicula (en su opinion y de 1-5): "))
                    it_is = True
                except ValueError: #error por si se ingresa algun tipo de dato
                    it_is = False
                if it_is == True:
                    siEs3 = True #saliendo del loop
                else:
                    print("\nSolo se aceptan numeros!")


            print("\nSeleccione el genero que contiene la pelicula a recomendar:")
            for number, genero in enumerate(listaGen): #imprimiendo los generos como listado
                print(number+1, genero)

        #haciendo un while para asegurar que se elija la opcion correcta
            opsgen = 0
            opsgens = False
            while not opsgens:
                try:
                    opsgen = int(input("\nGenero> "))
                #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
                except ValueError:
                    print('\nIngrese solo numeros!\n')
                #usar un if para asegurarnos que el usuario solo ponga un numero del 1-5    
                if opsgen >=1 and opsgen <=len(listaGen):
                    opsgens = True
                else:
                    print('\nIngrese valores solamente entre 1 y 5.\n')

            session.run("CREATE (p:Pelicula {titulo:'"+str(tituloPeli)+"', duracion:'"+str(duraPel)+"', año:'"+str(anoPel)+"', rating:'"+str(ratingPel)+"'})")
            session.run("MATCH (a:Pelicula{titulo:'"+str(tituloPeli)+"'}),(b:Genero{titulo:'"+listaGen[opsgen-1]+"'}) MERGE (a)-[r:es_genero]->(b)")


            print("\n"+tituloPeli+" se ha agregado a la base de datos! Muchas gracias " +nom_usuario+"!")

        if op3 ==2:
            
            op4 = 0
            ops4 = False
            while not ops4: #while para asegurar que ingresen una opcion valida
                print("\nQue quiere eliminar?")
                print("-----------------------------------")
                print("[1] Quiero Eiliminar una Pelicula |")
                print("-----------------------------------")
                print("[2] Quiero Eliminar un Usuario    |")
                print("-----------------------------------")
                try:
                    op4 = int(input("Opcion> "))
                #usar un except para asegurarnos que si el usuario ingresa letras, el código no parara abruptamente    
                except ValueError:
                    print('\nIngrese solo numeros!\n')
                #usar un if para asegurarnos que el usuario solo ponga un numero del 1-3  
                if op4 >=1 and op4 <=2:
                    ops4 = True
                else:
                    print('\nIngrese valores solamente entre 1 y 2.\n')

            if op4 ==1:
                
                tituloPeli2 = "" #inicializando el nombre de la peli como vacio para despues poder usarlo
                yaEsta2 = False
                #while para que ingrese el nombre de una pelicula que no este en la base de datos
                while not yaEsta2:
                    try:
                        tituloPeli2 = input("\nIngrese el titulo de la pelicula a eliminar: ")
                    except ValueError:
                        print("ya esta en la base!")
                    if tituloPeli2 in listaPel: #viendo si la pelicula esta en la base de datos ono
                        yaEsta2 = True
                    else:
                        print("\nEse titulo no esta en la base de datos!")

                session.run("MATCH (p:Pelicula {titulo: '"+tituloPeli2+"'}) DETACH DELETE p")

                print("\n"+tituloPeli2+" se ha eliminado de la base de datos, gracias "+nom_usuario+"!")

            if op4 == 2:
                
                usuarioBorrar = "" #inicializando el nombre de la peli como vacio para despues poder usarlo
                yaEsta3 = False
                #while para que ingrese el nombre de una pelicula que no este en la base de datos
                while not yaEsta3:
                    try:
                        usuarioBorrar = input("\nIngrese el usuario a eliminar: ")
                    except ValueError:
                        print("ya esta en la base!")
                    if usuarioBorrar in listaUs: #viendo si la pelicula esta en la base de datos ono
                        yaEsta3 = True
                    else:
                        print("\nEse usuario no esta en la base de datos!")

                session.run("MATCH (p:Usuario {titulo: '"+usuarioBorrar+"'}) DETACH DELETE p")

                print("\n"+usuarioBorrar+" se ha eliminado de la base de datos, gracias "+nom_usuario+"!")

    #iniciar opcion 3
    if opcion==4:
        #imprimir un par de mensajes
        print("\nGracias por utilizar PelRec, vuelve pronto!")
        print("Finalizando Programa...")
        print("Programa Finalizado\n")
        #salir del ciclo
        break
