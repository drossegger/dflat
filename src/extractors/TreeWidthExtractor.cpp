#include "TreeWidthExtractor.h"
TreeWidthExtractor::TreeWidthExtractor(std::string name, sharp::ExtendedHypertree* e){
	featurename=name;
	TreeWidthExtractor::instance=e;
}
bool TreeWidthExtractor::extract(double* r){

	*r=TreeWidthExtractor::instance->getTreeWidth();
	//cout << "DecompositionWidth: "<< *r << endl;
	return true;
}
