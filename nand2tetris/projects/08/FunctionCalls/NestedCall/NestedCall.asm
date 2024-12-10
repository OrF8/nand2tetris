// bootstrap code
@256
D=A
@SP
M=D
// call Sys.init 0
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

// label Sys$ret.1
(Sys$ret.1)


// function Sys.init 0
// label Sys.init
(Sys.init)

// push constant 4000
@4000
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// pop pointer 0
@0
D = A
@3
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

// push constant 5000
@5000
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// pop pointer 1
@1
D = A
@3
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

// call Sys.main 0
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
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// goto Sys.main
@Sys.main
0;JMP

// label Sys$ret.2
(Sys$ret.2)

// pop temp 1
@1
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

// label LOOP
(LOOP)

// goto LOOP
@LOOP
0;JMP

// function Sys.main 5
// label Sys.main
(Sys.main)

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
@SP
A = M
M = 0 
@SP
M = M + 1
// push constant 4001
@4001
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// pop pointer 0
@0
D = A
@3
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

// push constant 5001
@5001
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// pop pointer 1
@1
D = A
@3
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

// push constant 200
@200
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// pop local 1
@1
D = A
@LCL
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

// push constant 40
@40
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// pop local 2
@2
D = A
@LCL
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

// push constant 6
@6
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// pop local 3
@3
D = A
@LCL
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

// push constant 123
@123
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// call Sys.add12 1
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
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
// goto Sys.add12
@Sys.add12
0;JMP

// label Sys$ret.3
(Sys$ret.3)

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

// push local 2
@2
D=A
@LCL
A=M+D
D=M
@SP
A = M
M = D 
@SP
M = M + 1

// push local 3
@3
D=A
@LCL
A=M+D
D=M
@SP
A = M
M = D 
@SP
M = M + 1

// push local 4
@4
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

// add
@SP
AM=M-1
D=M
A=A-1
M=M+D

// add
@SP
AM=M-1
D=M
A=A-1
M=M+D

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

// function Sys.add12 0
// label Sys.add12
(Sys.add12)

// push constant 4002
@4002
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// pop pointer 0
@0
D = A
@3
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

// push constant 5002
@5002
D=A
@SP
A = M
M = D 
@SP
M = M + 1

// pop pointer 1
@1
D = A
@3
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

// push constant 12
@12
D=A
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

