from input import GrammarFromInput
from cmp.tools import *
from pprint import pprint
import streamlit as st


# text = '''
# Distinguido = <e, 'e'>
# NoTerminales = [<x, 'x'>, <y, 'y'>, <z, 'z'>]
# Terminales = [<a, 'b'>, <c, 'd'>]
# e = x
# x = y + z + a
# y = a + z; a + c
# z = c
# '''

# text = '''
# Distinguido = <e, 'e'>
# NoTerminales = []
# Terminales = [<a, 'b'>, <c, 'd'>]
# e = e + a; c
# '''

text = '''
Distinguido = E
NoTerminales = [ S ]
Terminales = [ a, b ]

E = S + a
S = b + S ; epsilon
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
        remove_useless_productions(G)
        st.write(G)
        remove_immediate_recursion(G)
        st.write(G)

        # firsts = compute_firsts(G)
        # follows = compute_follows(G, firsts)
        # M = build_parsing_table(G, firsts, follows)

        # st.dataframe(M)



def main2():
    G = GrammarFromInput(text).GiveGrammar()
    remove_immediate_recursion(G)
    pprint(G)



if __name__ == '__main__':
    main()



