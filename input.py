#LEXER
from cmp.lexer import Lexer

nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

lexer = Lexer([
    ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
    ('distinguido' , 'Distinguido'),
    ('terminal' , 'Terminales'),
    ('nterminal', 'NoTerminales'),
    ('coma', ','),
    ('equal', '='),
    ('plus', '+'),
    ('lcor', '['),
    ('rcor', ']'),
    ('lpar', '<'),
    ('rpar', '>'),
    ('salto', '\n'),
    ('comilla', '\''),
    ('space', '  *'),
    ('id', f'({letters})({letters}|0|{nonzero_digits})*'),
               ], 'eof')

# text = '''
# Distinguido = e
# NoTerminales = [<x, 'x'>, <y, 'y'>, <z, 'z'>]
# Terminales = [<a, 'b'>, <c, 'd'>]
# x = y + z
# y = a + b
# y = b
# z = d
# '''
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)