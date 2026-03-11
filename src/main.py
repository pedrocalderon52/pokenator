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
    color_value = color["value"]
    attributes.append(f"is_color_{color_value}")

# atributos gerais
for attr in questions_data["attributes"]:
    attributes.append(attr["key"])

# tipos
for pokemon_type in questions_data["types"]:
    type_value = pokemon_type["value"]
    attributes.append(f"type_{type_value}")

# mapeia atributos
for p in pokemon_data:
    attr_map = {}

    for color in questions_data["colors"]:
        color_value = color["value"]
        attr_map[f"is_color_{color_value}"] = p.get("color") == color_value

    for attr in questions_data["attributes"]:
        key = attr["key"]
        if key == "is_legendary":
            attr_map[key] = p.get("is_legendary", False)
        elif key == "is_mythical":
            attr_map[key] = p.get("is_mythical", False)
        elif key == "is_evolved":
            attr_map[key] = p.get("evolves_from") is not None
        elif key == "has_multiple_types":
            attr_map[key] = p.get("has_multiple_types", False)
        elif key == "is_firstgen":
            attr_map[key] = p.get("generation") == "generation-i"
        elif key == "is_short":
            attr_map[key] = p.get("height_category") == "short"
        elif key == "is_medium":
            attr_map[key] = p.get("height_category") == "medium"
        elif key == "is_tall":
            attr_map[key] = p.get("height_category") == "tall"
        else:
            attr_map[key] = bool(p.get(key, False))

    for pokemon_type in questions_data["types"]:
        type_value = pokemon_type["value"]
        attr_map[f"type_{type_value}"] = type_value in p.get("types", [])

    all_attrs[p["name"]] = attr_map

# -----------------------------
# Mapa perguntas
# -----------------------------
questions_map = {}
for color in questions_data["colors"]:
    color_value = color["value"]
    questions_map[f"is_color_{color_value}"] = color["question"]

for attr in questions_data["attributes"]:
    questions_map[attr["key"]] = attr["question"]

for pokemon_type in questions_data["types"]:
    type_value = pokemon_type["value"]
    questions_map[f"type_{type_value}"] = pokemon_type["question"]

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
    next_attr = choose_best_question(
        engine.possible_pokemons, all_attrs, attributes, asked_attrs
    )
    if not next_attr:
        break

    answer = input(questions_map[next_attr] + " (s/n): ").strip().lower()
    val = answer == "s"
    engine.declare(Answer(attribute=next_attr, value=val))
    engine.run()
    asked_attrs.add(next_attr)

# Resultado final
if len(engine.possible_pokemons) == 1: # alterar aqui para colocar a probabilidade
    print("O Pokemon é:", list(engine.possible_pokemons)[0])
elif engine.possible_pokemons:
    print("Pokemons possiveis:", engine.possible_pokemons)
else:
    print("Nenhum Pokemon corresponde as respostas.")
