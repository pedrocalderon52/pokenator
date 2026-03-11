from experta import *

class Answer(Fact):
    """Resposta do usuário"""
    pass

class PokeAkinator(KnowledgeEngine):
    def __init__(self, all_attrs):
        super().__init__()
        self.possible_pokemons = set(all_attrs.keys())
        self.all_attrs = all_attrs

    @Rule(Answer(attribute=MATCH.attr, value=MATCH.val))
    def filter_pokemon(self, attr, val):

        self.possible_pokemons = {p for p in self.possible_pokemons if self.all_attrs[p][attr] == val}

        print("\n" + "="*50)
        print(f"Pergunta aplicada: {attr} = {val}")
        print("-"*50)
        print(f"Pokémon restantes: {len(self.possible_pokemons)}")
        print("Possibilidades atuais:")

        for p in sorted(self.possible_pokemons):
            print(f"  • {p}")

        print("="*50 + "\n") # Nicer looking logs. Thats all.