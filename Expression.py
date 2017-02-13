from Constants import *
from MathExpression import *
from termcolor import colored
from AssignmentExpression import *
from LogicalExpression import *

class Expression:

    mathop_arr = [Constants.CONST_OP_PLUS,
                  Constants.CONST_OP_MINUS,
                  Constants.CONST_ASTERISK,
                  Constants.CONST_OP_DIV,
                  Constants.CONST_PERCENTAGE]
    logic_arr = [Constants.CONST_LOGIC_NOTEQUAL,
                 Constants.CONST_LOGIC_LESSTHANEQ,
                 Constants.CONST_LOGIC_EQUAL,
                 Constants.CONST_LOGIC_GREATERTHANEQ,
                 Constants.CONST_LESS_THAN,
                 Constants.CONST_GREATER_THAN,
                 Constants.CONST_AND,
                 Constants.CONST_OR]

    def __init__(self):
        self.items = []

    def evaluate(self, tokens, actual, varmap):
        result = True
        if len(tokens) > 2:
            exprtype = tokens[1]
            if exprtype != Constants.CONST_EQ:
                print(colored("'=' token expected", 'red'))
                result = False
        if result:
            mathOp = set(tokens).intersection(set(self.mathop_arr))
            if len(mathOp) >= 1:
                #print('mathexpr')
                me = MathExpression()
                result = me.checksyntax(tokens, actual)
                if result:
                    result, varmap = me.evaluate(tokens, actual, varmap)
            else:
                logicOp = set(tokens).intersection(set(self.logic_arr))
                if len(logicOp) >= 1:
                    #print('Logic')
                    l = LogicalExpression()
                    result = l.checksyntax(tokens, actual)
                    #print("Logic", result)
                    if result:
                        result, varmap = l.evaluate(tokens, actual, varmap)
                else:
                    #print('Assign')
                    a = AssignmentExpression()
                    result = a.checksyntax(tokens, actual)
                    if result:
                        result, varmap = a.evaluate(tokens, actual, varmap)
        return result, varmap