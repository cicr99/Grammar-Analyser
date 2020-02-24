import streamlit as st

format_collection = lambda x: ' **,** '.join([str(p) for p in x])

def display_table(table, headers, title):
    st.subheader(title)

    text = ['|']
    text.extend([str(item) for item in headers])
    text.append('\n')
    text.extend([':-:']*(len(headers) + 1))
    text.append('\n')

    for symbol in table:
        text.append(f'**{symbol}**')
        for item in headers:
            if item in table[symbol]:
                t = ' **,** '.join([str(p) for p in table[symbol][item]])
                text.append(f'**[**{t}**]**')
            else:
                text.append('')
        text.append('\n')

    st.markdown('|'.join(text))


def display_grammar(G, header):
    st.subheader(f'{header}: ')

    st.markdown(f'''**Non-Terminals**: {G.nonTerminals}''')
    st.write(f'**Terminals**: {G.terminals}')
    st.write('**Productions**:')

    for nt in G.nonTerminals:
        p = ' **|** '.join([str(prod.Right) for prod in nt.productions])
        st.write(f'        {nt} --> {p}')


