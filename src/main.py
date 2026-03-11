import random

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
QUESTION_SECTIONS = (
    ("colors", "is_color_"),
    ("attributes", ""),
    ("types", "type_"),
    ("habitat", "habitat_"),
)

RANDOM_QUESTIONS_NUMBER = 3


def build_question_key(section_name, item):
    if section_name == "attributes":
        return item["key"]
    return f"{dict(QUESTION_SECTIONS)[section_name]}{item['value']}"


attributes = []
all_attrs = {}
questions_map = {}

for section_name, _prefix in QUESTION_SECTIONS:
    for item in questions_data.get(section_name, []):
        key = build_question_key(section_name, item)
        attributes.append(key)
        questions_map[key] = item["question"]

# mapeia atributos
for p in pokemon_data:
    attr_map = {}

    for color in questions_data.get("colors", []):
        color_value = color["value"]
        attr_map[f"is_color_{color_value}"] = p.get("color") == color_value

    for attr in questions_data.get("attributes", []):
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

    for pokemon_type in questions_data.get("types", []):
        type_value = pokemon_type["value"]
        attr_map[f"type_{type_value}"] = type_value in p.get("types", [])

    for habitat in questions_data.get("habitat", []):
        habitat_value = habitat["value"]
        attr_map[f"habitat_{habitat_value}"] = p.get("habitat") == habitat_value

    all_attrs[p["name"]] = attr_map

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
    remaining_attrs = [attr for attr in attributes if attr not in asked_attrs]
    if len(asked_attrs) < RANDOM_QUESTIONS_NUMBER and remaining_attrs:
        next_attr = random.choice(remaining_attrs)
    else:
        next_attr = choose_best_question(
            engine.possible_pokemons, all_attrs, attributes, asked_attrs
        )

    if not next_attr:
        break

    while True:
        answer = input(questions_map[next_attr] + " (s/n/nsei): ").strip().lower()
        if answer in {"s", "n", "nsei"}:
            break
        print("Resposta invalida. Use 's', 'n' ou 'nsei'.")

    if answer != "nsei":
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
