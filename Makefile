# Makefile

# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 -lstdc++fs
OBJDIR = build_graph

# Targets and dependencies
all: $(OBJDIR) $(OBJDIR)/basefuncName $(OBJDIR)/csv callGraph

$(OBJDIR):
	mkdir -p $(OBJDIR)
	mkdir -p output

$(OBJDIR)/basefuncName: basefuncName.cpp
	$(CXX) $(CXXFLAGS) -o $(OBJDIR)/basefuncName basefuncName.cpp
# without inclusion of nf90 functions
	# $(OBJDIR)/basefuncName /mnt/h/IISc/Call_Graph/WORKING/callGraph/Build_roms --include-nf90

# with inclusion of nf90 functions as well
	$(OBJDIR)/basefuncName /mnt/h/IISc/Call_Graph/WORKING/callGraph/Build_roms
	@echo "Base function name is done"

$(OBJDIR)/csv: csv.cpp
	$(CXX) $(CXXFLAGS) -o $(OBJDIR)/csv csv.cpp
	$(OBJDIR)/csv
	@echo "csv is done"

callGraph: $(OBJDIR)/csv
	python3 callGraph.py build_graph/ROMS_call_graph.csv ocean callGraph.txt > $(OBJDIR)/recursive_Func.log
	@echo "call graph is generated"

clean:
	rm -rf $(OBJDIR) $(OBJDIR)/recursive_Func.log