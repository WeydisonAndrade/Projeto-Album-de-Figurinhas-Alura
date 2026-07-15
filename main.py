# Importa a classe FastAPI
from fastapi import FastAPI

# Cria a instância da aplicação FastAPI
app = FastAPI()

# Define o endpoint GET para o caminho raiz "/"
@app.get("/")
def hello_world():
    # Retorna o JSON com a mensagem de boas-vindas
    return {"mensagem": "Olá, mundo! 🌍"}
