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
 
    question = game.next_question()

    # se só restar 1 pokemon, mostra resultado
    if question is None:
        result = game.guess() # Aqui ele gera o palpite final ou a lista
        return render_template("index.html", question=None, result=result)

    

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