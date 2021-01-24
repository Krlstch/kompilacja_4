from collections import defaultdict
import ast2
from SymbolTable import SymbolTable, VectorType

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

ttype['+']["int"]["int"] = "int"
ttype['-']["int"]["int"] = "int"
ttype['*']["int"]["int"] = "int"
ttype['/']["int"]["int"] = "int"
ttype[".+"]["int"]["int"] = "int"
ttype[".-"]["int"]["int"] = "int"
ttype[".*"]["int"]["int"] = "int"
ttype["./"]["int"]["int"] = "int"
ttype['<']["int"]["int"] = "logic"
ttype['>']["int"]["int"] = "logic"
ttype["<="]["int"]["int"] = "logic"
ttype[">="]["int"]["int"] = "logic"
ttype["=="]["int"]["int"] = "logic"
ttype["!="]["int"]["int"] = "logic"

ttype['+']["int"]["float"] = "float"
ttype['-']["int"]["float"] = "float"
ttype['*']["int"]["float"] = "float"
ttype['/']["int"]["float"] = "float"
ttype[".+"]["int"]["float"] = "float"
ttype[".-"]["int"]["float"] = "float"
ttype[".*"]["int"]["float"] = "float"
ttype["./"]["int"]["float"] = "float"
ttype['<']["int"]["float"] = "logic"
ttype['>']["int"]["float"] = "logic"
ttype["<="]["int"]["float"] = "logic"
ttype[">="]["int"]["float"] = "logic"
ttype["=="]["int"]["float"] = "logic"
ttype["!="]["int"]["float"] = "logic"

ttype['+']["float"]["int"] = "float"
ttype['-']["float"]["int"] = "float"
ttype['*']["float"]["int"] = "float"
ttype['/']["float"]["int"] = "float"
ttype[".+"]["float"]["int"] = "float"
ttype[".-"]["float"]["int"] = "float"
ttype[".*"]["float"]["int"] = "float"
ttype["./"]["float"]["int"] = "float"
ttype['<']["float"]["int"] = "logic"
ttype['>']["float"]["int"] = "logic"
ttype["<="]["float"]["int"] = "logic"
ttype[">="]["float"]["int"] = "logic"
ttype["=="]["float"]["int"] = "logic"
ttype["!="]["float"]["int"] = "logic"

ttype['+']["float"]["float"] = "float"
ttype['-']["float"]["float"] = "float"
ttype['*']["float"]["float"] = "float"
ttype['/']["float"]["float"] = "float"
ttype[".+"]["float"]["float"] = "float"
ttype[".-"]["float"]["float"] = "float"
ttype[".*"]["float"]["float"] = "float"
ttype["./"]["float"]["float"] = "float"
ttype['<']["float"]["float"] = "logic"
ttype['>']["float"]["float"] = "logic"
ttype["<="]["float"]["float"] = "logic"
ttype[">="]["float"]["float"] = "logic"
ttype["=="]["float"]["float"] = "logic"
ttype["!="]["float"]["float"] = "logic"

