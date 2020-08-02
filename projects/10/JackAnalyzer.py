import os, sys, re
from typing import TextIO, Optional
import html
from functools import wraps

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


class JackTokenizerTester:
    def __init__(self, in_file: TextIO, out_file: TextIO):
        self.tokenizer = JackTokenizer(in_file)

    def execute(self):
        out_file.write("<tokens>\n")
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            token_type = self.tokenizer.token_type()
            if token_type == TokenType.KEYWORD:
                keyword = self.tokenizer.keyword()
                out_file.write(f"<keyword> {keyword} </keyword>\n")
            elif token_type == TokenType.SYMBOL:
                symbol = self.tokenizer.symbol()
                out_file.write(f"<symbol> {html.escape(symbol)} </symbol>\n")
            elif token_type == TokenType.IDENTIFIER:
                identifier = self.tokenizer.identifier()
                out_file.write(f"<identifier> {identifier} </identifier>\n")
            elif token_type == TokenType.INT_CONST:
                int_val = self.tokenizer.int_val()
                out_file.write(f"<integerConstant> {int_val} </integerConstant>\n")
            elif token_type == TokenType.STRING_CONST:
                string_val = self.tokenizer.string_val()
                out_file.write(f"<stringConstant> {string_val} </stringConstant>\n")

        out_file.write("</tokens>\n")


