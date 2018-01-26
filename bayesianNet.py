#TODO COMMENT ABOUT THE TOOLBOX

import numpy as np
import pandas as pd
import scipy as sp
import itertools
import functools

#TODO COMMENT IN DETAILS

class DirectedGraphNode(object):

     def __init__(self, x):
         '''
         :param x: string for the node name
         '''
         self.parents = None #DGN object
         self.name = x
         self.children = None #DGN object

class Factor(object):

    def __init__(self,scope,vals=None):
        '''
        :param scope: # tuple of chars
        :param vals: # diction of distribution of factor values on the random variable grid
        '''
        self.scope = scope
        self.var_assignment(); # assign values to each random variables to generate a grid
        if not vals:
            #TODO
            pass

    def var_assignment(self):
        self.vals=list(itertools.product((True,False),repeat=len(self.scope))) # repeat scope times to get the binary grid
        #TODO
        pass

    def add_val(self,vars,val):
        '''
        :param vars:
        :param val:
        :return:
        '''
        #TODO
        pass;

    def get_val(self,vars):
        #TODO
        pass;

class BayesianModel(object):

    def __init__(self,edges):
        #TODO
        pass;

    def add_nodes(self,edges):
        #TODO
        pass;

    def get_nodes(self):
        #TODO
        pass;

    def check_node(self,nodeName):
        #TODO
        pass;

    def add_cpd(self,mat,var,evidence):
        #TODO
        pass;

class VE(object):

    def __init__(self,model):

        self.model = model
        #TODO
        pass

    def facs_multi(self,factors,pre=None,isReduceVersion=False):

        if isReduceVersion:
            return functools.reduce(self.two_facs_multi,factors)

        # my own implementation: recursively compute 2 factor multiplication
        if not pre:
            pre = factors[0]
            factors = factors[1:]
        if factors:
            pre = self.two_facs_multi(factors[0],pre)
            res = self.facs_multi(factors[1:],pre)
            return res
        return pre

    def two_facs_multi(self,a,b):
        #TODO
        pass;

    def query(self,query,evidence):
        #TODO
        pass;

    def sum_product(self,vars):
        #TODO
        pass;

    def sum_prduct_var(self,var):
        #TODO
        pass;

    def topoSort(self):
        #TODO
        pass;


def main_test():
    #TODO IMPLEMENT A TEST FUNC
    pass;

if __name__ == '__main__':
    #TODO COMMENT ON THE MAIN
    main_test()