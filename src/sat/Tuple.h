#pragma once

#include <set>
#include <sharp/main>

#include "../Tuple.h"

namespace sat {

struct Tuple : public ::Tuple
{
	virtual bool operator<(const sharp::Tuple&) const;
	virtual bool operator==(const sharp::Tuple&) const;

	virtual bool matches(const ::Tuple& other) const;
	virtual Tuple* join(const ::Tuple& other) const;
	virtual void declare(std::ostream& out, const sharp::TupleSet::value_type& tupleAndSolution) const;
	virtual bool isValid(const sharp::Problem&, const sharp::ExtendedHypertree& root) const;

#ifdef VERBOSE
	virtual void print(std::ostream&, class ::Problem&) const; // prints names instead of vertex numbers for atoms
#endif	

	typedef std::set<sharp::Vertex> VertexSet;
	VertexSet atoms; // Atoms of the current bag that are true
	VertexSet clauses; // Clauses of the current bag that are true
};

} // namespace sat
