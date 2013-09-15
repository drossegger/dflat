#ifndef TREEWIDTHEXTRACTOR_H_
#define TREEWIDTHEXTRACTOR_H_
#include <sharp/main>
#include "FeatureExtractor.h"
class TreeWidthExtractor : public FeatureExtractor{
	public:
		TreeWidthExtractor(std::string name, sharp::ExtendedHypertree* e);
		bool extract(int* r);
	private:
		sharp::ExtendedHypertree* instance;
};
#endif
