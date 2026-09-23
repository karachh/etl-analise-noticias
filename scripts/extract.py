from dotenv import load_dotenv
import os
import requests
from raw import criar_conexao, criar_tabela, inserir_artigo 

load_dotenv()
api_key = os.environ["NEWSAPI_KEY"]

response = requests.get(
    "https://newsapi.org/v2/top-headlines",
    params={"category": "technology", "apiKey": api_key}
)

data = response.json()
artigo = data["articles"][0] 

conn = criar_conexao("raw.db")
criar_tabela(conn)
inserir_artigo(conn, artigo)
conn.close() 
