#include "GringoOutputProcessor.h"

namespace cyclic_ordering {

GringoOutputProcessor::GringoOutputProcessor(const sharp::Problem& problem)
	: problem(problem)
{
}

void GringoOutputProcessor::printSymbolTableEntry(const AtomRef &atom, uint32_t arity, const std::string &name)
{
	::GringoOutputProcessor::printSymbolTableEntry(atom, arity, name);

	if(arity == 2 && name == "map") { // FIXME: I'm dirty
		std::pair<std::stringstream,std::stringstream> args; // The two arguments
		ValVec::const_iterator k = vals_.begin() + atom.second;
		(k++)->print(s_, args.first);
		k->print(s_, args.second);
		ElementAndNumber ei;
		ei.first = args.first.str();
		args.second >> ei.second;
		map.push_back(MappingAndSymbolTableKey(ei, atom.first));
	}
}

} // namespace cyclic_ordering