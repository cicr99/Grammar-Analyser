from input import GrammarFromInput
from cmp.tools import compute_firsts, compute_follows
from pprint import pprint

text = '''
Distinguido = <e, 'e'>
NoTerminales = [<x, 'x'>, <y, 'y'>, <z, 'z'>]
Terminales = [<a, 'b'>, <c, 'd'>]
e = x
x = y + z + a
y = a + z; a + c
z = c
'''

if __name__ == '__main__':
    G = GrammarFromInput(text).GiveGrammar()
    print(G)

    firsts = compute_firsts(G)
    pprint(firsts)
    follows = compute_follows(G, firsts)
    print()
    pprint(follows)
    