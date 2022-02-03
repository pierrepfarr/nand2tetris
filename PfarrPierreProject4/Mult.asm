// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// Adds 1+...100.

// i recall in class saying to make a seperate pointer instead of decrementing R1
// However the test also pass if decrementing R1 directly, is it not more efficient 
// to directly decrement R1?

@1
D=M     //put R1 into memory

@count  //make a count pointer
M=D     //that is equal to R1 to decrement

@2      //location of our output
M=0     //initalize to zero

(LOOP)
    @count  //look at the curr number of times left to add
    D=M 
    @END    // if it is 0 then jump to end 
    D;JEQ   

    @count // decrement our times left to add by 1
    M=M-1 

    @2      // load current total
    D=M     // total into D
    @0      // load r0 
    D=D+M   // total + r0 store in D
    @2      // load output
    M=D     // set output to new running total
    
    @LOOP   // jump to the top of the loop
    0;JMP

(END)       // End with infinite loop
    @END
    0;JMP