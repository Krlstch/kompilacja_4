import numpy as np
from dataclasses import dataclass

symbols = {}


@dataclass
class Ast(object):
    params = None

    def __init__(self, params=None):
        self.params = params

    def execute(self):
        return

    @staticmethod
    def resolve(x):
        if isinstance(x, Ast):
            return x.execute()
        else:
            return x


class Print(Ast):
    def execute(self):
        print(' '.join(str(Ast.resolve(x)) for x in self.params))


class Assign(Ast):
    def execute(self):
        if self.params[0] == "=":
            symbols[self.params[1]] = Ast.resolve(self.params[2])
        elif self.params[0] == "+=":
            symbols[self.params[1]] = symbols[self.params[1]] + Ast.resolve(self.params[2])
        elif self.params[0] == "-=":
            symbols[self.params[1]] = symbols[self.params[1]] - Ast.resolve(self.params[2])
        elif self.params[0] == "*=":
            symbols[self.params[1]] = symbols[self.params[1]] * Ast.resolve(self.params[2])
        elif self.params[0] == "/=":
            symbols[self.params[1]] = symbols[self.params[1]] / Ast.resolve(self.params[2])


class Arrassign(Ast):
    def execute(self):
        if self.params[0] == "=":
            symbols[self.params[1]][self.params[2][0]][self.params[2][1]] = Ast.resolve(self.params[3])
        elif self.params[0] == "+=":
            symbols[self.params[1]][self.params[2][0]][self.params[2][1]] += Ast.resolve(self.params[3])
        elif self.params[0] == "-=":
            symbols[self.params[1]][self.params[2][0]][self.params[2][1]] -= Ast.resolve(self.params[3])
        elif self.params[0] == "*=":
            symbols[self.params[1]][self.params[2][0]][self.params[2][1]] *= Ast.resolve(self.params[3])
        elif self.params[0] == "/=":
            symbols[self.params[1]][self.params[2][0]][self.params[2][1]] /= Ast.resolve(self.params[3])


#
class Access(Ast):
    def execute(self):
        result = symbols[self.params[0]][self.params[1][0]][self.params[1][1]]
        return result


class Binop(Ast):
    def execute(self):
        result = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b
        }[self.params[0]](Ast.resolve(self.params[1]), Ast.resolve(self.params[2]))
        return result


class BinopMat(Ast):
    def execute(self):
        result = {
            '>': lambda a, b: (a > b),
            '>=': lambda a, b: (a >= b),
            '<': lambda a, b: (a < b),
            '<=': lambda a, b: (a <= b),
            '==': lambda a, b: (a == b),
            '!=': lambda a, b: (a != b)
        }[self.params[0]](Ast.resolve(self.params[1]), Ast.resolve(self.params[2]))
        return result


class Relation(Ast):
    def execute(self):
        result = {
            '>': lambda a, b: (a > b),
            '>=': lambda a, b: (a >= b),
            '<': lambda a, b: (a < b),
            '<=': lambda a, b: (a <= b),
            '==': lambda a, b: (a == b),
            '!=': lambda a, b: (a != b)
        }[self.params[0]](Ast.resolve(self.params[1]), Ast.resolve(self.params[2]))
        return result


class IfStatement(Ast):
    def execute(self):
        result = None
        if Ast.resolve(self.params[0]):
            result = Ast.resolve(self.params[1])
        return result


class IfElseStatement(Ast):
    def execute(self):
        if Ast.resolve(self.params[0]):
            result = Ast.resolve(self.params[1])
        else:
            result = Ast.resolve(self.params[2])
        return result


class WhileLoop(Ast):
    def execute(self):
        result = None
        while Ast.resolve(self.params[0]):
            print('|', end='  ')
            result = Ast.resolve(self.params[1])
            if result == "continue":
                continue
            if result == "break":
                break
        return result


class ForLoop(Ast):
    def execute(self):
        result = None
        symbols[self.params[0]] = Ast.resolve(self.params[1])
        while symbols[self.params[0]] <= Ast.resolve(self.params[2]):
            print('|', end='  ')
            result = Ast.resolve(self.params[3])
            if result == "continue":
                continue
            if result == "break":
                break
            symbols[self.params[0]] += 1
        return result


class Get(Ast):
    def execute(self):
        result = symbols.get(self.params)
        return result


class Matrix(Ast):
    def execute(self):
        pass


class Execute(Ast):
    def execute(self):
        result = None
        for instr in self.params:
            result = Ast.resolve(instr)
            if result in ["continue", "break"]:
                break
        return result


class BreakStatement(Ast):
    def execute(self):
        result = "break"
        return result


class ContinueStatement(Ast):
    def execute(self):
        result = "continue"
        return result


class ReturnStatement(Ast):
    def execute(self):
        exit(self.params)


class Uminus(Ast):
    def execute(self):
        result = - Ast.resolve(self.params)
        return result


class Transposition(Ast):
    def execute(self):
        result = np.transpose(Ast.resolve(self.params))
        return result


class Gen(Ast):
    def execute(self):
        result = {
            'zeros': lambda a: np.zeros(shape=[a, a]),
            'ones': lambda a: np.ones(shape=[a, a]),
            'eye': lambda a: np.eye(a)
        }[self.params[0]](Ast.resolve(self.params[1]))
        return result


from TreePrinter import addToClass
