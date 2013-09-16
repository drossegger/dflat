#include "AlgorithmSelector.h"

using namespace std;
Algorithm::portfolio AlgorithmSelector::select(){
	FeatureExtractor* fe=features.front();
	int* r=new int(0);
	
	fe->extract(r);
	float numbers[features.size()][PORTFOLIO_SIZE];
	float finalNumbers[PORTFOLIO_SIZE];
	vector<string> line;
	int helper=0;
	for(list<FeatureExtractor*>::iterator it=features.begin();it!=features.end();++it,++helper){
		line=readPerformance("learner/"+(*it)->getName()+".csv",*r);	
		if(!line.empty())
			for(int i=0;i<PORTFOLIO_SIZE;++i)numbers[helper][i]=atof(line.at(i).c_str());
	}
	for (int i=0; i<PORTFOLIO_SIZE;++i)finalNumbers[i]=numbers[0][i];
	/*if(features.size()>1){
		for(unsigned int i=1;i<features.size();++i){
			for(int j=0;j<PORTFOLIO_SIZE;++j){
				finalNumbers[j]=finalNumbers[j]*numbers[i][j];
			}
		}
	}*/
	return (Algorithm::portfolio)findMax(finalNumbers,PORTFOLIO_SIZE);
}

int AlgorithmSelector::findMax(float* f, int size){
	float temp=100.0f;
	int index=0;
	for(int i=0; i<size;++i)
		if(temp>f[i]){
			temp=f[i];
			index=i;
		}
	return index;
}
vector<string> AlgorithmSelector::readPerformance(string spath,int feature){
	string line;
	vector<string> cols;
	boost::filesystem::path p(spath);
	if(boost::filesystem::exists(p)){
		ifstream file(spath.c_str());
		if(file.is_open()){
			while(file.good()){
				getline(file,line);
				boost::split(cols,line,boost::is_any_of(";"));
				if(atoi(cols.at(0).c_str())<=feature && atoi(cols.at(1).c_str())>feature){
					cols.erase(cols.begin(),cols.begin()+1);
					return cols;
				}
			}
		}

	}
	return cols;

}
