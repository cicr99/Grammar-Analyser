from input import GrammarFromInput
from cmp.tools import compute_firsts, compute_follows
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

if __name__ == '__main__':
    st.title('Grammar Analyser')

    st.sidebar.markdown('''Produced by:  
    Carmen Irene Cabrera Rodríguez  
    Enrique Martínez González''')

    text = st.text_area('Input your grammar here:')

    if text:
        G = GrammarFromInput(text).GiveGrammar()
        # print(G)
        st.write(G)
        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)



