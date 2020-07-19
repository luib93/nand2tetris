import os, sys, re
from typing import TextIO, Optional, DefaultDict, NamedTuple, Dict
import html
from collections import defaultdict

KEYWORDS = (
    "class",
    "method",
    "function",
    "constructor",
    "int",
    "boolean",
    "char",
    "void",
    "var",
    "static",
    "field",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
    "true",
    "false",
    "null",
    "this",
)

SYMBOLS = (
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
)


class TokenType:
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "int_const"
    STRING_CONST = "string_const"


class TokenKeyword:
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    CONSTRUCTOR = "constructor"
    INT = "int"
    BOOLEAN = "boolean"
    CHAR = "char"
    VOID = "void"
    VAR = "var"
    STATIC = "static"
    FIELD = "field"
    LET = "let"
    DO = "do"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"


class JackTokenizer:
    def __init__(self, file: TextIO):
        self.text: str = file.read()
        self.current_index: int = 0
        self.current_token: Optional[str] = None
        self.next_index: Optional[int] = None
        self.next_token: Optional[str] = None
        file.seek(0)

    def has_more_tokens(self):
        if self.next_token:
            return True

        index = self.current_index
        if index >= len(self.text):
            return False

        # ignore whitespace and comments
        is_space = self.text[index].isspace()
        is_block_comment = self.text[index : index + 2] == "/*"
        is_inline_comment = self.text[index : index + 2] == "//"
        while is_space or is_block_comment or is_inline_comment:
            if is_space:
                index += 1
            elif is_inline_comment:
                # go to the next line
                index = self.text.index("\n", index + 1) + 1
            else:
                # go to the corresponding end block
                index = self.text.index("*/", index + 2) + 2
            if index >= len(self.text):
                return False

            is_space = self.text[index].isspace()
            is_block_comment = self.text[index : index + 2] == "/*"
            is_inline_comment = self.text[index : index + 2] == "//"

        curr_char: str = self.text[index]
        if curr_char in SYMBOLS:
            # can only be a symbol
            self.next_token = curr_char
            self.next_index = index + 1
        elif curr_char == '"':
            # can only be a string constant
            end_index = self.text.index('"', index + 1)
            self.next_token = self.text[index : end_index + 1]
            self.next_index = end_index + 1
        elif curr_char.isdigit():
            # can only be an integer constant
            token = curr_char
            index += 1
            while index < len(self.text) and self.text[index].isdigit():
                token += self.text[index]
                index += 1
            self.next_token = token
            self.next_index = index
        elif curr_char.isalpha():
            # can be either an identifier or keyword
            token = curr_char
            index += 1
            while (
                index < len(self.text)
                and self.text[index].isalnum()
                or self.text[index] == "_"
            ):
                token += self.text[index]
                index += 1
            self.next_token = token
            self.next_index = index
        else:
            raise Exception(f"Invalid character {curr_char}")
        return self.next_token is not None

    def advance(self):
        if not self.has_more_tokens():
            raise Exception("No more tokens to read")
        self.current_token = self.next_token
        self.current_index = self.next_index
        self.next_index = None
        self.next_token = None

    def token_type(self) -> TokenType:
        if self.current_token in KEYWORDS:
            return TokenType.KEYWORD

        if self.current_token in SYMBOLS:
            return TokenType.SYMBOL

        if self.current_token.isdigit():
            return TokenType.INT_CONST

        if self.current_token.startswith('"') and self.current_token.endswith('"'):
            return TokenType.STRING_CONST

        if re.search(r"[\w\d_]+", self.current_token):
            return TokenType.IDENTIFIER

        raise Exception(f"Cannot determine token type for {self.current_token}")

    def keyword(self):
        token_type = self.token_type()
        if token_type != TokenType.KEYWORD:
            raise Exception("Current token is not a keyword")
        mappings = {
            "class": TokenKeyword.CLASS,
            "method": TokenKeyword.METHOD,
            "function": TokenKeyword.FUNCTION,
            "constructor": TokenKeyword.CONSTRUCTOR,
            "int": TokenKeyword.INT,
            "boolean": TokenKeyword.BOOLEAN,
            "char": TokenKeyword.CHAR,
            "void": TokenKeyword.VOID,
            "var": TokenKeyword.VAR,
            "static": TokenKeyword.STATIC,
            "field": TokenKeyword.FIELD,
            "let": TokenKeyword.LET,
            "do": TokenKeyword.DO,
            "if": TokenKeyword.IF,
            "else": TokenKeyword.ELSE,
            "while": TokenKeyword.WHILE,
            "return": TokenKeyword.RETURN,
            "true": TokenKeyword.TRUE,
            "false": TokenKeyword.FALSE,
            "null": TokenKeyword.NULL,
            "this": TokenKeyword.THIS,
        }
        return mappings[self.current_token]

    def symbol(self):
        token_type = self.token_type()
        if token_type != TokenType.SYMBOL:
            raise Exception("Current token is not a symbol")
        return self.current_token

    def identifier(self):
        token_type = self.token_type()
        if token_type != TokenType.IDENTIFIER:
            raise Exception("Current token is not an identifier")
        return self.current_token

    def int_val(self):
        token_type = self.token_type()
        if token_type != TokenType.INT_CONST:
            raise Exception("Current token is not an integer constant")
        return int(self.current_token)

    def string_val(self):
        token_type = self.token_type()
        if token_type != TokenType.STRING_CONST:
            raise Exception("Current token is not a string constant")
        return self.current_token[1:-1]  # remove surrounding double quotes


