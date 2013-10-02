#include "AverageWidthExtractor.h"
AverageWidthExtractor::AverageWidthExtractor(std::string name, sharp::ExtendedHypertree* e){
	featurename=name;
	AverageWidthExtractor::instance=e;
}
bool AverageWidthExtractor::extract(double* r){

	*r=AverageWidthExtractor::instance->getAverageWidth();
	return true;
}
