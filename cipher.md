The high-level description of the algorithm 

1. KeyExpansion - round keys are derived from the cipher key using the 
AES key schedule. AES requires a seperate 128 - bit round key block for each
   round plus one more. 
   
2. Initial round key addition: 
AddRoundKey - each byte of the state is combined with a byte of the round key 
   using bitwise xor. 
   
3. 9, 11, 13 rounds: 
####1. SubBytes - a non-linear substituition step where each byte is replaced with another accordint to a lookup table 
####2. ShiftRows - a transposition step where the last three rows of the  state are shifted cyclically a certain number of steps. 
####3. MixColumns - a linear mixing operation which operates on the columns of the state, combining te four bytes in each column. 
####4. AddRoundKey 

4. Final round (making it either: 10, 12 or 14 rounds in total): 

#####1. SubBytes 
#####2. ShiftRows
#####4. AddRoundKey 



Currently im thinking the layout to be that 
the class of Cipher in AES.py should be called upon 
each block. Such that all the blocking logic happens elsewhere. 
