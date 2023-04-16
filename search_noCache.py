import requests
import json
from pprint import pprint
import time
import matplotlib.pyplot as plt


#Buscar pj por string.
def search_character(name):
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
            #"skills": character['skills']
        }
        characters.append(character_info)

    pprint(characters)
    return characters


#Buscar pjs asociados a afiliacion.
def search_affiliated(nation):
    response = requests.get(f"https://last-airbender-api.fly.dev/api/v1/characters?perPage=1000&affiliation={nation}")
    data = response.json()

    results = []
    for character in data:
        results.append(character['name'])

    pprint(results)
    return results


#Buscador de avatars
def search_avatars_by_name(query):
    url = 'https://last-airbender-api.fly.dev/api/v1/characters/avatar'
    response = requests.get(url)
    if response.ok:
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
        pprint(avatars_info)
        return "\n".join(avatars_info)
    else:
        print("no funciona bro")


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

#Inicia el cronómetro
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

#Para detener el cronómetro
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