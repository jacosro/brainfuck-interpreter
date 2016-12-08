#!/usr/bin/python
import sys, getch

def execute_program(code, braces, cells=30000, aCells=[0], p=0):
    instr_pointer = 0

    while instr_pointer < len(code):
        command = code[instr_pointer]

        if command == "+": aCells[p] += 1 if aCells[p] < 255 else 0
        elif command == "-": aCells[p] -= 1 if aCells[p] > 0 else 0
        elif command == "<":
            p -= 1
            if len(aCells) >= cells:
                print "Reached cells limit: " + str(cells)
                print "Last state:"
                print aCells
                sys.exit(1)
            if p < 0: 
                aCells.insert(0, 0)
                p = 0
        elif command == ">":
            p += 1
            if len(aCells) >= cells:
                print "Reached cells limit: " + str(cells)
                print "Last state:"
                print aCells
                sys.exit(1)
            if p == len(aCells): aCells.append(0)
        elif command == ".": sys.stdout.write(chr(aCells[p]))
        elif command == ",": aCells[p] = ord(getch.getch())
        elif command == "[":
            if aCells[p] == 0:
                instr_pointer = braces[instr_pointer] 
        else:
            if aCells[p] != 0:
                instr_pointer = braces[instr_pointer] 
        instr_pointer += 1
    return (aCells, p)

def get_braces(code):
    stack = list()
    final = dict()

    for index in range(0, len(code)):
        if code[index] == "[":
            stack.append(index)
        elif code[index] == "]":
            startBrace = stack.pop()
            final[startBrace] = index
            final[index] = startBrace
        index += 1
    return final



#######   DEBUGGING LOGIC   #######

def execute_program_debug(code, braces, cells=30000, aCells=[0], p=0):
    final_output = ""
    instr_pointer = 0

    while instr_pointer < len(code):
        command = code[instr_pointer]
        
        if command == ".": 
            print "Printing character: %s" % (chr(aCells[p]) if aCells[p] != 13 else "line-break")
            final_output += chr(aCells[p])
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
        else:
            aCells, p = execute_program([command], braces, cells, aCells, p)

            if command == "+": print "Incremented cell number"
            elif command == "-": print "Decremented cell number"
            elif command == "<": print "Pointer to left"
            elif command == ">": print "Pointer to right"
            elif command == ",": print "Got character: %s, ascii value: %d" % (chr(aCells[p]) if aCells[p] != 13 else "line-break", aCells[p])
        
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

    try:
        with open(file) as f: content = filter(lambda x: x in ["+", "-", "<", ">", ".", ",", "[", "]"], f.read())
    except IOError:
        print "Could not open file: %s" % file
        sys.exit(1)

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
        if code == "help":
            print "help: Shows help\nreset: Resets cells and pointer\nexit: Exit"
        elif code == "reset":
            cells = [0]
            pointer = 0
            print_status(cells, pointer)
        else:
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
                cells, pointer = execute_program(code, get_braces(code), aCells=cells, p=pointer)
                print ""
                print_status(cells, pointer)
        code = raw_input(prompt).replace(" ", "")


if __name__ == "__main__": 
    if len(sys.argv) == 1:
        interpreter()
    else:
        import argparse
        # brainfuck.py [-v] [-c cells] [-o output_file] file.bf
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", action="store_true", help="Verbosing")
        parser.add_argument("-c", "--cells", action="store", dest="cells", type=int, help="Cell limit")
        parser.add_argument("-o", "--output_file", action="store", dest="output_file", type=str, help="Output file")
        parser.add_argument("file", action="store", help="The brainfuck file (*.b/*.bf)")
        args = parser.parse_args()

        cell_limit = 30000
        file = args.file

        if not (file.endswith(".b") or file.endswith(".bf")):
            print "The file must be a brainfuck (*.b/*.bf) program"
            sys.exit(1)

        if args.cells:
            cell_limit = args.cells
        if args.output_file:
            sys.stdout = open(args.output_file, 'w')

        start(file, cell_limit, args.verbose)
