#ifndef AVERAGEWIDTHEXTRACTOR_H_
#define AVERAGEWIDTHEXTRACTOR_H_
#include <sharp/main>
#include "FeatureExtractor.h"
class AverageWidthExtractor : public FeatureExtractor{
	public:
		AverageWidthExtractor(std::string name, sharp::ExtendedHypertree* e);
		bool extract(double* r);
	private:
		sharp::ExtendedHypertree* instance;
};
#endif
