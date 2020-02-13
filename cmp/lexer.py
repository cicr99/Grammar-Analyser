from cmp.utils import Token
from cmp.regex import Regex
from cmp.automata import State

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            dfa = Regex(regex)
            automaton_list = State.from_nfa(dfa.automaton, 'texto random pra que haga lo que quiero')
            for i in automaton_list[1]:
                if(i.final):
                    i.tag = (n, token_type)
            regexs.append(automaton_list[0])
                
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        automatons = self.regexs
        for i in automatons:
            start.add_epsilon_transition(i)
        final = start.to_deterministic()
        return final
    
        
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''
        
        for symbol in string:
            try:
                state = state[symbol][0]
                lex += symbol
                if(state.final):
                    final = state
                    final_lex = lex
            except TypeError:
                # print(symbol, lex, string, state)
                break
                
        return final, final_lex
    
    def _tokenize(self, text):
        pos = 0
        while(len(text) > 0):
            temp = self._walk(text)
            
            if(temp[1] == ''):
                assert 1, 0
                
            pos = len(temp[1])
            text = text[pos:len(text)]
            mi = 9999
            final = None
            for i in temp[0].state:
                if i.final:
                    if i.tag[0] <  mi:
                        final = i
                        mi = i.tag[0]
            yield temp[1], final.tag[1]
        
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]