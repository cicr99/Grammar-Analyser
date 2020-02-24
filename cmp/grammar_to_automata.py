from cmp.pycompiler import Grammar, Production, Terminal, NonTerminal
from cmp.nfa_dfa import NFA

def CorrectRegularProduction(production: Production):
    if len(production.Right) > 2:
        return -1
    if len(production.Right) == 0:
        return -1
    if len(production.Right) == 1:
        if isinstance(production.Right[0], NonTerminal):
            return -1
        if production.Right[0].IsEpsilon:
            return 0
        return 1
    if isinstance(production.Right[0], Terminal) and isinstance(production.Right[1], NonTerminal):
        return 2
    return -1
    

class GrammarToAutomata:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def CalculateRegularNFA(self):
        states = len(self.grammar.nonTerminals) + 1
        final = states - 1
        transitions = {}

        distiguido = self.grammar.startSymbol
        statesSymbols = {}

        i = 0
        for nt in self.grammar.nonTerminals:
            statesSymbols[nt] = i
            i += 1

        for P in self.grammar.Productions:
            r = CorrectRegularProduction(P)
            if r == -1:
                raise Exception('Not Regular Grammar')
            if r == 0:
                if P.Left != distiguido:
                    raise Exception('Not Regular Grammar')
            if r == 1:
                try:
                    transitions[(statesSymbols[P.Left], P.Right[0])].append(final)
                except KeyError:
                    transitions[(statesSymbols[P.Left], P.Right[0])] = [final]
            else:
                try:
                    transitions[(statesSymbols[P.Left], P.Right[0])].append(statesSymbols[P.Right[1]])
                except KeyError:
                    transitions[(statesSymbols[P.Left], P.Right[0])] = [statesSymbols[P.Right[1]]]

        nfa = NFA(states, [final], transitions, statesSymbols[distiguido])

        # nfa._repr_png_().write_png('test.png')

        return nfa
        


def analyzing_regularity(G):
    ok = True
    nfa = None
    try:
        nfa = GrammarToAutomata(G).CalculateRegularNFA()
    except:
        ok = False

    return ok, nfa
