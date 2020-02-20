from input import GrammarFromInput
from cmp.tools import compute_firsts, compute_follows
from pprint import pprint
import streamlit as st
from cmp.grammar_to_automata import GrammarToAutomata
from cmp.automata_to_regex import AutomataToRegex
from pprint import pprint


# text = '''
# Distinguido = <e, 'e'>
# NoTerminales = [<x, 'x'>, <y, 'y'>, <z, 'z'>]
# Terminales = [<a, 'b'>, <c, 'd'>]
# e = x
# x = y + z + a
# y = a + z; a + c
# z = c
# '''

text = '''
Distinguido = <e, 'e'>
NoTerminales = [<x, 'x'>]
Terminales = [<a, 'a'>, <b, 'b'>, <c, 'c'>, <d, 'd'>, <f, 'f'>]
e = a + x
x = b + e; c; d + x; f
'''

if __name__ == '__main__':
    st.title('Grammar Analyser')

    st.sidebar.markdown('''Produced by:  
    Carmen Irene Cabrera Rodríguez  
    Enrique Martínez González''')

    # text = st.text_area('Input your grammar here:')

    if text:
        G = GrammarFromInput(text).GiveGrammar()

        st.write(G)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)

        nfa = GrammarToAutomata(G).CalculateRegularNFA()
        nfa._repr_png_().write_png('nfa.png')
        gnfa = AutomataToRegex(nfa).GetGNFA()
        gnfa._repr_png_().write_png('gnfa.png')
        print(AutomataToRegex(nfa).GetRegex())



