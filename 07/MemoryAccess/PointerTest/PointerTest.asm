// C_PUSH constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D

// C_PUSH constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D

// C_PUSH constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP this 2
@2
D=A
@THIS
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP that 6
@6
D=A
@THAT
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH pointer 0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1

// C_PUSH this 2
@2
D=A
@THIS
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1

// C_PUSH that 6
@6
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1

