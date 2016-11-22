#!/usr/bin/python
import sys, getch

mArray = [0, 0, 0, 0, 0, 0, 0]

p = 4

queue = []

def executeCommand(com):
	if com == "+":
		add()
	elif com == "-":
		sub()
	elif com == "<":
		left()
	elif com == ">":
		right()
	elif com == ".":
		out()
	elif com == ",":
		input()
	elif com == "[":
		doLoop()

def add():
	global mArray
	global p
	mArray[p] += 1

def sub():
	global mArray
	global p
	mArray[p] -= 1

def left():
	global mArray
	global p
	p -= 1
	if p < 0:
		raise Exception("Pointer pointing to pos -1!")

def right():
	global mArray
	global p
	p += 1
	if p == len(mArray):
		mArray.append(0)

def out():
	global mArray
	global p
	sys.stdout.write(chr(mArray[p]))

def input():
	global mArray
	global p
	mArray[p] = ord(getch.getch())



def doLoop():
	global mArray
	global p

	openCount = 1
	closeCount = 0

	loopList = ["["]
	stack = [0]

	braces = {}

	loopPointer = 1

	while closeCount < openCount:
		com = queue.pop()
		loopList.append(com)
		if com == "[":
			openCount += 1
			stack.append(loopPointer)
		elif com == "]":
			closeCount += 1
			startBrace = stack.pop()
			braces[startBrace] = loopPointer
			braces[loopPointer] = startBrace
		loopPointer += 1

	loopPointer = 0

	initialCell = p


	while mArray[initialCell] > 0:
		com = loopList[loopPointer]
		if com == "[":
			if mArray[p] == 0:
				loopPointer = braces[loopPointer] 
		elif com == "]":
			if mArray[p] != 0:
				loopPointer = braces[loopPointer] 
		else:
			executeCommand(com)
		loopPointer += 1



def start(file):
	global queue

	with open(file) as f:
		content = filter(lambda x: x in ["+", "-", "<", ">", ".", ",", "[", "]"], f.read())

		for s in content:
			queue.insert(0, s)

	# Start executing commands
	while len(queue) > 0:
		com = queue.pop()
		executeCommand(com)


if __name__ == "__main__": 
	if len(sys.argv) < 2:
		print "One file must be specified as argument"
		sys.exit(1)
	file = sys.argv[1]
	if not file.endswith(".b"):
		print "The file must be a brainfuck (*.b) program"
		sys.exit(1)

	start(file)
