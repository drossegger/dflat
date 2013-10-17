#ifndef NUMBEROFRULESEXTRACTOR_H_
#define NUMBEROFRULESEXTRACTOR_H_

#include "FeatureExtractor.h"
#include <vector>
#include <set>
#include <iostream>
#include <fstream>
#include <stdio.h>
class NumberOfRulesExtractor:public FeatureExtractor{
	public:
		NumberOfRulesExtractor(std::string name, std::string files,std::set<std::string> hyperedgePredicateNames);
		bool extract(double* r);
	private:
		std::string program;
		std::set<std::string> edges;
		
};
#endif
