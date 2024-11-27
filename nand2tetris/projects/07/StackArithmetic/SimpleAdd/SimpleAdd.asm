// push constant 7
@7 // D=7
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 8
@8 // D=8
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// add
@SP
AM=M-1
D=M
A=A-1
M=M+D

