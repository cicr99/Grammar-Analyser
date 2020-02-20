from cmp.gnfa import GNFA
from cmp.regex import Regex
from pprint import pprint

class AutomataToRegex:
    def __init__(self, nfa):
        self.gnfa = GNFA(nfa)
        
    def GetGNFA(self):
        return self.gnfa

    def _regex_to_q(self, i, q):
        for (regex, states) in self.gnfa.transitions[i].items():
            if q in states:
                states.remove(q)
                return(regex)
    
    def _regex_from_q(self, j, q):
        for (regex, states) in self.gnfa.transitions[q].items():
            if j in states:
                return regex

    def _regex_from_q_to_q(self, q):
        for (regex, states) in self.gnfa.transitions[q].items():
            if q in states:
                return regex



    def GetRegex(self):
        pprint(self.gnfa.transitions) 
        for q in range(1, self.gnfa.states - 1):
            for i in range(self.gnfa.states - 1):
                if i not in self.gnfa.transitions or i == q:
                    continue
                
                
                # temp.update(self.gnfa.transitions[i])
                
                # pprint(self.gnfa.transitions)
                print(q, i)
                regex_from_q_to_q = self._regex_from_q_to_q(q)
                print('q->q', regex_from_q_to_q.regular_exp)
                regex_to_q = self._regex_to_q(i, q)
                print('i->q', regex_to_q.regular_exp)

                temp = {}
                for key, values in self.gnfa.transitions[i].items():
                    temp[key] = list(values)

                for (regex, states) in self.gnfa.transitions[i].items():
                    if regex_to_q.regular_exp == '~':
                        continue
                    for j in states:
                        print(states)
                        if j == self.gnfa.start:
                            continue
                        print(j)
                        regex_from_q = self._regex_from_q(j, q)
                        if regex_from_q.regular_exp == '~':
                            continue
                        print('q->j', regex_from_q.regular_exp)
                        exp = ''
                        if regex_to_q.regular_exp != '~':
                            exp += '(' + regex_to_q.regular_exp + ')'
                        if regex_from_q_to_q.regular_exp != '~':
                            exp += '(' + regex_from_q_to_q.regular_exp + ')*'
                        if regex_from_q.regular_exp != '~':
                            exp += '(' + regex_from_q.regular_exp + ')'
                        exp_res = regex.regular_exp
                        if exp != '':
                            exp_res = exp
                            if regex.regular_exp != '~':
                                exp_res = '(' + regex.regular_exp + ')' + '|' + exp
                        print('resultado', exp_res)
                        temp[regex].remove(j)
                        if len(temp[regex]) == 0:
                            del temp[regex]
                        # print(states)
                        try:
                            temp[Regex(exp_res)].append(j)
                        except KeyError:
                            temp[Regex(exp_res)] = [j]

                self.gnfa.transitions[i] = temp
            del self.gnfa.transitions[q]
            self.gnfa._repr_png_().write_png(f'{q}.png')
            print(self.gnfa.transitions)
        return list(self.gnfa.transitions[0].items())[0]
