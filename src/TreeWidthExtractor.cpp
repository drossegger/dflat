#include "TreeWidthExtractor.h"

TreeWidthExtractor::TreeWidthExtractor(std::string name, sharp::ExtendedHypertree* e){
	featurename=name;
	TreeWidthExtractor::instance=e;
}
bool TreeWidthExtractor::extract(int* r){
	*r=TreeWidthExtractor::instance->getTreeWidth();
	return true;
}
