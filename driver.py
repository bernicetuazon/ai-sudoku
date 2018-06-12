'''
    File name: driver.py
    Author: Bernice Tuazon
    Date created: 4/5/2018
    Date last modified: 4/12/2018
    Python Version: 3.6
'''

#all modules in csp_lib were created by Prof. Marie Roch from San Diego State University
from csp_lib.sudoku import (Sudoku, easy1, harder1) #import easy and hard starting puzzles
from csp_lib.backtrack_util import (mrv, forward_checking)

from backtrack import backtracking_search
from constraint_prop import AC3

for puzzle in [easy1, harder1]:
    s  = Sudoku(puzzle)  # construct a Sudoku problem
    s.display(s.infer_assignment()) #print the initial game
    print("\n")
    
    if AC3(s):  #first try using AC-3 to solve the puzzle
        if s.goal_test(s.curr_domains): #easy1 puzzle
            print("Congratulations, easy game is solved!")
            s.display(s.infer_assignment()) #display solved puzzle
            print("\n")
        else:   #harder1 puzzle
            #solve with backtracking search and by using the minimum-remaining-values heuristic
            #to choose the next unassigned variable
            solved = backtracking_search(s, select_unassigned_variable=mrv, inference=forward_checking) 
            if solved is None:  #backtracking_search failed
                print("Puzzle cannot be solved by AC-3 or back tracking.\n")
            else:
                print("Congratulations, hard game is solved!")
                s.display(s.infer_assignment()) #display solved puzzle
