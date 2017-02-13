from Constants import *
import re
from termcolor import colored
from LexAnalyzer import *

class LogicalExpression:
    arth_arr = [Constants.CONST_LOGIC_NOTEQUAL,
                  Constants.CONST_LOGIC_LESSTHANEQ,
                  Constants.CONST_LOGIC_EQUAL,
                  Constants.CONST_LOGIC_GREATERTHANEQ,
                  Constants.CONST_LESS_THAN,
                  Constants.CONST_GREATER_THAN]
    log_arr = [Constants.CONST_AND,
			   Constants.CONST_OR]

    expr_arr = [[	0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	],
                [	2	,	0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	],
                [	0	,	3	,	0	,	0	,	0	,	0	,	0	,	0	,	0	],
                [	4	,	0	,	3	,	0	,	0	,	4	,	0	,	3	,	0	],
                [	0	,	0	,	0	,	4	,	5	,	0	,	6	,	0	,	0	],
                [	4	,	0	,	0	,	0	,	0	,	4	,	6	,	0	,	0	],
                [	4	,	0	,	3	,	0	,	0	,	4	,	0	,	4	,	0	],
                [	0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	],
                [	0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	,	0	]]

    unidentified = 8

    def __init__(self):
        self.value = 0

    def checksyntax(self, tokens, actual):
        #print(tokens)
        state = 1
        idx = 0
        parenCtr = 0
        for token in tokens:
            prev = state
            curr = self.getCode(token)
            if curr == self.unidentified:
                state = 0
                parenCtr = 0
                print(colored('Unexpected token %s' % actual[idx], 'red'))
                break
            if token == Constants.CONST_OPEN_PAREN:
                parenCtr += 1
            elif token == Constants.CONST_CLOSE_PAREN:
                parenCtr -= 1
            #print(actual[idx], "Token:", token, " Code:", curr, " State:", state)
            state = self.expr_arr[state][curr]
            #print(token,actual[idx], "-----> [", prev, "][", curr, "]=", state)
            idx += 1
        #print('parenCtr: ', parenCtr)
        if parenCtr > 0:
            print(colored('Missing )', 'red'))
            state = 0
        elif parenCtr < 0:
            print(colored('Unexpected )', 'red'))
            state = 0
        if state == 4:
            return True
        else:
            return False

    def getCode(self, token):
        if token == Constants.CONST_OPEN_PAREN:
            return 2
        elif token == Constants.CONST_CLOSE_PAREN:
            return 3
        elif token == Constants.CONST_VARIABLE:
            return 0
        elif (token == Constants.CONST_STRING_D or
				    token == Constants.CONST_STRING_S or
				    token == Constants.CONST_INT or
				    token == Constants.CONST_FLOAT):
            return 5
        elif token in self.arth_arr:
            return 4
        elif token in self.log_arr:
            return 6
        elif token == Constants.CONST_NOT:
            return 7
        elif token == Constants.CONST_EQ:
            return 1
        else:
            return 8

    def evaluate(self, token, actualtoken, varmap):
        # check if all variables are of the same type
        result = True
        vartype = 0
        var = varmap.get(actualtoken[0])
        if var != None and len(var) >= 2:
            vartype = var[1]
            # print(actualtoken[idx], idx, var, var[1], len(var))
            if vartype != Constants.CONST_TYPE_BOOL:
                print(colored("Data type of variable %s should be BOOL" % actualtoken[0], 'red'))
                result = False
        else:
            print(colored("Undefined variable %s " % actualtoken[0], 'red'))
            result = False
        #print("evaluate", vartype)
        if result:
            stack = self.infixToPostfix(token, actualtoken)
            #print("infix:", stack)
            result, val = self.assess(stack, varmap, vartype)
            #print("calculate: ", val)
            var = varmap.get(actualtoken[0])
            var[0] = val
            varmap[actualtoken[0]] = var
            #print(varmap)
        return result, varmap

    def infixToPostfix(self, tokenList, actualtoken):
        prec = {}
        prec["NOT"] = 2
        prec["OR"] = 2
        prec["AND"] = 2
        prec["<>"] = 3
        prec["=="] = 3
        prec[">="] = 3
        prec["<="] = 3
        prec["<"] = 3
        prec[">"] = 3
        prec["("] = 1
        opStack = []
        postfixList = []
        idx = 0
        for token in tokenList:
            if idx == 0:
                idx += 1
                continue
            elif (token == Constants.CONST_VARIABLE
                or token == Constants.CONST_INT or
                token == Constants.CONST_FLOAT):
                postfixList.append(actualtoken[idx])
            elif token == Constants.CONST_OPEN_PAREN:
                opStack.append(actualtoken[idx])
            elif token == Constants.CONST_CLOSE_PAREN:
                topToken = opStack.pop()
                while topToken != '(':
                    postfixList.append(topToken)
                    topToken = opStack.pop()
            elif token == Constants.CONST_EQ:
                idx += 1
                continue
            else:
                while (not len(opStack) == 0) and \
                (prec[opStack[len(opStack)-1]] >= prec[actualtoken[idx]]):
                    postfixList.append(opStack.pop())
                opStack.append(actualtoken[idx])
            idx += 1
        #print(opStack)
        while not len(opStack) == 0:
            postfixList.append(opStack.pop())
        return postfixList #" ".join(postfixList)

    def translateNumericValue(self, val, type):
        result = True
        if type == Constants.CONST_INT:
            return True, int(val)
        elif type == Constants.CONST_FLOAT:
            return True, float(val)
        else:
            print(colored("%s should be of INT/FLOAT type", 'red'))
            return False, False

    def examinemathvar(self, varmap, left, right, operator):
        result = True
        val = False
        if operator == '<':
            val = left < right
        elif operator == '>':
            val = left > right
        elif operator == '<=':
            val = left <= right
        elif operator == '>=':
            val = left >= right
        elif operator == '==':
            val = left == right
        elif operator == '<>':
            val = left != right
        return result, val

    def examinelogvar(self, varmap, left, right, operator):
        result = True
        val = False
        if operator == 'AND':
            val = left and right
        elif operator == 'OR':
            val = left or right
        else:
            val = False
        return result, val

    def assess(self, stack, varmap, vartype):
        ari_arr = ['<', '>', '<=', '>=', '==', '<>']
        log_arr = ['AND', 'OR']
        values = []
        idx = 0
        result = True
        #print(varmap)
        for token in stack:
            #print("token: [", idx, "] ", token)
            if token in ari_arr:
                right = values.pop()
                left = values.pop()
                #print('token', left, token, right)
                result, val = self.examinemathvar(varmap, left, right, token)
                #print(result, 'arithmetic: ', left, token, right, val)
                values.append(val)
                #print('values: ', values)
            elif token in log_arr:
                right = values.pop()
                left = values.pop()
                if isinstance(left, bool) and isinstance(right, bool):
                    result, val = self.examinelogvar(varmap, left, right, token)
                    #print(result, 'and/or: ', left, token, right, val)
                    values.append(val)
                else:
                    print(colored("Data type of variables for logical operator(ANd/OR) should be BOOL", 'red'))
                    result = False
            elif token == 'NOT':
                left = values.pop()
                if isinstance(left, bool):
                    val = not left
                    values.append(val)
                    #print(result, 'not: ', left, token, val)
                else:
                    print(colored("Data type of variables for logical operator(NOT) should be BOOL", 'red'))
                    result = False
            else:
                var = varmap.get(token)
                if var != None:
                    values.append(var[0])
                else:
                    l = LexAnalyzer()
                    type = l.checktoken(token)
                    result, val = self.translateNumericValue(token, type)
                    values.append(val)
                #print('values: ', values)
            idx += 1
            if not result:
                break
        return result, values[0]