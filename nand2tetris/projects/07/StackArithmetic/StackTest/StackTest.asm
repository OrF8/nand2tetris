// push constant 17
@17 // D=17
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 17
@17 // D=17
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.TRUE.1
D;JEQ
@SP
A=M-1
M=0
@StackTest.END.1
0;JMP
(StackTest.TRUE.1)
@SP
A=M-1
M=-1
(StackTest.END.1)

// push constant 17
@17 // D=17
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 16
@16 // D=16
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.TRUE.2
D;JEQ
@SP
A=M-1
M=0
@StackTest.END.2
0;JMP
(StackTest.TRUE.2)
@SP
A=M-1
M=-1
(StackTest.END.2)

// push constant 16
@16 // D=16
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 17
@17 // D=17
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.TRUE.3
D;JEQ
@SP
A=M-1
M=0
@StackTest.END.3
0;JMP
(StackTest.TRUE.3)
@SP
A=M-1
M=-1
(StackTest.END.3)

// push constant 892
@892 // D=892
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 891
@891 // D=891
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.TRUE.4
D;JLT
@SP
A=M-1
M=0
@StackTest.END.4
0;JMP
(StackTest.TRUE.4)
@SP
A=M-1
M=-1
(StackTest.END.4)

// push constant 891
@891 // D=891
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 892
@892 // D=892
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.TRUE.5
D;JLT
@SP
A=M-1
M=0
@StackTest.END.5
0;JMP
(StackTest.TRUE.5)
@SP
A=M-1
M=-1
(StackTest.END.5)

// push constant 891
@891 // D=891
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 891
@891 // D=891
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.TRUE.6
D;JLT
@SP
A=M-1
M=0
@StackTest.END.6
0;JMP
(StackTest.TRUE.6)
@SP
A=M-1
M=-1
(StackTest.END.6)

// push constant 32767
@32767 // D=32767
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 32766
@32766 // D=32766
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.TRUE.7
D;JGT
@SP
A=M-1
M=0
@StackTest.END.7
0;JMP
(StackTest.TRUE.7)
@SP
A=M-1
M=-1
(StackTest.END.7)

// push constant 32766
@32766 // D=32766
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 32767
@32767 // D=32767
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.TRUE.8
D;JGT
@SP
A=M-1
M=0
@StackTest.END.8
0;JMP
(StackTest.TRUE.8)
@SP
A=M-1
M=-1
(StackTest.END.8)

// push constant 32766
@32766 // D=32766
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 32766
@32766 // D=32766
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.TRUE.9
D;JGT
@SP
A=M-1
M=0
@StackTest.END.9
0;JMP
(StackTest.TRUE.9)
@SP
A=M-1
M=-1
(StackTest.END.9)

// push constant 57
@57 // D=57
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 31
@31 // D=31
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// push constant 53
@53 // D=53
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

// push constant 112
@112 // D=112
D=A
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

// neg
@SP
A=M-1
M=-M

// and
@SP
AM=M-1
D=M
A=A-1
M=M&D

// push constant 82
@82 // D=82
D=A
@SP // *SP=D
A=M
M=D
@SP // SP++
M=M+1

// or
@SP
AM=M-1
D=M
A=A-1
M=M|D

// not
@SP
A=M-1
M=!M

