import os
import re

f = open("C:/Users/rlau0/Documents/Projects/yts/YTS.py")

f = open(r"C:\Users\rlau0\Documents\Projects\Drone\PiStuffing\Quadcopter.py")
lines_after = 0
lines_before = 0

lines = f.readlines()
print("#"*10,"list comprehension(class or functions)")
deflines = [line for line in lines if "def " in line or "class " in line]
for defline in deflines:
	print(defline)

print("#"*10,"loop conditional(functions)")
for i,line in enumerate(lines):	
	if "def " in line:
		print("\n")
		for context_line in reversed(range(lines_before)):
			print((i-context_line-1),":",lines[i-context_line-1],end="")
		print("*",i,":",line,end="")
		for context_line in range(lines_after):
			print((i+context_line+1),":",lines[i+context_line+1],end="")

print("#"*10,"list regex(functions)")

for i,line in enumerate(lines):	
	if "def " in line:
		print("*",i,":",re.split("\s",line)[1])

f.close

