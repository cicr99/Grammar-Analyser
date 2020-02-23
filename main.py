from input import GrammarFromInput
from cmp.tools import *
from pprint import pprint
import streamlit as st
from cmp.grammar_to_automata import GrammarToAutomata
from cmp.automata_to_regex import AutomataToRegex
from pprint import pprint


text = '''
Distinguido = S
NoTerminales = [ A ]
Terminales = [ a, b, d ]
S = a + b + S; a + b + A; A
A = a + d; A + d; a + S; epsilon
'''

def main():
    st.title('Grammar Analyser')

    st.sidebar.markdown('''Produced by:  
    Carmen Irene Cabrera Rodríguez  
    Enrique Martínez González''')

    # text = st.text_area('Input your grammar here:')

    if text:
        G = grammar_from_input(text)
        #G = GrammarFromInput(text).GiveGrammar()
        st.write(G)
        simplifying_grammar(G)
        st.write(G)

        # firsts = compute_firsts(G)
        # follows = compute_follows(G, firsts)
        # M = build_parsing_table(G, firsts, follows)

        # st.dataframe(M)
        nfa = GrammarToAutomata(G).CalculateRegularNFA()
        nfa._repr_png_().write_png('nfa.png')
        gnfa = AutomataToRegex(nfa).GetGNFA()
        gnfa._repr_png_().write_png('gnfa.png')
        print(AutomataToRegex(nfa).GetRegex())



def main2():
    G = grammar_from_input(text)
    print(G)
    simplifying_grammar(G)
    print(G)

    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)

    # print('FIRSTS')
    # pprint(firsts)
    # print()
    # print('FOLLOWS')
    # pprint(follows)

    M,_  = build_parsing_table(G, firsts, follows)
    # print()
    # print('M')
    # pprint(M)
    print(ll1_conflict(G, M))

if __name__ == '__main__':
    main2()




