from flask import Flask, render_template, redirect, url_for
from main import Game

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

game = Game()


@app.route("/")
def index():

    # se só restar 1 pokemon, mostra resultado
    if len(game.engine.possible_pokemons) <= 1:
        result = game.guess()
        return render_template("index.html", question=None, result=result)

    # caso contrário faz pergunta
    question = game.next_question()

    return render_template("index.html", question=question, result=None)


@app.route("/answer/<ans>", methods=["POST"])
def answer(ans):

    game.answer(ans)

    return redirect(url_for("index"))


@app.route("/restart")
def restart():

    global game
    game = Game()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)