class CompilationEngine:
    def __init__(self, in_file: TextIO, out_file: TextIO):
        self.tokenizer: JackTokenizer = JackTokenizer(in_file)
        self.writer: VMWriter = VMWriter(out_file)
        self.class_table: SymbolTable = SymbolTable()
        self.subroutine_table: SymbolTable = SymbolTable()
        self.tokenizer.advance()

        self.class_name = None
        self.method_name = None
        self.label_count = 0
        self.expression_counts = []

    def compile_class(self):
        # 'class' className '{' classVarDec* subroutineDec* '}'
        if self.tokenizer.keyword() != TokenKeyword.CLASS:
            raise Exception
        self.tokenizer.advance()
        self.class_name = self.tokenizer.identifier()

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "{":
            raise Exception

        self.tokenizer.advance()
        while self.tokenizer.token_type() == TokenType.KEYWORD and self.tokenizer.keyword() in (
            TokenKeyword.STATIC,
            TokenKeyword.FIELD,
        ):
            self.compile_class_var_dec()
        while self.tokenizer.token_type() == TokenType.KEYWORD and self.tokenizer.keyword() in (
            TokenKeyword.CONSTRUCTOR,
            TokenKeyword.FUNCTION,
            TokenKeyword.METHOD,
        ):
            self.compile_subroutine_dec()

        if self.tokenizer.symbol() != "}":
            raise Exception
        self.writer.close()

    def compile_class_var_dec(self):
        # ('static'|'field') type varName (',' varName)*';'
        # type = 'int' | 'char' | 'boolean' | 'className'
        if self.tokenizer.keyword() not in (TokenKeyword.STATIC, TokenKeyword.FIELD):
            raise Exception

        var_kind = self.tokenizer.keyword()
        # handle type
        self.tokenizer.advance()
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            if self.tokenizer.keyword() in (
                TokenKeyword.INT,
                TokenKeyword.CHAR,
                TokenKeyword.BOOLEAN,
            ):
                var_type = self.tokenizer.keyword()
            else:
                raise Exception
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            var_type = self.tokenizer.identifier()
        else:
            raise Exception

        self.tokenizer.advance()
        var_name = self.tokenizer.identifier()
        self.class_table.define(var_name=var_name, var_type=var_type, var_kind=var_kind)

        self.tokenizer.advance()
        while (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ","
        ):
            self.tokenizer.advance()
            var_name = self.tokenizer.identifier()
            self.class_table.define(
                var_name=var_name, var_type=var_type, var_kind=var_kind
            )
            self.tokenizer.advance()

        if self.tokenizer.symbol() != ";":
            raise Exception

        self.tokenizer.advance()

    def compile_subroutine_dec(self):
        # ('constructor'|'function'|'method') ('void'|type)
        # subroutineName '('parameterList')' subroutineBody
        self.subroutine_table.start_subroutine()
        if self.tokenizer.keyword() not in (
            TokenKeyword.CONSTRUCTOR,
            TokenKeyword.FUNCTION,
            TokenKeyword.METHOD,
        ):
            raise Exception
        self.method_type = self.tokenizer.keyword()
        self.tokenizer.advance()
        if self.tokenizer.token_type() == TokenType.IDENTIFIER:
            self.return_type = self.tokenizer.identifier()
        elif self.tokenizer.token_type() == TokenType.KEYWORD:
            if self.tokenizer.keyword() not in (
                TokenKeyword.VOID,
                TokenKeyword.INT,
                TokenKeyword.CHAR,
                TokenKeyword.BOOLEAN,
            ):
                raise Exception
            else:
                self.return_type = self.tokenizer.keyword()
        else:
            raise Exception

        self.tokenizer.advance()
        self.method_name = self.tokenizer.identifier()
        self.tokenizer.advance()
        if self.tokenizer.symbol() != "(":
            raise Exception

        self.tokenizer.advance()
        self.compile_parameter_list()
        if self.tokenizer.symbol() != ")":
            raise Exception

        self.tokenizer.advance()
        self.compile_subroutine_body()

    def compile_parameter_list(self):
        # ((type varName) (',' type varName))
        # handle type
        if self.method_type == TokenKeyword.METHOD:
            self.subroutine_table.define(
                var_name="this", var_type=self.class_name, var_kind=VarKind.ARG
            )

        if self.tokenizer.token_type() == TokenType.KEYWORD:
            if self.tokenizer.keyword() in (
                TokenKeyword.INT,
                TokenKeyword.CHAR,
                TokenKeyword.BOOLEAN,
            ):
                var_type = self.tokenizer.keyword()
            else:
                raise Exception
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            var_type = self.tokenizer.identifier()
        else:
            return

        self.tokenizer.advance()
        var_name = self.tokenizer.identifier()
        self.subroutine_table.define(
            var_name=var_name, var_type=var_type, var_kind=VarKind.ARG
        )

        self.tokenizer.advance()
        while (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ","
        ):
            self.tokenizer.advance()
            # handle type
            if self.tokenizer.token_type() == TokenType.KEYWORD:
                if self.tokenizer.keyword() in (
                    TokenKeyword.INT,
                    TokenKeyword.CHAR,
                    TokenKeyword.BOOLEAN,
                ):
                    var_type = self.tokenizer.keyword()
                else:
                    raise Exception
            elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
                var_type = self.tokenizer.identifier()
            else:
                raise Exception

            self.tokenizer.advance()
            var_name = self.tokenizer.identifier()
            self.subroutine_table.define(
                var_name=var_name, var_type=var_type, var_kind=VarKind.ARG
            )
            self.tokenizer.advance()

    def compile_subroutine_body(self):
        # '{'varDec* statements'}'
        if self.tokenizer.symbol() != "{":
            raise Exception

        self.tokenizer.advance()
        while (
            self.tokenizer.token_type() == TokenType.KEYWORD
            and self.tokenizer.keyword() == TokenKeyword.VAR
        ):
            self.compile_var_dec()

        n_locals = self.subroutine_table.var_count(VarKind.LOCAL)
        n_fields = self.class_table.var_count(VarKind.FIELD)
        self.writer.write_function(
            name=f"{self.class_name}.{self.method_name}", n_locals=n_locals
        )
        if self.method_type == TokenKeyword.METHOD:
            # set THIS to the first argument
            self.writer.write_push(segment=VMSegment.ARG, index=0)
            self.writer.write_pop(segment=VMSegment.POINTER, index=0)
        elif self.method_type == TokenKeyword.CONSTRUCTOR:
            # allocate memory for field variables
            self.writer.write_push(segment=VMSegment.CONST, index=n_fields)
            self.writer.write_call(name="Memory.alloc", n_args=1)
            self.writer.write_pop(segment=VMSegment.POINTER, index=0)

        self.compile_statements()
        if self.tokenizer.symbol() != "}":
            raise Exception

        self.tokenizer.advance()

    def compile_var_dec(self):
        # 'var' type varName (',' varName)*';'
        # type = int | char | boolean | className
        if self.tokenizer.keyword() != TokenKeyword.VAR:
            raise Exception

        self.tokenizer.advance()
        # handle type
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            if self.tokenizer.keyword() in (
                TokenKeyword.INT,
                TokenKeyword.CHAR,
                TokenKeyword.BOOLEAN,
            ):
                var_type = self.tokenizer.keyword()
            else:
                raise Exception
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            var_type = self.tokenizer.identifier()
        else:
            raise Exception

        self.tokenizer.advance()
        var_name = self.tokenizer.identifier()
        self.subroutine_table.define(
            var_name=var_name, var_type=var_type, var_kind=VarKind.LOCAL
        )

        self.tokenizer.advance()
        while (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ","
        ):
            self.tokenizer.advance()
            var_name = self.tokenizer.identifier()
            self.subroutine_table.define(
                var_name=var_name, var_type=var_type, var_kind=VarKind.LOCAL
            )
            self.tokenizer.advance()

        if self.tokenizer.symbol() != ";":
            raise Exception
        self.tokenizer.advance()

    def compile_statements(self):
        while self.tokenizer.token_type() == TokenType.KEYWORD:
            keyword = self.tokenizer.keyword()
            if keyword == TokenKeyword.IF:
                self.compile_if()
            elif keyword == TokenKeyword.LET:
                self.compile_let()
            elif keyword == TokenKeyword.WHILE:
                self.compile_while()
            elif keyword == TokenKeyword.DO:
                self.compile_do()
            elif keyword == TokenKeyword.RETURN:
                self.compile_return()
            else:
                break

    def compile_let(self):
        # 'let' varName ('['expression']')?'='expression';'
        if self.tokenizer.keyword() != TokenKeyword.LET:
            raise Exception

        self.tokenizer.advance()
        var_name = self.tokenizer.identifier()

        # look at the subroutine table first
        var_kind = self.subroutine_table.kind_of(var_name)
        vm_index = self.subroutine_table.index_of(var_name)
        if var_kind == VarKind.NONE:
            # if it's not there, it's probably in the class table
            var_kind = self.class_table.kind_of(var_name)
            vm_index = self.class_table.index_of(var_name)
        if var_kind == VarKind.NONE:
            # if this is the case, then it is in neither tables
            raise Exception
        segment = VM_SEGMENT_BY_VAR_KIND[var_kind]
        self.tokenizer.advance()
        if self.tokenizer.symbol() == "[":
            # this is an array assignment
            self.writer.write_push(segment=segment, index=vm_index)
            self.tokenizer.advance()
            self.compile_expression()
            self.writer.write_arithmetic(VMArithmetic.ADD)
            # offset array by stack val
            if self.tokenizer.symbol() != "]":
                raise Exception
            self.tokenizer.advance()

            if self.tokenizer.symbol() != "=":
                raise Exception

            self.tokenizer.advance()
            self.compile_expression()
            self.writer.write_pop(segment=VMSegment.TEMP, index=0)
            self.writer.write_pop(segment=VMSegment.POINTER, index=1)
            self.writer.write_push(segment=VMSegment.TEMP, index=0)
            self.writer.write_pop(segment=VMSegment.THAT, index=0)
        else:
            # this is a non-array assignment
            if self.tokenizer.symbol() != "=":
                raise Exception

            self.tokenizer.advance()
            self.compile_expression()
            segment = VM_SEGMENT_BY_VAR_KIND[var_kind]
            self.writer.write_pop(segment=segment, index=vm_index)

        if self.tokenizer.symbol() != ";":
            raise Exception
        self.tokenizer.advance()

    def compile_if(self):
        # 'if' '('expression')' '{'statements'}'('else''{'statements'}')?
        if self.tokenizer.keyword() != TokenKeyword.IF:
            raise Exception

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "(":
            raise Exception

        self.tokenizer.advance()
        self.compile_expression()
        self.writer.write_arithmetic(VMArithmetic.NOT)
        else_label = f"L{self.label_count}"
        end_label = f"L{self.label_count + 1}"
        self.label_count += 2
        self.writer.write_if(else_label)

        if self.tokenizer.symbol() != ")":
            raise Exception

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "{":
            raise Exception

        self.tokenizer.advance()
        self.compile_statements()
        self.writer.write_goto(end_label)

        if self.tokenizer.symbol() != "}":
            raise Exception

        self.tokenizer.advance()
        self.writer.write_label(else_label)
        if (
            self.tokenizer.token_type() == TokenType.KEYWORD
            and self.tokenizer.keyword() == TokenKeyword.ELSE
        ):
            self.tokenizer.advance()
            if self.tokenizer.symbol() != "{":
                raise Exception
            self.tokenizer.advance()
            self.compile_statements()

            if self.tokenizer.symbol() != "}":
                raise Exception
            self.tokenizer.advance()
        self.writer.write_label(end_label)

    def compile_while(self):
        # 'while' '(' expression ')' '{' statements '}'
        if self.tokenizer.keyword() != TokenKeyword.WHILE:
            raise Exception

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "(":
            raise Exception

        self.tokenizer.advance()
        start_label = f"L{self.label_count}"
        end_label = f"L{self.label_count + 1}"
        self.label_count += 2
        self.writer.write_label(start_label)
        self.compile_expression()
        self.writer.write_arithmetic(VMArithmetic.NOT)
        self.writer.write_if(end_label)

        if self.tokenizer.symbol() != ")":
            raise Exception

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "{":
            raise Exception

        self.tokenizer.advance()
        self.compile_statements()
        self.writer.write_goto(start_label)

        if self.tokenizer.symbol() != "}":
            raise Exception

        self.writer.write_label(end_label)
        self.tokenizer.advance()

    def compile_do(self):
        # 'do' subroutineCall';'
        if self.tokenizer.keyword() != TokenKeyword.DO:
            raise Exception

        # handle subroutine call: subroutineName'('expressionList')' | (className|varName)'.'subroutineName'('expressionList')'
        self.tokenizer.advance()
        first_identifier = self.tokenizer.identifier()

        self.tokenizer.advance()
        if self.tokenizer.symbol() == ".":
            # (className|varName)'.'subroutineName'('expressionList')'
            self.tokenizer.advance()
            object_kind = self.subroutine_table.kind_of(first_identifier)
            object_index = self.subroutine_table.index_of(first_identifier)
            object_type = self.subroutine_table.type_of(first_identifier)
            if object_kind == VarKind.NONE:
                # lookup in the class table
                object_kind = self.class_table.kind_of(first_identifier)
                object_index = self.class_table.index_of(first_identifier)
                object_type = self.class_table.type_of(first_identifier)

            is_variable = object_kind != VarKind.NONE
            # if this is a method, we need to push the object as the first arg
            # otherwise, it is a function or static subroutine
            if is_variable:
                segment = VM_SEGMENT_BY_VAR_KIND[object_kind]
                self.writer.write_push(segment=segment, index=object_index)
                subroutine_name = f"{object_type}.{self.tokenizer.identifier()}"
            else:
                subroutine_name = f"{first_identifier}.{self.tokenizer.identifier()}"
            self.tokenizer.advance()
        else:
            # subroutineName'('expressionList')'
            self.writer.write_push(segment=VMSegment.POINTER, index=0)
            is_variable = True
            subroutine_name = f"{self.class_name}.{first_identifier}"

        if self.tokenizer.symbol() != "(":
            raise Exception

        self.tokenizer.advance()
        self.compile_expression_list()

        if self.tokenizer.symbol() != ")":
            raise Exception
        n_args = self.expression_counts.pop()
        if is_variable:
            n_args += 1
        self.writer.write_call(name=subroutine_name, n_args=n_args)
        self.tokenizer.advance()
        if self.tokenizer.symbol() != ";":
            raise Exception
        self.writer.write_pop(segment=VMSegment.TEMP, index=0)
        self.tokenizer.advance()

    def compile_return(self):
        if self.tokenizer.keyword() != TokenKeyword.RETURN:
            raise Exception

        self.tokenizer.advance()
        if (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ";"
        ):
            self.writer.write_push(segment=VMSegment.CONST, index=0)
            self.writer.write_return()
            self.tokenizer.advance()
            return

        self.compile_expression()
        self.writer.write_return()
        self.tokenizer.advance()

    def compile_expression(self):
        # term (op term)*
        self.compile_term()
        while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() in (
            "+",
            "-",
            "*",
            "/",
            "&",
            "|",
            "<",
            ">",
            "=",
        ):
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            if op == "+":
                self.writer.write_arithmetic(VMArithmetic.ADD)
            elif op == "-":
                self.writer.write_arithmetic(VMArithmetic.SUB)
            elif op == "*":
                self.writer.write_call("Math.multiply", 2)
            elif op == "/":
                self.writer.write_call("Math.divide", 2)
            elif op == "&":
                self.writer.write_arithmetic(VMArithmetic.AND)
            elif op == "|":
                self.writer.write_arithmetic(VMArithmetic.OR)
            elif op == "<":
                self.writer.write_arithmetic(VMArithmetic.LT)
            elif op == ">":
                self.writer.write_arithmetic(VMArithmetic.GT)
            elif op == "=":
                self.writer.write_arithmetic(VMArithmetic.EQ)

    def compile_term(self):
        # integerConstant | stringConstant | keywordConstant | varName |
        # varName '['expression']' | subroutineCall | '('expression')' | unaryOp term
        token_type = self.tokenizer.token_type()
        if token_type == TokenType.INT_CONST:
            # integerConstant
            self.writer.write_push(
                segment=VMSegment.CONST, index=self.tokenizer.int_val()
            )
            self.tokenizer.advance()
        elif token_type == TokenType.STRING_CONST:
            # stringConstant
            string_const = self.tokenizer.string_val()
            self.writer.write_push(segment=VMSegment.CONST, index=len(string_const))
            self.writer.write_call(name="String.new", n_args=1)
            for char in string_const:
                self.writer.write_push(segment=VMSegment.CONST, index=ord(char))
                self.writer.write_call(name="String.appendChar", n_args=2)
            self.tokenizer.advance()
        elif token_type == TokenType.KEYWORD and self.tokenizer.keyword() in (
            TokenKeyword.TRUE,
            TokenKeyword.FALSE,
            TokenKeyword.NULL,
            TokenKeyword.THIS,
        ):
            # keywordConstant
            if self.tokenizer.keyword() == TokenKeyword.TRUE:
                self.writer.write_push(segment=VMSegment.CONST, index=1)
                self.writer.write_arithmetic(VMArithmetic.NEG)
            elif self.tokenizer.keyword() == TokenKeyword.FALSE:
                self.writer.write_push(segment=VMSegment.CONST, index=0)
            elif self.tokenizer.keyword() == TokenKeyword.NULL:
                self.writer.write_push(segment=VMSegment.CONST, index=0)
            elif self.tokenizer.keyword() == TokenKeyword.THIS:
                self.writer.write_push(segment=VMSegment.POINTER, index=0)

            self.tokenizer.advance()
        elif token_type == TokenType.SYMBOL and self.tokenizer.symbol() == "(":
            # '(' expression ')'
            self.tokenizer.advance()
            self.compile_expression()
            if self.tokenizer.symbol() != ")":
                raise Exception
            self.tokenizer.advance()
        elif token_type == TokenType.SYMBOL and self.tokenizer.symbol() in ("-", "~"):
            # unaryOp term
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            if op == "-":
                self.writer.write_arithmetic(VMArithmetic.NEG)
            else:
                self.writer.write_arithmetic(VMArithmetic.NOT)
        elif token_type == TokenType.IDENTIFIER:
            # varName | varName'['expression']'| subroutineCall
            first_identifier = self.tokenizer.identifier()
            self.tokenizer.advance()

            if (
                self.tokenizer.token_type() == TokenType.SYMBOL
                and self.tokenizer.symbol() == "["
            ):
                # varName '['expression']'
                var_kind = self.subroutine_table.kind_of(first_identifier)
                var_index = self.subroutine_table.index_of(first_identifier)
                if var_kind == VarKind.NONE:
                    # look at class table
                    var_kind = self.class_table.kind_of(first_identifier)
                    var_index = self.class_table.index_of(first_identifier)
                # if we don't find it in either, then throw
                if var_kind == VarKind.NONE:
                    raise Exception
                segment = VM_SEGMENT_BY_VAR_KIND[var_kind]
                self.writer.write_push(segment=segment, index=var_index)
                self.tokenizer.advance()
                self.compile_expression()
                if self.tokenizer.symbol() != "]":
                    raise Exception
                self.writer.write_arithmetic(VMArithmetic.ADD)
                self.writer.write_pop(segment=VMSegment.POINTER, index=1)
                self.writer.write_push(segment=VMSegment.THAT, index=0)
                self.tokenizer.advance()
            elif (
                self.tokenizer.token_type() == TokenType.SYMBOL
                and self.tokenizer.symbol() == "("
            ):
                # handle subroutine call: subroutineName'('expressionList')'
                self.tokenizer.advance()
                self.compile_expression_list()
                if self.tokenizer.symbol() != ")":
                    raise Exception
                self.writer.write_push(segment=VMSegment.POINTER, index=0)
                expression_count = self.expression_counts.pop() + 1
                self.writer.write_call(
                    name=f"{self.class_name}.{first_identifier}",
                    n_args=expression_count,
                )
                self.tokenizer.advance()
            elif (
                self.tokenizer.token_type() == TokenType.SYMBOL
                and self.tokenizer.symbol() == "."
            ):
                # handle subroutine call: (className|varName)'.'subroutineName'('expressionList')'
                var_kind = self.subroutine_table.kind_of(first_identifier)
                var_index = self.subroutine_table.index_of(first_identifier)
                var_type = self.subroutine_table.type_of(first_identifier)
                if var_kind == VarKind.NONE:
                    # lookup in the class table
                    var_kind = self.class_table.kind_of(first_identifier)
                    var_index = self.class_table.index_of(first_identifier)
                    var_type = self.class_table.type_of(first_identifier)
                is_variable = var_kind != VarKind.NONE
                # skip the '.'
                self.tokenizer.advance()
                # if this is a method, we need to push the object as the first arg
                # otherwise, it is a function or static subroutine
                if is_variable:
                    segment = VM_SEGMENT_BY_VAR_KIND[var_kind]
                    self.writer.write_push(segment=segment, index=var_index)
                    subroutine_name = f"{var_type}.{self.tokenizer.identifier()}"
                else:
                    subroutine_name = (
                        f"{first_identifier}.{self.tokenizer.identifier()}"
                    )

                self.tokenizer.advance()
                if self.tokenizer.symbol() != "(":
                    raise Exception
                self.tokenizer.advance()
                self.compile_expression_list()
                if self.tokenizer.symbol() != ")":
                    raise Exception
                self.tokenizer.advance()
                n_args = self.expression_counts.pop()
                if is_variable:
                    n_args += 1
                self.writer.write_call(name=subroutine_name, n_args=n_args)
            else:
                # varName
                var_name = first_identifier
                var_kind = self.subroutine_table.kind_of(var_name)
                var_index = self.subroutine_table.index_of(var_name)
                if var_kind == VarKind.NONE:
                    # lookup in the class table
                    var_kind = self.class_table.kind_of(var_name)
                    var_index = self.class_table.index_of(var_name)

                segment = VM_SEGMENT_BY_VAR_KIND[var_kind]
                self.writer.write_push(segment=segment, index=var_index)
        else:
            raise Exception

    def compile_expression_list(self):
        token_type = self.tokenizer.token_type()
        expression_count = 0
        if token_type == TokenType.INT_CONST:
            self.compile_expression()
        elif token_type == TokenType.STRING_CONST:
            self.compile_expression()
        elif token_type == TokenType.KEYWORD and self.tokenizer.keyword() in (
            TokenKeyword.TRUE,
            TokenKeyword.FALSE,
            TokenKeyword.NULL,
            TokenKeyword.THIS,
        ):
            self.compile_expression()
        elif token_type == TokenType.SYMBOL and self.tokenizer.symbol() == "(":
            self.compile_expression()
        elif token_type == TokenType.SYMBOL and self.tokenizer.symbol() in ("-", "~"):
            self.compile_expression()
        elif token_type == TokenType.IDENTIFIER:
            self.compile_expression()
        else:
            self.expression_counts.append(expression_count)
            return

        expression_count += 1
        while (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ","
        ):
            expression_count += 1
            self.tokenizer.advance()
            self.compile_expression()
        self.expression_counts.append(expression_count)


