// push constant 3030
@3030 // D=3030
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

// push constant 3040
@3040 // D=3040
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

// push constant 32
@32 // D=32
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop this 2
@2 // D=index
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

// push constant 46
@46 // D=46
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// pop that 6
@6 // D=index
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

// push pointer 0
@THIS // D=THIS/THAT
D=M
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push pointer 1
@THAT // D=THIS/THAT
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

// push this 2
@2 // D=index
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

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// push that 6
@6 // D=index
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

