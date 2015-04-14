# Text Analysis Capstone
Code used for reading, counting, and pseudo-measuring the sentiment of environmentally sustainable words in company 10-K annual statements from the SEC. The program mainly uses the NLTK to extract words of interest (concept vectors) and also sentences that contain these words for 30 Fortune 500 companies.

# Functions
**getConceptVectors**: The program uses concept vectors or words that are of interest to search through the annual statements (10-K). This function extracts the Concept Vectors from a text file stored on the local computer.

**calculateWordFreq**: This function calculates the absolute frequency of the concept vectors in each of the 10-Ks that are being examined.

**calculateNormWordFreq**: This function calculates the normalized frequency of the concept vectors in each of the 10-Ks that are being examined.

**writeCSVWordFreqScores**: Writes the frequncies into a .csv file.

**sentExtract**: This function extracts the sentences within which the concept vectors occur. 

**getScores**: This function imports the 2010 Newsweek sustainability scores from a .txt file.

**matchScores**: The scores are matched to a given company (one of 30) that are being examined

**writeCSVRegression**: The function writes a .csv file that is later used to regress the frequency of sustainable words against the Newsweek sustainability score. 

**sentenceSentiment**: A pseudo sentiment analysis function that counts the frequency of positive and negative words in the sentences that contain the concept vectors (positive and negative word lists downloaded from: http://nealcaren.web.unc.edu/an-introduction-to-text-analysis-with-python-part-3/)

**findIndustry**: Extracts the industry of each of the companies from the Newsweek sustainability scores .txt file so that use of sustainable words can be generalized to the industry level. 

**writeCSVSentenceSentiment**: A .csv file is created with the company name, industry, psotive, and negative word frequencies for the sentences extracted. 

