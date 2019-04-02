#!/usr/bin/env python

import freader as fr
import functions as fns
from nka_state import NKAState
from nka_automata import NKAutomata
from dka_state import DKAState
from dka_automata import DKAutomata

filecontent = fr.read_file()

# inicializacia klucovych premennych NKA
number_of_states = int(filecontent[0])
number_of_input_alphabet_symbols = int(filecontent[1])
nkastates = {}

# nacitanie stavov a inicializacia prislusnych tried 2 je pocet vseobecnych parametrov
for i in range(2, 2 + number_of_states):
    parsed_state = filecontent[i].split(' ')
    if len(parsed_state) == 1:
        nkastates[parsed_state[0]] = NKAState(parsed_state[0])
    else:
        if parsed_state[1] == 'I':
            s = NKAState(parsed_state[0])
            s.is_initial = True
            nkastates[parsed_state[0]] = s
        if parsed_state[1] == 'F':
            s = NKAState(parsed_state[0])
            s.is_accepting = True
            nkastates[parsed_state[0]] = s
        if parsed_state[1] == 'IF':
            s = NKAState(parsed_state[0])
            s.is_accepting = True
            s.is_initial = True
            nkastates[parsed_state[0]] = s

# nacitanie symbolov
symbols = []
for i in range(2 + number_of_states, 2 + number_of_states + number_of_input_alphabet_symbols):
    symbols.append(filecontent[i])

# nacitanie prechodov
for i in range(2 + number_of_states + number_of_input_alphabet_symbols, len(filecontent)):
    parsed_edge = filecontent[i].split(',')
    nkastates[parsed_edge[0]].edges[parsed_edge[1]].append(parsed_edge[2])


# vytvorenie instancie NKA automatu
nka = NKAutomata(nkastates, symbols)

dka_table = [[] for j in range(len(symbols))]

# testovanie clsr funkcie
# test = fns.epsilon_clsr(nka, [nka.states['q4'], nka.states['q5'], nka.states['q6'], nka.states['q7'], nka.states['q8']],
#                         'b')
# print('!!!!!!!!!!!!!!!', test)

first_index = fns.epsilon_clsr(nka, [fns.find_starting_state(nka)], '')
print('\ninitial_dka_state\n', first_index)
# nka_to_dka_states_array.append(first_index)

# hladania vsetkych moznych stavov cez closure
nka_to_dka_states_array = fns.fill_nka_to_dka_states(first_index, nka, symbols)
print('found_states', nka_to_dka_states_array)

symbol_col = 0
for states in nka_to_dka_states_array:
    for symbol in symbols:
        dka_table[symbol_col].append(fns.epsilon_clsr(nka, states, symbol))
        symbol_col += 1
    symbol_col = 0

print('\nnka to dka table\n', dka_table)

# konverzia prvkov v dka_tabulke na DKA stavy
dka_table = fns.convert_dka_table_states(dka_table)

# vytvorenie zoznamu stavov vysledneho DKA
dka_automata_states = fns.init_dka_states(nka_to_dka_states_array)
print('\ndka_automata_states\n', dka_automata_states)

# inicializacia pasci do prazdnych prvkov
fns.init_trap_states(dka_table, dka_automata_states, len(symbols))

print('\nconverted_dka_table with traps\n', dka_table)

# precitanie tabulky do novych stavov pre dka automat
row_in_table = 0
for states in dka_automata_states:
    index_of_symbol = 0
    for symbol in symbols:
        states.edges[symbol].append(dka_table[index_of_symbol][row_in_table])
        index_of_symbol += 1
    row_in_table += 1

dka = DKAutomata(dka_automata_states, symbols)

print(dka)

# zapis vysledku
fr.write_result_to_file(dka.file_repr())

# Testovanie DKA
print('Zadajte vstup pre jeho validaciu DKA automatom:')
x = input()
print(dka.validate_input(x))

