// function Sys.init 0
// label Sys.Sys.init
(Sys.Sys.init)

// push constant 4000
@4000 // D=4000
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop pointer 0
@SP // SP--
AM=M-1
D=M // D = RAM[SP]
@THIS // THIS/THAT=*SP
M=D

// push constant 5000
@5000 // D=5000
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop pointer 1
@SP // SP--
AM=M-1
D=M // D = RAM[SP]
@THAT // THIS/THAT=*SP
M=D

// call Sys.main 0
@Sys$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL \ Push LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG \ Push ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS \ Push THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT \ Push THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP \ ARG = SP - 5 - n_args
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP \ LCL = SP
D=M
@LCL
M=D
@Sys.Sys.main \ goto Sys.Sys.main
0;JMP
(Sys$ret.1)
// pop temp 1
@6
D=A // D=addr
@R13 // R13=addr
M=D
@SP // SP--
AM=M-1
D=M // D=*SP
@R13 // *addr=*SP
A=M
M=D

// label LOOP
(LOOP)

// goto LOOP
@LOOP
0;JMP

// function Sys.main 5
// label Sys.Sys.main
(Sys.Sys.main)

// push constant 0
@0 // D=0
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 0
@0 // D=0
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 0
@0 // D=0
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 0
@0 // D=0
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 0
@0 // D=0
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 4001
@4001 // D=4001
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop pointer 0
@SP // SP--
AM=M-1
D=M // D = RAM[SP]
@THIS // THIS/THAT=*SP
M=D

// push constant 5001
@5001 // D=5001
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop pointer 1
@SP // SP--
AM=M-1
D=M // D = RAM[SP]
@THAT // THIS/THAT=*SP
M=D

// push constant 200
@200 // D=200
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop local 1
@1 // D=index
D=A
@LCL // D=segment + index
A=M+D
D=A
@R13 // R13=addr
M=D
@SP // SP--
AM=M-1
D=M
@R13 // *addr=*SP
A=M
M=D

// push constant 40
@40 // D=40
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop local 2
@2 // D=index
D=A
@LCL // D=segment + index
A=M+D
D=A
@R13 // R13=addr
M=D
@SP // SP--
AM=M-1
D=M
@R13 // *addr=*SP
A=M
M=D

// push constant 6
@6 // D=6
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop local 3
@3 // D=index
D=A
@LCL // D=segment + index
A=M+D
D=A
@R13 // R13=addr
M=D
@SP // SP--
AM=M-1
D=M
@R13 // *addr=*SP
A=M
M=D

// push constant 123
@123 // D=123
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// call Sys.add12 1
@Sys$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL \ Push LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG \ Push ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS \ Push THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT \ Push THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP \ ARG = SP - 5 - n_args
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP \ LCL = SP
D=M
@LCL
M=D
@Sys.Sys.add12 \ goto Sys.Sys.add12
0;JMP
(Sys$ret.2)
// pop temp 0
@12
D=A // D=addr
@R13 // R13=addr
M=D
@SP // SP--
AM=M-1
D=M // D=*SP
@R13 // *addr=*SP
A=M
M=D

// push local 0
@0 // D=index
D=A
@LCL // D=segment + index
A=M+D
D=A
@R13 // R13=addr
M=D
@R13 // D=*addr
A=M
D=M
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push local 1
@1 // D=index
D=A
@LCL // D=segment + index
A=M+D
D=A
@R13 // R13=addr
M=D
@R13 // D=*addr
A=M
D=M
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push local 2
@2 // D=index
D=A
@LCL // D=segment + index
A=M+D
D=A
@R13 // R13=addr
M=D
@R13 // D=*addr
A=M
D=M
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push local 3
@3 // D=index
D=A
@LCL // D=segment + index
A=M+D
D=A
@R13 // R13=addr
M=D
@R13 // D=*addr
A=M
D=M
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push local 4
@4 // D=index
D=A
@LCL // D=segment + index
A=M+D
D=A
@R13 // R13=addr
M=D
@R13 // D=*addr
A=M
D=M
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
@LCL // frame = LCL
D=M
@R13 // R13=frame
M=D
@5 // return_address = *(frame-5)
A=D-A
D=M
@R14 // R14=return_address
M=D
@SP // *ARG = pop()
AM=M-1
D=M
@ARG
A=M
M=D
@ARG // SP = ARG + 1
D=M+1
@SP
M=D
@R13 // THAT = *(frame-1)
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13 // THIS = *(frame-2)
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13 // ARG = *(frame-3)
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13 // LCL = *(frame-4)
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14 // goto return_address
A=M
0;JMP
// function Sys.add12 0
// label Sys.Sys.add12
(Sys.Sys.add12)

// push constant 4002
@4002 // D=4002
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop pointer 0
@SP // SP--
AM=M-1
D=M // D = RAM[SP]
@THIS // THIS/THAT=*SP
M=D

// push constant 5002
@5002 // D=5002
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop pointer 1
@SP // SP--
AM=M-1
D=M // D = RAM[SP]
@THAT // THIS/THAT=*SP
M=D

// push argument 0
@0 // D=index
D=A
@ARG // D=segment + index
A=M+D
D=A
@R13 // R13=addr
M=D
@R13 // D=*addr
A=M
D=M
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 12
@12 // D=12
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

// return
@LCL // frame = LCL
D=M
@R13 // R13=frame
M=D
@5 // return_address = *(frame-5)
A=D-A
D=M
@R14 // R14=return_address
M=D
@SP // *ARG = pop()
AM=M-1
D=M
@ARG
A=M
M=D
@ARG // SP = ARG + 1
D=M+1
@SP
M=D
@R13 // THAT = *(frame-1)
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13 // THIS = *(frame-2)
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13 // ARG = *(frame-3)
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13 // LCL = *(frame-4)
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14 // goto return_address
A=M
0;JMP
