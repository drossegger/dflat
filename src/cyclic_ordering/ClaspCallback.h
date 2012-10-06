#pragma once

#include <clasp/clasp_facade.h>

#include "ClaspAlgorithm.h"
#include "Tuple.h"

namespace cyclic_ordering {

class GringoOutputProcessor;

// Gets called by clasp whenever a model has been found
class ClaspCallback : public Clasp::ClaspFacade::Callback
{
public:
	ClaspCallback(const ClaspAlgorithm& algorithm, sharp::TupleSet& newTuples, const GringoOutputProcessor& gringoOutput, const sharp::VertexSet& vertices)
		: algorithm(algorithm), newTuples(newTuples), gringoOutput(gringoOutput), numVertices(vertices.size())
	{}

	// Called if the current configuration contains unsafe/unreasonable options
	virtual void warning(const char* msg);

	// Called on entering/exiting a state
	virtual void state(Clasp::ClaspFacade::Event, Clasp::ClaspFacade&);

	// Called for important events, e.g. a model has been found
	virtual void event(const Clasp::Solver& s, Clasp::ClaspFacade::Event e, Clasp::ClaspFacade& f);

private:
	const ClaspAlgorithm& algorithm;
	sharp::TupleSet& newTuples;
	const GringoOutputProcessor& gringoOutput;
	const unsigned int numVertices;

	typedef std::pair<std::string,unsigned> ElementAndNumber;
	typedef std::pair<ElementAndNumber, Clasp::Literal> MappingAndLiteral;
	typedef std::vector<MappingAndLiteral> MappingAndLiteralVec;
	MappingAndLiteralVec map;
};

} // namespace cyclic_ordering