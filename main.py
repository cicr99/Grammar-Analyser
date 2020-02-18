from input import GrammarFromInput
from cmp.tools import *
from pprint import pprint
import streamlit as st


text = '''
Distinguido = S
NoTerminales = [ A, B, C ]
Terminales = [ a, b, c, d ]
S = a + b + S ; a + b + A ; a + b + B
A = a + d
B = a + B
C = d + c
'''


def main():
    st.title('Grammar Analyser')

    st.sidebar.markdown('''Produced by:  
    Carmen Irene Cabrera Rodríguez  
    Enrique Martínez González''')

    text = st.text_area('Input your grammar here:')

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



def main2():
    G = grammar_from_input(text)
    print(G)
    simplifying_grammar(G)
    print(G)



if __name__ == '__main__':
    main2()



