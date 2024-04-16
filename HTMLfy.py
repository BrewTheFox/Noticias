import time
from gtts import gTTS
import os

def GenerarHTML(Noticia):
    plantilla = ""
    with open("./plantilla.html", "r+") as plantilla:
        plantilla = plantilla.read()
        
    articulo = Noticia.articulo.replace(".", ".\n")
    palabras_html = ""
    for palabra,significado in Noticia.diccionario.items():
        palabras_html += f"<li>{palabra.lower().capitalize()}: {significado}</li>"
    palabras_html = f"<ul>{palabras_html}</ul>"
    
    hora = str(int(time.time()))
    directorio = f"./{hora}"
    os.makedirs(directorio, exist_ok=True)
    with open(f"./{hora}/index.html", "w+") as HTML:
        plantilla = plantilla.replace("{{titulo}}", Noticia.titulo)
        plantilla = plantilla.replace("{{title}}", Noticia.title)
        plantilla = plantilla.replace("{{autor}}", Noticia.autor)
        plantilla = plantilla.replace("{{fecha}}", Noticia.fecha)
        plantilla = plantilla.replace("{{fuente}}", Noticia.link)
        plantilla = plantilla.replace("{{Noticia}}", articulo)
        plantilla = plantilla.replace("{{Imagen}}", Noticia.imagen)
        plantilla = plantilla.replace("{{IdeaPrincipal}}", Noticia.ideaPrincipal)
        plantilla = plantilla.replace("{{Palabras}}", palabras_html)
        plantilla = plantilla.replace("{{Resumen}}", Noticia.resumen)
        plantilla = plantilla.replace("{{OpinionPersonal}}", Noticia.OpinionPersonal)
        HTML.write(plantilla)
    gTTS(Noticia.ideaPrincipal.replace(".", " Punto....").replace(",", " Coma....").replace(":", " Dos puntos:....").replace(";", " Punto y coma...."), lang='es',slow=True).save(f"./{hora}/idea.mp3")
    gTTS(Noticia.resumen.replace(".", " Punto....").replace(",", " Coma....").replace(":", " Dos puntos:....").replace(";", " Punto y coma...."), lang='es',slow=True).save(f"./{hora}/resumen.mp3")
    gTTS(Noticia.OpinionPersonal.replace(".", " Punto....").replace(",", " Coma....").replace(":", " Dos puntos:....").replace(";", " Punto y coma...."), lang='es',slow=True).save(f"./{hora}/op.mp3")
