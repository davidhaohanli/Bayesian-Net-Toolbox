from bayesianNet import *

fac1 = Factor(('a', 'b'), {(True, True): 0.1, (False, True): 0.3, (True, False): 0.2, (False, False): 0.5})
fac2 = Factor(('b',), {(True,): 0.6, (False,): 0.9})
fac3 = Factor(('d', 'c', 'b'), {(True, True, True): 0.1, (False, True, True): 0.3, (True, False, True): 0.2,
                                (False, False, True): 0.5, (True, True, False): 0.1, (False, True, False): 0.3, (True, False, False): 0.2,
                                (False, False, False): 0.5})

ve = VE('notModelYet')

def facs_multi_test():

    res = ve.facs_multi([fac1, fac2, fac3])
    '''
    ############### NOT ('a','b','c','d') ##################
    res.scope = ('b','c','a','d')

    res.get_all_val()
    Out[2]:
    {(False, False, False, False): 0.225,       ---- checked
      ...
     (True, False, True, False): 0.03,          ---- checked
      ...
    }

     '''

    pass

def VE_test():
    #TODO UNFINISHED DEBUGGING
    res = ve.query(['a','d'],{'b':True},['a','b','c','d'],[fac1,fac2,fac3])

    pass

def sum_ve_test():
    res = ve.sum_ve(fac3,['b'])
    pass

def evidence_test():
    res = ve.giveEvidence(fac3, {'b':True})

    pass;

def sum_product_var_test():

    res=ve.sum_product_var([fac1,fac2,fac3],'a')

    pass

def sum_product_test():

    res=ve.sum_product([fac1,fac2,fac3],'a')

    pass

if __name__ == '__main__':
    while 1:

        functions={'multi':facs_multi_test,'sum_var':sum_product_var_test,\
                   'sum_ve':sum_ve_test,'evidence':evidence_test,'sum_product':sum_product_test,\
                   'VE':VE_test,'q':exit}

        functions[input('Please input the test function name {} for exit: '.format(list(functions.keys())))]()

