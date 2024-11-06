#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <unordered_map>
#include <vector>
#include <filesystem>

namespace fs = std::filesystem;

struct FunctionData
{
    std::string fileName;
    std::vector<std::string> callees;
};

void parseFortranFiles(const std::string &directory, std::unordered_map<std::string, FunctionData> &callGraph)
{
    std::regex callRegex(R"(\bCALL\s+(\w+))");                                                     // Detects function calls
    std::regex defRegex(R"(^\s*(program|subroutine|function|module)\s+(\w+))", std::regex::icase); // Detects definitions
    std::string currentFunction;

    for (const auto &entry : fs::recursive_directory_iterator(directory))
    {
        if (entry.path().extension() == ".f90" || entry.path().extension() == ".F")
        {
            std::ifstream file(entry.path());
            if (!file.is_open())
            {
                std::cerr << "Error opening file: " << entry.path() << std::endl;
                continue;
            }

            std::string line;
            while (std::getline(file, line))
            {
                std::smatch match;
                if (std::regex_search(line, match, defRegex))
                {
                    currentFunction = match[2];
                    callGraph[currentFunction].fileName = entry.path().filename().string(); // Store file name
                }
                else if (std::regex_search(line, match, callRegex))
                {
                    if (!currentFunction.empty())
                    {
                        callGraph[currentFunction].callees.push_back(match[1]);
                    }
                }
            }
        }
    }
}

void outputCallGraphDot(const std::unordered_map<std::string, FunctionData> &callGraph)
{
    std::ofstream outFile("call_graph.dot");
    outFile << "digraph CallGraph {" << std::endl;
    for (const auto &[caller, data] : callGraph)
    {
        for (const auto &callee : data.callees)
        {
            outFile << "    \"" << caller << " (" << data.fileName << ")\" -> \"" << callee << "\";" << std::endl;
        }
    }
    outFile << "}" << std::endl;
}

void outputCallGraphText(const std::unordered_map<std::string, FunctionData> &callGraph)
{
    std::ofstream outFile("base_call_graph.txt");
    for (const auto &[caller, data] : callGraph)
    {
        outFile << caller << " (" << data.fileName << ") -> ";
        bool first = true;
        for (const auto &callee : data.callees)
        {
            if (!first)
            {
                outFile << ", ";
            }
            outFile << callee;
            first = false;
        }
        outFile << std::endl
                << std::endl;
    }
}

int main()
{
    // replace the Build_roms directory path here
    std::string directory = "H:\IISc\Call_Graph\callGraph_ioecopy"; 
    std::unordered_map<std::string, FunctionData> callGraph;

    parseFortranFiles(directory, callGraph);
    // outputCallGraphDot(callGraph);  // Output DOT format
    outputCallGraphText(callGraph); // Output text format

    std::cout << "Call graph generated in call_graph.dot and base_call_graph.txt" << std::endl;
    return 0;
}