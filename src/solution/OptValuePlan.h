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

#include <sharp/main>

#include "../Tuple.h"

namespace solution {

class OptValuePlan : public sharp::Plan
{
public:
	static OptValuePlan* leaf(const Tuple& tuple);
	static OptValuePlan* extend(const OptValuePlan* base, const Tuple& extension);
	static OptValuePlan* unify(const OptValuePlan* left, const OptValuePlan* right);
	static OptValuePlan* join(const OptValuePlan* left, const OptValuePlan* right, const Tuple& joined);

protected:
	virtual sharp::Solution* materializeLeaf() const;
	virtual sharp::Solution* materializeExtension() const;
	virtual sharp::Solution* materializeUnion() const;
	virtual sharp::Solution* materializeJoin() const;

private:
	OptValuePlan(unsigned cost, unsigned currentCost);
	unsigned cost;
	unsigned currentCost;
};

} // namespace solution
