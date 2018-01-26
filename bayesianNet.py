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

    def __init__(self,scope,varValsDict=None):
        '''
        :param scope:  tuple of chars
        :param valsDistribution:  dict of distribution of factor values on the random variable grid
        '''
        if type(scope) is not tuple:
            scope=(scope,)
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
        if type(varVals) is not tuple:
            scope=(varVals,)
        self.valDistirution[varVals] = val

    def get_val(self,varVals):
        '''
        :param vars: tuples,assignment to query random variables
        :return: value of the grid point, None for unassigned yet
        '''
        if type(varVals) is not tuple:
            scope=(varVals,)
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
        '''
        :param a: a Factor
        :param b: a Factor
        :return: a new Factor
        '''
        newFactor = Factor(tuple(set(a.scope+b.scope))) #newFactor scope: scope of a + scope of b - common scope

        for thisVarVals in newFactor.val_check():

            thisVarValsDict = dict()
            for i,var in enumerate(newFactor.scope):
                thisVarValsDict[var] = thisVarVals[i]
            #dict form : {'a':True,'b':False,'c':True}

            a_val =  a.get_val(tuple([thisVarValsDict[var] for var in a.scope]))
            #find the random variable assignment of a scope e.g. (b,a) from the dict, and then get value
            b_val = b.get_val(tuple([thisVarValsDict[var] for var in b.scope]))
            # find the random variable assignment of b scope e.g. (c,a) from the dict, and then get value
            newFactor.add_val(thisVarVals,a_val*b_val)

        return newFactor

    def query(self,query,evidence):
        #TODO
        pass

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
    fac1=Factor(('a','b'),{(True,True):0.1,(False,True):0.3,(True,False):0.2,(False,False):0.5})
    fac2=Factor(('b',),{(True,):0.6,(False,):0.9})
    fac3=Factor(('d','c','b'),{(True,True,True):0.1,(False,True,True):0.3,(True,False,True):0.2,(False,False,True):0.5,\
                               (True, True, False): 0.1, (False, True, False): 0.3, (True, False, False): 0.2,(False, False, False): 0.5})
    ve=VE('notModelYet')
    res=ve.facs_multi([fac1,fac2,fac3])
    '''
    ############### NOT ('a','b','c','d') ##################
    res.scope = ('b','c','a','d')

    res.get_all_val()
    Out[2]:
    {(False, False, False, False): 0.225,       ---- checked
     (False, False, False, True): 0.09000000000000001,
     (False, False, True, False): 0.09000000000000001,
     (False, False, True, True): 0.036000000000000004,
     (False, True, False, False): 0.135,
     (False, True, False, True): 0.045000000000000005,
     (False, True, True, False): 0.054000000000000006,
     (False, True, True, True): 0.018000000000000002,
     (True, False, False, False): 0.09,
     (True, False, False, True): 0.036,
     (True, False, True, False): 0.03,          ---- checked
     (True, False, True, True): 0.012,
     (True, True, False, False): 0.054,
     (True, True, False, True): 0.018,
     (True, True, True, False): 0.018,
     (True, True, True, True): 0.006}
    '''
    #TODO IMPLEMENT A TEST FUNC
    pass

if __name__ == '__main__':
    # TODO PRINT WORDS ON THE TEST MAIN
    main_test()