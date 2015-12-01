# android_am_instrument_parser2jUnit-xml

Turn raw android "am instrument" commands run output into jUnit.xml. Gradle will normally do this for you. This might be useful if you need to run android unit tests separate from building the apk. Tested on Python 2.7.10

# usage
adb shell am instrument -r -w -e class com.organisation.app.test.UnitTestSuite com.organisation.app.test/android.support.test.runner.AndroidJUnitRunner raw_output.txt
python parseresults.py raw_output.txt test-junit.xml
