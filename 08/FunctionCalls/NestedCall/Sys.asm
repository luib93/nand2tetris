// function Sys.init 0
(Sys.init)

// C_PUSH constant 4000
@4000
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

// C_PUSH constant 5000
@5000
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

// call Sys.main 0
@Sys$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(Sys$ret.0)

// C_POP temp 1
@5
D=A
@1
D=D+A
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// label LOOP
(LOOP)

// goto LOOP
@LOOP
0;JMP

// function Sys.main 5
(Sys.main)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 4001
@4001
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

// C_PUSH constant 5001
@5001
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

// C_PUSH constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP local 1
@1
D=A
@LCL
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP local 2
@2
D=A
@LCL
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_POP local 3
@3
D=A
@LCL
D=D+M
@SP
M=M-1
A=M
D=D+M
A=D-M
M=D-A

// C_PUSH constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Sys.add12 1
@Sys$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(Sys$ret.1)

// C_POP temp 0
@5
D=A
@0
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

// C_PUSH local 1
@1
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH local 2
@2
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH local 3
@3
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH local 4
@4
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

// return
@LCL
D=M
@R13
M=D
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP

// function Sys.add12 0
(Sys.add12)

// C_PUSH constant 4002
@4002
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

// C_PUSH constant 5002
@5002
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

// C_PUSH constant 12
@12
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

// return
@LCL
D=M
@R13
M=D
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@1
D=D-A
A=D
D=M
@THAT
M=D
@R13
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@R13
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@R13
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@R14
A=M
0;JMP

