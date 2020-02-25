from input import GrammarFromInput
from cmp.tools import *
from pprint import pprint
import streamlit as st
from cmp.grammar_to_automata import *
from cmp.automata_to_regex import AutomataToRegex
from cmp.nfa_dfa import NFA
from pprint import pprint
from cmp.visual import *


def main():
    st.title('Grammar Analyser')

    st.sidebar.markdown('''Produced by:  
    Carmen Irene Cabrera Rodríguez  
    Enrique Martínez González''')

    text = st.text_area('Input your grammar here:')

    if text:
        try:
            G = GrammarFromInput(text).GiveGrammar()
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
                st.write('')
                word = st.text_area('Input a string to get the derivation tree:')
                if word:
                    st.subheader('Derivation tree of LL1:')
                    st.graphviz_chart(str(make_tree_LL1(G, word, M, firsts, follows).graph()))



            #SHIFT-REDUCE parsers analysis
            GG = G.AugmentedGrammar()

            parsers = [SLR1Parser, LR1Parser, LALR1Parser]
            parsers_name = ['SLR(1)', 'LR(1)', 'LALR(1)']
            words = ['' for _ in range(3)]
            for i, parser_class in enumerate(parsers):
                st.title(f'{parsers_name[i]} Parser')
                parser = parser_class(GG)
                ok, action, goto = parser.ok, parser.action, parser.goto
                display_table(action, G.terminals + [G.EOF], 'ACTION')
                display_table(goto, G.nonTerminals, 'GOTO')

                st.subheader(f'{parsers_name[i]} Automata')
                st.graphviz_chart(str(parser.automaton.graph()))

                if not ok:
                    st.write('')
                    st.error(f'It\'s not {parsers_name[i]}!')
                    st.write(f'Conflictive string: **\"{action_goto_conflict(action, goto)}\"**')
                else:
                    words[i] = st.text_area(f'Input a string to get the derivation tree of {parsers_name[i]} parser:')
                    if words[i]:
                        st.subheader(f'Derivation tree of {parsers_name[i]}:')
                        st.graphviz_chart(str(make_tree(G, words[i], parser).graph()))


            #Regular Grammar Analysis

            st.title('Is it a Regular Grammar?')
            is_Regular, nfa = analyzing_regularity(G)
            if is_Regular:
                st.subheader('It\'s regular')
                st.subheader('NFA')
                st.graphviz_chart(str(nfa.graph()))

                gnfa = AutomataToRegex(nfa).GetGNFA()
                # st.subheader('GNFA')
                # st.graphviz_chart(str(gnfa.graph()))

                st.subheader('Regular Expression')
                st.write(AutomataToRegex(nfa).GetRegex())
            else:
                st.write('')
                st.error(f'It\'s not!')
        except Exception as e:
            st.error('Unexpected error!!! You probably did something wrong :wink:')




if __name__ == '__main__':
    main()




