/*{{{
Copyright 2012-2013, Bernhard Bliem
WWW: <http://dbai.tuwien.ac.at/research/project/dflat/>.

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

#include <clasp/clasp_facade.h>
//}}}
#include "../Solver.h"
#include "../Application.h"
#include "../ItemTree.h"
#include "../Decomposition.h"
#include "../Debugger.h"
#include "asp/tables/GringoOutputProcessor.h"
#include "asp/tables/ClaspCallback.h"
#include "asp/trees/GringoOutputProcessor.h"
#include "asp/trees/ClaspCallback.h"
#include "asp/ClaspInputReader.h"


namespace solver {

class Asp : public Solver
{
public:
	Asp(const Decomposition& decomposition, const Application& app, const std::string& encodingFile, bool tableMode);

	virtual ItemTreePtr compute() override;

	static void declareDecomposition(const Decomposition& decomposition, std::ostream& out);
	static void declareItemTree(std::ostream& out, const ItemTree* itemTree, bool tableMode, unsigned int nodeId, const std::string& itemSetName, const std::string& parent = "", unsigned int level = 0);

protected:
	std::string encodingFile;
	bool tableMode;
private:
	void getClaspConfig(Clasp::ClaspConfig &config);
	void frumpyConfig(Clasp::ClaspConfig &config);
	void jumpyConfig(Clasp::ClaspConfig &config);
	void craftyConfig(Clasp::ClaspConfig &config);
	void nopreConfig(Clasp::ClaspConfig &config);
};


} // namespace solver
