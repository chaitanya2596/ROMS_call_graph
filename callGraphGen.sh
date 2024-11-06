#!/bin/sh -f

# generate text call graph
g++ -o basefuncName basefuncName.cpp -std=c++17 -lstdc++fs

# convert text call graph to csv    
g++ -o csv csv.cpp -std=c++17 

# generate call graph
# can change the function name to generate call graph for different function\
# python3 callGraph.py <csv file> <function name> <output file>
python3 callGraph.py ROMS_call_graph.csv ocean > callGraphFuncName.log