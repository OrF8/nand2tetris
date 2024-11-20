// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// Multiplies R0 and R1 and stores the result in R2.
//
// Assumptions:
// - R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.
// - You can assume that you will only receive arguments that satisfy:
//   R0 >= 0, R1 >= 0, and R0*R1 < 32768.
// - Your program does not need to test these conditions.
//
// Requirements:
// - Your program should not change the values stored in R0 and R1.
// - You can implement any multiplication algorithm you want.

// Put your code here.

// What my program does:
//	for (int i = 0; i < RAM[R1]; i++) {
//		RAM[R2] += RAM[R0]
//		i += 1
//	}
//	return RAM[R2]

	// Declare i and set i = 0
	@i
	M = 0
	// Make sure RAM[R2] = 0 before we start
	@R2
	M = 0
	
	// If RAM[R0] == 0 o RAM[R1] GOTO END
	@R0
	D = M
	@END
	D;JEQ
	@R1
	D = M
	@END
	D;JEQ

(LOOP)
	@R1
	D = M // D = RAM[R1]
	@i
	D = D - M // D = RAM[R1] - i
	@END
	D;JEQ // If i == RAM[R1] GOTO END
	
	// Perform the addition
	@R0
	D = M
	@R2
	M = M + D
	
	// Perform i++
	@i
	M = M + 1
	
	@LOOP
	0;JMP
	
(END)
	@END
	0;JMP