class VarKind:
    STATIC = "static"
    FIELD = "field"
    ARG = "arg"
    LOCAL = "local"
    NONE = "none"


class VarInfo(NamedTuple):
    var_name: str
    var_type: str
    var_kind: VarKind
    index: int


class SymbolTable:
    def __init__(self):
        self.start_subroutine()

    def start_subroutine(self):
        self.info_by_name: Dict[str, VarInfo] = {}
        self.count_by_kind: DefaultDict[VarKind, int] = defaultdict(int)

    def define(self, var_name: str, var_type: str, var_kind: VarKind):
        if var_name in self.info_by_name:
            raise Exception(f"Variable {var_name} already exists in the SymbolTable")
        index = self.count_by_kind[var_kind]
        self.info_by_name[var_name] = VarInfo(
            var_name=var_name, var_type=var_type, var_kind=var_kind, index=index
        )
        self.count_by_kind[var_kind] += 1

    def var_count(self, var_kind: VarKind):
        return self.count_by_kind[var_kind]

    def kind_of(self, name: str):
        if name not in self.info_by_name:
            return VarKind.NONE
        return self.info_by_name[name].var_kind

    def type_of(self, name: str):
        if name not in self.info_by_name:
            return None
        return self.info_by_name[name].var_type

    def index_of(self, name: str):
        if name not in self.info_by_name:
            return None
        return self.info_by_name[name].index


