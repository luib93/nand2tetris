// C_PUSH argument 1
@1
D=A
@ARG
A=D+M
D=M
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

// C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP that 0
@0
D=A
@THAT
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP that 1
@1
D=A
@THAT
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 2
@2
D=A
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

// C_POP argument 0
@0
D=A
@ARG
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// label MAIN_LOOP_START
(MAIN_LOOP_START)

// C_PUSH argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@COMPUTE_ELEMENT
D;JGT

// goto END_PROGRAM
@END_PROGRAM
0;JMP

// label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)

// C_PUSH that 0
@0
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH that 1
@1
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

// C_POP that 2
@2
D=A
@THAT
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 1
@1
D=A
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

// C_POP pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D

// C_PUSH argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 1
@1
D=A
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

// C_POP argument 0
@0
D=A
@ARG
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// goto MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP

// label END_PROGRAM
(END_PROGRAM)

