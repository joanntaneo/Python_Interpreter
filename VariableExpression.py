import Expression
from Constants import *
import re
from termcolor import colored

class VariableExpression():
    var_states = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [2, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # ,
                  [0, 3, 0, 0, 0, 6, 0, 2, 0, 0],  # = or ,
                  [0, 0, 2, 4, 0, 6, 0, 3, 0, 0],  # , or number or type or =
                  [0, 0, 0, 0, 5, 0, 0, 4, 2, 0],  # AS or type
                  [0, 0, 2, 0, 0, 6, 0, 5, 0, 0],  # , or type or AS
                  [0, 0, 0, 0, 0, 0, 7, 6, 0, 0],  # space or type
                  [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 8, 0, 0]]

    char_arr = [Constants.CONST_VAR,
                Constants.CONST_VARIABLE,
                Constants.CONST_EQ,
                Constants.CONST_STRING_S,
                Constants.CONST_STRING_D,
                Constants.CONST_COMMA,
                Constants.CONST_AS,
                Constants.CONST_TYPE_CHAR]

    int_arr = [Constants.CONST_VAR,
               Constants.CONST_VARIABLE,
               Constants.CONST_EQ,
               Constants.CONST_INT,
               Constants.CONST_COMMA,
               Constants.CONST_AS,
               Constants.CONST_TYPE_INT]

    float_arr = [Constants.CONST_VAR,
                 Constants.CONST_VARIABLE,
                 Constants.CONST_EQ,
                 Constants.CONST_FLOAT,
                 Constants.CONST_INT,
                 Constants.CONST_COMMA,
                 Constants.CONST_AS,
                 Constants.CONST_TYPE_FLOAT]

    bool_arr = [ Constants.CONST_VAR,
                 Constants.CONST_VARIABLE,
                 Constants.CONST_EQ,
                 Constants.CONST_BOOL_FALSE,
                 Constants.CONST_BOOL_TRUE,
                 Constants.CONST_COMMA,
                 Constants.CONST_AS,
                 Constants.CONST_TYPE_BOOL]

    def __init__(self):
        self.values = []
        self.vartype = 0

    def checksyntax(self, tokens):
        state = 1  # starting state
        for token in tokens:
            prev = state
            curr = self.getCode(token)
            #print("Token:", token, " Code:", curr, " State:", state)
            state = self.var_states[state][curr]
            #print("-----> [", prev, "][", curr, "]=", state)
        #print("valid" if state == 7 else "not valid")
        if state == 7:
            return True
        else:
            return False

    def getCode(self, token):
        if token == Constants.CONST_VAR:
            return 0
        elif token == Constants.CONST_SPACE:
            return 7
        elif token == Constants.CONST_AS:
            return 5
        elif token == Constants.CONST_COMMA:
            return 2
        elif token == Constants.CONST_EQ:
            return 3
        elif (token == Constants.CONST_TYPE_INT or
              token == Constants.CONST_TYPE_FLOAT or
              token == Constants.CONST_TYPE_CHAR or
              token == Constants.CONST_TYPE_BOOL):
            return 6
        elif token == Constants.CONST_VARIABLE:
            return 1
        elif (token == Constants.CONST_INT or
              token == Constants.CONST_FLOAT or
              token == Constants.CONST_STRING_S):
            return 4
        elif (token == Constants.CONST_BOOL_TRUE or
              token == Constants.CONST_BOOL_FALSE):
            return 8
        else:
            return 9

    def evaluate(self, token):
        result = True
        if Constants.CONST_TYPE_INT in token:
            res = set(token) - set(self.int_arr);
            if len(res) > 0:
                print(colored("Unexpected VAR token of type INT ", 'red'))
                result = False
            else:
                self.vartype = Constants.CONST_TYPE_INT

        elif Constants.CONST_TYPE_FLOAT in token:
            res = set(token) - set(self.float_arr);
            if len(res) > 0:
                print(colored("Unexpected VAR token of type FLOAT ", 'red'))
                result = False
            else:
                self.vartype = Constants.CONST_TYPE_FLOAT

        elif Constants.CONST_TYPE_CHAR in token:
            res = set(token) - set(self.char_arr);
            if len(res) > 0:
                print(colored("Unexpected VAR token of type CHAR ", 'red'))
                result = False
            else:
                self.vartype = Constants.CONST_TYPE_CHAR

        elif Constants.CONST_TYPE_BOOL in token:
            res = set(token) - set(self.bool_arr);
            if len(res) > 0:
                print(colored("Unexpected VAR token of type BOOL ", 'red'))
                result = False
            else:
                self.vartype = Constants.CONST_TYPE_BOOL

        #print("evaluate ", result)
        return result

    def getValues(self, token, actualtoken):
        indices = [i for i, x in enumerate(token) if x == Constants.CONST_VARIABLE]
        #print("indices ", indices)
        ctr = 0
        for idx in indices:
            if token[idx + 1] == Constants.CONST_EQ:
                #print("[",  actualtoken[idx], "][", actualtoken[idx + 2] , "]")
                if self.vartype == Constants.CONST_TYPE_BOOL:
                    if Constants.CONST_BOOL_TRUE == token[idx + 2] :
                        self.values.insert(ctr,[actualtoken[idx], True])
                    else:
                        self.values.insert(ctr, [actualtoken[idx], False])
                elif self.vartype == Constants.CONST_TYPE_INT:
                    self.values.insert(ctr, [actualtoken[idx], int(actualtoken[idx + 2])])
                elif self.vartype == Constants.CONST_TYPE_FLOAT:
                    self.values.insert(ctr, [actualtoken[idx], float(actualtoken[idx + 2])])
                else:
                    self.values.insert(ctr, [actualtoken[idx], re.sub('\'', '', actualtoken[idx + 2])])
            else:
                #print(actualtoken[idx], ctr)
                if self.vartype == Constants.CONST_TYPE_INT or Constants.CONST_TYPE_FLOAT:
                    self.values.insert(ctr, [actualtoken[idx], 0])
                elif self.vartype == Constants.CONST_TYPE_BOOL:
                    self.values.insert(ctr, [actualtoken[idx], False])
                elif self.vartype == Constants.CONST_TYPE_CHAR:
                    self.values.insert(ctr,  [actualtoken[idx], ''])
            ctr += 1