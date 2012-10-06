/*
Copyright 2012, Bernhard Bliem
WWW: <http://dbai.tuwien.ac.at/research/project/dynasp/dflat/>.

This file is part of D-FLAT.

D-FLAT is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

D-FLAT is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with D-FLAT.  If not, see <http://www.gnu.org/licenses/>.
*/

#pragma once

#include <clasp/reader.h>
#include <gringo/inclit.h>

#include "GringoOutputProcessor.h"

class ClaspInputReader : public Clasp::Input {
public:
	ClaspInputReader(Streams&, GringoOutputProcessor&);
	virtual ~ClaspInputReader();

	// Clasp::Input interface
	virtual Format format() const;
	virtual bool read(ApiPtr, int);
	virtual void addMinimize(Clasp::MinimizeBuilder&, ApiPtr);
	virtual void getAssumptions(Clasp::LitVec&);

private:
	typedef std::auto_ptr<Grounder> GrounderPtr;
	typedef std::auto_ptr<Parser> ParserPtr;

	TermExpansionPtr termExpansion;
	GrounderPtr grounder;
	ParserPtr parser;
	IncConfig config;
	GringoOutputProcessor& output;
};
