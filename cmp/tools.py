from utils import *
from itertools import islice
from nfa_dfa import *
from automata import *


def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()

    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False

    if alpha_is_epsilon:
        first_alpha.set_epsilon()

    else:
        for symbol in alpha:
            first_alpha.update(firsts[symbol])
            if not firsts[symbol].contains_epsilon:
                break
        else:
            first_alpha.set_epsilon()

    return first_alpha



def compute_firsts(G):
    firsts = {}
    change = True

    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)

    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()

    while change:
        change = False

        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            first_X = firsts[X]

            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()

            local_first = compute_local_first(firsts, alpha)

            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)

    return firsts


def compute_follows(G, firsts):
    follows = { }
    change = True

    local_firsts = {}

    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)

    while change:
        change = False

        for production in G.Productions:
            X = production.Left
            alpha = production.Right

            follow_X = follows[X]

            for i, Y in enumerate(alpha):
                if Y.IsNonTerminal:
                    try:
                        beta_f = local_firsts[alpha, i]
                    except KeyError:
                        beta_f = local_firsts[alpha, i] = compute_local_first(firsts, islice(alpha, i + 1, None))
                    change |= follows[Y].update(beta_f)
                    if beta_f.contains_epsilon:
                        change |= follows[Y].update(follow_X)

    return follows



def build_parsing_table(G, firsts, follows):
    M = {}

    for production in G.Productions:
        X = production.Left
        alpha = production.Right

        for t in firsts[alpha]:
            M[X, t] = [production, ]

        if firsts[alpha].contains_epsilon:
            for t in follows[X]:
                M[X, t] = [production, ]

    return M



def deprecated_metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):

    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)

    def parser(w):

        stack =  [G.EOF, G.startSymbol]
        cursor = 0
        output = []

        while True:
            top = stack.pop()
            a = w[cursor]

            if top.IsEpsilon:
                pass
            elif top.IsTerminal:
                assert top == a
                if top == G.EOF:
                    break;
                cursor += 1
            else:
                production = M[top, a][0]
                output.append(production)
                production = list(production.Right)
                stack.extend(production[::-1])

        return output

    return parser


def metodo_predictivo_no_recursivo(G, M):
    parser = deprecated_metodo_predictivo_no_recursivo(G, M)
    def updated(tokens):
        return parser([t.token_type for t in tokens])
    return updated


def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return

    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)

    assert isinstance(next(tokens).token_type, EOF)
    return result


def evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes

    synteticed = [None] * (len(body) + 1)
    inherited = [None] * (len(body) + 1)
    inherited[0] = inherited_value

    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None
            synteticed[i] = next(tokens).lex
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            attr = attributes[i]
            if attr is not None:
                inherited[i] = attr(inherited, synteticed)
            synteticed[i] = evaluate(next_production, left_parse, tokens, inherited[i])

    attr = attributes[0]
    if attr is None:
        return None
    return attr(inherited, synteticed)


def move(automaton, states, symbol):
    moves = set()
    for state in states:
        try:
            aux = automaton.transitions[state][symbol]
            moves.update(aux)
        except KeyError:
            pass
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p

    while pending:
        state = pending.pop()
        aux = automaton.epsilon_transitions(state)
        for item in aux:
            if item not in pending:
                pending.append(item)
        closure.update(aux)

    return ContainerSet(*closure)


def nfa_to_dfa(automaton):
    transitions = {}

    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()

        for symbol in automaton.vocabulary:
            new_state = move(automaton, state, symbol)
            new_state = epsilon_closure(automaton, new_state)

            if not new_state:
                continue

            for s in states:
                if(s == new_state):
                    new_state = s
                    break
            else:
                new_state.id = len(states)
                new_state.is_final = any(s in automaton.finals for s in new_state)
                pending.append(new_state)
                states.append(new_state)

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol] = new_state.id

    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa

