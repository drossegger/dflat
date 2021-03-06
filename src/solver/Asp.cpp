/*{{{
Copyright 2012-2013, Bernhard Bliem
WWW: <http://dbai.tuwien.ac.at/research/project/dflat/>.

This file is part of D-FLAT.

D-FLAT is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

D-FLAT is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with D-FLAT.  If not, see <http://www.gnu.org/licenses/>.
*/
//}}}
#include <sstream>
#include <iostream>
#include <gringo/streams.h>

#include "Asp.h"
using namespace solver::asp;
using ChildItemTrees = GringoOutputProcessor::ChildItemTrees;

namespace {

std::unique_ptr<GringoOutputProcessor> newGringoOutputProcessor(const ChildItemTrees& childItemTrees, bool tableMode)
{
	if(tableMode)
		return std::unique_ptr<GringoOutputProcessor>(new tables::GringoOutputProcessor(childItemTrees));
	else
		return std::unique_ptr<GringoOutputProcessor>(new trees::GringoOutputProcessor(childItemTrees));
}

std::unique_ptr<ClaspCallback> newClaspCallback(bool tableMode, const GringoOutputProcessor& gringoOutputProcessor, const ChildItemTrees& childItemTrees, bool prune, const Debugger& debugger)
{
	if(tableMode)
		return std::unique_ptr<ClaspCallback>(new tables::ClaspCallback(dynamic_cast<const tables::GringoOutputProcessor&>(gringoOutputProcessor), childItemTrees, debugger));
	else
		return std::unique_ptr<ClaspCallback>(new trees::ClaspCallback(dynamic_cast<const trees::GringoOutputProcessor&>(gringoOutputProcessor), childItemTrees, prune, debugger));
}

} // anonymous namespace

