from bayesianNet import *

fac1 = Factor(('a', 'b'), {(True, True): 0.1, (False, True): 0.3, (True, False): 0.2, (False, False): 0.5})

fac2 = Factor(('b',), {(True,): 0.6, (False,): 0.9})

fac3 = Factor(('d', 'c', 'b'), {(True, True, True): 0.1, (False, True, True): 0.3, (True, False, True): 0.2,
                                (False, False, True): 0.5, (True, True, False): 0.1, (False, True, False): 0.3, (True, False, False): 0.2,
                                (False, False, False): 0.5})

model = BayesianModel([('a','b'),('a','d'),('c','d')])
model.add_cpd('a',[[0.1,0.2],[0.3,0.5]],['b'])
model.add_cpd('b',[[0.6],[0.9]])
model.add_cpd('d',[[0.1,0.1,0.2,0.2],[0.3,0.3,0.5,0.5]],['c','b'])
gibbs_sampler = GibbsSampler(model,step=100,burnInCoefficient=0,thinningGap=1)
ve = VE(model)
grid_search_tuner = GridSearchTuner(gibbs_sampler,burnInCoefficient=np.arange(0,0.3,0.1),thinningGap=np.arange(1,4))

def VE_test():

    resVE = ve.query(['a'])

    resGibbs = gibbs_sampler.query(['a'])

def GridSearchTest():

    resVE = ve.query(['a'])

    bestModel = grid_search_tuner.tune(['a'],resVE)

    resGibbs = bestModel.query(['a'])

    pass

if __name__ == '__main__':
    while 1:

        functions={'VE':VE_test,'GS':GridSearchTest,'q':exit}

        functions[input('Please input the test function name {}, q for exit: '.format(list(functions.keys())))]()

