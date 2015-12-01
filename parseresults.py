import sys
from am_instrument_parser import TestResult
from am_instrument_parser import ParseAmInstrumentOutput

if(len(sys.argv) != 3):
    print("Please provide inputFile and outputFile as arguments!")
    sys.exit()

inputFile = sys.argv[1]
outputFile = sys.argv[2]

print("Will read from file '" + inputFile + "' and output to '" + outputFile + "'" )

with open(inputFile, "r") as myfile:
    data = myfile.read()

result = TestResult(data);

output = ParseAmInstrumentOutput(data)
testResults = output[0]

failures = 0
for result in testResults:
    if(result.GetStatusCode() < 0 ):
        failures += 1

print("Amount of steps = " + str(len(testResults)))

with open(outputFile, "w") as outfile:
    outfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    outfile.write("<testsuites name=\"Unit Tests\" tests=\"" + str(len(testResults)) + "\" failures=\"" + str(failures) + "\">\n")
    outfile.write("\t<testsuite name=\"Aggregated\" tests=\"" + str(len(testResults)) + "\" failures=\"" + str(failures)+ "\">\n")

    for result in testResults:
        outfile.write("\t\t<testcase name=\"" + result.GetTestName() + "\">\n")
        if(result.GetStatusCode() < 0 ):
            outfile.write("\t\t\t<failure> <![CDATA[" + result.GetFailureReason() + "]]></failure>\n")
        outfile.write("\t\t</testcase>\n");
    outfile.write("\t</testsuite>\n")
    outfile.write("</testsuites>\n")

print(outputFile + " exported")
