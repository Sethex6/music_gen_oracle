import json
from typing import NewType
from dataclasses import dataclass
import random as rd
import os


#__________________________________________________________________________________________________________________________________________________________________
#                                           TYPE DEF: FACTOR ORACLE AND TUNES
#__________________________________________________________________________________________________________________________________________________________________

class letter:                                     #Simplest class to describe a tune with its pitch and duration.
    def __init__(self, pitch:int, duration:float):
        self.pitch = pitch
        self.duration = duration

class intervalle_letter:                         #Rather than absolute pitches, this type records the intervalls between the tunes and follows therefore all the patterns in a score without any key issue.
    intervalle: int
    duration: float

class beat:                                      #More elaborate classe to describe a pattern (a beat made of several tunes)
    def __init__(self, b:list[letter]):
        self.b = b

class h_beat:                                    #Class that includes harmonicity: m is for the melody, h for the harmony.
    def __init__(self, m:beat, h:beat):
        self.m = m
        self.h = h

class some_class:                                #stands for a h_beat or a beat
    def __init__(self, c):
        self.c = c

class oracle :
    n : int                                        #number of states
    init : int                                     #initial state
    delta_trans : list[dict]                       #forward transitions
    supply : dict[some_class, int]                     #storage of the values of the supply function
    
 



#__________________________________________________________________________________________________________________________________________________________________
#                                                   CREATION OF FACTOR ORACLE
#__________________________________________________________________________________________________________________________________________________________________


#To compare two letters according to the alphabet
def compare_letter(l, lett, id):
    match id:
        case 0:
            return (l.pitch == lett.pitch and l.duration == lett.duration)
        #beats are considered identical if they share the same number of tunes and if the first tune of the beat is the same
        case 1:
            return ((l.b==[] and lett.b==[]) or ((len(l.b)==len(lett.b)) and compare_letter(l.b[0], lett.b[0], 0)))
        #h_beats are considered identical if their melody beats are identical
        case 2:
            return compare_letter(l.m, lett.m, 1)                

"""
CALC_SUPPLY:

From a given state i in the factor oracle, supply returns the final state of the longest postfix of pref(i) (and that is not i).
The convention is 0 if non is found, -1 if i=0.

sig : oracle -> int -> int
"""
def calc_supply (a : oracle, i, id):
    if (i in (a.supply).keys()):               #if the supply function has already been runned on this value it is stored in the dict
        return a.supply[i]
    
    if (i==0):
        a.supply[0] = (-1)                      #the initial state 's supply is (-1)
        return (-1)
    return a.supply[i]


#return -1 if no transition labeled by l in state k, else l
def letter_in_transition(a, l, k, id):
    for lett in a.delta_trans[k].keys():
        if compare_letter(l, lett, id):
            return lett                  #return l is not equivalent here, depending on the compare_letter function
    return -1          

"""
ADD_LETTER_TO_ORACLE:

Adds a class'object to a factor oracle and upgrades the supply numbers.

sig: oracle -> class'object -> int -> oracle
"""

def add_letter (a:oracle, le, id):
   
    l = serialized2type(le, id)             # O(1)
            
    a.n += 1
    a.delta_trans.append({})
   
    a.delta_trans[a.n-1][l] = a.n

    k = calc_supply(a, a.n-1, id)

    while (k>-1 and letter_in_transition(a, l, k, id)==-1):    #while there is no transition from k labeled l
        a.delta_trans[k][l] = a.n                          #creation of a new transition from k to last added state labeled l 
        k = calc_supply(a, k, id)                #k or k+1 
    
    s = int(0)
    if not(k == -1):
        le = letter_in_transition(a, l, k, id)
        s = a.delta_trans[k][le]
    a.supply[a.n] = s
    return a

"""
ON_LINE_CONSTRUCTION:

This function combines the previous constructions to build efficiently the factor oracle.

sig : list[letter] -> oracle
"""
def on_line(word, id):
    f = oracle()
    f.init = 0
    f.n = 0
    f.delta_trans = [{}]
    f.supply = {}

    f.supply[0] = (-1)

    for l in word:
        f = add_letter(f, l, id)
    return f


#__________________________________________________________________________________________________________________________________________________________________
#                                          SELF TYPES CONVERSION                                  
#_________________________________________________________________________________________________________________________________________________________________

def beat2tuple(b):
    l = []
    for lett in b.b:
        l.append((lett.pitch, lett.duration))
    return l

def h_beat2tuple(hb):
    l1 = beat2tuple(hb.m)
    l2 = beat2tuple(hb.h)
    return [l1, l2]

def self_type2tuple(l, id):
    match id:
        case 0:
            return (l.pitch, l.duration)
        case 1:
            return beat2tuple(l)
        case 2:
            return h_beat2tuple(l)

def serialized2letter(l):
    (p, d) = l
    return letter(p, d)
    
def serialized2beat(lett):
    lst = []
    for l in lett:
        lst.append(serialized2letter(l))
    return beat(lst)

def serialized2h_beat(lett):
    m = serialized2beat(lett[0])
    h = serialized2beat(lett[1])
    return h_beat(m, h)

def serialized2type(lett, id):
    match id:
        case 0:
            return serialized2letter(lett)
        case 1:
            return serialized2beat(lett)
        case 2: 
            return serialized2h_beat(lett)


#__________________________________________________________________________________________________________________________________________________________________
#                                          SERIALIZATION OF ORACLE - TO STORE IN A .DAT
#__________________________________________________________________________________________________________________________________________________________________


#To serialize an oracle we have to get rid of the defined types such as letter, hbeat,...

def treat_oracle_for_serialization( a:oracle, id):    
    o = {}
    o["init"] = a.init
    o["n"] = a.n
    o["id"] = id
    nb_trans = 0
    for s in range (a.n):
        #dictionnary for transitions in state s
        d = []
        t = 0
        for l in a.delta_trans[s].keys():
            t+=1
            nb_trans+=1
            match l:
                case letter():
                    lett = (l.pitch, l.duration)
                case beat():
                    lett = beat2tuple(l)
                case h_beat():
                    lett = h_beat2tuple(l)
            d.append((lett, a.delta_trans[s][l]))
        o[s] = d
        for i in range(5):
            if(t>nb_values[i]):
                nb_transi[i]+=1

    o["nb_trans"] = nb_trans
    return o

def serialized2oracle(o):
    a = oracle()
    a.init = o["init"]
    a.n = o["n"]
    a.supply = {}                    
    a.delta_trans = []

    #indicates whether letter, beat or h_beat
    id = o["id"]

    for s in range (a.n):
        d = {}
        for (lett, new_state) in o[str(s)]:
            l = serialized2type(lett, id)
            d[l] = new_state
        a.delta_trans.append(d)

    return a
