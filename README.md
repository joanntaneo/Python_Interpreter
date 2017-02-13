# Python_Interpreter
Simple Program Interpreter using Python

> CFPL.txt - Sample file to be interpreted
> Main.py - Starting point of the program. Reads the file to be processed eg. CFPL.txt
> Interpreter.py - runs the lexical analyzer and executes the file
> LexAnalyzer.py - breaks syntaxes to tokens
> Constants.py - contains all the constants used e.g tokens
> VariableExpression.py - processes and evaluates variable expression 
  e.g VAR abc, b, c AS INT
      VAR d=”FALSE” AS BOOL
> MathExpression.py - processes and evaluate mathematical expression 
  e.g abc = b + 10
> OutputExpression.py - processes and evaluates output expresion 
  e.g OUTPUT: abc & “hi” & b 
> AssignmentExpression.py - processes and evaluates assignment expression
  e.g c = 100
> LogicalExpression.py - processes and evaluates logical expression 
  e.g d = (a < b AND c <> 200)
> Expression.py - evaluates whether the expression is mathematical or logical or an assignment
      


