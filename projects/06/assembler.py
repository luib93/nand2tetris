class Parser:
    def __init__(self, filepath):
        super().__init__()
        self.lines: List[str] = []
        self.current_line: int = -1

        with open(filepath, 'r') as file:
            for line in file.readlines():
                cleaned_line = line.strip()
                if cleaned_line.startswith('//'):
                    continue
                if cleaned_line == '':
                    continue
                self.lines.append(cleaned_line.split('//')[0].strip())
    
    def has_more_commands(self):
        return self.current_line < len(self.lines) - 1
    
    def advance(self):
        if not self.has_more_commands():
            raise Exception('No more commands are available')
        self.current_line += 1
    
    def command_type(self):
        curr: str = self.lines[self.current_line]
        if curr.startswith('@'):
            return 'A_COMMAND'
        if curr.startswith('('):
            return 'L_COMMAND'
        return 'C_COMMAND'
    
    def symbol(self):
        curr: str = self.lines[self.current_line]
        if self.command_type() == 'A_COMMAND':
            return curr[1:]
        if self.command_type() == 'L_COMMAND':
            return curr.replace('(', '').replace(')', '')
        return None

    def dest(self):
        curr: str = self.lines[self.current_line]
        if self.command_type() != 'C_COMMAND':
            return None
        split = curr.split('=')
        if len(split) == 1:
            return None
        return split[0]
    
    def comp(self):
        curr: str = self.lines[self.current_line]
        if self.command_type() != 'C_COMMAND':
            return None
        # get text between the '=' and ';'
        has_dest = '=' in curr
        curr = curr.split('=')[1] if has_dest else curr
        has_jmp = ';' in curr
        curr = curr.split(';')[0] if has_jmp else curr
        return curr
    
    def jmp(self):
        curr: str = self.lines[self.current_line]
        if self.command_type() != 'C_COMMAND':
            return None
        split = curr.split(';')
        if len(split) == 1:
            return None
        return split[1]

class Code:
    @staticmethod
    def dest(mnemonic: str):
        if not mnemonic:
            return '000'
        dest_map: Dict[str, str] = {            
            'null': '000',
            'M': '001',
            'D': '010',
            'MD': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111',
        }
        return dest_map[mnemonic]

    @staticmethod
    def comp(mnemonic: str):
        if not mnemonic:
            return '0000000'
        comp_map: Dict[str, str] = {            
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            '!D': '0001101',
            '!A': '0110001',
            '-D': '0001111',
            '-A': '0110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'D+A': '0000010',
            'D-A': '0010011',
            'A-D': '0000111',
            'D&A': '0000000',
            'D|A': '0010101',
            'M': '1110000',
            '!M': '1110001',
            '-M': '1110011',
            'M+1': '1110111',
            'M-1': '1110010',
            'D+M': '1000010',
            'D-M': '1010011',
            'M-D': '1000111',
            'D&M': '1000000',
            'D|M': '1010101',
        }
        return comp_map[mnemonic]

    @staticmethod
    def jump(mnemonic: str):
        if not mnemonic:
            return '000'
        jmp_map: Dict[str, str] = {            
            'null': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }
        return jmp_map[mnemonic]

class SymbolTable:
    def __init__(self):
        super().__init__()
        self.entries: Dict[str, int] = {
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SCREEN': 16384,
            'KBD': 24576,
        }

    def add_entry(self, symbol: str, address: int):
        self.entries[symbol] = address

    def contains(self, symbol: str) -> bool:
        return symbol in self.entries
    
    def get_address(self, symbol: str) -> int:
        return self.entries.get(symbol)


if __name__ == "__main__":
    # init
    st = SymbolTable()
    curr_address = -1
    filepath = './Prog.asm'
    out_filepath = './Prog.hack'
    parser = Parser(filepath)
    
    # first pass (labels)
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type in ('A_COMMAND', 'C_COMMAND'):
            curr_address += 1
            continue
        
        symbol = parser.symbol()
        st.add_entry(symbol, curr_address + 1)

    # second pass (variables)
    curr_address = 16
    parser = Parser(filepath)

    with open(out_filepath, 'w') as file:
        while parser.has_more_commands():
            parser.advance()
            command_type = parser.command_type()
            if command_type == 'A_COMMAND':        
                symbol = parser.symbol()
                # see if its a number before looking at the S-T
                try:
                    parsed = int(symbol)
                    asm_line = '0{0:015b}\n'.format(parsed)
                    file.write(asm_line)
                except:
                    if not st.contains(symbol):
                        st.add_entry(symbol, curr_address)
                        curr_address += 1
                    symbol_address = st.get_address(symbol)
                    asm_line = '0{0:015b}\n'.format(symbol_address)
                    file.write(asm_line)
                continue

            if command_type == 'C_COMMAND':
                dest = parser.dest()
                comp = parser.comp()
                jmp = parser.jmp()

                asm_line = '111' + Code.comp(comp) + Code.dest(dest) + Code.jump(jmp) + '\n'
                file.write(asm_line)
                continue
