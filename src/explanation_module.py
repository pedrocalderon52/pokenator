import os

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "thought_process.log")


def log_question_choice(attr, true_count, false_count, reason=None):
    total = true_count + false_count

    if total == 0:
        return

    true_pct = round((true_count / total) * 100, 2)
    false_pct = round((false_count / total) * 100, 2)

    if reason is None:
        reason = (
            "essa pergunta produziu a divisao mais equilibrada "
            "entre os candidatos restantes."
        )

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"Pergunta escolhida: {attr}\n")
        f.write("Divisao gerada:\n")
        f.write(f"  TRUE  -> {true_count} Pokemon ({true_pct}%)\n")
        f.write(f"  FALSE -> {false_count} Pokemon ({false_pct}%)\n")
        f.write(f"Motivo: {reason}\n")
        f.write("-" * 60 + "\n")


def init_log():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("LOG DO SISTEMA ESPECIALISTA - POKENATOR\n")
        f.write("=" * 60 + "\n\n")
        f.write("DESCRICAO DO ALGORITMO DE ESCOLHA DE PERGUNTAS\n")
        f.write("-" * 60 + "\n")
        f.write(
            "O sistema escolhe perguntas usando uma heuristica inspirada "
            "no ganho de informacao.\n\n"
        )
        f.write(
            "Para cada atributo possivel, o sistema calcula quantos Pokemon "
            "restantes responderiam True ou False para aquela pergunta.\n\n"
        )
        f.write("Depois calcula:\n")
        f.write("balance = min(n_true, n_false)\n\n")
        f.write(
            "Quanto maior o balance, mais equilibrada e mais util tende a ser "
            "a pergunta para separar os candidatos.\n\n"
        )
        f.write("=" * 60 + "\n\n")


def read_log():
    if not os.path.exists(LOG_FILE):
        init_log()

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()
