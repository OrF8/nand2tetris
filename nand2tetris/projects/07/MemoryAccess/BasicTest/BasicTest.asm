// push constant 10
@10 // D=10
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop local 0
@0 // D=index
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

// push constant 21
@21 // D=21
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 22
@22 // D=22
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop argument 2
@2 // D=index
D=A
@ARG // D=segment + index
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

// pop argument 1
@1 // D=index
D=A
@ARG // D=segment + index
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

// push constant 36
@36 // D=36
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop this 6
@6 // D=index
D=A
@THIS // D=segment + index
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

// push constant 42
@42 // D=42
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 45
@45 // D=45
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop that 5
@5 // D=index
D=A
@THAT // D=segment + index
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

// pop that 2
@2 // D=index
D=A
@THAT // D=segment + index
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

// push constant 510
@510 // D=510
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop temp 6
@11
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

// push that 5
@5 // D=index
D=A
@THAT // D=segment + index
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

// push argument 1
@1 // D=index
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

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// push this 6
@6 // D=index
D=A
@THIS // D=segment + index
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

// push this 6
@6 // D=index
D=A
@THIS // D=segment + index
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

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// push temp 6
@11
D=M // D=*addr
@SP // *SP=*addr
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

