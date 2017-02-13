from Constants import *
import re
from termcolor import colored


class AssignmentExpression:
	expr_arr = [[	0	,	0	,	4	,	0	],
				[	2	,	0	,	0	,	0	],
				[	0	,	3	,	0	,	0	],
				[	4	,	0	,	4	,	0	],
				[	0	,	0	,	0	,	0	]]

	def __init__(self):
		self.value = 0


	def checksyntax(self, tokens, actual):
		# print(tokens)
		state = 1
		idx = 0
		parenCtr = 0
		for token in tokens:
			prev = state
			curr = self.getCode(token)
			# print(actual[idx], "Token:", token, " Code:", curr, " State:", state)
			state = self.expr_arr[state][curr]
			#print("-----> [", prev, "][", curr, "]=", state)
			idx += 1
		if state == 4:
			return True
		else:
			return False

	def getCode(self, token):
		if token == Constants.CONST_VARIABLE:
			return 0
		elif (token == Constants.CONST_STRING_D or
					  token == Constants.CONST_STRING_S or
					  token == Constants.CONST_INT or
					  token == Constants.CONST_FLOAT or
			  		  token == Constants.CONST_BOOL_FALSE or
			  		  token == Constants.CONST_BOOL_TRUE):
			return 2
		elif token == Constants.CONST_EQ:
			return 1
		else:
			return 3

	def evaluate(self, tokens, actualtoken, varmap):
		vartype = 0
		result = True
		if len(actualtoken) > 2: #Will access index 3 the <variable> = <val/variable>
			variable = varmap.get(actualtoken[0])
			if variable == None:
				print(colored("Undefined variable ", actualtoken[0], 'red'))
				result = False
			else:
				vartype = variable[1]
		else:
			print(colored("Unable to evaluate expression ", 'red'))
			result = False

		if result:
			#get value of last token abc=b=10, get 10
			count = len(tokens)
			idx = count-1
			if tokens[idx] == Constants.CONST_VARIABLE:
				var, result = self.getVariableValue(actualtoken[idx], varmap, vartype)
				value = var[0]
			else:
				value, result = self.getValue(tokens[idx], actualtoken[idx], vartype)
		idx -= 1
		#print('AssignmentExpresion', value)
		if result:
			while idx >= 0:
				#print('[', idx, ']', tokens[idx])
				if tokens[idx] == Constants.CONST_EQ:
					idx -= 1
					continue;
				else:
					if tokens[idx] == Constants.CONST_VARIABLE:
						#print('AssignmentExpresion', actualtoken[idx])
						variable, result = self.getVariableValue(actualtoken[idx], varmap, vartype)
					if result:
						variable[0] = value
						varmap[actualtoken[idx]] = variable
				idx -= 1
		#print('AssignmentExpresion', result)
		return result, varmap

	def getValue(self, token, actualtoken, vartype):
		if vartype == Constants.CONST_TYPE_BOOL:
			if '\"TRUE\"' == actualtoken:
				return True, True
			elif '\"FALSE\"' == actualtoken:
				return False, True
			else:
				print(colored("Value not valid %s " % actualtoken, actualtoken, 'red'))
				return False, False
		elif vartype == Constants.CONST_TYPE_INT and token == Constants.CONST_INT:
			return int(actualtoken), True
		elif vartype == Constants.CONST_TYPE_FLOAT and token in [Constants.CONST_INT, Constants.CONST_FLOAT]:
			return float(actualtoken), True
		elif token in [Constants.CONST_STRING_D, Constants.CONST_STRING_S]:
			return re.sub('\'', '', actualtoken), True
		else:
			print(colored("Undefined data type for %s " % actualtoken, 'red'))
			return '', False

	def getVariableValue(self, varname, varmap, vartype):
		result = True
		value = None
		var = varmap.get(varname)
		if var != None and len(var) >= 2:
			# print(actualtoken[idx], idx, var, var[1], len(var))
			if vartype != var[1]:
				print(colored("Data type mismatch for variable ", varname, 'red'))
				result = False
		else:
			print(colored("Undefined variable ", varname, 'red'))
			result = False
		return var, result