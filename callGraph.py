####################  without function name printed   ####################
 
# import csv
# import sys
# from collections import defaultdict

# def parse_csv(filename):
#     call_graph = defaultdict(list)
#     with open(filename, 'r') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)  # Skip header row
#         for row in reader:
#             caller = row[0].strip()
#             callee_functions = [callee.strip() for callee in row[2:] if callee.strip()]
#             call_graph[caller].extend(callee_functions)
#     return call_graph

# def print_call_graph(call_graph, function, level=0):
#     indent = '\t' * level
#     print(f"{indent}{function}")
#     for callee in call_graph[function]:
#         print_call_graph(call_graph, callee, level + 1)

# def main():
#     if len(sys.argv) != 3:
#         print("Usage: python call_graph.py <csv_file> <function_name>")
#         sys.exit(1)

#     csv_file = sys.argv[1]
#     function_name = sys.argv[2]

#     call_graph = parse_csv(csv_file)
#     if function_name in call_graph:
#         print_call_graph(call_graph, function_name)
#     else:
#         print(f"Function '{function_name}' not found in the call graph.")

# if __name__ == "__main__":
#     main()


####################  with function name printed  ######################
# To call this script, run the following command: 
#    python3 callGraph.py ROMS_call_graph.csv ocean > callGraphFuncName.log
# Explaination: python3 callGraph.py <csv_file> <function_name to start the graph from> > <output_file>

# one issue: caldate fucntion calling itself may get into infinite loop
# remove it form csv file to avoid it       


####################  with function name printed  ######################
import csv
import sys
from collections import defaultdict

def parse_csv(csv_file):
    call_graph = defaultdict(lambda: {'file': '', 'callees': []})
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            caller = row[0].strip()
            caller_file = row[1].strip()
            callee_functions = [callee.strip() for callee in row[2:] if callee.strip()]
            call_graph[caller]['file'] = caller_file
            call_graph[caller]['callees'].extend(callee_functions)
    return call_graph

def print_call_graph(call_graph, function, level=0):
    indent = '\t' * level
    file_name = call_graph[function]['file']
    print(f"{indent}{function} ({file_name})")
    for callee in call_graph[function]['callees']:
        print_call_graph(call_graph, callee, level + 1)

def main():
    if len(sys.argv) != 3:
        print("Usage: python call_graph.py <csv_file> <function_name>")
        sys.exit(1)

    csv_file = sys.argv[1]
    function_name = sys.argv[2]

    call_graph = parse_csv(csv_file)
    if function_name in call_graph:
        print_call_graph(call_graph, function_name)
    else:
        print(f"Function '{function_name}' not found in the call graph.")

if __name__ == "__main__":
    main()