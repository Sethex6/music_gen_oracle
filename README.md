# music_gen_oracle
Factor oracle is a FDA invented in 1999 that can be used in composition even thought it was not meant to this at the begining.

A complete construction of "the" factor oracle of a word using a linear algorithm such as introduced in [Factor Oracle: A New Structure for Pattern Matching by Cyril Allauzen, Maxime Crochemore⋆, and Mathieu Raffinot, 1999] is to be found in file "creation_factor_oracle.py".

In my project it was meant to be used on a data set of MIDI files. This is why everything is in python. 

I left the code for the alphabets I used but one can feel free to test other ones.
Still, be aware that with the current types, changing theese alphabets would require some changes in the compare_letter function and in the calc_supply function.

Some conversion functions to serialize the oracle are also provided.
