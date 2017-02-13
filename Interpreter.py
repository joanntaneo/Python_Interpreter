from _ast import Expression

from Constants import *
from VariableExpression import *
from OutputExpression import *
from Expression import *
from LexAnalyzer import *
from termcolor import colored, cprint

class Interpreter:

    variables = {}
    hasStarted = False
    hasEnded = False

    def __init__(self):
        self.status = True

    def execute(self, lines):
        linectr = 0
        p = LexAnalyzer()
        for str in lines:
            linectr += 1
            str = str.rstrip("\n")
            if len(str.strip()) == 0:
                continue
            arrforlex = actual = []
            arrforlex, actual = p.parse(str)
            if arrforlex[0] == Constants.CONST_ERROR:
                arrforlex[1] = arrforlex[1] + ' at line %d ' % linectr
                print(colored(arrforlex[1] , 'red'))
                self.status = False
                break
            self.run(arrforlex, actual)
            if (not self.status):
                print(colored("Parse Error at line %d" % linectr, 'blue'))
                break
        if self.status and self.hasStarted and (not self.hasEnded):
            print(colored("Missing STOP expression", 'red'))

    def run(self, tokens, actual):
        statementtype = tokens[0]
        if statementtype == Constants.CONST_VAR:
            v = VariableExpression()
            if (v.checksyntax(tokens) and v.evaluate(tokens)):
                v.getValues(tokens, actual)
                for var in v.values:
                    self.variables[var[0]] = [var[1], v.vartype]
            else:
                print(colored("Variable declarion invalid", 'red'))
                self.status = False
        elif statementtype == Constants.CONST_START:
            if len(tokens) == 1 and not self.hasStarted and not self.hasEnded:
                self.hasStarted = True
            else:
                print(colored("Unexpected token(s) on START expression", 'red'))
                self.status = False
        elif statementtype == Constants.CONST_STOP:
            self.hasEnded = True
            if len(tokens) == 1 and self.hasStarted:
                self.hasEnded = True
            else:
                self.status = False
                print(colored("Unexpected token(s) on STOP expression", 'red'))

        elif statementtype == Constants.CONST_ASTERISK: #comment
            return
        elif statementtype == Constants.CONST_OUTPUT:
            if self.hasStarted:
                if (len(tokens) > 1):
                    o = OutputExpression()
                    if o.checksyntax(tokens):
                        o.print(tokens, actual, self.variables)
                else:
                    print(colored("Missing parameters for OUTPUT command", 'red'))
                    self.status = Constants.CONST_ERROR
            else:
                print(colored("Unexpected OUTPUT command"), 'red')
                self.status = False
        elif statementtype == Constants.CONST_VARIABLE:
            expr = Expression()
            self.status, self.variables = expr.evaluate(tokens, actual, self.variables)
        else:
            self.status = False
            print(colored("Unknown expression"), 'red')
        return self.status
