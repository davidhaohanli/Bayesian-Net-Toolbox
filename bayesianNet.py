#TODO COMMENT ABOUT THE TOOLBOX

import itertools
import functools
import copy
import numpy as np
from abc import abstractmethod
from matplotlib import pyplot as plt

np.random.seed(1784)

#TODO COMMENT IN DETAILS

def plot(pointsA:list,pointB:int):
    plt.figure(figsize=(20, 5))
    plt.plot(pointsA)
    plt.plot([pointB]*len(pointsA), 'r--')
    plt.xlabel('Sample Size')
    plt.ylabel('Probability for True')
    plt.legend(['Gibbs Sampling', 'Variable Elimination'])
    plt.show()

def cleanser(theClass=tuple,posOfParam=2):
	def wrapper(func):
		def decFunc(*args,**kw):
			args=list(args)
			thisType = type(args[posOfParam-1])
			if thisType is not theClass:
				if thisType is str:
					args[posOfParam-1] = theClass([args[posOfParam-1],])
					return func(*args,**kw)
				try:
					thisType.__iter__
					args[posOfParam-1] = theClass(args[posOfParam-1])
				except:
					args[posOfParam-1] = theClass([args[posOfParam-1],])
			return func(*args,**kw)
		return decFunc
	return wrapper

class Factor(object):
    '''

    self.valDistribution is the factor value distribution on the random variable assignemnt grid
    in form as:
    {(True,True,True):0.1,(True,True,False):0.9,(True,False,True):None,...,(False,False,False):1.6}
    * None for value pending to be determined

    '''

    def __init__(self,scope:tuple,varValsDict=None,defaultVal=None):
        '''
        :param scope:  tuple of chars
        :param valsDistribution:  dict of distribution of factor values on the random variable grid
        '''
        self.scope = scope
        self.var_assignment(defaultVal); # assign values to each random variables to generate a grid
        if varValsDict:
            self.add_all_vals(varValsDict)

    def var_assignment(self,defaultVal=None):
        '''
        repeat scope size times to get the binary grid
        '''
        self.valDistribution = dict()
        for thisVarVals in itertools.product((True,False),repeat=len(self.scope)):
            self.valDistribution[thisVarVals] = defaultVal

    def add_all_vals(self,varValsDict):
        '''
        :param varValsDict: dict of [tuples,float]    e.g. {(True,True):0.9}
        '''
        for thisVarVals,val in varValsDict.items():
            self.add_val(thisVarVals,val)

    @cleanser()
    def add_val(self,varVals,val):
        '''
        :param varVals: tuples,assignment to random variables
        :param val: value of the grid point
        '''
        self.valDistribution[varVals] = val

    def get_val(self,varVals):
        '''
        :param vars: tuples,assignment to query random variables
        :return: value of the grid point, None for unassigned yet
        '''
        return self.valDistribution[varVals]

    def get_all_val(self):
        '''
        :return: self.valDistribution
        '''
        return self.valDistribution

    def val_check(self):
        '''
        :return: points on the grid with value unassigned. if all assigned, return True
        '''
        res=[]
        for thisVarVals,val in self.valDistribution.items():
            if val is None:
                res.append(thisVarVals)
        if res:
            return res
        return True

    def normalize(self):
        if self.val_check() is True:
            normalizer = sum(self.valDistribution.values())
            for thisVarVals in self.valDistribution.keys():
                self.valDistribution[thisVarVals]/=normalizer
        else:
            print ('some values unassigned\n')

class BayesianModel(object):
    '''
    self.nodes is the nodes over the graphical network, a dict of {str : list of str}   e.g. {'a':['b','c'],'b':[],'c':[],'d':['c']}
    self.factors is the factors of variables, a list of factors
    '''

    def __init__(self,edges=None):
        '''
        :param edges: in for [('a','b'),('c')] where 'a' is predecessor of 'b'
        '''
        self.nodes = dict()
        self.factors = list()
        if edges:
            self.add_edges(edges)

    @cleanser(list)
    def add_edges(self,edges):
        for edge in edges:
            self.add_edge(edge)

    @cleanser(tuple)
    def add_edge(self,edge):
        self.add_nodes(edge)
        if len(edge) > 1:
            self.nodes[edge[0]].append(edge[1])

    @cleanser(list)
    def add_nodes(self,nodes):
        for node in nodes:
            if node not in self.nodes.keys():
                self.nodes[node] = []

    @cleanser(list)
    def add_factors(self,factors):
        self.factors.extend(factors)

    def add_cpd(self,node:str, mat:'2d list', evidences:list=None)->'convert to factor':

        scope=[node]
        if evidences:
            scope+=evidences
        else:
            self.factors.append(Factor(scope,{(True,):mat[0][0],(False,):mat[1][0]}))
            return
        newFactor = Factor(tuple(scope))

        for i,nodeVal in enumerate((True,False)):
            for j,evidenceVals in enumerate(itertools.product((True,False),repeat=len(evidences))):
                thisVarValDict = dict()
                thisVarValDict[node] = nodeVal
                for ind,var in enumerate(evidences):
                    thisVarValDict[var] = evidenceVals[ind]
                newFactor.add_val(tuple([thisVarValDict[var] for var in newFactor.scope]),mat[i][j])

        self.factors.append(newFactor)

