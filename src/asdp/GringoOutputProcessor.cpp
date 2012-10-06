#include "GringoOutputProcessor.h"

namespace asdp {

GringoOutputProcessor::GringoOutputProcessor(const sharp::Problem& problem)
	: problem(problem)
#ifndef NDEBUG
	  , mapArity(0)
#endif
{
}

void GringoOutputProcessor::printSymbolTableEntry(const AtomRef &atom, uint32_t arity, const std::string &name)
{
	::GringoOutputProcessor::printSymbolTableEntry(atom, arity, name);

#ifndef NDEBUG
	// Arity of map must be used consistently
	if(name == "map") {
		assert(!mapArity || mapArity == arity);
		mapArity = arity;
	}
#endif

	if(name == "map") {
		if(arity == 3) {
			std::stringstream firstArg; // First argument
			std::ostringstream args[2]; // The last two arguments
			ValVec::const_iterator k = vals_.begin() + atom.second;
			(k++)->print(s_, firstArg);
			(k++)->print(s_, args[0]);
			k->print(s_, args[1]);

			unsigned int firstArgNum;
			firstArg >> firstArgNum;

			mapAtoms.push_back(MapAtom(firstArgNum, args[0].str(), args[1].str(), atom.first));
		}
		else if(arity == 2) {
			std::ostringstream args[2]; // The two arguments
			ValVec::const_iterator k = vals_.begin() + atom.second;
			(k++)->print(s_, args[0]);
			k->print(s_, args[1]);

			mapAtoms.push_back(MapAtom(0, args[0].str(), args[1].str(), atom.first));
		}
	}
	else if(name == "chosenChildTuple") {
		assert(arity == 1);
		storeChildTupleAtom(name, atom, chosenChildTupleAtoms);
	}
	else if(name == "chosenChildTupleL") {
		assert(arity == 1);
		storeChildTupleAtom(name, atom, chosenChildTupleLAtoms);
	}
	else if(name == "chosenChildTupleR") {
		assert(arity == 1);
		storeChildTupleAtom(name, atom, chosenChildTupleRAtoms);
	}
	else if(name == "currentCost") {
		assert(arity == 1);
		storeCostAtom(name, atom, currentCostAtoms);
	}
	else if(name == "introducedCost") {
		assert(arity == 1);
		storeCostAtom(name, atom, introducedCostAtoms);
	}
}

inline void GringoOutputProcessor::storeChildTupleAtom(const std::string& name, const AtomRef& atom, LongToSymbolTableKey& store)
{
	std::stringstream firstArg; // First argument
	ValVec::const_iterator k = vals_.begin() + atom.second;
	k->print(s_, firstArg);
	store[std::strtol(firstArg.str().c_str()+1, 0, 0)] = atom.first;
}

inline void GringoOutputProcessor::storeCostAtom(const std::string& name, const AtomRef& atom, LongToSymbolTableKey& store)
{
	std::stringstream firstArg; // First argument
	ValVec::const_iterator k = vals_.begin() + atom.second;
	k->print(s_, firstArg);
	store[std::strtol(firstArg.str().c_str(), 0, 0)] = atom.first;
}

} // namespace asdp