class VMSegment:
    CONST = "constant"
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


VM_SEGMENT_BY_VAR_KIND = {
    VarKind.STATIC: VMSegment.STATIC,
    VarKind.FIELD: VMSegment.THIS,
    VarKind.ARG: VMSegment.ARG,
    VarKind.LOCAL: VMSegment.LOCAL,
}


class VMArithmetic:
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


class VMWriter:
    def __init__(self, out_file: TextIO):
        self.out_file = out_file

    def write_push(self, segment: VMSegment, index: int):
        self.out_file.write(f"push {segment} {index}\n")

    def write_pop(self, segment: VMSegment, index: int):
        self.out_file.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command: VMArithmetic):
        self.out_file.write(f"{command}\n")

    def write_label(self, label: str):
        self.out_file.write(f"label {label}\n")

    def write_goto(self, label: str):
        self.out_file.write(f"goto {label}\n")

    def write_if(self, label: str):
        self.out_file.write(f"if-goto {label}\n")

    def write_call(self, name: str, n_args: int):
        self.out_file.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_locals: int):
        self.out_file.write(f"function {name} {n_locals}\n")

    def write_return(self):
        self.out_file.write("return\n")

    def close(self):
        self.out_file.close()


if __name__ == "__main__":
    path = sys.argv[1]
    if os.path.isdir(path):
        with os.scandir(path) as it:
            for entry in it:
                if entry.name.endswith(".jack") and entry.is_file():
                    out_path = os.path.splitext(entry.path)[0]
                    out_file = out_path + ".vm"
                    with open(entry.path, "r") as in_file, open(
                        out_file, "w"
                    ) as out_file:
                        tester = CompilationEngine(in_file=in_file, out_file=out_file)
                        tester.compile_class()

    else:
        out_path = os.path.splitext(path)[0]
        out_file = out_path + ".vm"
        with open(path, "r") as in_file, open(out_file, "w") as out_file:
            tester = CompilationEngine(in_file=in_file, out_file=out_file)
            tester.compile_class()
