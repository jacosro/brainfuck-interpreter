#!/usr/bin/python
import sys, getch

def execute_program(code, braces, cells):
	aCells = [0]
	p = 0

	instr_pointer = 0

	while instr_pointer < len(code):
		command = code[instr_pointer]

		if command == "+":	aCells[p] += 1
		elif command == "-": aCells[p] -= 1
		elif command == "<":
			p -= 1
			if p < 0:
				if len(aCells) >= cells:
					print "Reached cells limit: " + str(cells)
					sys.exit(1)
				aCells.insert(0, 0)
				p = 0
		elif command == ">":
			p += 1
			if p == len(aCells):
				if len(aCells) >= cells:
					print "Reached cells limit: " + str(cells)
					sys.exit(1)
				aCells.append(0)
		elif command == ".": sys.stdout.write(chr(aCells[p] % 256))
		elif command == ",": aCells[p] = ord(getch.getch())
		elif command == "[":
			if aCells[p] == 0:
				instr_pointer = braces[instr_pointer] 
		elif command == "]":
			if aCells[p] != 0:
				instr_pointer = braces[instr_pointer] 
		instr_pointer += 1

def get_braces(code):
	stack = list()
	final = dict()

	ordered = zip(code, range(len(code)))

	braces_position = filter(lambda (x,y): x in ["[","]"], ordered)

	for command, position in braces_position:
		if command == "[":
			stack.append(position)
		else:
			startBrace = stack.pop()
			final[startBrace] = position
			final[position] = startBrace
	return final



#######   DEBUGGING LOGIC  #######

def execute_program_debug(code, braces, cells):
	final_output = ""

	aCells = [0]
	p = 0

	instr_pointer = 0

	while instr_pointer < len(code):
		command = code[instr_pointer]

		if command == "+":	
			aCells[p] += 1
			print "Incremented cell number"
		elif command == "-": 
			aCells[p] -= 1
			print "Decremented cell number"
		elif command == "<":
			p -= 1
			print "Pointer to left"
			if p < 0:
				if len(aCells) >= cells:
					print "Reached cells limit: " + str(cells)
					sys.exit(1)
				aCells.insert(0, 0)
				p = 0
		elif command == ">":
			p += 1
			print "Pointer to right"
			if p == len(aCells):
				if len(aCells) >= cells:
					print "Reached cells limit: " + str(cells)
					sys.exit(1)
				aCells.append(0)
		elif command == ".": 
			final_output += (chr(aCells[p] % 256))
			print "Printing character: %s" % (chr(aCells[p] % 256))
		elif command == ",": 
			aCells[p] = ord(getch.getch())
			print "Got character: %s, ascii value: %d" % (chr(aCells[p]), aCells[p])
		elif command == "[":
			print "Entering loop on position: should we do it?",
			if aCells[p] == 0:
				print "No, jumping to the end"
				instr_pointer = braces[instr_pointer] 
			else:
				print "Yes, execute it"
		elif command == "]":
			print "Closing loop, does it end? ",
			if aCells[p] != 0:
				print "It does not end, jumping to the start" 
				instr_pointer = braces[instr_pointer] 
			else:
				print "It ends, continue program."
		instr_pointer += 1
		print aCells
		print_pointer(aCells,p)
	return final_output

def getLength(number):
	number /= 10
	if number != 0:
		return 1 + getLength(number)
	return 1

def print_pointer(aCells, p):
	jumps = 1 + 2*p + sum(map(getLength, aCells[0:p]))
	print " " * jumps + "^"

###################################################


def start(file, cells, debug):
	content = list()

	with open(file) as f: content = filter(lambda x: x in ["+", "-", "<", ">", ".", ",", "[", "]"], f.read())

	if debug:
		print "### Program %s ###" % file
		print execute_program_debug(content, get_braces(content), cells)
	else:
		execute_program(content, get_braces(content), cells)

if __name__ == "__main__": 

	help_message = """ Usage: brainfuck [-d] [-l cell-limit] filename.bf
		-d: Debug program. Show every step
		-l number_of_cells: Limit number of cells to number_of_cells. Default is 30000"""

	if not (len(sys.argv) >= 2 and len(sys.argv) <= 5) :
		print help_message
		sys.exit(1)

	cell_limit = 30000
	debug = False

	if "-d" in sys.argv:
		debug = True
	if "-l" in sys.argv:
		index = sys.argv.index("-l") + 1
		if len(sys.argv) <= index:
			print help_message
			sys.exit(1)
		try:
			cell_limit = int(sys.argv[index])
		except ValueError:
			print help_message
			sys.exit(1)

	file = sys.argv.pop()

	if not (file.endswith(".b") or file.endswith(".bf")):
		print "The file must be a brainfuck (*.b/*.bf) program"
		sys.exit(1)

	start(file, cell_limit, debug)