class Inference(object):
    #TODO abstract the class
    #TODO collect the common methods

    def __init__(self,model):
        '''
        :param model: A Bayesian Model
        '''
        self.model = model

    @abstractmethod
    def query(self,queries,evidences):
        raise NotImplementedError()

    def topoSort(self,vars=None):
        '''
        :param vars: variables to be ordered according to topological orders
        :return:  ordered variables (reversed)
        '''
        if vars is None:
            vars = list(self.model.nodes.keys())

        color=dict()
        for node in self.model.nodes.keys():
            color[node]='white'
        time = 0
        res = []

        def dfs(node,time):
            color[node]='grey'
            time += 1
            for adj in self.model.nodes[node]:
                if color[adj] == 'white':
                    time = dfs(adj,time)
            color[node] = 'black'
            time+=1
            if node in vars:
                res.append(node)
            return time

        for node in self.model.nodes.keys():
            if color[node] == 'white':
                time = dfs(node,time)

        return res

class VE(Inference):

    @cleanser(list)
    def query(self,queries:list,evidences:dict=dict(),printTrigger:bool=True)->Factor:
        '''
        :param queries: list of joint conditional probabilities pending to query      e.g. ['a','b']
        :param evidences: dict of evidences       e.g. {'c':True,'d':False}
        :return: a factor with value distribution on query variables only (normalized)
        '''
        factors = copy.deepcopy(self.model.factors)

        varsToBeEliminated = set(self.model.nodes.keys())-set(queries)-set(evidences.keys())

        for i in range(len(factors)):
            factors[i] = self.giveEvidence(factors[i],evidences)

        cpd_factor = self.sum_product(factors,varsToBeEliminated)
        cpd_factor.normalize()

        if printTrigger:
            print('Variables: {}\n Probability Distribution:\n{}\n'.format(cpd_factor.scope, \
                                                                           cpd_factor.get_all_val()))

        return cpd_factor

    def sum_product(self,factors,vars)->Factor:
        '''
        :param factors: all factors
        :param vars: variables to be eliminated
        :return:
        '''
        vars = self.topoSort(vars)
        while vars:
            var = vars.pop()
            factors = self.sum_product_var(factors,var)
        return self.facs_multi(factors)

    def sum_product_var(self,factors,var)->'list of Factors':
        '''
        :param factors: all factors
        :param var:  variable to be eliminated
        :return: set of all factors after VE of this variable
        '''
        involvedFactors = []
        otherFactors = []
        for factor in factors:
            if var in factor.scope:
                involvedFactors.append(factor)
            else:
                otherFactors.append(factor)
        newFactor = self.sum_ve(self.facs_multi(involvedFactors),var)
        return otherFactors+[newFactor]

    def facs_multi(self,factors,pre=None,isReduceVersion=False)->Factor:
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

    def two_facs_multi(self,a,b)->Factor:
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

    @cleanser(list,3)
    def sum_ve(self,factor,vars)->Factor:
        '''
        :param factor: factor containing variables
        :param vars: variables to be eliminated
        :return: new factor
        '''

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

    def giveEvidence(self,factor,evidences)->Factor:
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

