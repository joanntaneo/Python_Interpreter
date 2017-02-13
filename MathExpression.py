from Constants import *
import re
from termcolor import colored

class MathExpression:
    mathop_arr = [Constants.CONST_OP_PLUS,
                  Constants.CONST_OP_MINUS,
                  Constants.CONST_ASTERISK,
                  Constants.CONST_OP_DIV,
			      Constants.CONST_PERCENTAGE]

    expr_arr = [[	0	,	0	,	0	,	0	,	0	,	0 ],
                [	2	,	0	,	0	,	0	,	0	,	0 ],
                [	0	,	3	,	0	,	0	,	0	,	0 ],
                [	4	,	0	,	3	,	0	,	0	,	4 ],
                [	0	,	0	,	0	,	4	,	5	,	0 ],
                [	4	,	0	,	3	,	0	,	0	,	4 ]]

    unidentified = 6

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
            #print("-----> [", prev, "][", curr, "]=", state)
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

    def evaluate(self, token, actualtoken, varmap):
        # check if all variables are of the same type
        indices = [i for i, x in enumerate(token) if x == Constants.CONST_VARIABLE]
        vartype = 0
        result = True
        #print(indices)
        vartype = 0
        for idx in indices:
            #print(idx)
            var = varmap.get(actualtoken[idx])
            if var != None and len(var) >= 2:
                #print(actualtoken[idx], idx, var, var[1], len(var))
                if vartype == 0:
                    vartype = var[1]
                elif vartype != var[1]:
                    print(colored("Data type mismatch for variable %s" % actualtoken[idx], 'red'))
                    result = False
                    break
            else:
                print(colored("Undefined variable  %s" % actualtoken[idx], 'red'))
                result = False
                break
        if result:
            stack = self.infixToPostfix(token, actualtoken)
            #print("infix:", stack)
            val = self.calculate(stack, varmap, vartype)
            #print("calculate: ", val)
            var = varmap.get(actualtoken[0])
            var[0] = val
            varmap[actualtoken[0]] = var
            #print(varmap)
        return result, varmap

    def calculate(self, stack, varmap, vartype):
        values = []
        idx = 0
        #print(varmap)
        for token in stack:
            #print("token: [", idx, "] ", token)
            if token in ['+', '-', '*', '/', '%']:
                right = values.pop()
                left = values.pop()
                #print('token', left, token, right)
                if token == '+':
                    val = left + right
                elif token == '-':
                    val = left - right
                elif token == '*':
                    val = left * right
                elif token == '/':
                    val = left / right
                elif token == '%':
                    val = left % right
                    #print('mod: ', left, token, right)
                values.append(val)
                #print('values: ', values)
            else:
                val = varmap.get(token)[0] if varmap.get(token) else token
                if vartype == Constants.CONST_TYPE_INT:
                    val = int(val)
                elif vartype ==Constants.CONST_TYPE_FLOAT:
                    val = float(val)
                values.append(val)
                #print('values: ', values)
            idx += 1
        return values[0]


    def getCode(self, token):
        if token == Constants.CONST_OPEN_PAREN:
            return 2
        if token == Constants.CONST_CLOSE_PAREN:
            return 3
        elif token == Constants.CONST_VARIABLE:
            return 0
        elif (token == Constants.CONST_STRING_D or
              token == Constants.CONST_STRING_S or
              token == Constants.CONST_INT or
              token == Constants.CONST_FLOAT):
            return 5
        elif token in self.mathop_arr:
            return 4
        elif token == Constants.CONST_EQ:
            return 1
        else:
            return 6

    def infixToPostfix(self, tokenList, actualtoken):
        prec = {}
        prec["*"] = 3
        prec["/"] = 3
        prec["%"] = 3
        prec["+"] = 2
        prec["-"] = 2
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