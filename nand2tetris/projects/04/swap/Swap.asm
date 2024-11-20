// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.

// Initializes key variables
(START)
	// Set new variable arr to the address at RAM[14]
	@R14
	D = M
	@arr
	M = D

	// Set new variable length to the number at RAM{15]
	@R15
	D = M
	@length
	M = D
	
	// Set new variable max to the minimum value it can hold (-16384)
	@16384
	D = A
	@max
	M = -D
	
	// Set new variable min to the maximum value it can hold (16384)
	@16384
	D = A
	@min
	M = D
	
	// Set new variable maxAddr to the start of the array
	@arr
	D = M
	@maxAddr
	M = D
	
	// Set new variable minAddr to the start of the array
	@arr
	D = M
	@minAddr
	M = D

// Loop to find max and min
(LOOP)
	// If length < 0, GOTO END_OF_LOOP
	@length
    D = M
    @END_OF_LOOP
    D;JEQ

	// Check if current value is greater than max
    @arr
    A = M 	// A = address stored in arr
    D = M 	// D = value at RAM[A]
    @max
    D = D - M
    @UPDATE_MAX
    D;JGT	// If D (current value) > max, update max

    // Check if current value is less than min
    @arr
    A = M 	// A = address stored in arr
    D = M 	// D = value at RAM[A]
    @min
    D = D - M
    @UPDATE_MIN
    D;JLT	// If D (current value) < min, update min

    @SKIP_UPDATE
    0;JMP	// Skip updates

(UPDATE_MAX)
    @arr
    A = M 	// A = address stored in arr
    D = M 	// D = value at RAM[A]
    @max
    M = D	// max = current value

    @arr
    A = M 	// A = address stored in arr
    D = A 	// D = value at RAM[A]
    @maxAddr
    M = D	// maxAddr = current address
    @SKIP_UPDATE
    0;JMP	// Skip updates

(UPDATE_MIN)
    @arr
    A = M 	// A = address stored in arr
    D = M 	// D = value at RAM[A]
    @min
    M = D	// min = current value

    @arr
    A = M 	// A = address stored in arr
    D = A 	// D = value at RAM[A]
    @minAddr
    M = D	// minAddr = current address

(SKIP_UPDATE)
    @arr
    M = M + 1	// arr++

    @length
    M = M - 1	// length--

    @LOOP
    0;JMP	// Repeat loop

// The loop has ended, swap the elements
(END_OF_LOOP)
    // Swap max and min elements
    @maxAddr
    A = M
    D = M   // D = max element value

    @temp
    M = D   // temp = max element value

    @minAddr
    A = M
    D = M   // D = min element value

    @maxAddr
    A = M
    M = D   // Swap: maxAddr value = min element value

    @temp
    D = M
    @minAddr
    A = M
    M = D   // Swap: minAddr value = temp (original max element)
    
    @END
    0;JMP

(END)
    @END
    0;JMP
