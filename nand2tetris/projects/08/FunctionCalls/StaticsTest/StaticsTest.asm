// bootstrap code
@256
D=A
@SP
M=D
// call Sys.init 0
@Class1$ret.1
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

// label Class1$ret.1
(Class1$ret.1)


// function Class1.set 0
// label Class1.set
(Class1.set)

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

// pop static 0
@SP
AM=M-1
D=M
@Class1.0
M=D

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

// pop static 1
@SP
AM=M-1
D=M
@Class1.1
M=D

// push constant 0
@0
D=A
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

// function Class1.get 0
// label Class1.get
(Class1.get)

// push static 0
@Class1.0
D=M
@SP
A = M
M = D 
@SP
M = M + 1

// push static 1
@Class1.1
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

// function Class2.set 0
// label Class2.set
(Class2.set)

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

// pop static 0
@SP
AM=M-1
D=M
@Class2.0
M=D

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

// pop static 1
@SP
AM=M-1
D=M
@Class2.1
M=D

// push constant 0
@0
D=A
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

// function Class2.get 0
// label Class2.get
(Class2.get)

// push static 0
@Class2.0
D=M
@SP
A = M
M = D 
@SP
M = M + 1

// push static 1
@Class2.1
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

// function Sys.init 0
// label Sys.init
(Sys.init)

// push constant 6
@6
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// push constant 8
@8
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// call Class1.set 2
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
@7
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// goto Class1.set
@Class1.set
0;JMP

// label Sys$ret.1
(Sys$ret.1)

// pop temp 0
@0
D = A
@5
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

// push constant 23
@23
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// push constant 15
@15
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// call Class2.set 2
@Sys$ret.2
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
@7
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// goto Class2.set
@Class2.set
0;JMP

// label Sys$ret.2
(Sys$ret.2)

// pop temp 0
@0
D = A
@5
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

// call Class1.get 0
@Sys$ret.3
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
// goto Class1.get
@Class1.get
0;JMP

// label Sys$ret.3
(Sys$ret.3)

// call Class2.get 0
@Sys$ret.4
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
// goto Class2.get
@Class2.get
0;JMP

// label Sys$ret.4
(Sys$ret.4)

// label WHILE
(WHILE)

// goto WHILE
@WHILE
0;JMP

