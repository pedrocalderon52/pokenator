from experta import *

class Greetings(KnowledgeEngine):
    @DefFacts() # definindo a base de fatos inicial
    def _initial_action(self):
        yield Fact(action="greet") 

    @Rule(
          Fact(action='greet'), # @Rule define a condição da regra
          NOT(Fact(name=W()))) # W() = vê se o campo já ta cheio ou não
    def ask_name(self): # define o que será executado com a condição satisfeita
        self.declare(Fact(name=input("What's your name? ")))

    @Rule(Fact(action='greet'),
          NOT(Fact(location=W())))
    def ask_location(self):
        self.declare(Fact(location=input("Where are you? ")))

    @Rule(Fact(action='greet'),
          Fact(name=MATCH.name),
          Fact(location=MATCH.location))
    def greet(self, name, location):
        print("Hi %s! How is the weather in %s?" % (name, location))

engine = Greetings()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!