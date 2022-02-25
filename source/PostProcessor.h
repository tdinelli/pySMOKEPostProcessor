#ifndef POSTPROCESSOR_H
#define POSTPROCESSOR_H

#include <boost/filesystem.hpp>

#include "ProfilesDatabase.h"

class PostProcessor
{
public:
	
	
	PostProcessor(std::string postprocessorType, std::string kineticFolder, std::string outputFolder);
	
	~PostProcessor();

	void Prepare();

	void ComputeROPA();

	void SensitivityAnalysis();

	void PrintRecap_ROPA();

	void PrintRecap_SENSITIVITY();

	std::string ropaType_;
	std::string sensitivityType_;
	std::string kineticFolder_;
	std::string outputFolder_;
	std::string species_;

	std::string normalizationType_;
	std::string orderingType_;

	double localValue_;
	double lowerBound_;
	double upperBound_;
private:
	std::string postprocessorType_;
	ProfilesDatabase *data_;
};

#endif // POSTPROCESSOR_H
