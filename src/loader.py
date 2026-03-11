# Funções para carregar os JSONs
import json

def load_pokemons(path="data/pokemons.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        dicionario_pokemons = json.load(f)
        if isinstance(dicionario_pokemons, dict) and "pokemon" in dicionario_pokemons:
            return dicionario_pokemons["pokemon"]
        return dicionario_pokemons

def load_questions(path="data/questions.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
