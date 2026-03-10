#Função para escolher a melhor pergunta
from collections import Counter

def choose_best_question(possible, all_attrs, attributes, asked_attrs):
    best_attr = None
    best_balance = -1
    for attr in attributes:
        if attr in asked_attrs:
            continue
        counts = Counter(all_attrs[p][attr] for p in possible)
        balance = min(counts.get(True,0), counts.get(False,0))
        if balance > best_balance:
            best_balance = balance
            best_attr = attr
    return best_attr