# Makefile

# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 -lstdc++fs
OBJDIR = build_graph
DIR = /mnt/h/IISc/Call_Graph/WORKING/callGraph/Build_roms
INCLUDE_NF90 = 0  # Set to 1 to include nf90 functions, 0 otherwise
StartFunction = ocean

# Targets and dependencies
all: $(OBJDIR) $(OBJDIR)/basefuncName $(OBJDIR)/csv callGraph

$(OBJDIR):
	mkdir -p $(OBJDIR)

$(OBJDIR)/basefuncName: basefuncName.cpp
	$(CXX) $(CXXFLAGS) -o $(OBJDIR)/basefuncName basefuncName.cpp
ifeq ($(INCLUDE_NF90), 1)
	$(OBJDIR)/basefuncName DIR --include-nf90
else
	$(OBJDIR)/basefuncName DIR
endif
	@echo "Parsing done"

$(OBJDIR)/csv: csv.cpp
	$(CXX) $(CXXFLAGS) -o $(OBJDIR)/csv csv.cpp
	$(OBJDIR)/csv

	@echo "Coverting to csv done"

callGraph: $(OBJDIR)/csv
	python3 callGraph.py build_graph/ROMS_call_graph.csv StartFunction callGraph.txt > $(OBJDIR)/recursive_Func.log

	@echo "call graph is generated as callGraph.txt"

clean:
	rm -rf $(OBJDIR) 