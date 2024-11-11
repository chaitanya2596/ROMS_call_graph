# # function calling itself may get into infinite loop
# import csv
# import sys
# from collections import defaultdict

# def parse_csv(csv_file):
#     call_graph = defaultdict(lambda: {'file': '', 'callees': []})
#     with open(csv_file, 'r') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             caller = row[0].strip()
#             caller_file = row[1].strip()
#             callee_functions = [callee.strip() for callee in row[2:] if callee.strip()]
#             call_graph[caller]['file'] = caller_file
#             call_graph[caller]['callees'].extend(callee_functions)
#     return call_graph

# def print_call_graph(call_graph, function, level=0):
#     indent = '\t' * level
#     file_name = call_graph[function]['file']
#     print(f"{indent}{function} ({file_name})")
#     for callee in call_graph[function]['callees']:
#         if callee != function:  # Ignore if the function is calling itself
#             print_call_graph(call_graph, callee, level + 1)

# def main():
#     if len(sys.argv) != 3:
#         print("Usage: python call_graph.py <csv_file> <function_name>")
#         sys.exit(1)

#     csv_file = sys.argv[1]
#     function_name = sys.argv[2]

#     call_graph = parse_csv(csv_file)
#     if function_name in call_graph:
#         print_call_graph(call_graph, function_name)

# if __name__ == "__main__":
#     main()



# # writing to a file
# import csv
# import sys
# from collections import defaultdict

# def parse_csv(csv_file):
#     call_graph = defaultdict(lambda: {'file': '', 'callees': []})
#     with open(csv_file, 'r') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             caller = row[0].strip()
#             caller_file = row[1].strip()
#             callee_functions = [callee.strip() for callee in row[2:] if callee.strip()]
#             call_graph[caller]['file'] = caller_file
#             call_graph[caller]['callees'].extend(callee_functions)
#     return call_graph

# def write_call_graph(call_graph, function, file, level=0):
#     indent = '\t' * level
#     file_name = call_graph[function]['file']
#     file.write(f"{indent}{function} ({file_name})\n")
#     for callee in call_graph[function]['callees']:
#         if callee != function:  # Ignore if the function is calling itself
#             write_call_graph(call_graph, callee, file, level + 1)

# def main():
#     if len(sys.argv) != 4:
#         print("Usage: python callGraph.py <csv_file> <function_name> <output_file>")
#         sys.exit(1)

#     csv_file = sys.argv[1]
#     function_name = sys.argv[2]
#     output_file = sys.argv[3]

#     call_graph = parse_csv(csv_file)
#     if function_name in call_graph:
#         with open(output_file, 'w') as file:
#             write_call_graph(call_graph, function_name, file)

# if __name__ == "__main__":
#     main()

# reporting the recursive fucntions and writing to a file
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

def write_call_graph(call_graph, function, file, visited, level=0):
    indent = '\t' * level
    file_name = call_graph[function]['file']
    file.write(f"{indent}{function} ({file_name})\n")
    visited.add(function)
    for callee in call_graph[function]['callees']:
        if callee == function:  # Detect recursive call
            print(f"Recursive call detected: {callee}")
            file.write(f"{indent}\tRecursive call detected: {callee}\n")
        elif callee not in visited:  # Avoid infinite recursion
            write_call_graph(call_graph, callee, file, visited, level + 1)
    visited.remove(function)

def main():
    if len(sys.argv) != 4:
        print("Usage: python callGraph.py <csv_file> <function_name> <output_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    function_name = sys.argv[2]
    output_file = sys.argv[3]

    call_graph = parse_csv(csv_file)
    if function_name in call_graph:
        with open(output_file, 'w') as file:
            write_call_graph(call_graph, function_name, file, set())

if __name__ == "__main__":
    main()