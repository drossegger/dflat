#ifndef FEATUREEXTRACTOR_H_
#define FEATUREEXTRACTOR_H_
#include <iostream>
class FeatureExtractor{
	public:
		//FeatureExtractor(std::string name,Input* i);
		virtual bool extract(double* r){return NULL;};
		std::string getName();
	protected: 
		std::string featurename;
};

#endif
