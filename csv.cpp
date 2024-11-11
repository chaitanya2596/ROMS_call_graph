#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>

using namespace std;

// Function to parse the input file and store the data in a map
map<string, pair<string, vector<string>>> parseFile(const string& filename) {
    ifstream file(filename);
    string line;
    map<string, pair<string, vector<string>>> callGraph;

    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return callGraph;
    }

    while (getline(file, line)) {
        size_t pos1 = line.find('(');
        size_t pos2 = line.find(')');
        size_t pos3 = line.find("->");

        if (pos1 != string::npos && pos2 != string::npos && pos3 != string::npos) {
            string callerFunction = line.substr(0, pos1 - 1);
            string callerFunctionDefined = line.substr(pos1 + 1, pos2 - pos1 - 1);
            string calleeFunctions = line.substr(pos3 + 2);

            stringstream ssCallees(calleeFunctions);
            string calleeFunction;
            vector<string> callees;
            while (getline(ssCallees, calleeFunction, ',')) {
                calleeFunction.erase(0, calleeFunction.find_first_not_of(" \t\n\r\f\v")); // Trim leading whitespace
                callees.push_back(calleeFunction);
            }
            callGraph[callerFunction] = make_pair(callerFunctionDefined, callees);
        }
    }

    return callGraph;
}

// Function to write the call graph to a CSV file
void writeCSV(const string& filename, const map<string, pair<string, vector<string>>>& callGraph) {
    ofstream outFile(filename);
    if (!outFile.is_open()) {
        cerr << "Error opening output file: " << filename << endl;
        return;
    }

    // Write the header
    outFile << "caller function,caller function defined,callee functions" << endl;

    // Write the data
    for (const auto& [callerFunction, data] : callGraph) {
        const auto& [callerFunctionDefined, callees] = data;
        outFile << callerFunction << "," << callerFunctionDefined << ",";
        bool first = true;
        for (const auto& callee : callees) {
            if (!first) {
                outFile << ", ";
            }
            outFile << callee;
            first = false;
        }
        outFile << endl;
    }
}

int main() {
    string inputFilename = "build_graph/base_call_graph.txt"; // Update this to your actual input file path
    string outputFilename = "build_graph/ROMS_call_graph.csv"; // Update this to your desired output file path

    // Parse the input file
    map<string, pair<string, vector<string>>> callGraph = parseFile(inputFilename);

    // Write the call graph to a CSV file
    writeCSV(outputFilename, callGraph);

    cout << "Call graph converted to CSV format in " << outputFilename << endl;
    return 0;
}