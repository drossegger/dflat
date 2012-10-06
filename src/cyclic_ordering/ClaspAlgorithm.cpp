#include "ClaspAlgorithm.h"
#include "Problem.h"
#include "GringoOutputProcessor.h"
#include "ClaspCallback.h"
#if PROGRESS_REPORT > 1
#include <iomanip>
#endif

namespace cyclic_ordering {

ClaspAlgorithm::ClaspAlgorithm(Problem& problem, const char* exchangeNodeProgram, const std::string& instanceFacts, sharp::NormalizationType normalizationType)
	: ::ClaspAlgorithm(problem, exchangeNodeProgram, instanceFacts, normalizationType)
{
}


std::auto_ptr<Clasp::ClaspFacade::Callback> ClaspAlgorithm::newClaspCallback(sharp::TupleSet& newTuples, const ::GringoOutputProcessor& gringoOutput, const sharp::VertexSet& vertices) const
{
	return std::auto_ptr<Clasp::ClaspFacade::Callback>(new ClaspCallback(*this, newTuples, dynamic_cast<const GringoOutputProcessor&>(gringoOutput), vertices));
}

std::auto_ptr< ::GringoOutputProcessor> ClaspAlgorithm::newGringoOutputProcessor() const
{
	return std::auto_ptr< ::GringoOutputProcessor>(new GringoOutputProcessor(problem));
}

} // namespace cyclic_ordering
