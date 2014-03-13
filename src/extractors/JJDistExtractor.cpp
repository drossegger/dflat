#include "JJDistExtractor.h"
JJDistExtractor::JJDistExtractor(std::string name, sharp::ExtendedHypertree* e){
	featurename=name;
	JJDistExtractor::instance=e;
}
bool JJDistExtractor::extract(double* r){

	*r=JJDistExtractor::instance->getJoinJoinDistanceSum();
	//cout << "DecompositionWidth: "<< *r << endl;
	return true;
}
