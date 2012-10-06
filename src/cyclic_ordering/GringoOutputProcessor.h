#pragma once

#include "../GringoOutputProcessor.h"

#include <sharp/main>

namespace cyclic_ordering {

class GringoOutputProcessor : public ::GringoOutputProcessor
{
public:
	GringoOutputProcessor(const sharp::Problem& problem);
	virtual void printSymbolTableEntry(const AtomRef &atom, uint32_t arity, const std::string &name);

	typedef std::pair<std::string,unsigned> ElementAndNumber; // Element and the number it is assigned
	typedef std::pair<ElementAndNumber,Clasp::SymbolTable::key_type> MappingAndSymbolTableKey;
	typedef std::vector<MappingAndSymbolTableKey> MappingAndSymbolTableKeyVec;
	const MappingAndSymbolTableKeyVec& getMap() const { return map; }

private:
	const sharp::Problem& problem;

	MappingAndSymbolTableKeyVec map; // Holds pairs of 1) pairs ("arg1","arg2") and 2) the key in the symbol table which is mapped to the clasp variable corresponding to "map(arg1,arg2)" (different keys may be mapped to the same variables due to clasp internals)
};

} // namespace cyclic_ordering