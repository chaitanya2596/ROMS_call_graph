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

void parseFortranFiles(const std::string &directory, std::unordered_map<std::string, FunctionData> &callGraph, bool includeNf90)
{
    std::regex callRegex(R"(\bCALL\s+(\w+))");                                                     // Detects function calls
    std::regex defRegex(R"(^\s*(program|subroutine|function|module)\s+(\w+))", std::regex::icase); // Detects definitions
    std::regex nf90Regex(R"(\bnf90_\w+)"); // Detects nf90_ functions
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
                // Ignore lines that start with '!'
                if (line.empty() || line[0] == '!')
                {
                    continue;
                }

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
                else if (includeNf90 && std::regex_search(line, match, nf90Regex))
                {
                    if (!currentFunction.empty())
                    {
                        callGraph[currentFunction].callees.push_back(match[0]);
                    }
                }
            }
        }
    }
}

void outputCallGraphText(const std::unordered_map<std::string, FunctionData> &callGraph)
{
    std::ofstream outFile("build_graph/base_call_graph.txt");
    if (!outFile.is_open())
    {
        std::cerr << "Error opening output file" << std::endl;
        return;
    }

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
        outFile << std::endl << std::endl;
    }
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        std::cerr << "Usage: " << argv[0] << " <directory> [--include-nf90]" << std::endl;
        return 1;
    }

    std::string directory = argv[1];
    bool includeNf90 = (argc > 2 && std::string(argv[2]) == "--include-nf90");

    std::unordered_map<std::string, FunctionData> callGraph;

    parseFortranFiles(directory, callGraph, includeNf90);
    outputCallGraphText(callGraph); // Output text format

    std::cout << "dependency graph generated in base_call_graph.txt" << std::endl;
    return 0;
}