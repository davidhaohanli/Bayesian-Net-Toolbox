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
    '''

    self.valDistirution is the factor value distribution on the random variable assignemnt grid
    in form as:
    {(True,True,True):0.1,(True,True,False):0.9,(True,False,True):None,...,(False,False,False):1.6}
    * None for value pending to be determined

    '''

    def __init__(self,name,scope,varValsDict=None):
        '''
        :param scope:  tuple of chars
        :param valsDistribution:  dict of distribution of factor values on the random variable grid
        '''
        self.name=name
        self.scope = scope
        self.var_assignment(); # assign values to each random variables to generate a grid
        if varValsDict:
            self.add_all_vals(varValsDict)

    def var_assignment(self):
        '''
        repeat scope size times to get the binary grid
        '''
        self.valDistirution = dict()
        for thisVarVals in itertools.product((True,False),repeat=len(self.scope)):
            self.valDistirution[thisVarVals] = None

    def add_all_vals(self,varValsDict):
        '''
        :param varValsDict: dict of [tuples,float]    e.g. {(True,True):0.9}
        '''
        for thisVarVals,val in varValsDict.items():
            self.add_val(thisVarVals,val)

    def add_val(self,varVals,val):
        '''
        :param varVals: tuples,assignment to random variables
        :param val: value of the grid point
        '''
        self.valDistirution[varVals] = val

    def get_val(self,varVals):
        '''
        :param vars: tuples,assignment to query random variables
        :return: value of the grid point, None for unassigned yet
        '''
        return self.valDistirution[varVals]

    def get_all_val(self):
        '''
        :return: self.valDistribution
        '''
        return self.valDistirution

    def val_check(self):
        '''
        :return: points on the grid with value unassigned. if all assigned, return True
        '''
        res=[]
        for thisVarVals,val in self.valDistirution.items():
            if val is None:
                res.append(thisVarVals)
        if res:
            return res
        return True

class BayesianModel(object):
    #TODO DESIGN OF NET

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
        '''
        :param model: a BayesianModel
        '''
        self.model = model

    def facs_multi(self,factors,pre=None,isReduceVersion=False):
        '''
        :param factors: list of Factors
        :param pre: a Factor
        :param isReduceVersion: use functools.reduce or my own implementation
        :return: new Factor
        '''
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
    # TODO PRINT WORDS ON THE TEST MAIN
    main_test()