class GibbsSampler(Inference):

    def __init__(self,model,step=1000,burnInCoefficient=0.3,thinningGap=5):
        super().__init__(model)
        self.hyperParamSet({'step':step,'burnInCoefficient':burnInCoefficient,'thinningGap':thinningGap})
        self.initStepCollector()

    def initStepCollector(self):
        self.stepVals=[]

    def hyperParamSet(self,hyperParams={'step':1000,'burnInCoefficient':0.3,'thinningGap':5}):
        '''
        :param step: sample size
        :param burnInCoefficient: proportion of starting samples to be dropped
        :param thinningGap: selection gap for i.i.d
        '''
        if hyperParams.get('step') is not None:
            self.step = hyperParams['step']
        self.burnInNum = self.step * hyperParams['burnInCoefficient']
        self.thinningGap = hyperParams['thinningGap']

    @cleanser(list)
    def query(self,queries:list,evidences:dict=dict(),printTrigger:bool=True,trueValForStepShow:float=None)->Factor:
        '''
        :param queries: list of joint conditional probabilities pending to query      e.g. ['a','b']
        :param evidences: dict of evidences       e.g. {'c':True,'d':False}
        :return: a probability distribution, Factor
        '''
        varsToBeSampled = self.topoSort(set(self.model.nodes.keys()) - set(evidences.keys()))[::-1]

        if trueValForStepShow is not None:
            self.initStepCollector()

        cpd = self.gibbs(varsToBeSampled,queries,evidences,trueValForStepShow)

        if trueValForStepShow is not None:
            plot(self.stepVals,trueValForStepShow)

        if printTrigger:
            print('Variables: {}\n Probability Distribution:\n{}\n'.format(cpd.scope, \
                                                                           cpd.get_all_val()))
        return cpd

    def gibbs(self,vars:list,queries:list,evidences:dict,trueValForStepShow:int=None)->Factor:
        '''
        :param factors: all factors
        :param vars: sorted vars to be sampled
        :param steps: number of sample sets needed
        :return: desired cpd factor
        '''
        samplePool = {}

        newFactor = Factor(tuple(queries),defaultVal=0)

        if trueValForStepShow is not None:
            tempFactor = Factor(tuple(queries),defaultVal=0)

        for t in range(self.step):

            thisVarValDict=dict()

            for var in vars:
                samplePool = self.sample(var,samplePool,evidences)
                if var in queries:
                    thisVarValDict[var] = samplePool[var]

            thisVarVals = tuple([thisVarValDict[var] for var in newFactor.scope])

            if trueValForStepShow is not None:
                tempFactor.add_val(thisVarVals,tempFactor.get_val(thisVarVals) + 1)
                self.stepCollect(tempFactor)

            if t >= self.burnInNum and not t % self.thinningGap:
                newFactor.add_val(thisVarVals,newFactor.get_val(thisVarVals)+1)

        newFactor.normalize()

        return newFactor

    def sample(self,var:str,samplePool:dict,evidences:dict)->dict:
        '''
        :param samplePool: dict of samples
        :param factors: all factors from model
        :param var: variable to be sampled
        :return: the updated dictionary of samples
        '''
        samplePool.pop(var,None)

        fullEvidence = {**samplePool,**evidences}

        cpd = VE(self.model).query([var],fullEvidence,False)

        particle = np.random.rand()

        if particle <= cpd.get_val((True,)):
            newSampleVal = True
        else:
            newSampleVal = False

        samplePool[var] = newSampleVal

        return samplePool

    def stepCollect(self,theFactor:Factor):

        theFactor = copy.deepcopy(theFactor)

        theFactor.normalize()

        self.stepVals.append(theFactor.get_val((True,)))

class GridSearchTuner(object):

    def __init__(self,model:GibbsSampler,**hyperParamCandidates):
        '''
        :param model: of which hyper-parameters pending to be tuned
        :param hyperParams: the candidates of hyper-parameters, concatenated in a dictionary   e.g.{}
        '''
        self.model = model
        self.hyperParamCandidates = hyperParamCandidates

    def tune(self,queries:list,targets:Factor,evidences:dict=dict()):
        '''
        :param queries: same as model.query
        :param evidences: same as model.query
        :param targets: real values for query variable probability distribution, Factor
        :return: best model
        '''
        def search(hyperParamKeys:list,hyperParamVals:dict,bestHyperParamValsAndError:list)->list:

            if not hyperParamKeys:
                self.model.hyperParamSet(hyperParamVals)
                cpdFactor = self.model.query(queries,evidences,False)
                error = abs(cpdFactor.get_val((True,))-targets.get_val((True,)))
                if error < bestHyperParamValsAndError[1]:
                    bestHyperParamValsAndError = [hyperParamVals,error]
                return bestHyperParamValsAndError

            hyperParamKey = hyperParamKeys[0]

            for thisKeyVal in self.hyperParamCandidates[hyperParamKey]:
                bestHyperParamValsAndError = search(hyperParamKeys[1:],{**hyperParamVals,hyperParamKey:thisKeyVal},\
                                                    bestHyperParamValsAndError)
            return bestHyperParamValsAndError

        bestHyperParamValsAndError = search(list(self.hyperParamCandidates.keys()),dict(),[dict(),float('inf')])
        self.model.hyperParamSet(bestHyperParamValsAndError[0])
        return self.model

def main_test():
    #TODO IMPLEMENT A GENERAL TEST FUNC
    pass

if __name__ == '__main__':
    main_test()
