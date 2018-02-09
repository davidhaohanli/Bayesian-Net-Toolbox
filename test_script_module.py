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
gibbs_sampler = Gibbs_sampler(model)

def VE_test():

    res = gibbs_sampler.query(['a','d'],{'b':True})

if __name__ == '__main__':
    while 1:

        functions={'VE':VE_test,'q':exit}

        functions[input('Please input the test function name {}, q for exit: '.format(list(functions.keys())))]()

