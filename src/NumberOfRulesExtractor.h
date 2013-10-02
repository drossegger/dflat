#ifndef NUMBEROFRULESEXTRACTOR_H_
#define NUMBEROFRULESEXTRACTOR_H_

#include "FeatureExtractor.h"
#include <vector>
#include <iostream>
#include <fstream>
#include <stdio.h>
class NumberOfRulesExtractor:public FeatureExtractor{
	public:
		NumberOfRulesExtractor(std::string name, std::vector<std::string> files);
		bool extract(double* r);
	private:
		std::vector<std::string> programfiles;

		
};
#endif
