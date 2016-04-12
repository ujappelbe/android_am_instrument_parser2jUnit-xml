#############################################################
# This script will use am_instrument_parser from android SDK  #
# to parse android am instruments test raw output into        #
# junit.xml format.                                           #
# Usage: python parseresults.py req1 req2 opt1                #
#   req1: input raw file path                                 #
#   req2: output junit.xml file path                          #
#   opt1: name of Root- test suite (default "Root")           #
#############################################################

import sys
import re
import string
import argparse
from am_instrument_parser import TestResult
from am_instrument_parser import ParseAmInstrumentOutput


def writeOutput(outfile, testResults, resultsDict):
    # add the step that checks that all tests have been executed the
    # the number of total test steps
    totalNumTests = len(testResults) + 1
    failures = resultsDict['failures']
    skipped = resultsDict['skipped']

    with open(outputFile, "w") as outfile:
        outfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        outfile.write("<testsuites name=\"Unit Tests\" tests=\"" +
                      str(totalNumTests) + "\" failures=\"" + str(failures) +
                      "\" skipped=\"" + str(skipped) + "\"" + ">\n")
        outfile.write("\t<testsuite name=\"" + rootSuiteName + "\" tests=\"" +
                      str(totalNumTests) + "\" failures=\"" + str(failures) +
                      "\" skipped=\"" + str(skipped) + "\"" + ">\n")

        for result in testResults:
            outfile.write("\t\t<testcase name=\"" + str(result.GetTestName()) +
                          "\">\n")
            if(result.GetStatusCode() < 0):
                if(result.GetStatusCode() == -3):
                    outfile.write("\t\t\t<skipped />\n")
                else:
                    outfile.write("\t\t\t<failure> <![CDATA[" +
                                  str(result.GetFailureReason()) +
                                  "]]></failure>\n")
            outfile.write("\t\t</testcase>\n")
        outfile.write("\t\t<testcase name=\"All tests were executed\">\n")
        if(resultsDict['numTests'] != str(len(testResults))):
            outfile.write("\t\t\t<failure> <![CDATA[ Expected '" + resultsDict['numTests'] +
                          "' steps. Got results for '" +
                          str(len(testResults)) + "'" "]]></failure>\n")
        outfile.write("\t\t</testcase>\n")
        outfile.write("\t</testsuite>\n")
        outfile.write("</testsuites>\n")


# Returns tuple of testResults-object and dict with result metrics
def processRawResultsFile(inputFile):
    with open(inputFile, "r") as myfile:
        data = myfile.read()

    numTests = "-1"
    numTestsLine = -1
    reNumTests = re.compile(r'INSTRUMENTATION_STATUS: numtests=(\d*)$')
    for line in data.splitlines():
        numTestsLine += 1
        if(reNumTests.match(line)):
            numTests = str(reNumTests.search(line).group(1))
            break

    output, bundle = ParseAmInstrumentOutput(data)
    testResults = output
    resultSum = {}

    resultSum['failures'] = 0
    resultSum['skipped'] = 0
    resultSum['numTests'] = numTests
    for result in testResults:
        if(result.GetStatusCode() < 0):
            if(result.GetStatusCode() == -3):
                resultSum['skipped'] += 1
            else:
                resultSum['failures'] += 1
    if(numTests != str(len(testResults))):
        resultSum['failures'] += 1

    print("Amount of steps = " + str(len(testResults)) +
          " (Claimed " + str(numTests) + ")")
    return testResults, resultSum

# Parse arguments

parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('--infile', nargs='+', required=True,
                    action='append', dest='inputFiles', default=[])
parser.add_argument('--outfile', nargs=1, required=True,
                    dest='outputFile', action='store')
parser.add_argument('--rootname', nargs=1, required=False,
                    dest='rootSuiteName', action='store')

parsedArguments = parser.parse_args()

inputFiles = parsedArguments.inputFiles[0]
outputFile = parsedArguments.outputFile[0]

if(parsedArguments.rootSuiteName):
    rootSuiteName = parsedArguments.rootSuiteName[0]
else:
    rootSuiteName = "Root"


rootSuiteName = re.sub('[^A-Za-z0-9\.\-_, ]+', '', rootSuiteName)

print("Will read from files '" + str(inputFiles) + "' and output to '" +
      outputFile + "'")
print("Using '" + rootSuiteName + "' as test suite root name")

# Parse results
mergedResults = []
mergedResultsDict = None
for inputFile in inputFiles:
    testResults, resultsDict = processRawResultsFile(inputFile)
    mergedResults += testResults
    mergedResultsDict = mergedResultsDict or resultsDict
    for key in resultsDict:
        print("Checking key '" + key + "'")
        mergedResultsDict[key] += resultsDict[key]
    print("Results is a '" + type(testResults).__name__ + "'")

# Write output

writeOutput(outputFile, mergedResults, mergedResultsDict)

print(outputFile + " exported")