namespace solver {

Asp::Asp(const Decomposition& decomposition, const Application& app, const std::string& encodingFile, bool tableMode)
	: Solver(decomposition, app)
	, encodingFile(encodingFile)
	, tableMode(tableMode)
{
}

ItemTreePtr Asp::compute()
{
	// Compute item trees of child nodes
	ChildItemTrees childItemTrees;
	for(const auto& child : decomposition.getChildren()) {
		ItemTreePtr itree = child->getSolver().compute();
		if(!itree)
			return itree;
		childItemTrees.emplace(child->getRoot().getGlobalId(), std::move(itree));
	}

	// Input: Child item trees
	std::unique_ptr<std::stringstream> childItemTreesInput(new std::stringstream);
	*childItemTreesInput << "% Child item tree facts" << std::endl;

	for(const auto& childItemTree : childItemTrees) {
		std::ostringstream rootItemSetName;
		rootItemSetName << 'n' << childItemTree.first;
		declareItemTree(*childItemTreesInput, childItemTree.second.get(), tableMode, childItemTree.first, rootItemSetName.str());
	}

	app.getDebugger().solverInvocationInput(decomposition.getRoot(), childItemTreesInput->str());

	// Input: Original problem instance
	std::unique_ptr<std::stringstream> instanceInput(new std::stringstream);
	*instanceInput << app.getInputString();

	// Input: Decomposition
	std::unique_ptr<std::stringstream> decompositionInput(new std::stringstream);
	declareDecomposition(decomposition, *decompositionInput);

	app.getDebugger().solverInvocationInput(decomposition.getRoot(), decompositionInput->str());

	// Put these inputs together
	Streams inputStreams;
	inputStreams.addFile(encodingFile, false); // Second parameter: "relative" here means relative to the file added previously, which does not exist yet
	// Remember: "Streams" deletes the appended streams -_-
	inputStreams.appendStream(Streams::StreamPtr(instanceInput.release()), "<instance>");
	inputStreams.appendStream(Streams::StreamPtr(decompositionInput.release()), "<decomposition>");
	inputStreams.appendStream(Streams::StreamPtr(childItemTreesInput.release()), "<child_itrees>");

	// Call the ASP solver
	std::unique_ptr<GringoOutputProcessor> outputProcessor(newGringoOutputProcessor(childItemTrees, tableMode));
	ClaspInputReader inputReader(inputStreams, *outputProcessor);
	std::unique_ptr<ClaspCallback> cb(newClaspCallback(tableMode, *outputProcessor, childItemTrees, app.isPruningDisabled() == false, app.getDebugger()));
	Clasp::ClaspConfig config;
	getClaspConfig(config);
	config.enumerate.numModels = 0;
	
	Clasp::ClaspFacade clasp;
	clasp.solve(inputReader, config, cb.get());

	ItemTreePtr result = cb->finalize();

	app.getDebugger().solverInvocationResult(decomposition.getRoot(), result.get());

	return result;
}

void Asp::getClaspConfig(Clasp::ClaspConfig & config){
	std::vector<Param> params=extraParams;
	Param p;
	while (!params.empty()){
		p=params.back();
		params.pop_back();
		if(p.name.compare("portfolio")==0){
			switch(p.value){
				case JUMPY:		
					jumpyConfig(config);
					break;
				case FRUMPY:
					frumpyConfig(config);
					break;
				case CRAFTY:
					craftyConfig(config);
					break;
				case NOPRE:
					nopreConfig(config);
					break;
				default:
					;
			}

		}
	}
}
void Asp::jumpyConfig(Clasp::ClaspConfig & config)
{
		config.master()->solver->strategies().heuId     = Clasp::ClaspConfig::heu_vsids; //heuristic
		config.master()->solver->strategies().updateLbd = 3; //update-lbd
		config.master()->solver->strategies().strRecursive = true; //strengthen
		config.master()->solver->strategies().otfs = 2; //otfs
		config.master()->solver->strategies().saveProgress = 70; //save-progress

		config.master()->params.reduce.strategy.fReduce = 75; //deletion 2
		config.master()->params.reduce.strategy.score   = Clasp::ReduceStrategy::reduce_linear; //del-algo
		config.master()->params.reduce.strategy.algo    = 2; //del-algo
		config.master()->params.reduce.strategy.glue    = 2; //del-glue

		config.master()->params.reduce.initRange.lo     = 1000; //del-init-r 1
		config.master()->params.reduce.initRange.hi     = 21000; //del-init-r 2
		config.master()->params.reduce.fGrow			      = 1.1; //del-grow
		config.master()->params.reduce.fMax 			      = 25; //del-grow
		config.master()->params.reduce.growSched	      = Clasp::ScheduleStrategy::geom(100,1.5); //del-grow
		config.master()->params.reduce.cflSched	        = Clasp::ScheduleStrategy::geom(10000,1.1); //del-cfl
		config.master()->params.restart.sched           = Clasp::ScheduleStrategy::luby(100); //restarts

}
void Asp::nopreConfig(Clasp::ClaspConfig & config)
{
		config.eq.noEq();
}
void Asp::frumpyConfig(Clasp::ClaspConfig & config)
{
		config.master()->solver->strategies().heuId     = Clasp::ClaspConfig::heu_berkmin; //heuristic
		config.master()->solver->strategies().strRecursive = false; //strengthen
		config.master()->solver->strategies().saveProgress = 180; //save-progress
		config.master()->solver->strategies().loopRep=Clasp::DefaultUnfoundedCheck::common_reason;//loops
		config.master()->solver->strategies().compress=250;//contractions

		config.master()->params.reduce.growSched				=	Clasp::ScheduleStrategy::none(); //deletion 1
		config.master()->params.reduce.fMax=0;
		config.master()->params.reduce.strategy.fReduce = 75; //deletion 2
		config.master()->params.reduce.strategy.score   = Clasp::ReduceStrategy::reduce_linear; //del-algo
		config.master()->params.reduce.initRange.lo     = 200; //del-init-r 1
		config.master()->params.reduce.initRange.hi     = 40200; //del-init-r 2
		config.master()->params.reduce.fGrow			      = 1.1; //del-grow
		config.master()->params.restart.sched           = Clasp::ScheduleStrategy::geom(100,1.5); //restarts
 
}
void Asp::craftyConfig(Clasp::ClaspConfig & config)
{
		config.master()->solver->strategies().heuId     = Clasp::ClaspConfig::heu_vsids; //heuristic
		config.master()->solver->strategies().strRecursive = false; //strengthen
		config.master()->solver->strategies().saveProgress = 180; //save-progress
		config.master()->solver->strategies().loopRep=Clasp::DefaultUnfoundedCheck::common_reason;//loops
		config.master()->solver->strategies().compress=250;//contractions

		config.master()->params.reduce.strategy.glue    = 2; //del-glue
		config.master()->solver->strategies().otfs = 2; //otfs
		config.master()->solver->strategies().compress = 250; //contraction
		config.master()->solver->strategies().reverseArcs = 1; //reverse-arcs
		config.master()->params.reduce.strategy.fReduce = 75; //deletion 2
		config.master()->params.reduce.fMax 			      = 20; //del-grow
		config.master()->params.reduce.fInit=(float)0.1;
		config.master()->params.reduce.strategy.score   = Clasp::ReduceStrategy::reduce_linear; //del-algo
		config.master()->params.reduce.initRange.lo     = 1000; //del-init-r 1
		config.master()->params.reduce.initRange.hi     = 10000; //del-init-r 2
		config.master()->params.reduce.fGrow			      = 1.1; //del-grow
		config.master()->params.restart.sched           = Clasp::ScheduleStrategy::geom(128,1.5); //restarts
		config.master()->params.restart.counterRestart = 3;
		config.master()->params.reduce.cflSched	        = Clasp::ScheduleStrategy::arith(1000,1000); //del-cfl
}
void Asp::declareDecomposition(const Decomposition& decomposition, std::ostream& out)
{
	out << "% Decomposition facts" << std::endl;
	out << "currentNode(" << decomposition.getRoot().getGlobalId() << ")." << std::endl;
	for(const auto& v : decomposition.getRoot().getBag()) {
		out << "bag(" << decomposition.getRoot().getGlobalId() << ',' << v << "). ";
		out << "current(" << v << ")." << std::endl;
	}

	for(const auto& child : decomposition.getChildren()) {
		out << "childNode(" << child->getRoot().getGlobalId() << ")." << std::endl;
		for(const auto& v : child->getRoot().getBag()) {
			out << "bag(" << child->getRoot().getGlobalId() << ',' << v << "). ";
			out << "-introduced(" << v << ")." << std::endl; // Redundant
		}
	}

	if(decomposition.getParents().empty())
		out << "final." << std::endl;
	else {
		for(const auto& parent : decomposition.getParents()) {
			out << "parentNode(" << parent->getRoot().getGlobalId() << ")." << std::endl;
			for(const auto& v : parent->getRoot().getBag())
				out << "bag(" << parent->getRoot().getGlobalId() << ',' << v << ")." << std::endl;
		}
	}

	// Redundant predicates for convenience...
	out << "introduced(X) :- current(X), not -introduced(X)." << std::endl;
	out << "removed(X) :- childNode(N), bag(N,X), not current(X)." << std::endl;
}

void Asp::declareItemTree(std::ostream& out, const ItemTree* itemTree, bool tableMode, unsigned int nodeId, const std::string& itemSetName, const std::string& parent, unsigned int level)
{
	if(!itemTree)
		return;

	// Declare this item set
	if(tableMode) {
		if(parent.empty() == false)
			out << "childRow(" << itemSetName << ',' << nodeId << ")." << std::endl;
	} else {
		out << "atLevel(" << itemSetName << ',' << level << ")." << std::endl;
		out << "atNode(" << itemSetName << ',' << nodeId << ")." << std::endl;
		if(parent.empty()) {
			out << "root(" << itemSetName << ")." << std::endl;
			out << "rootOf(" << itemSetName << ',' << nodeId << ")." << std::endl;
		} else {
			out << "sub(" << parent << ',' << itemSetName << ")." << std::endl;
			if(itemTree->getChildren().empty()) {
				out << "leaf(" << itemSetName << ")." << std::endl;
				out << "leafOf(" << itemSetName << ',' << nodeId << ")." << std::endl;
			}
		}
	}
	for(const auto& item : itemTree->getRoot()->getItems())
		out << "childItem(" << itemSetName << ',' << item << ")." << std::endl;
	for(const auto& item : itemTree->getRoot()->getAuxItems())
		out << "childAuxItem(" << itemSetName << ',' << item << ")." << std::endl;

	// Declare item tree node type
	switch(itemTree->getRoot()->getType()) {
		case ItemTreeNode::Type::UNDEFINED:
			break;
		case ItemTreeNode::Type::OR:
			out << "childOr(" << itemSetName << ")." << std::endl;
			break;
		case ItemTreeNode::Type::AND:
			out << "childAnd(" << itemSetName << ")." << std::endl;
			break;
		case ItemTreeNode::Type::ACCEPT:
			out << "childAccept(" << itemSetName << ")." << std::endl;
			break;
		case ItemTreeNode::Type::REJECT:
			out << "childReject(" << itemSetName << ")." << std::endl;
			break;
	}

	// If this is a leaf, declare cost
	const ItemTree::Children& children = itemTree->getChildren();
	if(children.empty()) {
		out << "childCost(" << itemSetName << ',' << itemTree->getRoot()->getCost() << ")." << std::endl;
	}
	else {
		// Declare child item sets
		size_t i = 0;
		for(const auto& child : children) {
			std::ostringstream childName;
			childName << itemSetName << '_' << i++;
			declareItemTree(out, child.get(), tableMode, nodeId, childName.str(), itemSetName, level+1);
		}
	}
}

} // namespace solver
