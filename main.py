from input import GrammarFromInput
from cmp.tools import *
from pprint import pprint
import streamlit as st
from cmp.grammar_to_automata import *
from cmp.automata_to_regex import AutomataToRegex
from cmp.nfa_dfa import NFA
from pprint import pprint
from cmp.visual import *


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
        # gnfa._repr_png_().write_png('gnfa.png')
        print(AutomataToRegex(nfa).GetRegex())



def main2():
    st.title('Grammar Analyser')

    st.sidebar.markdown('''Produced by:  
    Carmen Irene Cabrera Rodríguez  
    Enrique Martínez González''')

    text = st.text_area('Input your grammar here:')

    if text:
        G = grammar_from_input(text)
        display_grammar(G, 'Given Grammar')

        simplifying_grammar(G)
        display_grammar(G, 'Fixed Grammar')


        #LL1 analysis
        st.title('LL1Parser')
        firsts, follows, M, is_ll1 = ll1_analysis(G)

        display_table(M, G.terminals + [G.EOF], 'LL1 TABLE')

        if not is_ll1:
            st.write('')
            st.error('It\'s not LL(1)!')
            st.write(f'Conflictive string: **\"{ll1_conflict(G, M)}\"**')

        else:
            word = st.text_area('Input a string to get the derivation tree:')
            if word:
                make_tree_LL1(G, word, M, firsts, follows)



        #SHIFT-REDUCE parsers analysis
        GG = G.AugmentedGrammar()

        parsers = [SLR1Parser, LR1Parser, LALR1Parser]
        parsers_name = ['SLR(1)', 'LR(1)', 'LALR(1)']
        words = []
        for i, parser_class in enumerate(parsers):
            st.title(f'{parsers_name[i]} Parser')
            parser = parser_class(GG)
            ok, action, goto = parser.ok, parser.action, parser.goto
            display_table(action, G.terminals + [G.EOF], 'ACTION')
            display_table(goto, G.nonTerminals, 'GOTO')

            if not ok:
                st.write('')
                st.error(f'It\'s not {parsers_name[i]}!')
                st.write(f'Conflictive string: **\"{action_goto_conflict(action, goto)}\"**')


        #Regular Grammar Analysis

        st.title('Is it a Regular Grammar?')
        is_Regular, nfa = analyzing_regularity(G)
        if is_Regular:
            nfa._repr_png_().write_png('nfa.png')
            gnfa = AutomataToRegex(nfa).GetGNFA()
            gnfa._repr_png_().write_png('gnfa.png')
            print(AutomataToRegex(nfa).GetRegex())
        else:
            st.write('')
            st.error(f'It\'s not!')

if __name__ == '__main__':
    main2()




