// function SimpleFunction.test 2
// label SimpleFunction.test
(SimpleFunction.test)

@SP
A = M
M = 0 
@SP
M = M + 1
@SP
A = M
M = 0 
@SP
M = M + 1
// push local 0
@0
D=A
@LCL
A=M+D
D=M
@SP
A = M
M = D 
@SP
M = M + 1

// push local 1
@1
D=A
@LCL
A=M+D
D=M
@SP
A = M
M = D 
@SP
M = M + 1

// add
@SP
AM=M-1
D=M
A=A-1
M=M+D

// not
@SP
A=M-1
M=!M

// push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A = M
M = D 
@SP
M = M + 1

// add
@SP
AM=M-1
D=M
A=A-1
M=M+D

// push argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A = M
M = D 
@SP
M = M + 1

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// return
@LCL
D=M
@R14
M=D
@5
D=A
@R14
D=M-D
A=D
D=M
@R15
M=D
@0
D = A
@ARG
A=M
D=A+D
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R14
M=M-1
A=M
D=M
@THAT
M=D
@R14
M=M-1
A=M
D=M
@THIS
M=D
@R14
M=M-1
A=M
D=M
@ARG
M=D
@R14
M=M-1
A=M
D=M
@LCL
M=D
@R15
A=M
0;JMP

