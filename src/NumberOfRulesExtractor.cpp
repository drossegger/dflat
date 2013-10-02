#include "NumberOfRulesExtractor.h"
#include <boost/filesystem.hpp>
#include <boost/algorithm/string.hpp>
using namespace std;
NumberOfRulesExtractor::NumberOfRulesExtractor(string name,vector<string> files){
	programfiles=files;
		featurename=name;
}
bool NumberOfRulesExtractor::extract(double* r){
	string gringoPath="/home/dino/workspace/dflat/tools/bin/gringo";
	string clasprePath="/home/dino/workspace/dflat/tools/bin/claspre";
	string fileString="";
	char buffer[128];
	string result = "";
	vector<string> resultLines;
	vector<string> resultsplitted;

	ofstream myfile;
  myfile.open ("program.txt");
  myfile << programfiles.at(1);
  myfile.close();
	string cmd=gringoPath +" " + programfiles.at(0) + " program.txt | " + clasprePath + " --claspfolio 1";
	FILE* pipe = popen(cmd.c_str(), "r");
  if (!pipe) return false;
	result = "";
	while(!feof(pipe)) {
		if(fgets(buffer, 128, pipe) != NULL)
			result += buffer;
	}
	pclose(pipe);
	
	
	boost::split(resultLines,result,boost::is_any_of("\n"));
	boost::split(resultsplitted,resultLines.at(resultLines.size()-2),boost::is_any_of(","));
  boost::filesystem::path p("program.txt");
	boost::filesystem::remove(p);
	*r=atoi(resultsplitted.at(4).c_str());
	
	return true;


}
