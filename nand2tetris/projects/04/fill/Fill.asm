// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// This program illustrates low-level handling of the screen and keyboard
// devices, as follows.
//
// The program runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
// 
// Assumptions:
// Your program may blacken and clear the screen's pixels in any spatial/visual
// Order, as long as pressing a key continuously for long enough results in a
// fully blackened screen, and not pressing any key for long enough results in a
// fully cleared screen.
//
// Test Scripts:
// For completeness of testing, test the Fill program both interactively and
// automatically.
// 
// The supplied FillAutomatic.tst script, along with the supplied compare file
// FillAutomatic.cmp, are designed to test the Fill program automatically, as 
// described by the test script documentation.
//
// The supplied Fill.tst script, which comes with no compare file, is designed
// to do two things:
// - Load the Fill.hack program
// - Remind you to select 'no animation', and then test the program
//   interactively by pressing and releasing some keyboard keys

// Put your code here.
	
// Checks for user input
(CHECK)
	// Recieve input from the keyboard (RAM[KBD])
	@KBD
	D = M
	
	// Whites out the screen if no keys are pressed
	@CLEAR
	D;JEQ
	
	// Blacks out the screen if a key is pressed
	@BLACK
	D;JNE
	
// Clears the screen (sets all pixels to white)
(CLEAR)
	// Reset address to the start of the screen
    @SCREEN
    D = A
    @address
    M = D

	// Reset pixelCounter
    @8192
    D = A
    @pixelCounter
    M = D

(CLEAR_LOOP)
    @address
    A = M	// Load address
    M = 0	// White out address

    @address
    M = M + 1	// address++

    @pixelCounter
    M = M - 1	// pixelCounter--
	
	// Repeat while pixelCounter is greater than 0
    D = M
    @CLEAR_LOOP
    D;JGT         

	// If we get hre, this means that pixelCounter = 0 i.e there are no more pixels to white out
    @CHECK
    0;JMP 
	
// Blacks the screen (sets all pixels to black)
(BLACK)
	// Reset address to the start of the screen
    @SCREEN
    D = A
    @address
    M = D

	// Reset pixelCounter
    @8192
    D = A
    @pixelCounter
    M = D

(BLACK_LOOP)
    @address
    A = M	// Load address
    M = -1	// Black out address

    @address
    M = M + 1	// address++

    @pixelCounter
    M = M - 1	// pixelCounter--
	
	// Repeat while pixelCounter is greater than 0
    D = M
    @BLACK_LOOP
    D;JGT         

	// If we get hre, this means that pixelCounter = 0 i.e there are no more pixels to white out
    @CHECK
    0;JMP 
