// bootstrap code
@256
D=A
@SP
M=D
// call Sys.init 0
@Main$ret.1
D=A
@SP
A = M
M = D 
@SP
M = M + 1
@LCL
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@ARG
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@THIS
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@THAT
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// goto Sys.init
@Sys.init
0;JMP

// label Main$ret.1
(Main$ret.1)


// function Main.fibonacci 0
// label Main.fibonacci
(Main.fibonacci)

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

// push constant 2
@2
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@Main.TRUE.0
D;JLT
@SP
A=M-1
M=0
@Main.END.0
0;JMP
(Main.TRUE.0)
@SP
A=M-1
M=-1
(Main.END.0)

// if-goto IF_TRUE
@SP
AM=M-1
D=M
@IF_TRUE
D;JNE

// goto IF_FALSE
@IF_FALSE
0;JMP

// label IF_TRUE
(IF_TRUE)

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

// label IF_FALSE
(IF_FALSE)

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

// push constant 2
@2
D=A
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

// call Main.fibonacci 1
@Main$ret.2
D=A
@SP
A = M
M = D 
@SP
M = M + 1
@LCL
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@ARG
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@THIS
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@THAT
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// goto Main.fibonacci
@Main.fibonacci
0;JMP

// label Main$ret.2
(Main$ret.2)

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

// push constant 1
@1
D=A
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

// call Main.fibonacci 1
@Main$ret.3
D=A
@SP
A = M
M = D 
@SP
M = M + 1
@LCL
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@ARG
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@THIS
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@THAT
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// goto Main.fibonacci
@Main.fibonacci
0;JMP

// label Main$ret.3
(Main$ret.3)

// add
@SP
AM=M-1
D=M
A=A-1
M=M+D

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

// function Sys.init 0
// label Sys.init
(Sys.init)

// push constant 4
@4
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// call Main.fibonacci 1
@Sys$ret.1
D=A
@SP
A = M
M = D 
@SP
M = M + 1
@LCL
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@ARG
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@THIS
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@THAT
D=M
@SP
A = M
M = D 
@SP
M = M + 1
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// goto Main.fibonacci
@Main.fibonacci
0;JMP

// label Sys$ret.1
(Sys$ret.1)

// label WHILE
(WHILE)

// goto WHILE
@WHILE
0;JMP

