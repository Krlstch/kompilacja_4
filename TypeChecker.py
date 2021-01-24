from collections import defaultdict
import ast2
from SymbolTable import SymbolTable, VariableSymbol, VectorType


types = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
opers = ['+', '-', '*', '/']
mat_opers = ['.+', '.-', '.*', './']
rel_opers = ['<', '>', '>=', '<=', '==', '!=']
ass_opers = ['+=', '-=', '*=', '/=']

for op in opers + ass_opers:
    types[op]['int']['float'] = 'float'
    types[op]['float']['int'] = 'float'
    types[op]['float']['float'] = 'float'
    types[op]['int']['int'] = 'int'

for op in opers[0:3] + ass_opers[0:3]:
    types[op]['vector']['vector'] = 'vector'

types['\'']['vector'][None] = 'vector'
types['-']['vector'][None] = 'vector'
types['-']['int'][None] = 'int'
types['-']['float'][None] = 'float'

symtab = SymbolTable(None, "Symtab")


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, ast2.Ast):
                            self.visit(item)
                elif isinstance(child, ast2.Ast):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


def print_error(text, node.line_no):
    print(str(node.line_no) + ': ' + text)


class ErrorType:
    def __str__(self):
        return 'Error'


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, 'program')
        self.depth = 0

    def visit_Program(self, node):
        for inst in node.instr:
            self.visit(inst)

    def visit_Print(self, node):
        self.visit(node.params[0])

    def visit_Assign(self, node):
        type2 = self.visit(node.right)
        if isinstance(type2, ErrorType):
            return type2

        if node.op == "=":
            self.symbol_table.put(node.left.name, VariableSymbol(node.left.id, type2))

        if node.op != "=":
            type1 = self.visit(node.left)
            result_type = types[node.op][str(type1)][str(type2)]
            if result_type is not None:
                if result_type == 'vector':
                    if isinstance(type1, VectorType) and isinstance(type2, VectorType):
                        if type1.type != type2.type:
                            print("[Semantic Error at line {}] Different types in matrices!".format(node.line))
                            return ErrorType()
                        if node.op == '*=':
                            if type1.dims != 2:
                                print("[Semantic Error at line {}] Multiplying only for matrices!".format(node.line))
                                return ErrorType()
                            elif type1.sizes[1] != type2.sizes[0]:
                                print("[Semantic Error at line {}] Incorrect sizes for multiplication!".format(node.line))
                                return ErrorType()
                            else:
                                result_type = VectorType(type1.dims, [type1.sizes[0], type2.sizes[1]], type1.type)
                        else:
                            if type1.sizes != type2.sizes:
                                print("[Semantic Error at line {}] Different sizes of operands!".format(node.line))
                                return ErrorType()
                            else:
                                result_type = type1
                return result_type
            else:
                print("[Semantic Error at line {}] Incorrect types of operands!".format(node.line))
                return ErrorType()

    def visit_Arrassign(self, node):
        pass

    def visit_Access(self, node):
        if len(node.arr) > 2:
            print("[Semantic Error at line {}] Too many dimensions provided!".format(node.line))
            return ErrorType()

        var_type = self.visit(node.id)
        if str(var_type) != 'vector':
            print("[Semantic Error at line {}] Variable not a matrix!".format(node.line))
            return ErrorType()

        if isinstance(node.arr[0], int) and isinstance(node.arr[1], int):
            if node.arr[0] >= var_type.sizes[0] or node.arr[1] >= var_type.sizes[1] or node.arr[0] < 0 or node.arr[1] < 0:
                print("[Semantic Error at line {}] Index out of bounds!".format(node.line))
                return ErrorType()
            return var_type.type
        else:
            print("[Semantic Error at line {}] Indices must be integers".format(node.line))
            return ErrorType()

    def visit_Binop(self, node):
        pass

    def visit_BinopMat(self, node):
        pass

    def visit_Relation(self, node):
        pass

    def visit_IfStatement(self, node):
        type1 = self.visit(node.cond)
        if type1 != "logic":
            # error
            print_error('range must to be int', node.line_no)
        symtab.pushScope("if")
        self.visit(node.instr)
        symtab.popScope()

    def visit_IfElseStatement(self, node):
        type1 = self.visit(node.cond)
        if type1 != "logic":
            # error
            print_error('range must to be int', node.line_no)
        symtab.pushScope("if")
        self.visit(node.instr)
        symtab.popScope()

        symtab.pushScope("else")
        self.visit(node.else_instr)
        symtab.popScope()

    def visit_WhileLoop(self, node):
        type1 = self.visit(node.cond)
        if type1 != "logic":
            # error
            print_error('range must to be int', node.line_no)
        symtab.pushScope("loop")
        self.visit(node.instr)
        symtab.popScope()

    def visit_ForLoop(self, node):
        type1 = self.visit(node.limit)
        if type1 != "int":
            # error
            print_error('range must to be int', node.line_no)
        symtab.put(node.expr.name, type1)
        symtab.pushScope("loop")
        self.visit(node.instr)
        symtab.popScope()

    def visit_Matrix(self, node):
        pass

    def visit_Execute(self, node):
        self.visit(node.instr)  # nie jestem pewny

    def visit_BreakStatement(self, node):
        loop = symtab.getScope("loop")
        if not loop:
            print_error('continue must be used in loop', node.line_no)

    def visit_ContinueStatement(self, node):
        loop = symtab.getScope("loop")
        if not loop:
            print_error('continue must be used in loop', node.line_no)

    def visit_ReturnStatement(self, node):
        if node.value:
            self.visit(node.value)

    def visit_Uminus(self, node):
        return self.expr

    def visit_Transposition(self, node):
        matrix = self.node

        if not isinstance(matrix, tuple):
            # error
            print_error('wrong transposition', node.line_no)
        return (matrix[1], matrix[0], matrix[2])

    def visit_Gen(self, node):
        pass


