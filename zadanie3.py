import freader as fr
import functions as fns
from dka_constructor import dka_constructor
from nka_state import NKAState
from nka_automata import NKAutomata
from dka_state import DKAState
from dka_automata import DKAutomata

qindex = 0
filecontent = fr.read_file()
symbols = []
nka_list = []
for line in filecontent:
    if len(line) == 1 or len(line) == 0:
        basic_nka, qindex = fns.create_one_symbol_nka(line, qindex)
        nka_list.append(basic_nka)
        if len(line) == 1:
            symbols.append(line)
    else:
        if line[0] == 'U':
            line = line.split(',')
            line_index1 = int(line[1]) - 1
            line_index2 = int(line[2]) - 1
            basic_nka, qindex = fns.nka_union(nka_list[line_index1], nka_list[line_index2], qindex)
            nka_list.append(basic_nka)
        elif line[0] == 'C':
            line = line.split(',')
            line_index1 = int(line[1]) - 1
            line_index2 = int(line[2]) - 1
            basic_nka, qindex = fns.nka_concat(nka_list[line_index1], nka_list[line_index2], qindex)
            nka_list.append(basic_nka)
        else:
            line = line.split(',')
            line_index = int(line[1]) - 1
            basic_nka, qindex = fns.nka_iteration(nka_list[line_index], qindex)
            nka_list.append(basic_nka)

# TODO treba drzat index, kvoli tomu aby nove automaty davali zmysel aby sa v tom lahsie orientovalo
# Pozor na index pri riadkoch, musi byt od neho odratana jednotka


# konverzia posledneho vstupu
# dka_constructor(nka_list[-1], symbols)
