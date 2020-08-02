import sys
import traceback
import os
from typing import List
from collections import defaultdict

class Command:
    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"


class Segment:
    LOCAL = "local"
    ARGUMENT = "argument"
    THIS = "this"
    THAT = "that"
    CONSTANT = "constant"
    STATIC = "static"
    TEMP = "temp"
    POINTER = "pointer"


class Parser:
    def __init__(self, filename: str):
        super().__init__()
        self.lines: List[List[str]] = []
        self.curr_line = -1

        with open(filename, "r") as file:
            for line in file.readlines():
                cleaned = line.strip()
                if not cleaned:
                    continue
                if cleaned.startswith("//"):
                    continue

                removed_comment = cleaned.split("//")[0].strip()
                self.lines.append(removed_comment.split(" "))

    def has_more_commands(self):
        return self.curr_line < len(self.lines) - 1

    def advance(self):
        if not self.has_more_commands():
            raise Exception("No more commands left.")
        self.curr_line += 1

    def command_type(self):
        curr = self.lines[self.curr_line]
        command = curr[0]

        if command in ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"):
            return Command.C_ARITHMETIC
        if command == "pop":
            return Command.C_POP
        if command == "push":
            return Command.C_PUSH
        if command == "label":
            return Command.C_LABEL
        if command == "goto":
            return Command.C_GOTO
        if command == "if-goto":
            return Command.C_IF
        if command == "function":
            return Command.C_FUNCTION
        if command == "call":
            return Command.C_CALL
        if command == "return":
            return Command.C_RETURN
        raise Exception(f"Unsupported command type {command}")

    def arg_1(self):
        if self.command_type() == Command.C_RETURN:
            raise Exception("No arg1 for return command")
        curr = self.lines[self.curr_line]
        if self.command_type() == Command.C_ARITHMETIC:
            return curr[0]
        return curr[1]

    def arg_2(self):
        if self.command_type() not in (
            Command.C_PUSH,
            Command.C_POP,
            Command.C_FUNCTION,
            Command.C_CALL,
        ):
            raise Exception(f"No arg2 for {self.command_type()}")
        curr = self.lines[self.curr_line]
        return curr[2]


