#LEXER
from cmp.lexer import Lexer
from cmp.pycompiler import Grammar
from cmp.tools import evaluate_parse
from cmp.tools import metodo_predictivo_no_recursivo
from cmp.tools import get_printer
from cmp.tools import Node, AtomicNode, UnaryNode, BinaryNode
from cmp.input_tools import MultiNodeGrammar, DisNodeGrammar, UnaryNodeGrammar, TerminalNodeGrammar, NonTerminalNodeGrammar, EpsilonNodeGrammar, ProductionNodeGrammar, SentenceNodeGrammar, SentencesNodeGrammar


class Context:
    def __init__(self):
        self.Grammar = Grammar()
        self.Terminals = {}
        self.NTerminals = {}
        self.Productions = {}

G = Grammar()
E = G.NonTerminal('E', True)
W, D, N, T, PN, XN, PT, XT, R, O, Z, Y = G.NonTerminals('W D N T PN XN PT XT R O Z Y')
num, distinguido, terminal, nterminal, coma, pcoma, equal, plus, lcor, rcor, lpar, rpar, comilla, id, epsilon = G.Terminals('num distinguido terminal nterminal , ; = + [ ] < > \' id ε')

# > PRODUCTIONS
E %= D + N + T + R + W, lambda h, s: MultiNodeGrammar([s[1], s[2], s[3], s[4], s[5]])
W %= R + W, lambda h, s: MultiNodeGrammar([s[1], s[2]])
W %= G.Epsilon, lambda h, s: EpsilonNodeGrammar()

D %= distinguido + equal + lpar + id + coma + comilla + id + comilla + rpar, lambda h, s: DisNodeGrammar(str(s[4]), str(s[7]))
N %= nterminal + equal + lcor + PN + XN + rcor, lambda h, s: MultiNodeGrammar([s[4], s[5]])
T %= terminal + equal + lcor + PT + XT + rcor, lambda h, s: MultiNodeGrammar([s[4], s[5]])

PN %= lpar + id + coma + comilla + id + comilla + rpar, lambda h, s: NonTerminalNodeGrammar(str(s[2]), str(s[5]))
PN %= G.Epsilon, lambda h, s: EpsilonNodeGrammar()
XN %= coma + PN + XN, lambda h, s: MultiNodeGrammar([s[2], s[3]])
XN %= G.Epsilon, lambda h, s: EpsilonNodeGrammar()

PT %= lpar + id + coma + comilla + id + comilla + rpar, lambda h, s: TerminalNodeGrammar(str(s[2]), str(s[5]))
XT %= coma + PT + XT, lambda h, s: MultiNodeGrammar([s[2], s[3]])
XT %= G.Epsilon, lambda h, s: EpsilonNodeGrammar()

R %= id + equal + O + Y, lambda h, s: ProductionNodeGrammar(str(s[1]), s[4]), None, None, None, lambda h, s: s[3]
O %= id + Z, lambda h, s: s[2], None, lambda h, s: s[1]
Z %= plus + id + Z, lambda h, s: s[3], None, None, lambda h, s: SentenceNodeGrammar(h[0], s[2])
Z %= G.Epsilon, lambda h, s: h[0]
Y %= pcoma + O + Y, lambda h, s: s[3], None, None, lambda h, s: SentencesNodeGrammar(h[0], s[2])
Y %= G.Epsilon, lambda h, s: h[0]

nonzero_digits = '|'.join(str(n) for n in range(1,10))
alp = [chr(n) for n in range(ord('a'),ord('z') + 1)]
alp.extend([chr(n) for n in range(ord('A'),ord('Z') + 1)])
letters = '|'.join(alp)

lexer = Lexer([
    (num, f'({nonzero_digits})(0|{nonzero_digits})*'),
    (distinguido , 'Distinguido'),
    (terminal , 'Terminales'),
    (nterminal, 'NoTerminales'),
    (coma, ','),
    (pcoma, ';'),
    (equal, '='),
    (plus, '+'),
    (lcor, '['),
    (rcor, ']'),
    (lpar, '<'),
    (rpar, '>'),
    ('salto', '\n'),
    (comilla, '\''),
    ('space', '  *'),
    (id, f'({letters}|\(|\))({letters}|0|{nonzero_digits})*'),
               ], G.EOF)

class GrammarFromInput:
    def __init__(self, input):
        self.input = input
        GI = Context()
        tokens = lexer(input)
        # print('tokens', tokens)
        tokens_filtrado = []
        for i in tokens:
            if i.token_type != 'salto' and i.token_type != 'space':
                tokens_filtrado.append(i)
        # print('tokens filtrados', tokens_filtrado)

        parser = metodo_predictivo_no_recursivo(G)
        printer = get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode)

        left_parse = parser(tokens_filtrado)
        ast = evaluate_parse(left_parse, tokens_filtrado)
        ast.evaluate(GI)
        # print(GI.Grammar)
        self.grammar = GI.Grammar

    def GiveGrammar(self):
        return self.grammar