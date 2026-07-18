import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Cria a instância da aplicação FastAPI
app = FastAPI()

# Configura o CORS para permitir requisições de qualquer origem (essencial para o frontend carregar os dados)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define o caminho absoluto da pasta de imagens (para encontrar a pasta independentemente de onde for executado)
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(PASTA_BASE, "figurinhas")

# Configura o serviço de arquivos estáticos, montando a pasta de imagens na rota "/imgs"
app.mount("/imgs", StaticFiles(directory=PASTA_IMAGENS), name="imgs")

# Lista contendo todas as figurinhas correspondentes aos slots do álbum
figurinhas = [
    {"id": 1, "nome": "Alan Turing", "categoria": "IA", "imagem_url": "/imgs/01-alan-turing.jpg"},
    {"id": 2, "nome": "John McCarthy", "categoria": "IA", "imagem_url": "/imgs/02-john-mccarthy.jpg"},
    {"id": 3, "nome": "Sam Altman", "categoria": "IA", "imagem_url": "/imgs/03-sam.jpg"},
    {"id": 4, "nome": "Geoffrey Hinton", "categoria": "IA", "imagem_url": "/imgs/04-Geoffrey.jpg"},
    {"id": 5, "nome": "Yann LeCun", "categoria": "IA", "imagem_url": "/imgs/05-Yann.jpeg"},
    {"id": 6, "nome": "Guido van Rossum", "categoria": "PYTHON", "imagem_url": "/imgs/06-Guido.jpg"},
    {"id": 7, "nome": "Tim Peters", "categoria": "PYTHON", "imagem_url": "/imgs/07-Tim.jpeg"},
    {"id": 8, "nome": "Raymond Hettinger", "categoria": "PYTHON", "imagem_url": "/imgs/08-Ray.jpeg"},
    {"id": 9, "nome": "Travis Oliphant", "categoria": "PYTHON", "imagem_url": "/imgs/09-Travis.jpg"},
    {"id": 10, "nome": "Wes McKinney", "categoria": "PYTHON", "imagem_url": "/imgs/10-Wes.jpg"},
    {"id": 11, "nome": "Edgar F. Codd", "categoria": "BANCO DE DADOS", "imagem_url": "/imgs/11-Edgar.jpeg"},
    {"id": 12, "nome": "Larry Ellison", "categoria": "BANCO DE DADOS", "imagem_url": "/imgs/12-Larry.jpg"},
    {"id": 13, "nome": "Michael Widenius", "categoria": "BANCO DE DADOS", "imagem_url": "/imgs/13-Michael.webp"},
    {"id": 14, "nome": "Salvatore Sanfilippo", "categoria": "BANCO DE DADOS", "imagem_url": "/imgs/14-Salvatore.png"},
    {"id": 15, "nome": "Eliot Horowitz", "categoria": "BANCO DE DADOS", "imagem_url": "/imgs/15-Eliot.png"},
    {"id": 16, "nome": "Linus Torvalds", "categoria": "SISTEMAS OPERACIONAIS", "imagem_url": "/imgs/16-Linus.jpg"},
    {"id": 17, "nome": "Dennis Ritchie", "categoria": "SISTEMAS OPERACIONAIS", "imagem_url": "/imgs/17-Dennis.png"},
    {"id": 18, "nome": "Richard Stallman", "categoria": "SISTEMAS OPERACIONAIS", "imagem_url": "/imgs/18-Richard.jpg"},
    {"id": 19, "nome": "Bill Gates", "categoria": "SISTEMAS OPERACIONAIS", "imagem_url": "/imgs/19-bill.jpg"},
    {"id": 20, "nome": "Steve Jobs", "categoria": "SISTEMAS OPERACIONAIS", "imagem_url": "/imgs/20-Steve.webp"},
    {"id": 21, "nome": "Paulo Silveira", "categoria": "BRASIL", "imagem_url": "/imgs/21-Paulo.avif"},
    {"id": 22, "nome": "Guilherme Silveira", "categoria": "BRASIL", "imagem_url": "/imgs/22-Guilherme.jpeg"},
    {"id": 23, "nome": "Gustavo Guanabara", "categoria": "BRASIL", "imagem_url": "/imgs/23-Gus.png"},
    {"id": 24, "nome": "Maurício Aniche", "categoria": "BRASIL", "imagem_url": "/imgs/24-Mauricio.jpeg"},
    {"id": 25, "nome": "Andre David", "categoria": "BRASIL", "imagem_url": "/imgs/25-Andre.jpeg"},
    {"id": 26, "nome": "Guilherme Lima", "categoria": "BRASIL", "imagem_url": "/imgs/26-Guilherme.jpeg"},
    {"id": 27, "nome": "Gi Space Coding", "categoria": "BRASIL", "imagem_url": "/imgs/27-Gi.jpeg"},
    {"id": 28, "nome": "Vinicius Neves", "categoria": "BRASIL", "imagem_url": "/imgs/28-Vinicius.png"},
    {"id": 29, "nome": "Rafaela Ballerini", "categoria": "BRASIL", "imagem_url": "/imgs/29-Rafa.jpeg"}
]

# Endpoint GET que retorna a lista de todas as figurinhas
@app.get("/figurinhas")
def listar_figurinhas():
    # Retorna a lista contendo as figurinhas cadastradas
    return figurinhas