class CompilationEngine:
    def __init__(self, in_file: TextIO, out_file: TextIO):
        self.tokenizer: JackTokenizer = JackTokenizer(in_file)
        self.out_file = out_file
        self.current_level = 0
        self.tokenizer.advance()

    def _write(self, line):
        self.out_file.write(' ' * (self.current_level - 1) + f'{line}\n')

    def _write_symbol(self):
        self._write(f"<symbol> {html.escape(self.tokenizer.symbol())} </symbol>")

    def _write_keyword(self):
        self._write(f"<keyword> {self.tokenizer.keyword()} </keyword>")

    def _write_identifier(self, identifier: str = None):
        if not identifier:
            identifier = self.tokenizer.identifier()
        self._write(
            f"<identifier> {identifier} </identifier>"
        )

    def compile_class(self):
        self._write(f"<class>")
        if self.tokenizer.keyword() != TokenKeyword.CLASS:
            raise Exception(f"Unexpected token {self.tokenizer.keyword()}")
        self._write_keyword()

        self.tokenizer.advance()
        self._write_identifier()

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "{":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

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
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self._write(f"</class>")

    def compile_class_var_dec(self):
        self._write(f"<classVarDec>")
        if self.tokenizer.keyword() in (TokenKeyword.STATIC, TokenKeyword.FIELD):
            self._write_keyword()
        else:
            raise Exception(f"Unexpected keyword {self.tokenizer.keyword()}")

        # handle type
        self.tokenizer.advance()
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            if self.tokenizer.keyword() in (
                TokenKeyword.INT,
                TokenKeyword.CHAR,
                TokenKeyword.BOOLEAN,
            ):
                self._write_keyword()
            else:
                raise Exception(f"Unexpected keyword {self.tokenizer.keyword()}")
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            self._write_identifier()
        else:
            raise Exception(f"Unexpected token type {self.tokenizer.token_type()}")

        self.tokenizer.advance()
        self._write_identifier()

        self.tokenizer.advance()
        while (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ","
        ):
            self._write_symbol()

            self.tokenizer.advance()
            self._write_identifier()
            self.tokenizer.advance()

        if self.tokenizer.symbol() != ";":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self._write(f"</classVarDec>")
        self.tokenizer.advance()

    def compile_subroutine_dec(self):
        self._write(f"<subroutineDec>")
        if self.tokenizer.keyword() in (
            TokenKeyword.CONSTRUCTOR,
            TokenKeyword.FUNCTION,
            TokenKeyword.METHOD,
        ):
            self._write_keyword()
        else:
            raise Exception(f"Unexpected token {self.tokenizer.keyword()}")

        self.tokenizer.advance()
        if self.tokenizer.token_type() == TokenType.IDENTIFIER:
            self._write_identifier()
        elif self.tokenizer.token_type() == TokenType.KEYWORD:
            if self.tokenizer.keyword() in (
                TokenKeyword.VOID,
                TokenKeyword.INT,
                TokenKeyword.CLASS,
                TokenKeyword.BOOLEAN,
            ):
                self._write_keyword()
            else:
                raise Exception(f"Unexpected keyword {self.tokenizer.keyword()}")
        else:
            raise Exception(f"Unexpected token type {self.tokenizer.token_type()}")

        self.tokenizer.advance()
        self._write_identifier()
        self.tokenizer.advance()
        if self.tokenizer.symbol() != "(":
            raise Exception
        self._write_symbol()

        self.tokenizer.advance()
        self.compile_parameter_list()
        if self.tokenizer.symbol() != ")":
            raise Exception
        self._write_symbol()

        self.tokenizer.advance()
        self.compile_subroutine_body()

        self._write(f"</subroutineDec>")

    def compile_parameter_list(self):
        self._write(f"<parameterList>")
        # handle type
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            if self.tokenizer.keyword() in (
                TokenKeyword.INT,
                TokenKeyword.CHAR,
                TokenKeyword.BOOLEAN,
            ):
                self._write_keyword()
            else:
                raise Exception(f"Unexpected keyword {self.tokenizer.keyword()}")
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
            self._write_identifier()
        else:
            self._write(f"</parameterList>")
            return

        self.tokenizer.advance()
        self._write_identifier()

        self.tokenizer.advance()
        while (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ","
        ):
            self._write_symbol()
            self.tokenizer.advance()
            # handle type
            if self.tokenizer.token_type() == TokenType.KEYWORD:
                if self.tokenizer.keyword() in (
                    TokenKeyword.INT,
                    TokenKeyword.CHAR,
                    TokenKeyword.BOOLEAN,
                ):
                    self._write_keyword()
                else:
                    raise Exception(f"Unexpected keyword {self.tokenizer.keyword()}")
            elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
                self._write_identifier()
            else:
                raise Exception

            self.tokenizer.advance()
            self._write_identifier()
            self.tokenizer.advance()
        self._write(f"</parameterList>")

    def compile_subroutine_body(self):
        self._write(f"<subroutineBody>")
        if self.tokenizer.symbol() != "{":
            raise Exception
        self._write_symbol()

        self.tokenizer.advance()
        while (
            self.tokenizer.token_type() == TokenType.KEYWORD
            and self.tokenizer.keyword() == TokenKeyword.VAR
        ):
            self.compile_var_dec()

        self.compile_statements()
        if self.tokenizer.symbol() != "}":
            raise Exception
        self._write_symbol()

        self._write(f"</subroutineBody>")
        self.tokenizer.advance()

    def compile_var_dec(self):
        self._write(f"<varDec>")
        if self.tokenizer.keyword() != TokenKeyword.VAR:
            raise Exception
        self._write_keyword()

        self.tokenizer.advance()
        # handle type
        if self.tokenizer.token_type() == TokenType.KEYWORD:
            if self.tokenizer.keyword() in (
                TokenKeyword.INT,
                TokenKeyword.CHAR,
                TokenKeyword.BOOLEAN,
            ):
                self._write_keyword()
            else:
                raise Exception(f"Unexpected keyword {self.tokenizer.keyword()}")
        elif self.tokenizer.token_type() == TokenType.IDENTIFIER:
                self._write_identifier()
        else:
            raise Exception

        self.tokenizer.advance()
        self._write_identifier()

        self.tokenizer.advance()
        while (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ","
        ):
            self._write_symbol()

            self.tokenizer.advance()
            self._write_identifier()
            self.tokenizer.advance()

        if self.tokenizer.symbol() != ";":
            raise Exception
        self._write_symbol()
        self.tokenizer.advance()
        self._write(f"</varDec>")

    def compile_statements(self):
        self._write(f"<statements>")
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
        self._write(f"</statements>")

    def compile_let(self):
        self._write(f"<letStatement>")
        if self.tokenizer.keyword() != TokenKeyword.LET:
            raise Exception(f"Unexpected token {self.tokenizer.keyword()}")
        self._write_keyword()

        self.tokenizer.advance()
        self._write_identifier()

        self.tokenizer.advance()
        if self.tokenizer.symbol() == "[":
            self._write_symbol()
            self.tokenizer.advance()
            self.compile_expression()
            if self.tokenizer.symbol() != "]":
                raise Exception(f"Unexpected token {self.tokenizer.token_type()}")
            self._write_symbol()
            self.tokenizer.advance()
        if self.tokenizer.symbol() != "=":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        self.compile_expression()

        if self.tokenizer.symbol() != ";":
            raise Exception(f"Unexpected token {self.tokenizer.symbol()}")
        self._write_symbol()

        self._write(f"</letStatement>")
        self.tokenizer.advance()

    def compile_if(self):
        self._write(f"<ifStatement>")
        if self.tokenizer.keyword() != TokenKeyword.IF:
            raise Exception(f"Unexpected token {self.tokenizer.keyword()}")
        self._write_keyword()

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "(":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        self.compile_expression()

        if self.tokenizer.symbol() != ")":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "{":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        self.compile_statements()

        if self.tokenizer.symbol() != "}":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        if (
            self.tokenizer.token_type() == TokenType.KEYWORD
            and self.tokenizer.keyword() == TokenKeyword.ELSE
        ):
            self._write_keyword()
            self.tokenizer.advance()
            if self.tokenizer.symbol() != "{":
                raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
            self._write_symbol()

            self.tokenizer.advance()
            self.compile_statements()

            if self.tokenizer.symbol() != "}":
                raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
            self._write_symbol()
            self.tokenizer.advance()

        self._write(f"</ifStatement>")

    def compile_while(self):
        self._write(f"<whileStatement>")
        if self.tokenizer.keyword() != TokenKeyword.WHILE:
            raise Exception(f"Unexpected token {self.tokenizer.keyword()}")
        self._write_keyword()

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "(":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        self.compile_expression()

        if self.tokenizer.symbol() != ")":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        if self.tokenizer.symbol() != "{":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        self.compile_statements()

        if self.tokenizer.symbol() != "}":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self._write(f"</whileStatement>")
        self.tokenizer.advance()

    def compile_do(self):
        self._write(f"<doStatement>")
        if self.tokenizer.keyword() != TokenKeyword.DO:
            raise Exception(f"Unexpected token {self.tokenizer.keyword()}")
        self._write_keyword()

        # handle subroutine call
        self.tokenizer.advance()
        self._write_identifier()

        self.tokenizer.advance()
        if self.tokenizer.symbol() == ".":
            self._write_symbol()

            self.tokenizer.advance()
            self._write_identifier()
            self.tokenizer.advance()

        if self.tokenizer.symbol() != "(":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        self.compile_expression_list()

        if self.tokenizer.symbol() != ")":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self.tokenizer.advance()
        if self.tokenizer.symbol() != ";":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self._write(f"</doStatement>")
        self.tokenizer.advance()

    def compile_return(self):
        self._write(f"<returnStatement>")
        if self.tokenizer.keyword() != TokenKeyword.RETURN:
            raise Exception(f"Unexpected token {self.tokenizer.keyword()}")
        self._write_keyword()

        self.tokenizer.advance()
        if (
            self.tokenizer.token_type() == TokenType.SYMBOL
            and self.tokenizer.symbol() == ";"
        ):
            self._write_symbol()
            self._write(f"</returnStatement>")
            self.tokenizer.advance()
            return

        self.compile_expression()
        if self.tokenizer.symbol() != ";":
            raise Exception(f"Unexpected symbol {self.tokenizer.symbol()}")
        self._write_symbol()

        self._write(f"</returnStatement>")
        self.tokenizer.advance()

    def compile_expression(self):
        self._write("<expression>")
        self.compile_term()
        while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() in ('+', '-', '*', '/', '&', '|', '<', '>', '='):
            self._write_symbol()
            self.tokenizer.advance()
            self.compile_term()
        self._write("</expression>")

    def compile_term(self):
        self._write("<term>")
        token_type = self.tokenizer.token_type()
        if token_type == TokenType.INT_CONST:
            self._write(f'<integerConstant> {self.tokenizer.int_val()} </integerConstant>')
            self.tokenizer.advance()
        elif token_type == TokenType.STRING_CONST:
            self._write(f'<stringConstant> {self.tokenizer.string_val()} </stringConstant>')
            self.tokenizer.advance()
        elif token_type == TokenType.KEYWORD and self.tokenizer.keyword() in (TokenKeyword.TRUE, TokenKeyword.FALSE, TokenKeyword.NULL, TokenKeyword.THIS):
            self._write_keyword()
            self.tokenizer.advance()
        elif token_type == TokenType.SYMBOL and self.tokenizer.symbol() == '(':
            self._write_symbol()
            self.tokenizer.advance()
            self.compile_expression()
            if self.tokenizer.symbol() != ')':
                raise Exception
            self._write_symbol()
            self.tokenizer.advance()
        elif token_type == TokenType.SYMBOL and self.tokenizer.symbol() in ('-', '~'):
            self._write_symbol()
            self.tokenizer.advance()
            self.compile_term()
        elif token_type  == TokenType.IDENTIFIER:
            curr = self.tokenizer.identifier()
            self.tokenizer.advance()

            if self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == '[':
                self._write_identifier(curr)
                self._write_symbol()
                self.tokenizer.advance()
                self.compile_expression()
                if self.tokenizer.symbol() != ']':
                    raise Exception
                self._write_symbol()
                self.tokenizer.advance()
            elif self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == '(':
            # handle subroutine call
                self._write_identifier(curr)
                self._write_symbol()
                self.tokenizer.advance()
                self.compile_expression_list()
                if self.tokenizer.symbol() != ')':
                    raise Exception
                self._write_symbol()
                self.tokenizer.advance()
            elif self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == '.':
            # handle subroutine call
                self._write_identifier(curr)
                self._write_symbol()
                self.tokenizer.advance()
                self._write_identifier()
                self.tokenizer.advance()
                if self.tokenizer.symbol() != '(':
                    raise Exception
                self._write_symbol()
                self.tokenizer.advance()
                self.compile_expression_list()
                if self.tokenizer.symbol() != ')':
                    raise Exception
                self._write_symbol()
                self.tokenizer.advance()
            else:
                self._write_identifier(curr)
        else:
            raise Exception
        self._write("</term>")

    def compile_expression_list(self):
        self._write("<expressionList>")
        token_type = self.tokenizer.token_type()
        if token_type == TokenType.INT_CONST:
            self.compile_expression()
        elif token_type == TokenType.STRING_CONST:
            self.compile_expression()
        elif token_type == TokenType.KEYWORD and self.tokenizer.keyword() in (TokenKeyword.TRUE, TokenKeyword.FALSE, TokenKeyword.NULL, TokenKeyword.THIS):
            self.compile_expression()
        elif token_type == TokenType.SYMBOL and self.tokenizer.symbol() == '(':
            self.compile_expression()
        elif token_type == TokenType.SYMBOL and self.tokenizer.symbol() in ('-', '~'):
            self.compile_expression()
        elif token_type  == TokenType.IDENTIFIER:
            self.compile_expression()
        else:
            self._write("</expressionList>")
            return
        while self.tokenizer.token_type() == TokenType.SYMBOL and self.tokenizer.symbol() == ',':
            self._write_symbol()
            self.tokenizer.advance()
            self.compile_expression()
        self._write("</expressionList>")


if __name__ == "__main__":
    path = sys.argv[1]
    if os.path.isdir(path):
        with os.scandir(path) as it:
            for entry in it:
                if entry.name.endswith(".jack") and entry.is_file():
                    out_path = os.path.splitext(entry.path)[0]
                    out_file = out_path + ".my.xml"
                    with open(entry.path, "r") as in_file, open(
                        out_file, "w"
                    ) as out_file:
                        tester = CompilationEngine(in_file=in_file, out_file=out_file)
                        tester.compile_class()

    else:
        out_path = os.path.splitext(path)[0]
        out_file = out_path + ".my.xml"
        with open(path, "r") as in_file, open(out_file, "w") as out_file:
            tester = CompilationEngine(in_file=in_file, out_file=out_file)
            tester.compile_class()
