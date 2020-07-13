// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP)
@i // row counter
M=0
@8192
D=A
@n // total rows
M=D

@KBD
D=M
@FILL
D;JNE // if the keyboard input is not 0 then jump to fill logic

(CLEAR)
@i
D=M
@n
D=D-M
@LOOP
D;JEQ // if we went through the last row, go back to the beginning

@i
D=M
@SCREEN
A=D+A
M=0 // set current row to 0

@i
M=M+1 // increment row counter
@CLEAR
0;JMP // jump to clear 

(FILL)
@i
D=M
@n
D=D-M
@LOOP
D;JEQ // if we went through the last row, go back to the beginning

@i
D=M
@SCREEN
A=D+A
M=-1 // set current row to -1

@i
M=M+1 // increment row counter
@FILL
0;JMP // jump to fill