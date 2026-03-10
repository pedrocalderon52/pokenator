# Funções para carregar os JSONs
import json

def load_pokemons(path="data/pokemons.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_questions(path="data/questions.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)