class CodeWriter:
    def __init__(self, filename: str):
        super().__init__()
        self.class_name = os.path.splitext(os.path.basename(filename))[0]
        self.file = open(filename, "w")
        self.label_count = 0
        self.ret_count_by_fn = defaultdict(int)

    def set_file_name(self, filename: str):
        self.class_name = os.path.splitext(os.path.basename(filename))[0]

    def close(self):
        self.file.close()

    def writeline(self, command: str):
        self.file.write(f"{command}\n")

    def write_arithmetic(self, command: str):
        self.writeline(f"// {command}")
        self.writeline(f"@SP")
        self.writeline(f"M=M-1")
        self.writeline(f"A=M")
        # Unary commands
        if command == 'neg':
            self.writeline(f"M=-M")
            # Increment stack pointer
            self.writeline(f"@SP")
            self.writeline(f"M=M+1")
            self.writeline(f"")
            return
        elif command == 'not':
            self.writeline('M=!M')
            # Increment stack pointer
            self.writeline(f"@SP")
            self.writeline(f"M=M+1")
            self.writeline(f"")
            return

        # Binary Commands
        self.writeline(f"D=M")
        # D contains the second arg
        self.writeline(f"@SP")
        self.writeline(f"M=M-1")
        self.writeline(f"A=M")
        if command == 'add':            
            self.writeline(f"M=D+M")
        elif command == 'sub':
            self.writeline(f"M=M-D")
        elif command == 'and':
            self.writeline(f"M=D&M")
        elif command == 'or':
            self.writeline(f"M=D|M")
        elif command == 'eq':
            else_label = f'LABEL{self.label_count}'
            end_label = f'LABEL{self.label_count + 1}'
            self.label_count += 2

            self.writeline(f"D=M-D")
            self.writeline(f"@{else_label}")
            self.writeline(f"D;JNE")
            self.writeline(f"@SP")
            self.writeline(f"A=M")
            self.writeline(f"M=-1")
            self.writeline(f"@{end_label}")
            self.writeline(f"0;JMP")
            self.writeline(f"({else_label})")
            self.writeline(f"@SP")
            self.writeline(f"A=M")
            self.writeline(f"M=0")
            self.writeline(f"({end_label})")
        elif command == 'gt':
            else_label = f'LABEL{self.label_count}'
            end_label = f'LABEL{self.label_count + 1}'
            self.label_count += 2

            self.writeline(f"D=M-D")
            self.writeline(f"@{else_label}")
            self.writeline(f"D;JLE")
            self.writeline(f"@SP")
            self.writeline(f"A=M")
            self.writeline(f"M=-1")
            self.writeline(f"@{end_label}")
            self.writeline(f"0;JMP")
            self.writeline(f"({else_label})")
            self.writeline(f"@SP")
            self.writeline(f"A=M")
            self.writeline(f"M=0")
            self.writeline(f"({end_label})")
        elif command == 'lt':
            else_label = f'LABEL{self.label_count}'
            end_label = f'LABEL{self.label_count + 1}'
            self.label_count += 2

            self.writeline(f"D=M-D")
            self.writeline(f"@{else_label}")
            self.writeline(f"D;JGE")
            self.writeline(f"@SP")
            self.writeline(f"A=M")
            self.writeline(f"M=-1")
            self.writeline(f"@{end_label}")
            self.writeline(f"0;JMP")
            self.writeline(f"({else_label})")
            self.writeline(f"@SP")
            self.writeline(f"A=M")
            self.writeline(f"M=0")
            self.writeline(f"({end_label})")
        # Increment stack pointer
        self.writeline(f"@SP")
        self.writeline(f"M=M+1")
        self.writeline(f"")

    def write_push_pop(self, command: str, segment: str, index: int):
        self.writeline(f"// {command} {segment} {index}")
        if command == Command.C_PUSH:
            if segment == Segment.CONSTANT:
                self.writeline(f"@{index}")
                self.writeline(f"D=A")
            elif segment in (
                Segment.LOCAL,
                Segment.ARGUMENT,
                Segment.THIS,
                Segment.THAT,
            ):
                self.writeline(f"@{index}")
                self.writeline(f"D=A")
                address_by_segment = {
                    Segment.LOCAL: "LCL",
                    Segment.ARGUMENT: "ARG",
                    Segment.THIS: "THIS",
                    Segment.THAT: "THAT",
                }
                self.writeline(f"@{address_by_segment[segment]}")
                self.writeline(f"A=D+M")
                self.writeline(f"D=M")
            elif segment == Segment.STATIC:
                self.writeline(f"@{self.class_name}.{index}")
                self.writeline(f"D=M")
            elif segment == Segment.TEMP:
                self.writeline(f"@{index}")
                self.writeline(f"D=A")
                self.writeline(f"@5")
                self.writeline(f"A=D+A")
                self.writeline(f"D=M")
            elif segment == Segment.POINTER:
                if index == 0:
                    self.writeline(f"@THIS")
                else:
                    self.writeline(f"@THAT")
                self.writeline(f"D=M")
            # D contains the value to be inserted into the stack
            # Insert it into the stack and increment stack pointer
            self.writeline(f"@SP")
            self.writeline(f"A=M")
            self.writeline(f"M=D")
            self.writeline(f"@SP")
            self.writeline(f"M=M+1")
        elif command == Command.C_POP:
            if segment in (Segment.LOCAL, Segment.ARGUMENT, Segment.THIS, Segment.THAT):
                self.writeline(f"@{index}")
                self.writeline(f"D=A")
                address_by_segment = {
                    Segment.LOCAL: "LCL",
                    Segment.ARGUMENT: "ARG",
                    Segment.THIS: "THIS",
                    Segment.THAT: "THAT",
                }
                self.writeline(f"@{address_by_segment[segment]}")
                self.writeline(f"D=D+M")
                self.writeline(f"@SP")
                self.writeline(f"M=M-1")
                self.writeline(f"A=M")
                self.writeline(f"D=D+M")
                self.writeline(f"A=D-M")
                self.writeline(f"M=D-A")
            elif segment == Segment.STATIC:
                self.writeline(f"@SP")
                self.writeline(f"M=M-1")
                self.writeline(f"A=M")
                self.writeline(f"D=M")
                self.writeline(f"@{self.class_name}.{index}")
                self.writeline(f"M=D")
            elif segment == Segment.TEMP:
                self.writeline(f"@5")
                self.writeline(f"D=A")
                self.writeline(f"@{index}")
                self.writeline(f"D=D+A")
                self.writeline(f"@SP")
                self.writeline(f"M=M-1")
                self.writeline(f"A=M")
                self.writeline(f"D=D+M")
                self.writeline(f"A=D-M")
                self.writeline(f"M=D-A")
            elif segment == Segment.POINTER:
                self.writeline(f"@SP")
                self.writeline(f"M=M-1")
                self.writeline(f"A=M")
                self.writeline(f"D=M")
                if index == 0:
                    self.writeline(f"@THIS")
                else:
                    self.writeline(f"@THAT")
                self.writeline(f"M=D")
        else:
            raise Exception(f'Invalid command {command} for write_push_pop')
        self.writeline(f"")

    def write_init(self):
        self.writeline(f"// init")
        self.writeline(f"@256")
        self.writeline(f"D=A")
        self.writeline(f"@SP")
        self.writeline(f"M=D")
        self.write_call('Sys.init', 0)
        self.writeline(f"")
    
    def write_label(self, label: str):
        self.writeline(f"// label {label}")
        self.writeline(f"({label})")
        self.writeline(f"")

    def write_goto(self, label: str):
        self.writeline(f"// goto {label}")
        self.writeline(f'@{label}')
        self.writeline(f"0;JMP")
        self.writeline(f"")

    def write_if(self, label: str):
        self.writeline(f"// if-goto {label}")
        self.writeline(f"@SP")
        self.writeline(f"M=M-1")
        self.writeline(f"A=M")
        self.writeline(f"D=M")
        self.writeline(f'@{label}')
        self.writeline(f"D;JNE")
        self.writeline(f"")

    def write_function(self, function_name: str, num_vars: int):
        self.writeline(f"// function {function_name} {num_vars}")
        self.writeline(f"({function_name})")
        for i in range(num_vars):
            self.writeline(f"@0")
            self.writeline(f"D=A")
            self.writeline(f"@SP")
            self.writeline(f"A=M")
            self.writeline(f"M=D")
            self.writeline(f"@SP")
            self.writeline(f"M=M+1")
        self.writeline(f"")

    def write_call(self, function_name: str, num_vars: int):
        self.writeline(f"// call {function_name} {num_vars}")
        ret_count = self.ret_count_by_fn[function_name]
        ret_addr_label = f'{function_name}$ret.{ret_count}'
        self.ret_count_by_fn[function_name] += 1

        # push retAddrLabel
        self.writeline(f'@{ret_addr_label}')
        self.writeline(f'D=A')
        self.writeline(f"@SP")
        self.writeline(f"A=M")
        self.writeline(f"M=D")
        self.writeline(f"@SP")
        self.writeline(f"M=M+1")

        # push LCL
        self.writeline(f'@LCL')
        self.writeline(f'D=M')
        self.writeline(f"@SP")
        self.writeline(f"A=M")
        self.writeline(f"M=D")
        self.writeline(f"@SP")
        self.writeline(f"M=M+1")

        # push ARG
        self.writeline(f'@ARG')
        self.writeline(f'D=M')
        self.writeline(f"@SP")
        self.writeline(f"A=M")
        self.writeline(f"M=D")
        self.writeline(f"@SP")
        self.writeline(f"M=M+1")

        # push THIS
        self.writeline(f'@THIS')
        self.writeline(f'D=M')
        self.writeline(f"@SP")
        self.writeline(f"A=M")
        self.writeline(f"M=D")
        self.writeline(f"@SP")
        self.writeline(f"M=M+1")

        # push THAT
        self.writeline(f'@THAT')
        self.writeline(f'D=M')
        self.writeline(f"@SP")
        self.writeline(f"A=M")
        self.writeline(f"M=D")
        self.writeline(f"@SP")
        self.writeline(f"M=M+1")
        
        # ARG = SP-5-nArgs
        self.writeline(f'@SP')
        self.writeline(f'D=M')
        self.writeline(f'@5')
        self.writeline(f'D=D-A')
        self.writeline(f'@{num_vars}')
        self.writeline(f'D=D-A')
        self.writeline(f'@ARG')
        self.writeline(f'M=D')

        # LCL = SP
        self.writeline(f'@SP')
        self.writeline(f'D=M')
        self.writeline(f'@LCL')
        self.writeline(f'M=D')

        # goto functionName
        self.writeline(f'@{function_name}')
        self.writeline(f"0;JMP")

        # (retAddrLabel)
        self.writeline(f"({ret_addr_label})")
        self.writeline('')

    def write_return(self):
        self.writeline(f"// return")

        # endFrame (R13) = LCL
        self.writeline(f'@LCL')
        self.writeline(f'D=M')
        self.writeline(f'@R13')
        self.writeline(f'M=D')

        # retAddr (R14) = *(endFrame – 5)
        self.writeline(f'@R13')
        self.writeline(f'D=M')
        self.writeline(f'@5')
        self.writeline(f'D=D-A')
        self.writeline(f'A=D')
        self.writeline(f'D=M')
        self.writeline(f'@R14')
        self.writeline(f'M=D')

        # *ARG=pop()
        self.writeline(f'@SP')
        self.writeline(f"M=M-1")
        self.writeline(f"A=M")
        self.writeline(f"D=M")
        self.writeline(f'@ARG')
        self.writeline(f"A=M")
        self.writeline(f"M=D")

        # SP = ARG + 1
        self.writeline(f'@ARG')
        self.writeline(f"D=M+1")
        self.writeline(f'@SP')
        self.writeline(f'M=D')

        # THAT = *(endFrame – 1)
        self.writeline(f'@R13')
        self.writeline(f'D=M')
        self.writeline(f'@1')
        self.writeline(f'D=D-A')
        self.writeline(f'A=D')
        self.writeline(f'D=M')
        self.writeline(f'@THAT')
        self.writeline(f'M=D')

        # THIS = *(endFrame – 2)
        self.writeline(f'@R13')
        self.writeline(f'D=M')
        self.writeline(f'@2')
        self.writeline(f'D=D-A')
        self.writeline(f'A=D')
        self.writeline(f'D=M')
        self.writeline(f'@THIS')
        self.writeline(f'M=D')

        # ARG = *(endFrame – 3)
        self.writeline(f'@R13')
        self.writeline(f'D=M')
        self.writeline(f'@3')
        self.writeline(f'D=D-A')
        self.writeline(f'A=D')
        self.writeline(f'D=M')
        self.writeline(f'@ARG')
        self.writeline(f'M=D')
        
        # LCL = *(endFrame – 4)
        self.writeline(f'@R13')
        self.writeline(f'D=M')
        self.writeline(f'@4')
        self.writeline(f'D=D-A')
        self.writeline(f'A=D')
        self.writeline(f'D=M')
        self.writeline(f'@LCL')
        self.writeline(f'M=D')

        # goto retAddr (R14)
        self.writeline(f'@R14')
        self.writeline(f'A=M')
        self.writeline(f"0;JMP")
        self.writeline(f"")


