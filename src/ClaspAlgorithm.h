#pragma once

#include <clasp/clasp_facade.h>

#include "Algorithm.h"

class GringoOutputProcessor;
class Problem;

class ClaspAlgorithm : public Algorithm
{
public:
	ClaspAlgorithm(Problem& problem, const char* exchangeNodeProgram);

protected:
	virtual sharp::TupleSet* exchangeLeaf(const sharp::VertexSet& vertices, const sharp::VertexSet& introduced, const sharp::VertexSet& removed);
	virtual sharp::TupleSet* exchangeNonLeaf(const sharp::VertexSet& vertices, const sharp::VertexSet& introduced, const sharp::VertexSet& removed, const sharp::TupleSet& childTuples);
	virtual void setClaspConfig(Clasp::ClaspConfig& config) const;
	virtual std::auto_ptr<Clasp::ClaspFacade::Callback> newClaspCallback(sharp::TupleSet& newTuples, const GringoOutputProcessor&) const = 0;
	virtual std::auto_ptr<GringoOutputProcessor> newGringoOutputProcessor() const;

private:
	const char* exchangeNodeProgram;
	Clasp::ClaspFacade clasp;
};
