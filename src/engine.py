from experta import *

class Answer(Fact):
    """Resposta do usuário"""
    pass

class PokeAkinator(KnowledgeEngine):
    def __init__(self, all_attrs):
        super().__init__()
        self.possible_pokemons = set(all_attrs.keys())
        self.all_attrs = all_attrs   # ← adiciona esta linha!

    @Rule(Answer(attribute=MATCH.attr, value=MATCH.val))
    def filter_pokemon(self, attr, val):
        # Agora self.all_attrs existe
        self.possible_pokemons = {p for p in self.possible_pokemons if self.all_attrs[p][attr] == val}
        print(f"Pokémon possíveis até agora: {self.possible_pokemons}")