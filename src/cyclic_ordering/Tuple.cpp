#include <cassert>
#include <boost/foreach.hpp>
#define foreach BOOST_FOREACH

#include "Tuple.h"
#include "Problem.h"

namespace cyclic_ordering {

bool Tuple::operator<(const sharp::Tuple& rhs) const
{
	return ordering < dynamic_cast<const Tuple&>(rhs).ordering;
}

bool Tuple::operator==(const sharp::Tuple& rhs) const
{
	return ordering == dynamic_cast<const Tuple&>(rhs).ordering;
}

bool Tuple::matches(const ::Tuple& other) const
{
	return ordering == dynamic_cast<const Tuple&>(other).ordering;
}

Tuple* Tuple::join(const ::Tuple& other) const
{
	return new Tuple(*this);
}

void Tuple::declare(std::ostream& out, const sharp::TupleSet::value_type& tupleAndSolution, const sharp::VertexSet& currentVertices) const
{
	out << "childTuple(t" << &tupleAndSolution << ")." << std::endl;
	for(unsigned int i = 0; i < ordering.size(); ++i) {
		const std::string& element = ordering[i];
		// TODO: Maybe only declare current vertices?
		out << "mapped(t" << &tupleAndSolution << ',' << element << ',' << i << ")." << std::endl;
	}
}

bool Tuple::isValid(const sharp::Problem& problem, const sharp::ExtendedHypertree& root) const
{
	// We only generate valid tuples in the first place
	return true;	
}

#ifdef VERBOSE
void Tuple::print(std::ostream& str, const sharp::Problem& problem) const
{
	str << "Tuple: ";
	foreach(std::string element, ordering)
		str << element << ' ';
	str << std::endl;
}
#endif

} // namespace cyclic_ordering