def _process_vm_file(in_file: str, writer: CodeWriter):
    parser = Parser(in_file)
    writer.set_file_name(in_file)
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == Command.C_ARITHMETIC:
            writer.write_arithmetic(parser.arg_1())
        elif command_type in (Command.C_PUSH, Command.C_POP):
            writer.write_push_pop(command_type, parser.arg_1(), int(parser.arg_2()))
        elif command_type == Command.C_LABEL:
            writer.write_label(parser.arg_1())
        elif command_type == Command.C_GOTO:
            writer.write_goto(parser.arg_1())
        elif command_type == Command.C_IF:
            writer.write_if(parser.arg_1())
        elif command_type == Command.C_FUNCTION:
            writer.write_function(parser.arg_1(), int(parser.arg_2()))
        elif command_type == Command.C_CALL:
            writer.write_call(parser.arg_1(), int(parser.arg_2()))
        elif command_type == Command.C_RETURN:
            writer.write_return()

if __name__ == "__main__":
    filename = sys.argv[1]
    try:
        if os.path.isdir(filename):  
            dir_name = os.path.basename(filename)
            out_file = dir_name + '.asm'
            writer = CodeWriter(os.path.join(filename, out_file))    
            writer.write_init()
            with os.scandir(filename) as it:
                for entry in it:
                    if entry.name.endswith(".vm") and entry.is_file():            
                        _process_vm_file(in_file=entry.path, writer=writer)
        else:
            path = os.path.splitext(filename)[0]
            out_file = path + '.asm'
            writer = CodeWriter(out_file)
            _process_vm_file(in_file=filename, writer=writer)
        writer.close()
    except Exception as e:
        traceback.print_exc()
        writer.close()
