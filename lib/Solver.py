# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 13:55:31 2016

@author: Xiaotao Wang
"""

import cPickle, time, copy

# An implementation for Algorithm X using Python's built-in types
def exactcover(X, Y, solution = []):
    """
    Core worker for the exact cover problem solver.
    
    Parameters
    ----------
    X : dict
        Standard representation of the exact cover problem, with the key
        indicating the subset, and the value, which is stored as list, indicating
        elements contained in corresponding subset.
    Y : dict
        Inverse representation. The key indicates the element, and the vaule,
        stored as set, lists the subsets corresponding element is contained in.
    solution : list
        To find all solutions, this list is updated and yielded dynamically
        during the algorithm.
    """
    if not len(Y):
        yield sorted(solution)
    else:
        minc = None; numr = float('inf')
        for k in Y:
            if len(Y[k]) < numr:
                numr = len(Y[k])
                minc = k
        for r in Y[minc]:
            solution.append(r)
            cache = trim(X, Y, r)
            # The algorithm clones itself into subalgorithms
            for s in exactcover(X, Y, solution):
                yield s
            recover(X, Y, r, cache)
            solution.pop()

def trim(X, Y, r):
    
    cache = {} # Cache columns for recovering the last-stage problem
    for j in X[r]:
        for i in Y[j]:
            for k in X[i]:
                if k != j:
                    Y[k].remove(i) # mask rows
        cache[j] = Y.pop(j) # mask columns
    return cache

def recover(X, Y, r, cache):
    
    # To reverse the trim operation, we should add the column reversely
    # Since the rows in the last-removed column now don't cover columns
    # removed previously.
    for j in reversed(X[r]): # X remains intact
        Y[j] = cache.pop(j) # recover columns
        for i in Y[j]:
            for k in X[i]:
                if k != j:
                    Y[k].add(i) # recover rows

# Translate Su Doku into the exact cover problem
standard, inverse = cPickle.load(open('constraints.db','rb'))

class sudoku(object):
    
    def __init__(self, ori, X = standard, Y = copy.deepcopy(inverse)):
        # Add additional constraints
        for i in range(len(ori)):
            for j in range(len(ori[i])):
                if ori[i][j] != '0':
                    trim(X, Y, (i,j,ori[i][j]))
        
        self.X = X
        self.Y = Y
        self.ori = ori
    
    def solve(self):
        start = time.time()
        self.solutions = set()
        X = self.X; Y = copy.deepcopy(self.Y)
        gensolution = exactcover(X, Y)
        for s in gensolution:
            self.solutions.add(tuple(s))
        self.elapse = time.time() - start
        self.solutions = list(self.solutions)
    
    def _report(self, idx):
        
        print('Problem:\n')
        self.pretty_print(self.ori)
        print('Solved in %.4gs, found %d solution(s)\n' % (self.elapse,
              len(self.solutions)))
        if len(self.solutions):
            candi = self.solutions[idx]
            print('Solution %d view:\n' % (idx+1))
            self.pretty_print(candi)
    
    def pretty_print(self, data):
        
        solution = copy.deepcopy(self.ori)
        for r in data:
            solution[r[0]][r[1]] = r[2]
        template = ['|','','','','|','','','','|','','','','|']
        mapidx = [1, 2, 3, 5, 6, 7, 9, 10, 11]
        string = '+-----------------------+\n'
        for i in range(len(solution)):
            for j, idx in enumerate(mapidx):
                template[idx] = solution[i][j]
            string += (' '.join(template)+'\n')
            if (i % 3 == 2) and (i != 8):
                string += '|-------+-------+-------|\n'
        string += '+-----------------------+\n'
        
        print(string)
