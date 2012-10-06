#pragma once

#include <set>
#include <boost/foreach.hpp>
#define foreach BOOST_FOREACH
#include <sharp/main>

struct Tuple : public sharp::Tuple
{
	virtual ~Tuple();
	virtual bool operator<(const sharp::Tuple&) const;
	virtual bool operator==(const sharp::Tuple&) const;
	virtual int hash() const;

	typedef std::set<sharp::Vertex> VertexSet;
	VertexSet m;

#ifndef NDEBUG
	void print(std::ostream&) const;
	void print(std::ostream&, class Problem&) const; // prints names instead of vertex numbers for atoms
#endif
};
