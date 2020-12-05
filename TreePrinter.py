from __future__ import print_function
import ast2


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def makeIndentation(indent):
    for i in range(indent):
        print('|', end='  ')


class TreePrinter:

    @addToClass(ast2.Ast)
    def printTree(self, indent=0):
        for x in self.params:
            x.printTree()

    @addToClass(ast2.Print)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print('PRINT')

        indent += 1
        for x in self.params:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.Assign)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print(self.params[0])

        indent += 1
        makeIndentation(indent)
        print(self.params[1])
        x = self.params[2]
        if isinstance(x, ast2.Ast):
            x.printTree(indent)
        else:
            makeIndentation(indent)
            print(x)

    @addToClass(ast2.Arrassign)
    def printTree(self, indent=0):

        makeIndentation(indent)
        print(self.params[0])
        indent += 1
        makeIndentation(indent)
        print("REF")

        indent += 1
        makeIndentation(indent)
        print(self.params[1])

        for x in self.params[2]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)
        indent -= 1
        x = self.params[3]
        if isinstance(x, ast2.Ast):
            x.printTree(indent)
        else:
            makeIndentation(indent)
            print(x)

    @addToClass(ast2.Binop)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print(self.params[0])

        indent += 1
        for x in [self.params[1], self.params[2]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.BinopMat)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print(self.params[0])

        indent += 1
        for x in [self.params[1], self.params[2]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.BinopMat)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print(self.params[0])

        indent += 1
        for x in [self.params[1], self.params[2]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.Relation)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print(self.params[0])

        indent += 1
        for x in [self.params[1], self.params[2]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.IfStatement)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print('IF')

        x = self.params[0]
        indent += 1
        if isinstance(x, ast2.Ast):
            x.printTree(indent)
        else:
            makeIndentation(indent)
            print(x)

        makeIndentation(indent - 1)
        print('THEN')

        for x in [self.params[1]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.IfElseStatement)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print('IF')

        x = self.params[0]
        indent += 1
        if isinstance(x, ast2.Ast):
            x.printTree(indent)
        else:
            makeIndentation(indent)
            print(x)

        makeIndentation(indent - 1)
        print('THEN')

        for x in [self.params[1]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)
        makeIndentation(indent - 1)
        print("ELSE")
        for x in [self.params[2]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.WhileLoop)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print('while')

        indent += 1
        for x in [self.params[1]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.ForLoop)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print('for')
        indent += 1
        makeIndentation(indent)
        print(self.params[0])
        makeIndentation(indent)
        print('RANGE')
        indent += 1
        for x in [self.params[1], self.params[2]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)
        indent -= 1
        for x in [self.params[3]]:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.Get)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print(self.params)

    @addToClass(ast2.Gen)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print(self.params[0])
        x = self.params[1]

        indent += 1
        if isinstance(x, ast2.Ast):
            x.printTree(indent)
        else:
            makeIndentation(indent)
            print(x)

    @addToClass(ast2.BreakStatement)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print("BREAK")

    @addToClass(ast2.ContinueStatement)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print("CONTINUE")

    @addToClass(ast2.ReturnStatement)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print("RETURN")

    @addToClass(ast2.Uminus)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print("MINUS")

        indent += 1
        x = self.params
        if isinstance(x, ast2.Ast):
            x.printTree(indent)
        else:
            makeIndentation(indent)
            print(x)

    @addToClass(ast2.Transposition)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print("TRANSPOSITION")

        indent += 1
        x = self.params
        if isinstance(x, ast2.Ast):
            x.printTree(indent)
        else:
            makeIndentation(indent)
            print(x)

    @addToClass(ast2.Execute)
    def printTree(self, indent=0):
        for x in self.params:
            if isinstance(x, ast2.Ast):
                x.printTree(indent)
            else:
                makeIndentation(indent)
                print(x)

    @addToClass(ast2.Matrix)
    def printTree(self, indent=0):
        makeIndentation(indent)
        print("Vector")
        indent += 1
        for x in self.params:
            makeIndentation(indent)
            print("Vector")
            for number in x:
                makeIndentation(indent + 1)
                print(number)

