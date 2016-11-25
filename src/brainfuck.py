#!/usr/bin/python
import sys, getch

def execute_program(code, braces, cells=30000, aCells=[0], p=0):
	instr_pointer = 0

	while instr_pointer < len(code):
		command = code[instr_pointer]

		if command == "+":	aCells[p] += 1 if aCells[p] < 255 else 0
		elif command == "-": aCells[p] -= 1 if aCells[p] > 0 else 0
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
		elif command == ".": sys.stdout.write(chr(aCells[p]))
		elif command == ",": aCells[p] = ord(getch.getch())
		elif command == "[":
			if aCells[p] == 0:
				instr_pointer = braces[instr_pointer] 
		elif command == "]":
			if aCells[p] != 0:
				instr_pointer = braces[instr_pointer] 
		instr_pointer += 1
	return (aCells, p)

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



#######   DEBUGGING LOGIC   #######

def execute_program_debug(code, braces, cells=30000, aCells=[0], p=0):
	final_output = ""
	instr_pointer = 0

	while instr_pointer < len(code):
		command = code[instr_pointer]

		if command == "+":	
			print "Incremented cell number"
			aCells[p] += 1 if aCells[p] < 255 else 0
		elif command == "-": 
			print "Decremented cell number"
			aCells[p] -= 1 if aCells[p] > 0 else 0
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
			final_output += (chr(aCells[p]))
			print "Printing character: %s" % (chr(aCells[p]))
		elif command == ",": 
			aCells[p] = ord(getch.getch())
			print "Got character: %s, ascii value: %d" % (chr(aCells[p]) if aCells[p] != 13 else "line-break", aCells[p])
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
		print_status(aCells,p)
	return (aCells, p, "Program output: %s" % final_output)

def getLength(number):
	number /= 10
	if number != 0:
		return 1 + getLength(number)
	return 1

def print_status(aCells, p):
	print aCells
	jumps = 1 + 2*p + sum(map(getLength, aCells[0:p]))
	print " " * jumps + "^"

###################################################


def start(file, cells, debug):
	content = list()

	with open(file) as f: content = filter(lambda x: x in ["+", "-", "<", ">", ".", ",", "[", "]"], f.read())

	if debug:
		print "### Program %s ###" % file
		print execute_program_debug(content, get_braces(content), cells)[2]
	else:
		execute_program(content, get_braces(content), cells)


def interpreter():
	import signal
	def signal_handler(signal, frame):
		print ""
		sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	prompt = "bf> "
	print "### Brainfuck interpreter ###"
	print "Type 'exit' to exit"
	code = raw_input(prompt).replace(" ", "")
	cells = [0]
	pointer = 0
	while code != "exit":
		error = False
		for i in range(len(code)):
			if code[i] not in ["+", "-", "<", ">", ".", ",", "[", "]"]:
				print ""
				print "\t" + str(code[0:i+1])
				print "\t" + " " * i + "^"
				print ""
				print "Syntax Error: character not valid! column: %d" % i
				error = True
				break
		if not error:
			result = execute_program(code, get_braces(code), aCells=cells, p=pointer)
			print ""
			cells = result[0]
			pointer = result[1]
			print_status(cells, pointer)
		code = raw_input(prompt).replace(" ", "")


if __name__ == "__main__": 

	if len(sys.argv) == 1:
		interpreter()
	else:
		help_message = """ Usage: 
	Interactive: brainfuck
	Interpreter: brainfuck [-d] [-l <cell-limit>] filename.bf
		-d: Debug program. Show every step
		-l <cell-limit>: Limit number of cells to <cell-limit>. Default is 30000"""

		if not (len(sys.argv) >= 2 and len(sys.argv) <= 5) :
			print help_message
			sys.exit(1)

		cell_limit = 30000
		debug = False

		if "--help" in sys.argv:
			print help_message
			sys.exit(0)
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