# reporting the recursive functions and writing to a file
import csv
import sys
from collections import defaultdict

def normalize_function_name(function_name):
    return function_name.replace('*', '').strip()

def parse_csv(csv_file):
    call_graph = defaultdict(lambda: {'file': '', 'callees': [], 'original_names': set()})
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            caller = row[0].strip()
            caller_file = row[1].strip()
            callee_functions = [callee.strip() for callee in row[2:] if callee.strip()]
            normalized_caller = normalize_function_name(caller)
            call_graph[normalized_caller]['file'] = caller_file
            call_graph[normalized_caller]['callees'].extend(callee_functions)
            call_graph[normalized_caller]['original_names'].add(caller)
            for callee in callee_functions:
                normalized_callee = normalize_function_name(callee)
                call_graph[normalized_callee]['original_names'].add(callee)
    return call_graph

def write_call_graph(call_graph, function, file, visited, level=0):
    indent = '\t' * level
    original_names = call_graph[function]['original_names']
    file_name = call_graph[function]['file']
    # Write the function name with the star if it exists
    function_name_to_write = next((name for name in original_names if '*' in name), function)
    file.write(f"{indent}{function_name_to_write} ({file_name})\n")
    visited.add(function)
    for callee in call_graph[function]['callees']:
        normalized_callee = normalize_function_name(callee)
        if normalized_callee == function:  # Detect recursive call
            print(f"Recursive call detected: {callee}")
            file.write(f"{indent}\tRecursive call detected: {callee}\n")
        elif normalized_callee not in visited:  # Avoid infinite recursion
            write_call_graph(call_graph, normalized_callee, file, visited, level + 1)
    visited.remove(function)

def main():
    if len(sys.argv) != 4:
        print("Usage: python callGraph.py <csv_file> <function_name> <output_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    function_name = normalize_function_name(sys.argv[2])
    output_file = sys.argv[3]

    call_graph = parse_csv(csv_file)
    if function_name in call_graph:
        with open(output_file, 'w') as file:
            write_call_graph(call_graph, function_name, file, set())
        print(f"Call graph written to {output_file}")
    else:
        print(f"Function {function_name} not found in call graph")

if __name__ == "__main__":
    main()