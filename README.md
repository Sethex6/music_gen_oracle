# music_gen_oracle
Factor oracle is a FDA invented in 1999 that can be used in composition even thought it was not meant to this purpose.

A complete construction of "the" factor oracle of a word using a linear algorithm such as introduced in [Factor Oracle: A New Structure for Pattern Matching by Cyril Allauzen, Maxime Crochemore⋆, and Mathieu Raffinot, 1999] is to be found in file "factor oracle".

In my project it was meant to be used on a data set of MIDI file so everything is in python and I left some suggestion of the alphabets I used.

With the current types used, changing theese alphabets would require some changes in the compare_letter function and in the calc_supply function.

Some conversion functions to serialize the oracle are also provided.
