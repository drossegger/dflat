#include <boost/spirit/include/qi.hpp>
#include <boost/spirit/include/phoenix.hpp>
#include <boost/bind.hpp>
#include <boost/foreach.hpp>
#define foreach BOOST_FOREACH
#include <sharp/main>

#include "Problem.h"

namespace cyclic_ordering {

namespace qi = boost::spirit::qi;

namespace {	// Skipper for comments and whitespace
	template <typename Iterator>
	struct SkipperGrammar : qi::grammar<Iterator>
	{
		SkipperGrammar() : SkipperGrammar::base_type(start)
		{
			start = qi::space | ('%' >> *(qi::char_ - qi::eol));
		}
		qi::rule<Iterator> start;
	};

	template <typename Iterator>
	struct InstanceGrammar : qi::grammar<Iterator, SkipperGrammar<Iterator> >
	{
		typedef SkipperGrammar<Iterator> Skipper;

		InstanceGrammar(Problem& problem) : InstanceGrammar::base_type(start)
		{
			identifier = qi::char_("a-z") >> *qi::char_("A-Za-z0-9_");

			order = "order" >> qi::lit('(') >> identifier >> ',' >> identifier >> ',' >> identifier >> ')' >> '.';
			start = *order[boost::bind(&Problem::parsedOrdering, &problem, _1)];
		}

		qi::rule<Iterator, std::string()> identifier;
		qi::rule<Iterator, Skipper, std::vector<std::string>()> order;
		qi::rule<Iterator, Skipper> start;
	};
}




Problem::Problem(const std::string& input)
	: input(input)
{
}

void Problem::parsedOrdering(const std::vector<std::string>& args)
{
	sharp::VertexSet hyperedge;

	foreach(const std::string& arg, args) {
		sharp::Vertex v = storeVertexName(arg);
		vertices.insert(v);
		hyperedge.insert(v);
	}

	hyperedges.insert(hyperedge);
}

void Problem::parse()
{
	SkipperGrammar<std::string::const_iterator> skipper;
	InstanceGrammar<std::string::const_iterator> instanceParser(*this);

	std::string::const_iterator it = input.begin();
	std::string::const_iterator end = input.end();

	bool result = qi::phrase_parse(
			it,
			end,
			instanceParser,
			skipper
			);

	if(!result || it != end)
		throw std::runtime_error("Parse error");
}

void Problem::preprocess()
{
}

sharp::Hypergraph* Problem::buildHypergraphRepresentation()
{
	return createHypergraphFromSets(vertices, hyperedges);
}

} // namespace cyclic_ordering
