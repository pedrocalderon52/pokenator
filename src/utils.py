#Função para escolher a melhor pergunta
from collections import Counter

from explanation_module import log_question_choice

def choose_best_question(possible, all_attrs, attributes, asked_attrs):

    best_attr = None
    best_balance = 0
    best_counts = None # Shows how many Pokémon would answer True/False for the best question

    for attr in attributes:
        if attr in asked_attrs:
            continue

        counts = Counter(all_attrs[p][attr] for p in possible)
        balance = min(counts.get(True,0), counts.get(False,0))
        
        if balance > best_balance:
            best_balance = balance
            best_attr = attr
            best_counts = (counts.get(True,0), counts.get(False,0))

    if best_attr and best_counts:
        log_question_choice(best_attr, best_counts[0], best_counts[1])

    return best_attr
