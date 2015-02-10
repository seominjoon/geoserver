'''
Created on Oct 3, 2014

@author: minjoon
'''

from tempfile import mkdtemp

from geosolver.text.syntax.parsers import stanford_parser

def get_graph_paths(text):
    graphs = core_nlp.get_graphs(text)
    temp_path = mkdtemp()
    paths = CoreNLP.save_graphs(graphs, temp_path)
    return paths
    
        