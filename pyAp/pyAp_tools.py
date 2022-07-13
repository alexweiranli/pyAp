"""
Weiran Li & Yishen Zhang

2022-02-20, v0.2

"""

import numpy as np
import pandas as pd
import time, sys


## allow users to type in "y/n" or "yes/no" for next steps when running examples in pyAp
def yes_or_no(question):
    
    answer = input(question + "(y/n): ").lower().strip()
    print("")
    
    while not(answer == "y" or answer == "yes" or \
    answer == "n" or answer == "no"):
        print("Input y (yes) or n (no)")
        answer = input(question + "(y/n):").lower().strip()
        print("")

    if answer[0] == "y":
        return True
    else:
        return False


## for mc calculation 
def ap_mc(comp, std, i, mc):
    """
    MC calculation model for pyAp

    Parameters:
    --------
    comp: :class: `pandas.Dataframe`
    std: :class: `pandas.Dataframe`
    i: :class: `numpy.array`
        index for iteration
    mc: :class: `numpy.array`
        number of monte carlo simulation

    Returns:
    ---------
    df: :class: `pandas.Dataframe`
        expanded dataframe after monte carlo simulation
    """
    comp = comp.copy()
    std = std.copy()
    index = i
    index = np.ones(mc) * index

    
    comp_mc =  comp.iloc[i,:]
    std_mc = std.iloc[i,:]
    comp_mc = np.ones((mc,1)) * comp_mc.to_numpy()
    std_mc = np.random.normal(0,1,(mc, len(std_mc))) * std_mc.to_numpy()
    comp_mc = comp_mc + std_mc
    df = pd.DataFrame(comp_mc)
    df.index = index    

    return df

# Function for implementing the loading animation
def load_animation():

    # String to be displayed when the application is loading
    load_str = "Running Monte Carlo Simulation"
    ls_len = len(load_str)


    # String for creating the rotating line
    animation = "|/-\\"
    anicount = 0

    # used to keep the track of
    # the duration of animation
    counttime = 0

    # pointer for travelling the loading string
    i = 0

    while (counttime != 100):

        # used to change the animation speed
        # smaller the value, faster will be the animation
        time.sleep(0.075)

        # converting the string to list
        # as string is immutable
        load_str_list = list(load_str)

        # x->obtaining the ASCII code
        x = ord(load_str_list[i])

        # y->for storing altered ASCII code
        y = 0

        # if the character is "." or " ", keep it unaltered
        # switch uppercase to lowercase and vice-versa
        if x != 32 and x != 46:
            if x>90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i]= chr(y)

        # for storing the resultant string
        res =''
        for j in range(ls_len):
            res = res + load_str_list[j]

        # displaying the resultant string
        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()

        # Assigning loading string
        # to the resultant string
        load_str = res


        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len
        counttime = counttime + 1
