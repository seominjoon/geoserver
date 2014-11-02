'''
Created on Oct 3, 2014

@author: minjoon
'''

from tempfile import mkdtemp

from geosolver.text.deptree_parsers import CoreNLP

def get_graph_paths(text):
    corenlp = CoreNLP()
    graphs = corenlp.get_graphs(text)
    temp_path = mkdtemp()
    paths = CoreNLP.save_graphs(graphs, temp_path)
    return paths
    
        