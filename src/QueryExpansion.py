
import constants
import math
import sys
import pandas
import numpy
from nltk.stem import PorterStemmer

class RocchioAlgoImplementation:
    def __init__(self, termOne):
        self.query = {}
        self.query[termOne] = 1
     
        
    def RocchioAlgo(self, invertedFile, documentsList, relevantDocs, nonrelevantDocs):
        p = PorterStemmer()
        weights = {}
        for i in invertedFile.iterkeys():
            sterm = i
            if constants.STEM_IN_ROCCHIO:
                sterm = p.stem(i.lower(), 0,len(i)-1)            
            weights[sterm] = 0.0    
        print()

        TFWeights_Relevant,TFWeights_Nonrelevant = {},{}

        for i in relevantDocs:
            doc = documentsList[i]
            for term in doc["tfVector"]:
                sterm = term
                if constants.STEM_IN_ROCCHIO:
                    sterm = p.stem(term.lower(), 0,len(term)-1)

                if sterm in TFWeights_Relevant:
                    TFWeights_Relevant[sterm] = TFWeights_Relevant[sterm] + doc["tfVector"][term]
                else:
                    TFWeights_Relevant[sterm] = doc["tfVector"][term]

        
        for j in nonrelevantDocs:
            doc = documentsList[j]
            for term in doc["tfVector"]:
                sterm = term
                if constants.STEM_IN_ROCCHIO:
                    sterm = p.stem(term.lower(), 0,len(term)-1)                

                if sterm in TFWeights_Nonrelevant:
                    TFWeights_Nonrelevant[sterm] = TFWeights_Nonrelevant[sterm] + doc["tfVector"][term]
                else:
                    TFWeights_Nonrelevant[sterm] = doc["tfVector"][term]

        # CALCULATE ROCCHIO VECTOR
        for term in invertedFile.iterkeys():
            len1 = float(len(documentsList))
            idf = math.log( len1 / float(len(invertedFile[term].keys())), 10)


            sterm = term
            if constants.STEM_IN_ROCCHIO:
                sterm = p.stem(term.lower(), 0,len(term)-1)


            # CALCULATING THE TERM2 AND TERM3 OF RELEVANT AND NON-RELEVANT DOCS
            for docId in invertedFile[term].iterkeys():
                if documentsList[docId]['IsRelevant'] == 1:
                    # TERM 2: Relevant documents weights normalized 
                    weights[sterm] = weights[sterm] + constants.BETA * idf * (TFWeights_Relevant[sterm] / len(relevantDocs))
                if documentsList[docId]['IsRelevant'] != 1:
                    # Term 3: NonRelevant documents weights normalized 
                    weights[sterm] = weights[sterm] - constants.GAMMA * idf * (TFWeights_Nonrelevant[sterm]/len(nonrelevantDocs))

            # Term 1 of Rocchio, query terms
            if term in self.query:
                self.query[term] = constants.ALPHA * self.query[term] + weights[sterm]   #build new query vector of weights
            elif weights[sterm] > 0:
                self.query[term] = weights[sterm]

        return self.query