
#!/usr/bin/python
from Interpreter import Interpreter

f = open('CFPL.txt', "r")
lines = f.readlines()
f.close()
i = Interpreter()
i.execute(lines)