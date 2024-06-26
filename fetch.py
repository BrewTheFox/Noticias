import requests
import re
import random
import json
import AI
import os
from translate import Translator
import random
import HTMLfy

traductor = Translator(from_lang="es",to_lang="en")
directorios = os.listdir("./LLms")
modelos = []
if len(directorios) > 1:
    for modelo in directorios:
        if modelo.lower().endswith(".gguf"):
            modelos.append(modelo)
for index, modelo in enumerate(modelos):
    print(f"{index}){modelo.lower().capitalize()}")
try:
    modelo = "./LLms/" + modelos[int(input("¿Que modelo deseas usar (Indice)? \n >"))]
    AI.LoadModel(modelo)
except ValueError:
    raise Exception("No se admite texto como entrada.")
except IndexError:
    raise Exception("No se encontro el indice.")


def ObtenerDatos():
    class Noticia:
        def __init__(self, autor=None, titulo=None, fecha=None, fuente=None, articulo=None, imagen=None, link=None):
            self.autor = autor
            self.titulo = titulo
            self.title = traductor.translate(titulo)
            self.fecha = fecha
            self.fuente = fuente
            self.articulo = articulo
            self.imagen = imagen
            self.link = link

        def Resumir(self):
            self.resumen = AI.GenerarResumen(self.articulo)
            return self.resumen
        
        def GenerarPalabras(self):
            diccionario = {}
            palabras = self.articulo.split(" ")
            palabras = list(dict.fromkeys(palabras))
            palabrasF = []
            for palabra in palabras:
                if len(palabra) > 4:
                    if not "&" in palabra and not "/" in palabra and not "’" in palabra and not "“" in palabra and not ";" in palabra and not "," in palabra and not "*" in palabra and not '"' in palabra and not "." in palabra and not ":" in palabra and not "@" in palabra and not "(" in palabra and not ")" in palabra and not "'" in palabra and not "-" in palabra:
                        if palabra != "None":
                            palabrasF.append(palabra)
            
            for opcion in random.sample(palabrasF, min(5, len(palabrasF))):
                url = f"https://www.diccionarios.com/diccionario/espanol/{opcion}"
                response = requests.get(url)
                rediccionario = re.compile(r'<font class="gris13">([^<]*)</font>')
                definiciones = rediccionario.findall(response.text)
                for definicion in definiciones:
                    palabras_definicion = definicion.strip().split()
                    if len(palabras_definicion) >= 5:
                        diccionario[opcion] = definicion.strip()
                        break
            self.diccionario = diccionario
            return diccionario
        
        def GenerarIdeaPrincipal(self):
            self.ideaPrincipal = AI.GenerarIdeaPrincipal(self.articulo)
            return self.ideaPrincipal
        
        def GenerarOpinion(self):
            self.OpinionPersonal = AI.GenerarOpinion(self.articulo)
            return self.OpinionPersonal
            
    opciones = ["colombia", "economia", "mundo", "politica", "justicia", "tecnosfera"]
    opcion = random.choice(opciones)
    Peticion = requests.get("https://www.eltiempo.com/" + opcion)
    Noticias= []
    expresion = re.compile(f"/{opcion}/[a-zA-Z]*/.*\">")
    expresion2 = re.compile("<script\n.*>(.*}}})")
    for match in expresion.finditer(Peticion.text):
        Noticias.append(match.group().replace('">', ""))
    
    urlnoticia = "http://www.eltiempo.com" + random.choice(Noticias)
    print(urlnoticia)
    ContenidoNoticia = requests.get(urlnoticia)
    with open("prueba.html", "w+") as archivo:
        archivo.write(ContenidoNoticia.text)

    for Contenido in expresion2.finditer(ContenidoNoticia.text):
        informacion = json.loads(Contenido.group(1).replace('<script type="application/ld+json">', ""))
    try:
        preautor = informacion["author"]["name"]
    except:
        preautor = informacion["author"][0]["name"]
    noticia = Noticia(
    autor=preautor,
    titulo=informacion["headline"],
    fecha=informacion["datePublished"],
    fuente=informacion["isPartOf"]["sku"],
    imagen=informacion["image"][0]["url"],
    articulo=informacion["articleBody"],
    link=urlnoticia
    )
    return noticia

if __name__ == "__main__":
    for i in range(1):
        Noticia = ObtenerDatos()
        print(Noticia.Resumir())
        os.system("clear")
        print(Noticia.resumen)
        print(Noticia.titulo)
        print(Noticia.title)
        print(Noticia.link)
        print(Noticia.autor)
        print(Noticia.fecha)
        print(Noticia.fuente)
        print(Noticia.GenerarPalabras())
        print(Noticia.GenerarIdeaPrincipal())
        print(Noticia.GenerarOpinion())
        HTMLfy.GenerarHTML(Noticia)
