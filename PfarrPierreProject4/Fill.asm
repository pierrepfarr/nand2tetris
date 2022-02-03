// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(Lower)     // this will be our lower bound 
@curr       // have a pointer to the curr pixel past the screen start  
M=0         // start at zero

(LOOP)      // while loop
    @curr   // load address of current pixel
    D=M     // put value in D
    
    @Lower  // if less than zero jmp to reset at 0
    D;JLT

    @8192   // keyboard input - screen input to set our upper bound 24576-16384 = 8192
    D=D-A
    
    @Upper  // if we have reach the upper bound jmp to move our curr back to last pixel before keyboard
    D;JEQ

    @KBD        // load  keyboard input 
    D=M         
    @Decrement  // if keyboard input is 0 or no key pressed then move to our Decrement code
    D;JEQ       
    @Increment  // else keyboard input is valid then move to our Increment code
    0;JMP       

(Increment)
@SCREEN     // load the start of the screen
D=A         // put in D
@curr       // load curr pixel past screen start
A=D+M       // point address to screen start + curr pixels past start
M=-1        // set M to -1 so the 16 pixels are black
@curr       // Increment our current pixels past start
M=M+1
@LOOP       // jump to beginning of loop
0;JMP

(Decrement)
@SCREEN     // load the start of the screen
D=A         // put in D 
@curr       // load curr pixel past screen start
A=D+M       // point address to screen start + curr pixels past start
M=0         // set M to 0 so the 16 pixels are white
@curr       // Decrement our current pixels past start
M=M-1
@LOOP       // jump to beginning of loop
0;JMP

(Upper)
@8191       // 8191 is last space past screen start and before keyboard
D=A         // load to D
@curr       // load curr pixel group past screen start
M=D         // set curr pixel group past screen start to D
@LOOP       // jmp to loop
0;JMP
