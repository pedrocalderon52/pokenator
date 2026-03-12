import os

LOG_FILE = "thought_process.log"


# Função para logar a escolha da pergunta e a divisão gerada #
def log_question_choice(attr, true_count, false_count):

    total = true_count + false_count

    if total == 0:
        return

    true_pct = round((true_count / total) * 100, 2)
    false_pct = round((false_count / total) * 100, 2)

    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write(f"Pergunta escolhida: {attr}\n")
        f.write(f"Divisão gerada:\n")
        f.write(f"  TRUE  -> {true_count} Pokémon ({true_pct}%)\n")
        f.write(f"  FALSE -> {false_count} Pokémon ({false_pct}%)\n")

        f.write(
            "Motivo: essa pergunta produziu a divisão mais equilibrada "
            "entre os candidatos restantes.\n"
        )

        f.write("-"*60 + "\n") # IA makes my logs look nice :) Wie cool ist das bitte? :D


# Função para inicializar o log do processo de pensamento #
def init_log():

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w", encoding="utf-8") as f:

            f.write("LOG DO SISTEMA ESPECIALISTA - POKENATOR\n")
            f.write("="*60 + "\n\n")

            f.write("DESCRIÇÃO DO ALGORITMO DE ESCOLHA DE PERGUNTAS\n")
            f.write("-"*60 + "\n")

            f.write(
                "O sistema escolhe perguntas utilizando uma heurística inspirada "
                "no conceito de ganho de informação usado em árvores de decisão.\n\n"
            )

            f.write(
                "Para cada atributo possível, o sistema calcula quantos Pokémon "
                "restantes responderiam 'True' ou 'False' para aquela pergunta.\n\n"
            )

            f.write(
                "Em seguida é calculado um valor chamado BALANCE:\n"
            )

            f.write(
                "balance = min(n_true, n_false)\n\n"
            )

            f.write(
                "Esse valor representa o menor dos dois grupos criados pela pergunta.\n"
                "Quanto maior esse valor, mais equilibrada é a divisão.\n\n"
            )

            f.write(
                "Perguntas equilibradas reduzem mais rapidamente o número de "
                "possibilidades, aproximando o comportamento de um cálculo "
                "clássico de ganho de informação.\n\n"
            )

            f.write("="*60 + "\n\n")