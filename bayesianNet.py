#TODO COMMENT ABOUT THE TOOLBOX

import numpy as np
import pandas as pd
import scipy as sp
import itertools
import functools

#TODO COMMENT IN DETAILS

class Factor(object):
    #TODO REDESIGN FOR EVIDENCE
    '''

    self.valDistirution is the factor value distribution on the random variable assignemnt grid
    in form as:
    {(True,True,True):0.1,(True,True,False):0.9,(True,False,True):None,...,(False,False,False):1.6}
    * None for value pending to be determined

    '''

    def __init__(self,scope,varValsDict=None,default=None):
        '''
        :param scope:  tuple of chars
        :param valsDistribution:  dict of distribution of factor values on the random variable grid
        '''
        if type(scope) is not tuple:
            scope=(scope,)
        self.scope = scope
        self.var_assignment(default); # assign values to each random variables to generate a grid
        if varValsDict:
            self.add_all_vals(varValsDict)

    def var_assignment(self,default=None):
        '''
        repeat scope size times to get the binary grid
        '''
        self.valDistirution = dict()
        for thisVarVals in itertools.product((True,False),repeat=len(self.scope)):
            self.valDistirution[thisVarVals] = default

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
            varVals=(varVals,)
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

    def normalize(self):
        if self.val_check():
            normalizer = sum(self.valDistirution.values())
            for thisVarVals in self.valDistirution.keys():
                self.valDistirution[thisVarVals]/=normalizer
        else:
            print ('some values unassigned\n')

class DirectedGraphNode(object):

     def __init__(self, x):
         '''
         :param x: string for the node name
         '''
         self.parents = None #DGN object
         self.name = x
         self.children = None #DGN object

class BayesianModel(object):
    '''
    self.nodes is the nodes over the graphical network
    self.edges is the connection of all the nodes
    self.factors is the factors of variables
    '''
    #TODO DESIGN OF NET

    def __init__(self,edges):
        #TODO
        pass;

    def add_edges(self,edges):
        #TODO
        pass

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

    def query(self,queries,evidences,testNodes=None,testFactors=None):
        #TODO DELETE TEST VARS AND CORRESPONDING STATEMENT
        '''
        :param queries: list of joint conditional probabilities pending to query      e.g. ['a','b']
        :param evidences: dict of evidences       e.g. {'c':True,'d':False}
        :return: a factor with value distribution on query variables only (normalized)
        '''
        if testNodes:
            factors = testFactors
            allVars = testNodes
        else:
            factors = self.model.factors
            allVars = self.model.nodes

        varsToBeEliminated = []
        for var in allVars:
            if var not in queries:
                if var not in evidences.keys():
                    varsToBeEliminated.append(var)

        for i in range(len(factors)):
            factors[i] = self.giveEvidence(factors[i],evidences)

        factor_with_evidence = self.sum_product(factors,varsToBeEliminated)
        factor_with_evidence.normalizing()

        print ('Query Variables: {}\n Probability Distribution:\n{}\n'.format(factor_with_evidence.scope,\
                                                                              factor_with_evidence.get_all_val()))
        return factor_with_evidence

    def sum_product(self,factors,vars):
        '''
        :param factors: all factors
        :param vars: variables to be eliminated
        :return:
        '''
        if type(vars) is not list:
            vars = vars
        vars = self.topoSort(vars)
        for var in vars:
            factors = self.sum_product_var(factors,var)
        return self.facs_multi(factors)

    def sum_product_var(self,factors,var):
        '''
        :param factors: all factors
        :param var:  variable to be eliminated
        :return: set of all factors after VE of this variable
        '''
        if type(factors) is not list:
            factors = [factors]
        involvedFactors = []
        otherFactors = []
        for factor in factors:
            if var in factor.scope:
                involvedFactors.append(factor)
            else:
                otherFactors.append(factor)
        newFactor = self.sum_ve(self.facs_multi(involvedFactors),var)
        return otherFactors+[newFactor]

    def facs_multi(self,factors,pre=None,isReduceVersion=False):
        '''
        :param factors: list of Factors
        :param pre: a Factor
        :param isReduceVersion: use functools.reduce or my own implementation
        :return: new Factor
        '''
        if type(factors) is not list:
            factors = [factors]

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

            # dict form : {'a':True,'b':False,'c':True}
            thisVarValsDict = dict()
            for i,var in enumerate(newFactor.scope):
                thisVarValsDict[var] = thisVarVals[i]

            a_val = a.get_val(tuple([thisVarValsDict[var] for var in a.scope]))
            #find the random variable assignment of a scope e.g. (b,a) from the dict, and then get value
            b_val = b.get_val(tuple([thisVarValsDict[var] for var in b.scope]))
            # find the random variable assignment of b scope e.g. (c,a) from the dict, and then get value
            newFactor.add_val(thisVarVals,a_val*b_val)

        return newFactor

    def giveEvidence(self,factor,evidences):
        '''
        :param factor: factor containing evidence variables
        :param evidences: dict of evidences       e.g. {'c':True,'d':False}
        :return: new factor
        '''
        newFactor = Factor(tuple(set(factor.scope)-set(evidences.keys())))
        for thisVarVals in newFactor.val_check():

            # dict form : {'a':True}
            thisVarValsDict = dict()
            for i, var in enumerate(newFactor.scope):
                thisVarValsDict[var] = thisVarVals[i]
            # merge thisVarValsDict (in newFactor) and evidences
            thisVarValsDict.update(evidences)

            newFactor.add_val(thisVarVals,factor.get_val(tuple([thisVarValsDict[var] for var in factor.scope])))

        return newFactor

    def sum_ve(self,factor,vars):
        '''
        :param factor: factor containing variables
        :param vars: variables to be eliminated
        :return: new factor
        '''
        if type (vars) is not list:
            vars = [vars]

        newFactor = Factor(tuple(set(factor.scope) - set(vars)))
        for thisVarVals in newFactor.val_check():

            # dict form : {'a':True}
            thisVarValsDict = dict()
            for i, var in enumerate(newFactor.scope):
                thisVarValsDict[var] = thisVarVals[i]

            val=0
            for eliminateVarVals in itertools.product((True, False), repeat=len(vars)):
                factorVarValsDict = dict()
                for i, var in enumerate(vars):
                    factorVarValsDict[var] = eliminateVarVals[i]
                factorVarValsDict.update(thisVarValsDict)

                val += factor.get_val(tuple([factorVarValsDict[var] for var in factor.scope]))

            newFactor.add_val(thisVarVals,val)

        return newFactor

    def topoSort(self,vars):
        '''
        :param vars: variables to be ordered according to topological orders
        :return:  ordered variables
        '''



        #TODO
        return vars


def main_test():
    #TODO IMPLEMENT A GENERAL TEST FUNC
    pass

if __name__ == '__main__':
    # TODO PRINT WORDS ON THE TEST MAIN
    main_test()