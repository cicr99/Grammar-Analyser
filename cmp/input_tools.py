from cmp.tools import Node
from cmp.pycompiler import Production, Sentence, Epsilon

class MultiNodeGrammar(Node):
    def __init__(self, lis):
        self.lis = lis

    def evaluate(self, context):
        for i in self.lis:
            # print(i)
            i.evaluate(context)

class EpsilonNodeGrammar(Node):
    def __init__(self):
        pass

    def evaluate(self, context):
        return

class DisNodeGrammar(Node):
    def __init__(self, dis, sym):
        self.dis = dis
        self.sym = sym

    def evaluate(self, context):
        context.NTerminals[self.dis] = context.Grammar.NonTerminal(self.sym, True)

class UnaryNodeGrammar(Node):
    def __init__(self, node, context):
        self.node = node
        self.context = context

    def evaluate(self):
        node.evaluate(self.context)

class NonTerminalNodeGrammar(Node):
    def __init__(self, izq, der):
        self.izq = izq
        self.der = der

    def evaluate(self, context):
        context.NTerminals[self.izq] = context.Grammar.NonTerminal(self.der)

class TerminalNodeGrammar(Node):
    def __init__(self, izq, der):
        self.izq = izq
        self.der = der

    def evaluate(self, context):
        context.Terminals[self.izq] = context.Grammar.Terminal(self.der)

class ProductionNodeGrammar(Node):
    def __init__(self, izq, der):
        self.izq = izq
        self.der = der


    def evaluate(self, context):

        if isinstance(self.der, SentenceNodeGrammar):
            p = self.der.evaluate(context)
            context.Productions[context.NTerminals[str(self.izq)]] = Production(context.NTerminals[str(self.izq)], p)
            context.NTerminals[str(self.izq)].Grammar.Add_Production(Production(context.NTerminals[str(self.izq)], p))
            return

        elif isinstance(self.der, SentencesNodeGrammar):
            for i in self.der.evaluate(context):
                sentence = i
                if isinstance(sentence, SentenceNodeGrammar):
                    sentence = i.evaluate(context)

                try:
                    context.Productions[context.NTerminals[str(self.izq)]].append(Production(context.NTerminals[str(self.izq)], sentence))
                except:
                    context.Productions[context.NTerminals[str(self.izq)]] = [Production(context.NTerminals[str(self.izq)], sentence)]

                context.NTerminals[str(self.izq)].Grammar.Add_Production(Production(context.NTerminals[str(self.izq)], sentence))
            return

        b = context.Terminals[str(self.der)] if str(self.der) in context.Terminals else context.NTerminals[str(self.der)]
        
        if(str(self.der) == 'epsilon'):
            b = context.Grammar.Epsilon

        # print(b)

        context.Productions[context.NTerminals[str(self.izq)]] = Production(context.NTerminals[str(self.izq)], Sentence(b))
        context.NTerminals[str(self.izq)].Grammar.Add_Production(Production(context.NTerminals[str(self.izq)], Sentence(b)))

class SentencesNodeGrammar(Node):
    def __init__(self, izq, der):
        self.izq = izq
        self.der = der

    def evaluate(self, context):
        ret = []
        if not isinstance(self.der, SentenceNodeGrammar):
            if(str(self.der) == 'epsilon'):
                self.der = context.Grammar.Epsilon
            else:
                der = context.Terminals[str(self.der)] if str(self.der) in context.Terminals else context.NTerminals[str(self.der)]
                self.der = Sentence(der)
        if isinstance(self.izq, SentenceNodeGrammar):
            return [self.izq, self.der]
        elif isinstance(self.izq, SentencesNodeGrammar):
            temp = self.izq.evaluate(context)
            for i in temp:
                ret.append(i)
            ret.append(self.der)
            return ret
        b = context.Terminals[str(self.izq)] if str(self.izq) in context.Terminals else context.NTerminals[str(self.izq)]
        return [Sentence(b)]

class SentenceNodeGrammar(Node):
    def __init__(self, izq, der):
        self.izq = izq
        self.der = der

    def evaluate(self, context):
        b = context.Terminals[str(self.der)] if str(self.der) in context.Terminals else context.NTerminals[str(self.der)]
        if not isinstance(self.izq, SentenceNodeGrammar):
            a = context.Terminals[str(self.izq)] if str(self.izq) in context.Terminals else context.NTerminals[str(self.izq)]
            return a + b
        temp = self.izq.evaluate(context)
        return temp + b

