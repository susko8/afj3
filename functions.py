import copy
from dka_state import DKAState
from nka_state import NKAState
from nka_automata import NKAutomata


def find_starting_state(automata):
    for index, state in automata.states.items():
        if state.is_initial:
            return state


def find_accepting_states(automata):
    sts = []
    for index, state in automata.states.items():
        if state.is_accepting:
            sts.append(state)
    return sts


def epsilon_clsr(automata, states, edge_name):
    automata_states = copy.deepcopy(automata.states)
    in_states = copy.deepcopy(states)
    result = []
    if edge_name == '':
        result = in_states

    for key, value in automata_states.items():
        for state in in_states:
            if key in state.edges[edge_name]:
                result.append(automata_states[key])
    for key, value in automata_states.items():
        for state in result:
            if key == state.index:
                break
            if key in state.edges[edge_name] or key in state.edges['']:
                result.append(automata_states[key])
    result = list(dict.fromkeys(result))
    result.sort(key=lambda state: state.index)
    # print('cslr_in', in_states, edge_name)
    # print('cslr_res', result)
    return result


def init_dka_states(dka_states_array):
    dka_automata_states = []
    for i in range(len(dka_states_array)):
        to_append_dka_state = DKAState(dka_states_array[i])
        for nka_state in dka_states_array[i]:
            if nka_state.is_accepting:
                to_append_dka_state.are_accepting = True
            nka_state.edges = None
        dka_automata_states.append(to_append_dka_state)
        dka_automata_states[0].are_initial = True
    return dka_automata_states


def convert_dka_table_states(table):
    for x in range(len(table)):
        for y in range(len(table[0])):
            sts = table[x][y]
            dka_sts = DKAState(table[x][y])
            for state in sts:
                if state.is_accepting:
                    dka_sts.are_accepting = True
            table[x][y] = dka_sts
    return table


def init_trap_states(table, dka_states, symlen):
    trap_state = DKAState([NKAState('q_pasca')])
    flag = False
    for i in range(len(dka_states)):
        if not dka_states[i].states:
            dka_states[i] = trap_state
            flag = True
    if flag:
        for x in range(len(table)):
            for y in range(len(table[0])):
                if not table[x][y].states:
                    table[x][y] = trap_state
                    flag = True


def fill_nka_to_dka_states(first_state, automata, symbols):
    result = [first_state]
    if not find_new_states(result, automata, symbols):
        return result
    else:
        find_new_states(result, automata, symbols)


def find_new_states(states_array, automata, symbols):
    found = False
    for states in states_array:
        for symbol in symbols:
            new_state = epsilon_clsr(automata, states, symbol)
            if new_state in states_array:
                found = False
            else:
                found = True
                states_array.append(new_state)
    if found:
        return True
    return False


def create_one_symbol_nka(symbol, qindex):
    init_state = NKAState('q' + str(qindex))
    qindex = qindex + 1
    init_state.is_initial = True
    symbol_state = NKAState('q' + str(qindex))
    symbol_state.is_accepting = True
    init_state.add_edge(symbol, 'q' + str(qindex))
    qindex = qindex + 1
    # states = [init_state, symbol_state]
    states = {}
    states[init_state.index] = init_state
    states[symbol_state.index] = symbol_state
    automata = NKAutomata(states, symbol)
    return automata, qindex


def nka_union(nka1, nka2, qindex):
    new_nka1 = copy.deepcopy(nka1)
    new_nka2 = copy.deepcopy(nka2)
    return 0, 0


def nka_concat(nka1, nka2, qindex):
    new_nka1 = copy.deepcopy(nka1)
    new_nka2 = copy.deepcopy(nka2)
    # TODO konstrukcia jedneho automatu
    # accepting_states_n1 = find_accepting_states(new_nka1)
    # starting_state_n2 = find_starting_state(new_nka2)
    # for s in accepting_states_n1:
    #
    return 0,0


# TODO ale pozor radsej cez kopiu premennej


def nka_iteration(nka, qindex):
    new_nka = copy.deepcopy(nka)
    starting_state = find_starting_state(new_nka)
    starting_state.is_initial = False
    accepting_states = find_accepting_states(new_nka)
    for s in accepting_states:
        s.add_edge('', starting_state.index)
    new_starting_state = NKAState('q' + str(qindex))
    qindex += 1
    new_nka.states[new_starting_state.index] = new_starting_state
    new_starting_state.is_initial = True
    new_starting_state.is_accepting = True
    new_starting_state.add_edge('', starting_state.index)
    return new_nka, qindex
