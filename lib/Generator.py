# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 14:21:42 2016

@author: Xiaotao Wang
"""

import random, copy, time
from Solver import sudoku, exactcover
from collections import OrderedDict

class SuDoCreater(sudoku):
    
    def __init__(self):
        # Randomize the basic constraints
        ridx = range(9); cidx = range(9); nums = range(1, 10)
        X = OrderedDict()
        random.shuffle(ridx); random.shuffle(cidx); random.shuffle(nums)
        for i in ridx: # row number
            for j in cidx: # column number
                for n in nums: # 1-9
                    t = (i, j, str(n)) # possibilities
                    rc = (i, j, None) # Row-Column constraint
                    rn = (i, None, str(n)) # Row-Number constraint
                    cn = (None, j, str(n)) # Column-Number constraint
                    bn = (i//3, j//3, str(n)) # Box-Number constraint
                    X[t] = [rc, rn, cn, bn]
        Y = OrderedDict()
        for sub in X:
            for e in X[sub]:
                if e in Y:
                    Y[e].add(sub)
                else:
                    Y[e] = {sub}
        self.X = X
        self.Y = Y
    
    def oriBoard(self):
        # Initialize the solver with an empty board
        ori = [['0']*9 for i in range(9)]
        sudoku.__init__(self, ori, self.X, self.Y)
        # Fill the board with 1-9 under the sudoku basic constraints
        board = self.solve(1)[0]
        
        return board
    
    def solve(self, maxnum = 1):
        solutions = set()
        X = self.X; Y = copy.deepcopy(self.Y)
        gensolution = exactcover(X, Y, solution = [])
        for s in gensolution:
            solutions.add(tuple(s))
            if len(solutions) >= maxnum:
                break
        solutions = list(solutions)
        
        return solutions
    
    