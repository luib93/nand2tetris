// C_PUSH constant 10
@10
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

// C_PUSH constant 21
@21
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 22
@22
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP argument 2
@2
D=A
@ARG
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_POP argument 1
@1
D=A
@ARG
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH constant 36
@36
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP this 6
@6
D=A
@THIS
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH constant 42
@42
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 45
@45
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP that 5
@5
D=A
@THAT
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

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

// C_PUSH constant 510
@510
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP temp 6
@5
D=A
@6
D=D+A
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

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

// C_PUSH that 5
@5
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

// C_PUSH this 6
@6
D=A
@THIS
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH this 6
@6
D=A
@THIS
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

// C_PUSH temp 6
@6
D=A
@5
A=D+A
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

