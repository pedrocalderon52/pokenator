from loader import load_pokemons, load_questions
from utils import choose_best_question
from engine import Answer, PokeAkinator
from experta import MATCH

# -----------------------------
# Carrega dados
# -----------------------------
pokemon_data = load_pokemons()
questions_data = load_questions()

# -----------------------------
# Cria atributos
# -----------------------------
attributes = []
all_attrs = {}

# cores
for color in questions_data["colors"]:
    key = f"is_color_{color}"
    attributes.append(key)

# atributos gerais
for attr in questions_data["attributes"]:
    attributes.append(attr["key"])

# tipos
for t in questions_data["types"]:
    attributes.append(f"type_{t}")

# mapeia atributos
for p in pokemon_data:
    attr_map = {}
    for color in questions_data["colors"]:
        attr_map[f"is_color_{color}"] = (p["color"] == color)
    for attr in questions_data["attributes"]:
        key = attr["key"]
        if key == "is_legendary":
            attr_map[key] = p["is_legendary"]
        elif key == "is_quadruped":
            attr_map[key] = (p["shape"] == "quadruped")
    for t in questions_data["types"]:
        attr_map[f"type_{t}"] = (t in p["types"])
    all_attrs[p["name"]] = attr_map

# -----------------------------
# Mapa perguntas
# -----------------------------
questions_map = {}
for color in questions_data["colors"]:
    questions_map[f"is_color_{color}"] = f"Seu Pokémon é {color}?"
for attr in questions_data["attributes"]:
    questions_map[attr["key"]] = attr["question"]
for t in questions_data["types"]:
    questions_map[f"type_{t}"] = f"Ele é do tipo {t}?"

# -----------------------------
# Inicializa motor
# -----------------------------
engine = PokeAkinator(all_attrs)
engine.reset()
asked_attrs = set()

# -----------------------------
# Loop de perguntas
# -----------------------------
while len(engine.possible_pokemons) > 1:
    next_attr = choose_best_question(engine.possible_pokemons, all_attrs, attributes, asked_attrs)
    if not next_attr:
        break
    answer = input(questions_map[next_attr] + " (s/n): ").strip().lower()
    val = answer == "s"
    engine.declare(Answer(attribute=next_attr, value=val))
    engine.run()
    asked_attrs.add(next_attr)

# Resultado final
if len(engine.possible_pokemons) == 1:
    print("O Pokémon é:", list(engine.possible_pokemons)[0])
elif engine.possible_pokemons:
    print("Pokémon possíveis:", engine.possible_pokemons)
else:
    print("Nenhum Pokémon corresponde às respostas.")