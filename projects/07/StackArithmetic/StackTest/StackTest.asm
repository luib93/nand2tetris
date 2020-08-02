// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LABEL0
D;JNE
@SP
A=M
M=-1
@LABEL1
0;JMP
(LABEL0)
@SP
A=M
M=0
(LABEL1)
@SP
M=M+1

// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LABEL2
D;JNE
@SP
A=M
M=-1
@LABEL3
0;JMP
(LABEL2)
@SP
A=M
M=0
(LABEL3)
@SP
M=M+1

// C_PUSH constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LABEL4
D;JNE
@SP
A=M
M=-1
@LABEL5
0;JMP
(LABEL4)
@SP
A=M
M=0
(LABEL5)
@SP
M=M+1

// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LABEL6
D;JGE
@SP
A=M
M=-1
@LABEL7
0;JMP
(LABEL6)
@SP
A=M
M=0
(LABEL7)
@SP
M=M+1

// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LABEL8
D;JGE
@SP
A=M
M=-1
@LABEL9
0;JMP
(LABEL8)
@SP
A=M
M=0
(LABEL9)
@SP
M=M+1

// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LABEL10
D;JGE
@SP
A=M
M=-1
@LABEL11
0;JMP
(LABEL10)
@SP
A=M
M=0
(LABEL11)
@SP
M=M+1

// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LABEL12
D;JLE
@SP
A=M
M=-1
@LABEL13
0;JMP
(LABEL12)
@SP
A=M
M=0
(LABEL13)
@SP
M=M+1

// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LABEL14
D;JLE
@SP
A=M
M=-1
@LABEL15
0;JMP
(LABEL14)
@SP
A=M
M=0
(LABEL15)
@SP
M=M+1

// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

// gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@LABEL16
D;JLE
@SP
A=M
M=-1
@LABEL17
0;JMP
(LABEL16)
@SP
A=M
M=0
(LABEL17)
@SP
M=M+1

// C_PUSH constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

// C_PUSH constant 53
@53
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

// C_PUSH constant 112
@112
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

// neg
@SP
M=M-1
A=M
M=-M
@SP
M=M+1

// and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D&M
@SP
M=M+1

// C_PUSH constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

// or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D|M
@SP
M=M+1

// not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1

