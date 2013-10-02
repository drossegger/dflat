#ifndef ALGORITHMSELECTOR_H_
#define ALGORITHMSELECTOR_H_

#include <list>
#include "Algorithm.h"
#include "FeatureExtractor.h"
#include <boost/filesystem.hpp>
#include <iostream>
#include <fstream>
#include <boost/algorithm/string.hpp>
class AlgorithmSelector{
	public:
		AlgorithmSelector(std::list<FeatureExtractor*>& fe) : features(fe){};
		Algorithm::portfolio select();
	private:
		std::list<FeatureExtractor*>& features;
		
		int findMax(float* input,int size);
		std::vector<std::string> readPerformance(std::string spath,double feature);
};

#endif
