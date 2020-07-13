// C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP local 0
@0
D=A
@LCL
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// label LOOP_START
(LOOP_START)

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

// C_PUSH local 0
@0
D=A
@LCL
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

// C_POP local 0
@0
D=A
@LCL
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

// if-goto LOOP_START
@SP
M=M-1
A=M
D=M
@LOOP_START
D;JGT

// C_PUSH local 0
@0
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

