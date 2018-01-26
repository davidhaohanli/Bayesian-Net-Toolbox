import numpy as np
import pandas as pd
import scipy as sp
import os
import sys

class GraphNode(object):
     def __init__(self, x):
         self.parents = None
         self.name = x
         self.children = None

class Factor():
    def __init__(self):
        #TODO
        pass;

class BayesianModel(object):
    def __init__(self,*edges):
        #TODO
        pass;
    def add_nodes(self,*edges):
        #TODO
        pass;
    def get_nodes(self):
        #TODO
        pass;
    def check_node(self,nodeName):
        #TODO
        pass;
    def query_VE(self,*query,**evidence):
        #TODO
        pass;
    def sum_product_VE(self,*vars):
        #TODO
        pass;
    def sum_prduct_VE_var(self,var):
        #TODO
        pass;
    def topoSort(self):
        #TODO
        pass;
    def add_cpd(self,mat,var,*evidence):
        #TODO
        pass;

def main_test():
    #TODO IMPLEMENT A TEST FUNC
    pass;

if __name__ == '__main__':
    #TODO COMMENT ON THE MAIN
    main_test()