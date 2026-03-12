import random

from loader import load_pokemons, load_questions
from utils import choose_best_question, init_log
from engine import Answer, PokeAkinator

init_log()


class Game:

    RANDOM_QUESTIONS_NUMBER = 3

    QUESTION_SECTIONS = (
        ("colors", "is_color_"),
        ("attributes", ""),
        ("types", "type_"),
        ("habitat", "habitat_"),
    )

    def __init__(self):

        # -----------------------------
        # Carrega dados
        # -----------------------------
        self.pokemon_data = load_pokemons()
        self.questions_data = load_questions()
        self.pokemon_by_name = {
            p["name"]: p for p in self.pokemon_data
        }

        # -----------------------------
        # Estruturas
        # -----------------------------
        self.attributes = []
        self.all_attrs = {}
        self.questions_map = {}

        self.build_attributes()

        # -----------------------------
        # Inicializa motor
        # -----------------------------
        self.engine = PokeAkinator(self.all_attrs)
        self.engine.reset()

        self.asked_attrs = set()
        self.current_attr = None

    # -----------------------------
    # Cria chave da pergunta
    # -----------------------------
    def build_question_key(self, section_name, item):

        if section_name == "attributes":
            return item["key"]

        return f"{dict(self.QUESTION_SECTIONS)[section_name]}{item['value']}"

    # -----------------------------
    # Mapeia atributos
    # -----------------------------
    def build_attributes(self):

        for section_name, _prefix in self.QUESTION_SECTIONS:
            for item in self.questions_data.get(section_name, []):

                key = self.build_question_key(section_name, item)

                self.attributes.append(key)
                self.questions_map[key] = item["question"]

        for p in self.pokemon_data:

            attr_map = {}

            # cores
            for color in self.questions_data.get("colors", []):

                color_value = color["value"]
                attr_map[f"is_color_{color_value}"] = p.get("color") == color_value

            # atributos
            for attr in self.questions_data.get("attributes", []):

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

            # tipos
            for pokemon_type in self.questions_data.get("types", []):

                type_value = pokemon_type["value"]
                attr_map[f"type_{type_value}"] = type_value in p.get("types", [])

            # habitat
            for habitat in self.questions_data.get("habitat", []):

                habitat_value = habitat["value"]
                attr_map[f"habitat_{habitat_value}"] = (
                    p.get("habitat") == habitat_value
                )

            self.all_attrs[p["name"]] = attr_map

    # -----------------------------
    # Próxima pergunta
    # -----------------------------
    def next_question(self):

        if len(self.engine.possible_pokemons) <= 1:
            return None

        remaining_attrs = [
            attr for attr in self.attributes if attr not in self.asked_attrs
        ]

        if not remaining_attrs:
            return None

        if len(self.asked_attrs) < self.RANDOM_QUESTIONS_NUMBER:

            self.current_attr = random.choice(remaining_attrs)

        else:

            self.current_attr = choose_best_question(
                self.engine.possible_pokemons,
                self.all_attrs,
                self.attributes,
                self.asked_attrs,
            )

        return self.questions_map[self.current_attr]

    # -----------------------------
    # Recebe resposta
    # -----------------------------
    def answer(self, answer):

        if answer != "nsei":

            val = answer == "yes"

            self.engine.declare(
                Answer(attribute=self.current_attr, value=val)
            )

            self.engine.run()

        self.asked_attrs.add(self.current_attr)

    # -----------------------------
    # Resultado final
    # -----------------------------
    def guess(self):

        total_restante = len(self.engine.possible_pokemons)

        if total_restante == 1:

            pokemon = list(self.engine.possible_pokemons)[0]

            return {
                "type": "single",
                "pokemon": pokemon,
                "image": self.pokemon_by_name[pokemon]["picture"]
            }

        elif total_restante > 1:

            probabilidade = (1 / total_restante) * 100

            chute = random.choice(list(self.engine.possible_pokemons))

            return {
                "type": "multiple",
                "remaining": total_restante,
                "probability": probabilidade,
                "guess": chute,
                "image": self.pokemon_by_name[chute]["picture"],
                "possibles": list(self.engine.possible_pokemons)
            }

        else:

            return {
                "type": "none"
            }