castable_operations = ['/', '+', '-', '*', '>', '<', ">=", "<=", "==", "!="]
castable_matrix_operations = [".+", ".-", ".*", "./"]
castable_types = ["int", "float"]


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


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, 'program')
        self.depth = 0

    def visit_Program(self, node):
        for inst in node.instr:
            self.visit(inst)

    def visit_Print(self, node):
        self.visit(node.arg[0])

    def visit_Assign(self, node):
        type2 = self.visit(node.right)
        if node.op == '=':
            self.symbol_table.put(node.left.name, type2)
        else:
            type1 = self.visit(node.left)
            if type1 == type2:
                return
            elif type1 == "int" and type2 == "float":
                self.symbol_table.put(node.left.name, type2)
            else:
                print("Error at line {0}: Variables of incompatible types".format(node.line))

    def visit_Arrassign(self, node):
        if len(node.arr) != 2:
            print("Error at line {0}: Access array must be of length 2".format(node.line))
            return None
        arr_type0 = self.visit(node.arr[0])
        arr_type1 = self.visit(node.arr[1])
        if arr_type0 != "int" or arr_type1 != "int":
            print("Error at line {0}: Access array elements must be integers".format(node.line))
            return None

        m_type = self.visit(node.left.mat[0][0])
        type2 = self.visit(node.right)
        if node.op == '=':
            self.symbol_table.put(node.left.name, type2)
        e
            else:
                print("Error at line {0}: Variables of incompatible types".format(node.line))

    def visit_Access(self, node):
        pass

    def visit_Binop(self, node):
        pass

    def visit_BinopMat(self, node):
        pass

    def visit_Relation(self, node):
        pass

    def visit_IfStatement(self, node):
        type1 = self.visit(node.cond)
        if type1 == "bool":
            self.symbol_table.push_scope("ifscope")
            for inst in node.instr:
                self.visit(inst)
            self.symbol_table.pop_scope()
        else:
            print("Error at line {0}: Condition in if statement must be boolean".format(node.line))

    def visit_IfElseStatement(self, node):
        type1 = self.visit(node.cond)
        if type1 == "bool":
            self.symbol_table.push_scope("ifscope")
            for inst in node.instr:
                self.visit(inst)
            self.symbol_table.pop_scope()
            self.symbol_table.push_scope("elsescope")
            for inst in node.else_instr:
                self.visit(inst)
            self.symbol_table.pop_scope()
        else:
            print("Error at line {0}: Condition in if statement must be boolean".format(node.line))


    def visit_WhileLoop(self, node):
        type1 = self.visit(node.cond)
        if type1 == "bool":
            self.symbol_table.push_scope("loop")
            self.visit(node.instr)
            self.symbol_table.pop_scope()
        else:
            print("Error at line {0}: Condition in while loop must be boolean".format(node.line))

    def visit_ForLoop(self, node):
        type1 = self.visit(node.expr)
        type2 = self.visit(node.limit)
        if type1 == "int" and type2 == "int":
            self.symbol_table.push_scope("loop")
            self.symbol_table.put(node.id.name, type1)
            self.visit(node.instr)
            self.symbol_table.pop_scope()
        else:
            print("Error at line {0}: For loop's range must be integers ".format(node.line))

    def visit_Matrix(self, node):
        rows_count = len(node.mat)
        row_len = len(node.mat[0])
        m_type = self.visit(node.mat[0][0])

        for row in node.mat:
            if len(row) != row_len:
                print("Error at line {0}: Matrix rows must have the same length ".format(node.line))
            for element in row:
                if self.visit(element) != m_type:
                    print("Error at line {0}: Matrix elements must be of the same type".format(node.line))

        return VectorType(width=row_len, height=rows_count, type=m_type)

    def visit_Scope(self, node):
        self.symbol_table.push_scope("scope")
        for inst in node.instr:
            self.visit(inst)
        self.symbol_table.pop_scope()

    def visit_BreakStatement(self, node):
        loop_scope = self.symbol_table.get_scope("loop")
        if loop_scope is None:
            print("Error at line {0}: Break ouside of loop scope".format(node.line))

    def visit_ContinueStatement(self, node):
        loop_scope = self.symbol_table.get_scope("loop")
        if loop_scope is None:
            print("Error at line {0}: Continue ouside of loop scope".format(node.line))

    def visit_ReturnStatement(self, node):
        self.visit(node.value)

    def visit_Uminus(self, node):
        return self.visit(node.expr)

    def visit_Variable(self, node):
        var = self.symbol_table.get(node.name)
        if var is not None:
            return var.type
        else:
            print("Error at line {0}: Variable {1} undeclared".format(node.line, node.name))
            return None

    def visit_Transposition(self, node):
        type1 = self.visit(node.mat)
        if isinstance(type1, VectorType):
            return VectorType(width=type1.height, height=type1.width, type=type1)
        else:
            print("Error at line {0}: Can only transpose matrix".format(node.line))
            return None

    def visit_Gen(self, node):
        type1 = self.visit(node.arg)
        if type1 == "int":
            size = node.arg.value
            return VectorType(width=size, height=size, type=type1)
        else:
            print("Error at line {0}: Function {1} argument must be int".format(node.line, node.func))
            return None

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_String(self, node):
        return "str"