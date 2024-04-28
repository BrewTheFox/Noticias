from llama_cpp import Llama
import sys
import os

template = """  
    [INST] <<SYS>>    Eres un asistente servicial, respetuoso y honesto. Responda siempre de la manera más útil posible y siendo seguro.
    Tus respuestas no deben incluir ningún contenido dañino, poco ético, racista, sexista, tóxico, peligroso o ilegal.
    Asegúrese de que sus respuestas sean socialmente imparciales y de naturaleza positiva.
    Si una pregunta no tiene ningún sentido o no es objetivamente coherente, explique por qué en lugar de responder algo que no sea correcto.
    Si no sabe la respuesta a una pregunta, no comparta información falsa. 
    <</SYS>>    {INSERT_PROMPT_HERE} [/INST]    """  

class suppress_stdout_stderr(object):
    def __enter__(self):
        self.outnull_file = open(os.devnull, 'w')
        self.errnull_file = open(os.devnull, 'w')

        self.old_stdout_fileno_undup    = sys.stdout.fileno()
        self.old_stderr_fileno_undup    = sys.stderr.fileno()

        self.old_stdout_fileno = os.dup ( sys.stdout.fileno() )
        self.old_stderr_fileno = os.dup ( sys.stderr.fileno() )

        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        os.dup2 ( self.outnull_file.fileno(), self.old_stdout_fileno_undup )
        os.dup2 ( self.errnull_file.fileno(), self.old_stderr_fileno_undup )

        sys.stdout = self.outnull_file        
        sys.stderr = self.errnull_file
        return self

    def __exit__(self, *_):        
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        os.dup2 ( self.old_stdout_fileno, self.old_stdout_fileno_undup )
        os.dup2 ( self.old_stderr_fileno, self.old_stderr_fileno_undup )

        os.close ( self.old_stdout_fileno )
        os.close ( self.old_stderr_fileno )

        self.outnull_file.close()
        self.errnull_file.close()

llm = None

def LoadModel(Modelo):
    global llm
    llm = Llama(  
        model_path=Modelo,  
        n_ctx=12288,  
        n_batch=512,  
        n_threads=8,  
        verbose=True, 
        n_gpu_layers=-1
    ) 


def GenerarResumen(Texto:str):
    print("Generando...")

    prompt = (  
        "Resume la siguiente noticia en minimo 6 parrafos: "  
        + Texto  
    )

    prompt = template.replace("INSERT_PROMPT_HERE", prompt) 

    output = llm(prompt, max_tokens=-1, echo=True, temperature=0.2, top_p=0.1)  
    return output["choices"][0]["text"].replace(prompt, "")

def GenerarIdeaPrincipal(Texto:str):
  print("Generando...")
  with suppress_stdout_stderr():
        prompt = (  
        "Genera una idea principal corta del siguiente texto: "  
        + Texto  
    )

        prompt = template.replace("INSERT_PROMPT_HERE", prompt) 

        output = llm(prompt, max_tokens=-1, echo=True, temperature=0.2, top_p=0.1)  
        return output["choices"][0]["text"].replace(prompt, "")

def GenerarOpinion(Texto:str):
    print("Generando...")
    with suppress_stdout_stderr():
        prompt = (  
        "Esta noticia es verdadera, tu tienes que generar una opinion que diria una persona positiva acerca del tema:"  
        + Texto  
         )
        prompt = template.replace("INSERT_PROMPT_HERE", prompt) 
        output = llm(prompt, max_tokens=-1, echo=True, temperature=0.2, top_p=0.1)  
        return output["choices"][0]["text"].replace(prompt, "")
