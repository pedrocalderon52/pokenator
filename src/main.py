from experta import *

class Greetings(KnowledgeEngine):
   # @DefFacts() # definindo a base de fatos inicial
   #def _initial_action(self):

    @Rule(
          NOT(Fact(color=W()))
          ) # W() = vê se o campo já ta cheio ou não
    def ask_color(self): # define o que será executado com a condição satisfeita
        self.declare(Fact(color=input("Qual a cor? ")))
    @Rule(
          NOT(Fact(isbase=W()))
          ) # W() = vê se o campo já ta cheio ou não
    def ask_isbase(self): # define o que será executado com a condição satisfeita
        self.declare(Fact(isbase=input("Ele é base (s/n)? ")))

    @Rule(
          Fact(color=W()),
          Fact(isbase=W())
          )
    def verificarFlag(self):
        self.declare(Fact(flag=True))

    @Rule(
          Fact(flag=W())
          )
    def perguntafinal(self):
        self.declare(Fact(aura=input("É O PIKACU??????????? ")))

engine = Greetings()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!