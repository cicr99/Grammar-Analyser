from cmp.pycompiler import Grammar
from cmp.utils import Token
from cmp.nfa_dfa import NFA, DFA
from cmp.tools import evaluate_parse
from cmp.tools import metodo_predictivo_no_recursivo
from cmp.tools import nfa_to_dfa
from cmp.tools import automata_union, automata_concatenation, automata_closure, automata_minimization
from cmp.tools import get_printer
from pprint import pprint as pp
import pydot

class Node:
    def evaluate(self):
        raise NotImplementedError()
        
class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node
        
    def evaluate(self):
        value = self.node.evaluate() 
        return self.operate(value)
    
    @staticmethod
    def operate(value):
        raise NotImplementedError()
        
class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def evaluate(self):
        lvalue = self.left.evaluate() 
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)
    
    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()
        

EPSILON = 'ε'

class EpsilonNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        states = 0
        start = 0
        finals = [0]
        transitions = {}
        return NFA(states, finals, transitions, start)

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        states = 2
        start = 0
        finals = [1]
        transitions = {}
        transitions[(0, s)] = [1]
        return NFA(states, finals, transitions, start)

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)



G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

# > PRODUCTIONS???
E %= T + X, lambda h, s: s[2], None, lambda h, s: s[1]

X %= pipe + T + X, lambda h, s: s[3], None, None, lambda h, s: UnionNode(h[0], s[2])
X %= G.Epsilon, lambda h, s: h[0]

T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]

Y %= F + Y, lambda h, s: s[2], None, lambda h, s: ConcatNode(h[0], s[1])
Y %= G.Epsilon, lambda h, s: h[0]

F %= A + Z, lambda h, s: s[2], None, lambda h, s: s[1]

Z %= star + Z, lambda h, s: s[2], None, lambda h, s: ClosureNode(h[0])
Z %= G.Epsilon, lambda h, s: h[0]

A %= symbol, lambda h, s: SymbolNode(s[1])
A %= opar + E + cpar, lambda h, s: s[2], None, None, None
A %= epsilon, lambda h, s: EpsilonNode(s[1])



def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        if(char == '*'):
            tokens.append(Token('*', star))
        elif(char == '('):
            tokens.append(Token('(', opar))
        elif(char == ')'):
            tokens.append(Token(')', cpar))
        elif(char == '|'):
            tokens.append(Token('|', pipe))
        elif(char == 'ε'):
            tokens.append(Token('ε', epsilon))
        else:
            tokens.append(Token(char, symbol))

    tokens.append(Token('$', G.EOF))
    return tokens


parser = metodo_predictivo_no_recursivo(G)



printer = get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode)

class Regex:
    def __init__(self, regular_exp):
        print(regular_exp)
        
        self.tokens = regex_tokenizer(regular_exp, G, False)
        self.left_parse = parser(self.tokens)
        self.ast = evaluate_parse(self.left_parse, self.tokens)
        self.nfa = self.ast.evaluate()
        self.dfa = nfa_to_dfa(self.nfa)
        self.mini = automata_minimization(self.dfa)
        self.automaton = self.mini

        
        #Debugin
        print(printer(self.ast))
        # self.mini._repr_png_().write_png(f'{regular_exp}.png')

    def __call__(string):
        return self.mini.recognize(string)