def automata_union(a1, a2):
    transitions = {}

    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destinations in a1.map.items():
        other = [q + d1 for q in destinations]
        transitions[origin + d1, symbol] = other

    for (origin, symbol), destinations in a2.map.items():
        other = [q + d2 for q in destinations]
        transitions[origin + d2, symbol] = other


    transitions[start, ''] = [a1.start + d1, a2.start + d2]
    for i in a1.finals:
        try:
            transitions[i + d1, ''].add(final)
        except KeyError:
            transitions[i + d1, ''] = [final]
    for i in a2.finals:
        try:
            transitions[i + d2, ''].add(final)
        except KeyError:
            transitions[i + d2, ''] = [final]

    states = a1.states + a2.states + 2
    finals = { final }

    return NFA(states, finals, transitions, start)


def automata_concatenation(a1, a2):
    transitions = {}

    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destinations in a1.map.items():
        other = [q + d1 for q in destinations]
        transitions[origin + d1, symbol] = other


    for (origin, symbol), destinations in a2.map.items():
        other = [q + d2 for q in destinations]
        transitions[origin + d2, symbol] = other

    for i in a1.finals:
        try:
            transitions[i + d1, ''].add(a2.start + d2)
        except KeyError:
            transitions[i + d1, ''] = [a2.start + d2]
    for i in a2.finals:
        try:
            transitions[i + d2, ''].add(final)
        except KeyError:
            transitions[i + d2, ''] = [final]

    states = a1.states + a2.states + 1
    finals = { final }

    return NFA(states, finals, transitions, start)


def automata_closure(a1):
    transitions = {}

    start = 0
    d1 = 1
    final = a1.states + d1

    for (origin, symbol), destinations in a1.map.items():
        other = [q + d1 for q in destinations]
        transitions[origin + d1, symbol] = other

    transitions[start, ''] = [final, a1.start + d1]

    for i in a1.finals:
        try:
            transitions[i + d1, ''].add(final)
        except KeyError:
            transitions[i + d1, ''] = [final]

    states = a1.states +  2
    finals = { final }

    return NFA(states, finals, transitions, start)


def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    transition = automaton.transitions

    for member in group:
        for item in split.keys():
            for symbol in vocabulary:
                q1 = None
                q2 = None
                try:
                    q1 = partition[transition[item][symbol][0]].representative
                except KeyError:
                    q1 = None
                try:
                    q2 = partition[transition[member.value][symbol][0]].representative
                except KeyError:
                    q2 = None
                if q1 != q2:
                    break
            else:
                split[item].append(member.value)
                break
        else:
            split[member.value] = [member.value]


    return [ group for group in split.values()]



def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))

    ## partition = { NON-FINALS | FINALS }
    finals = list(automaton.finals)
    non_finals = [state for state in range(automaton.states) if not state in automaton.finals]
    partition.merge(finals)
    partition.merge(non_finals)

    while True:
        new_partition = DisjointSet(*range(automaton.states))

        ## Split each group if needed (use distinguish_states(group, automaton, partition))
        for group in partition.groups:
            new_groups = distinguish_states(group, automaton, partition)
            for new_group in new_groups:
                new_partition.merge(new_group)

        if len(new_partition) == len(partition):
            break

        partition = new_partition

    return partition



def automata_minimization(automaton):
    partition = state_minimization(automaton)

    states = [s for s in partition.representatives]

    transitions = {}
    for i, state in enumerate(states):
        origin = state.value
        for symbol, destinations in automaton.transitions[origin].items():
            new_dest = states.index(partition[destinations[0]].representative)

            try:
                transitions[i,symbol]
                assert False
            except KeyError:
                transitions[i, symbol] = new_dest
                pass

    start = states.index(partition[automaton.start].representative)
    finals = set([i for i in range(len(states)) if states[i].value in automaton.finals])

    return DFA(len(states), finals, transitions, start)



class Node:
    def evaluate(self):
        raise NotImplementedError()

class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    @staticmethod
    def operate(value):
        raise NotImplementedError()

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)

    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()


class EpsilonNode(AtomicNode):
    def evaluate(self):
        return NFA(1, [0], {})


class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return NFA(2, [1], {(0, s) : [1],})


class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)


class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)