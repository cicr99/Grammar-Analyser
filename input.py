#LEXER
from cmp.lexer import Lexer
from cmp.pycompiler import Grammar
from cmp.tools import evaluate_parse
from cmp.tools import metodo_predictivo_no_recursivo
from cmp.tools import get_printer
from cmp.tools import Node, AtomicNode, UnaryNode, BinaryNode


GI = Grammar()


G = Grammar()

E = G.NonTerminal('E', True)
W, D, N, T, P, X, R, O, Z, Y = G.NonTerminals('W D N T P X R O Z Y')
num, distinguido, terminal, nterminal, coma, pcoma, equal, plus, lcor, rcor, lpar, rpar, comilla, id, epsilon = G.Terminals('num distinguido terminal nterminal , ; = + [ ] < > \' id ε')

# > PRODUCTIONS
E %= D + N + T + R + W, lambda h, s: 
W %= R + W, None
W %= G.Epsilon, None

D %= distinguido + equal + id, lambda h, s: GI.NonTerminal(str(id), True)
N %= nterminal + equal + lcor + P + X + rcor, None
T %= terminal + equal + lcor + P + X + rcor, None

P %= lpar + id + coma + comilla + id + comilla + rpar, None
X %= coma + P + X, None
X %= G.Epsilon, None

R %= id + equal + O + Y, None
O %= id + Z, None
Z %= plus + id + Z, None
Z %= G.Epsilon, None
Y %= pcoma + O + Y, None
Y %= G.Epsilon, None

nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

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
    (id, f'({letters})({letters}|0|{nonzero_digits})*'),
               ], G.EOF)

text = '''
Distinguido = e
NoTerminales = [<x, 'x'>, <y, 'y'>, <z, 'z'>]
Terminales = [<a, 'b'>, <c, 'd'>]
x = y + z
y = a + b
y = b
z = d
'''
# print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
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
print(printer(ast))
