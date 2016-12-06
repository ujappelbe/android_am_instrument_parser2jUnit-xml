# android_am_instrument_parser2jUnit-xml

From https://github.com/ujappelbe/android_am_instrument_parser2jUnit-xml

Turn raw android "am instrument" commands run output into jUnit.xml. Gradle will normally do this for you. This might be useful if you need to run android unit tests separate from building the apk. Tested on Python 2.7.10

Built on am_instrument_parser.py from https://github.com/android/platform_development/blob/master/testrunner/am_instrument_parser.py

# usage
```
python parseresults.py req1 req2 opt1 opt2
```
**legend**
`req1` input raw file path
`req2` output junit.xml file path
`opt1` name of root- test suite (default "Root")
`opt2` style of prepended timestamp in raw result file (default empty = no timestamp)

**note**
the third argument can either be the root suite name or the timestamp style. if four arguments are provided the third is used as root suite name and the fourth as timestamp style.

## example

## without timestamp (default)
```
adb shell am instrument -r -w -e class com.organisation.app.test.UnitTestSuite com.organisation.app.test/android.support.test.runner.AndroidJUnitRunner raw_output.txt
python parseresults.py raw_output.txt test-junit.xml
```

## with timestamp

```
adb shell am instrument -r -w -e class com.organisation.app.test.UnitTestSuite com.organisation.app.test/android.support.test.runner.AndroidJUnitRunner | while read -r line; do echo "$(date '+%Y-%m-%d_%T') $line"; done| tee raw_output.txt
python parseresults.py raw_output.txt test-junit.xml %Y-%m-%d_%H:%M:%S
```
