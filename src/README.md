# AES
### Author: Vegard Berge
This is my go at the awesome block cipher AES. 

Advanced Encryption Standard, also known by its original name Rijndael is the
standard cryptographical cipher choosen by NIST. 

For AES we generally support three different key lengths: 
##### 128, 196 and 256 bits. 

AES is a substitution - permutation network. This means that from a 
high level view we can describe the cipher as follow: 

##### SubBytes step 
##### ShiftRows step 
##### MixColumns step 
##### AddRoundKey step 
