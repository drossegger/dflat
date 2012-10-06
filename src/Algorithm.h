#pragma once

#include <sharp/main>

class Algorithm : public sharp::AbstractSemiNormalizedHTDAlgorithm
{
public:
	//! @param normalizationType either sharp::SemiNormalization or sharp::DefaultNormalization
	Algorithm(sharp::Problem& problem, const sharp::PlanFactory& planFactory, sharp::NormalizationType normalizationType = sharp::SemiNormalization);

protected:
	virtual sharp::Plan* selectPlan(sharp::TupleTable* table, const sharp::ExtendedHypertree* root);

	/**
	 * Do not override this! Rather override exchangeLeaf() and
	 * exchangeNonLeaf(). This method calls them, deletes the child tuple set
	 * afterwards, and optionally outputs debug information.
	 */
	sharp::TupleTable* evaluatePermutationNode(const sharp::ExtendedHypertree* node);
	//! The same goes for this method.
	sharp::TupleTable* evaluateBranchNode(const sharp::ExtendedHypertree* node);

	// Override these methods to process exchange nodes. Potential child tuples are passed to exchangeNonLeaf().
	virtual sharp::TupleTable* exchangeLeaf(const sharp::VertexSet& vertices, const sharp::VertexSet& introduced, const sharp::VertexSet& removed) = 0;
	virtual sharp::TupleTable* exchangeNonLeaf(const sharp::VertexSet& vertices, const sharp::VertexSet& introduced, const sharp::VertexSet& removed, const sharp::TupleTable& childTable) = 0;
	// Override this method to process join nodes. If you don't, there's a default implementation.
	virtual sharp::TupleTable* join(const sharp::VertexSet& vertices, sharp::TupleTable& childTableLeft, sharp::TupleTable& childTableRight);

	virtual sharp::ExtendedHypertree* prepareHypertreeDecomposition(sharp::ExtendedHypertree* root);

	sharp::Problem& problem;
	sharp::NormalizationType normalizationType;

#if PROGRESS_REPORT > 0
	int nodesProcessed; // For progress report
	virtual void printProgressLine(const sharp::ExtendedHypertree* node, size_t numChildTuples = 0);
	virtual sharp::TupleTable* evaluateNode(const sharp::ExtendedHypertree* node);
#endif
#ifdef VERBOSE
	virtual void printBagContents(const sharp::VertexSet& vertices) const;
#endif
};
