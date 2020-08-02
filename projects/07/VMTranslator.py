import sys
import traceback
import os

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
        self.static_prefix = os.path.splitext(os.path.basename(filename))[0]
        self.file = open(filename, "w")
        self.label_count = 0

    def close(self):
        self.file.close()

    def write_arithmetic(self, command: str):
        self.file.write(f"// {command}\n")
        self.file.write(f"@SP\n")
        self.file.write(f"M=M-1\n")
        self.file.write(f"A=M\n")
        # Unary commands
        if command == 'neg':
            self.file.write(f"M=-M\n")
            # Increment stack pointer
            self.file.write(f"@SP\n")
            self.file.write(f"M=M+1\n")
            self.file.write(f"\n")
            return
        elif command == 'not':
            self.file.write('M=!M\n')
            # Increment stack pointer
            self.file.write(f"@SP\n")
            self.file.write(f"M=M+1\n")
            self.file.write(f"\n")
            return

        # Binary Commands
        self.file.write(f"D=M\n")
        # D contains the second arg
        self.file.write(f"@SP\n")
        self.file.write(f"M=M-1\n")
        self.file.write(f"A=M\n")
        if command == 'add':            
            self.file.write(f"M=D+M\n")
        elif command == 'sub':
            self.file.write(f"M=M-D\n")
        elif command == 'and':
            self.file.write(f"M=D&M\n")
        elif command == 'or':
            self.file.write(f"M=D|M\n")
        elif command == 'eq':
            else_label = f'LABEL{self.label_count}'
            end_label = f'LABEL{self.label_count + 1}'
            self.label_count += 2

            self.file.write(f"D=M-D\n")
            self.file.write(f"@{else_label}\n")
            self.file.write(f"D;JNE\n")
            self.file.write(f"@SP\n")
            self.file.write(f"A=M\n")
            self.file.write(f"M=-1\n")
            self.file.write(f"@{end_label}\n")
            self.file.write(f"0;JMP\n")
            self.file.write(f"({else_label})\n")
            self.file.write(f"@SP\n")
            self.file.write(f"A=M\n")
            self.file.write(f"M=0\n")
            self.file.write(f"({end_label})\n")
        elif command == 'gt':
            else_label = f'LABEL{self.label_count}'
            end_label = f'LABEL{self.label_count + 1}'
            self.label_count += 2

            self.file.write(f"D=M-D\n")
            self.file.write(f"@{else_label}\n")
            self.file.write(f"D;JLE\n")
            self.file.write(f"@SP\n")
            self.file.write(f"A=M\n")
            self.file.write(f"M=-1\n")
            self.file.write(f"@{end_label}\n")
            self.file.write(f"0;JMP\n")
            self.file.write(f"({else_label})\n")
            self.file.write(f"@SP\n")
            self.file.write(f"A=M\n")
            self.file.write(f"M=0\n")
            self.file.write(f"({end_label})\n")
        elif command == 'lt':
            else_label = f'LABEL{self.label_count}'
            end_label = f'LABEL{self.label_count + 1}'
            self.label_count += 2

            self.file.write(f"D=M-D\n")
            self.file.write(f"@{else_label}\n")
            self.file.write(f"D;JGE\n")
            self.file.write(f"@SP\n")
            self.file.write(f"A=M\n")
            self.file.write(f"M=-1\n")
            self.file.write(f"@{end_label}\n")
            self.file.write(f"0;JMP\n")
            self.file.write(f"({else_label})\n")
            self.file.write(f"@SP\n")
            self.file.write(f"A=M\n")
            self.file.write(f"M=0\n")
            self.file.write(f"({end_label})\n")
        # Increment stack pointer
        self.file.write(f"@SP\n")
        self.file.write(f"M=M+1\n")
        self.file.write(f"\n")


    def write_push_pop(self, command: str, segment: str, index: str):
        self.file.write(f"// {command} {segment} {index}\n")
        if command == Command.C_PUSH:
            if segment == Segment.CONSTANT:
                self.file.write(f"@{index}\n")
                self.file.write(f"D=A\n")
            elif segment in (
                Segment.LOCAL,
                Segment.ARGUMENT,
                Segment.THIS,
                Segment.THAT,
            ):
                self.file.write(f"@{index}\n")
                self.file.write(f"D=A\n")
                address_by_segment = {
                    Segment.LOCAL: "LCL",
                    Segment.ARGUMENT: "ARG",
                    Segment.THIS: "THIS",
                    Segment.THAT: "THAT",
                }
                self.file.write(f"@{address_by_segment[segment]}\n")
                self.file.write(f"A=D+M\n")
                self.file.write(f"D=M\n")
            elif segment == Segment.STATIC:
                self.file.write(f"@{self.static_prefix}.{index}\n")
                self.file.write(f"D=M\n")
            elif segment == Segment.TEMP:
                self.file.write(f"@{index}\n")
                self.file.write(f"D=A\n")
                self.file.write(f"@5\n")
                self.file.write(f"A=D+A\n")
                self.file.write(f"D=M\n")
            elif segment == Segment.POINTER:
                if int(index) == 0:
                    self.file.write(f"@THIS\n")
                else:
                    self.file.write(f"@THAT\n")
                self.file.write(f"D=M\n")
            # D is the value to be inserted into the stack
            # Insert it into the stack and increment stack pointer
            self.file.write(f"@SP\n")
            self.file.write(f"A=M\n")
            self.file.write(f"M=D\n")
            self.file.write(f"@SP\n")
            self.file.write(f"M=M+1\n")
        else:
            if segment in (Segment.LOCAL, Segment.ARGUMENT, Segment.THIS, Segment.THAT):
                self.file.write(f"@{index}\n")
                self.file.write(f"D=A\n")
                address_by_segment = {
                    Segment.LOCAL: "LCL",
                    Segment.ARGUMENT: "ARG",
                    Segment.THIS: "THIS",
                    Segment.THAT: "THAT",
                }
                self.file.write(f"@{address_by_segment[segment]}\n")
                self.file.write(f"D=D+M\n")
                self.file.write(f"@SP\n")
                self.file.write(f"M=M-1\n")
                self.file.write(f"A=M\n")
                self.file.write(f"D=D+M\n")
                self.file.write(f"A=D-M\n")
                self.file.write(f"M=D-A\n")
            elif segment == Segment.STATIC:
                self.file.write(f"@SP\n")
                self.file.write(f"M=M-1\n")
                self.file.write(f"A=M\n")
                self.file.write(f"D=M\n")
                self.file.write(f"@{self.static_prefix}.{index}\n")
                self.file.write(f"M=D\n")
            elif segment == Segment.TEMP:
                self.file.write(f"@5\n")
                self.file.write(f"D=A\n")
                self.file.write(f"@{index}\n")
                self.file.write(f"D=D+A\n")
                self.file.write(f"@SP\n")
                self.file.write(f"M=M-1\n")
                self.file.write(f"A=M\n")
                self.file.write(f"D=D+M\n")
                self.file.write(f"A=D-M\n")
                self.file.write(f"M=D-A\n")
            elif segment == Segment.POINTER:
                self.file.write(f"@SP\n")
                self.file.write(f"M=M-1\n")
                self.file.write(f"A=M\n")
                self.file.write(f"D=M\n")
                if int(index) == 0:
                    self.file.write(f"@THIS\n")
                else:
                    self.file.write(f"@THAT\n")
                self.file.write(f"M=D\n")
        
        self.file.write(f"\n")


if __name__ == "__main__":
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    try:
        parser = Parser(in_file)
        writer = CodeWriter(out_file)
        while parser.has_more_commands():
            parser.advance()
            command_type = parser.command_type()
            if command_type == Command.C_ARITHMETIC:
                # print(f'{command_type} {parser.arg_1()}')
                writer.write_arithmetic(parser.arg_1())
            elif command_type in (Command.C_PUSH, Command.C_POP):
                # print(f'{command_type} {parser.arg_1()} {parser.arg_2()}')
                writer.write_push_pop(command_type, parser.arg_1(), parser.arg_2())
        writer.close()
    except Exception as e:
        traceback.print_exc()
        writer.close()
