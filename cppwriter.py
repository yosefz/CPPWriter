from sys import argv
from os.path import exists

script, header = argv

filename = header.split('.')[0]
filename += ".cpp"

input = open(header)
line = input.readline()
output = open(filename, 'w')

output.write("#include <" + header + ">\n")
classDef = ""
bracketCount = 0
privateFunc = False

while line:
	line = line.lstrip().rstrip()
	lineArray = line.split(' ')
	if lineArray[0] == "using":
		output.write("using namespace " + lineArray[2] + ";\n")
	elif lineArray[0] == "class":
		classDef = lineArray[1]
		bracketCount += 1
		if '}' in line:
			bracketCount -= 1
	elif lineArray[0] == "private:":
		privateFunc = True
	elif lineArray[0] == "public:":
		privateFunc = False
	elif lineArray[0] == "}":
		bracketCount -= 1
	elif privateFunc and lineArray[0] == classDef + "();":
		privateFunc = privateFunc
	elif line.find(" :") > 0: 
		while line.find("}") < 0:
			line = input.readline()
	elif '(' in line:
		line = line.replace(';', '')
		if privateFunc:
			output.write("private ")
		for current in lineArray:
			current = current.replace(';', '')
			if '(' in current:
				if bracketCount > 0:
					classDefDec = classDef + "::"
				else:
					classDefDec = ""

				if ')' in current:
					output.write(classDefDec + current)
				else:
					output.write(classDefDec + current + " ")
			else:
				output.write(current + " ")
		while True:
			if line.find(')') > 0:
				break
			else:
				line = input.readline()
			line = line.replace(';','')
			output.write("\n")
			output.write(line)


		output.write("{\n\n}\n\n")
	

	line = input.readline()

output.close()
input.close()
