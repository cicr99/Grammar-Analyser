from cmp.regex import Regex
from cmp.nfa_dfa import NFA
import pydot
from pprint import pprint

class GNFA:
    def __init__(self, nfa :NFA):
        self.nfa = nfa
        self.states = nfa.states + 2
        self.start = 0
        self.finals = [nfa.states + 1]
        self.transitions = { state: {} for state in range(self.states) }

        for start in range(nfa.states):
            for finish in range(nfa.states):
                if self._regexes(start, finish) == '':
                    continue
                try:
                    self.transitions[start + 1][Regex(self._regexes(start, finish))].append(finish + 1)
                except KeyError:
                    self.transitions[start + 1][Regex(self._regexes(start, finish))] = [finish + 1]

        # for start, dic in nfa.transitions.items():
        #     for regex, destinations in dic.items():
        #         for d in destinations:
        #             try:
        #                 self.transitions[start + 1][self._regexes(start, d)].append(d + 1)
        #             except KeyError:
        #                 self.transitions[start + 1][self._regexes(start, d)] = [d + 1]

                # self.transitions[start + 1][self._regexes(start, ) Regex(str(regex))] = [i + 1 for i in destinations]

        # pprint(nfa.transitions)

        for start, dic in nfa.transitions.items():
            if len(dic.items()) == 0:
                # print(start)
                uni = [i + 1 for i in range(nfa.states)]
                # print(uni)
                self.transitions[start + 1][Regex('~')] = uni
            else:
                s = set()
                for regex, destinations in dic.items():
                    for item in destinations:
                        s.add(item)
                # print(s)
                uni = set([i for i in range(nfa.states)])
                dif = uni.difference(s)
                for state in dif:
                    self.transitions[start + 1][Regex('~')] = [state + 1]

        self.transitions[0][Regex('ε')] = [nfa.start + 1]
        self.transitions[0][Regex('~')] = [i + 1 for i in range(nfa.states + 1) if i != nfa.start]

        for i in range(nfa.states):
            if not i in nfa.finals:
                self.transitions[i + 1][Regex('~')] = [nfa.states + 1]
            else:
                self.transitions[i + 1][Regex('ε')] = [nfa.states + 1]

        # pprint(self.transitions)



        # print(self.transitions)

        # for (origin, regex), destinations in transitions.items():
        #     assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
        #     self.transitions[origin][regex] = destinations

    def _regexes(self, i, j):
        regexes = ''
        for regex, value in self.nfa.transitions[i].items():
            if j in value:
                if regexes == '':
                    regexes = str(regex)
                else:
                    regexes += '|' + str(regex)
                continue
        return regexes

    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()

    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for start, dic in self.transitions.items():
            for regex, destination in dic.items():
                tran = 'ε' if regex.regular_exp == '' else regex.regular_exp
                G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
                for end in destination:
                    G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                    G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

    def _repr_png_(self):
        # try:
        return self.graph()
        # except:
            # pass