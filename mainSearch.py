import requests
import json
from pprint import pprint
import redis
import hashlib
import time
from random import randint
import matplotlib.pyplot as plt

#Configuracion Redis para redis1, redis2, redis3
r1 = redis.Redis(host='localhost', port=6379)
r2 = redis.Redis(host='localhost', port=6380)
r3 = redis.Redis(host='localhost', port=6381)
r1.flushall()
r2.flushall()
r3.flushall()

#Funcion de hash
def get_hash(key):
    return hashlib.sha256(key.encode()).hexdigest()

#Dividir el rango de valores hash en tres partes iguales
range1 = ('0', '5555555555555555555555555555555555555555555555555555555555555555')
range2 = ('5555555555555555555555555555555555555555555555555555555555555556', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
range3 = ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')


#########   FUNCIONES DE BUSQUEDA   #########

#Buscar pj por string.
def search_character(name):
    print("Buscando '{name}'")
    key = f"search_character:{name}"
    h = get_hash(key)

    #Determinar a qué partición pertenece
    if h >= range1[0] and h <= range1[1]:
        print("particion r1")
        r = r1
    elif h >= range2[0] and h <= range2[1]:
        print("particion r2")
        r = r2
    else:
        print("particion r3")
        r = r3

    #Buscar la clave en la instancia de Redis correspondiente
    result = r.get(key)
    print("Está en esta partición?")

    #Si no se encuentra en Redis, buscar en la API y guardar el resultado en Redis
    if result is None:
        print("No está en cache, lo busco en la API")
        api_url = f"https://last-airbender-api.fly.dev/api/v1/characters?name={name}"
        response = requests.get(api_url)
        data = response.json()

        characters = []
        for character in data:
            character_info = {
                "name": character['name'],
                "affiliation": character.get('affiliation', ''),
                "allies": character['allies'],
                "enemies": character['enemies']
            }
            characters.append(character_info)

        result = str(characters)
        r.set(key, result, ex=3600)
    print(result)
    return result


#Buscar pjs por affiliation
def search_affiliated(nation):
    key = f"search_affiliated:{nation}"
    h = get_hash(key)

    #Determinar a qué partición pertenece
    if h >= range1[0] and h <= range1[1]:
        print("particion r1")
        r = r1
    elif h >= range2[0] and h <= range2[1]:
        print("particion r2")
        r = r2
    else:
        print("particion r3")
        r = r3

    #Buscar datos en Redis
    data = r.get(key)
    if data is not None:
        #Si los datos existen en Redis, convertirlos en una lista de Python
        print(f"Estoy en caché jeje")
        results = json.loads(data)
        print(results)
    else:
        print("Estoy en la API")
        #Si los datos no existen en Redis, se hace la petición HTTP
        response = requests.get(f"https://last-airbender-api.fly.dev/api/v1/characters?perPage=1000&affiliation={nation}")
        data = response.json()
        #Extraer solo los nombres de los personajes
        results = []
        for character in data:
            results.append(character['name'])
        #Convertir la lista de Python en un JSON y almacenarla en Redis
        r.set(key, json.dumps(results), ex=3600)
        print(results)

    return results

#Buscar avatar por nombre
def search_avatars_by_name(query):
    key = f"search_avatars_by_name:{query.lower()}"
    h = get_hash(key)

    #Determinar a qué partición pertenece
    if h >= range1[0] and h <= range1[1]:
        print("particion r1")
        r = r1
    elif h >= range2[0] and h <= range2[1]:
        print("particion r2")
        r = r2
    else:
        print("particion r3")
        r = r3

    #Verificamos si el resultado ya se encuentra en caché de la partición correspondiente
    cached_result = r.get(query.lower())
    if cached_result:
        print("Está en caché")
        print(cached_result)
        return cached_result.decode('utf-8')

    #Si el resultado no está en caché, hacemos la petición a la API
    url = 'https://last-airbender-api.fly.dev/api/v1/characters/avatar'
    response = requests.get(url)

    if response.ok:
        print("No está en caché, lo busco en la API")
        data = response.json()
        result = []
        for avatar in data:
            if query.lower() in avatar['name'].lower():
                result.append(avatar)
        keys = ['name', 'affiliation', 'allies' , 'enemies', 'position', 'profession', 'predecessor']
        avatars_info = []
        for avatar in result:
            avatar_info = []
            for key in keys:
                avatar_info.append(f"{key}: {avatar.get(key)}")
            avatars_info.append(", ".join(avatar_info))

        #Guardamos los resultados en caché de la partición correspondiente
        r.set(query.lower(), "\n".join(avatars_info), ex=3600)

        print(avatars_info)
        return "\n".join(avatars_info)
    else:
        print("No se pudo obtener la información de la API")


#Lista de nombres de pj y affiliation
characters = ['Aang', 'Zuko', 'Katara', 'Sokka', 'Toph', 'Iroh', 'Aang', 'Katara', 'Aang', 'Zuko','Azula', 'Wei', 'Kya', 'Ozai', 'Gyatso', 'Jet', 'Appa', 
              'Katara', 'Joo Dee', 'Haru', 'Momo', 'Aang', 'Zuko', 'Toph', 'Jin', 'Beifong', 'Poppy Beifong', 'Gyatso', 'Aang', 'Zuko', 'Tah', 'Jin', 'Katara', 
              'Ozai', 'Appa', 'Zuko', 'Fong','Juno', 'Aang', 'Fong', 'Joo Dee', 'Toph', 'Huan', 'Raiko', 'Azulon', 'Roku', 'Kyoshi', 'Bosco', 'Jee', 'Kya', 'Katara', 'Zuko',
              'Aang', 'Zuko', 'Katara', 'Sokka', 'Toph', 'Iroh', 'Aang', 'Katara', 'Aang', 'Zuko','Azula', 'Wei', 'Kya', 'Ozai', 'Gyatso', 'Jet', 'Appa', 
              'Katara', 'Joo Dee', 'Haru', 'Momo', 'Aang', 'Zuko', 'Toph', 'Jin', 'Beifong', 'Poppy Beifong', 'Gyatso', 'Aang', 'Zuko', 'Tah', 'Jin', 'Katara', 
              'Ozai', 'Appa', 'Zuko', 'Juno', 'Aang', 'Fong', 'Joo Dee', 'Toph', 'Huan', 'Raiko', 'Azulon', 'Roku', 'Kyoshi', 'Bosco', 'Jee', 'Kya', 'Katara', 'Zuko',
              'Fong'] 

found_count = 0
not_found_count = 0

#Start tiempo
start_time = time.time()

search_times = []

#Iterar sobre la lista de personajes y buscarlos en la API
for character in characters:

    #Obtener el tiempo de inicio de la búsqueda
    search_start_time = time.time()
    
    result = search_character(character)

    #Obtener el tiempo de fin de la búsqueda
    search_end_time = time.time()

    #Calcular el tiempo de búsqueda
    search_time = search_end_time - search_start_time

    if result:
        found_count += 1
    else:
        not_found_count += 1

    # Si la tasa de éxito comienza a disminuir, detener la búsqueda
    success_rate = found_count / (found_count + not_found_count)
    if success_rate < 0.9:
        break

    search_times.append(search_time)

    print(f'Tiempo de búsqueda para {character}: {search_time} segundos')

#Stop tiempo
end_time = time.time()
total_time = end_time - start_time

#Gráfico cache
plt.bar(range(len(search_times)), search_times)
plt.title('Tiempo de búsqueda de personajes')
plt.xlabel('Personaje')
plt.ylabel('Tiempo de búsqueda (segundos)')
plt.show()

print(f'Número de personajes encontrados: {found_count}')
print(f'Número de personajes no encontrados: {not_found_count}')
print(f'Tiempo total de búsqueda: {total_time} segundos')


#search_character(input("Enter character name: "))
#search_affiliated(input("Enter affiliation name: "))
#search_avatars_by_name(input("Buscador de avatar: "))
