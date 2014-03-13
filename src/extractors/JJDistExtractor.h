#ifndef JJDISTEXTRACTOR_H_
#define JJDISTEXTRACTOR_H_
#include <sharp/main>
#include "FeatureExtractor.h"
class JJDistExtractor : public FeatureExtractor{
	public:
		JJDistExtractor(std::string name, sharp::ExtendedHypertree* e);
		bool extract(double* r);
	private:
		sharp::ExtendedHypertree* instance;
};
#endif
