.PHONY: install lint type-check test test-e2e build sonar coverage clean

install:
	.\\gradlew.bat dependencies

lint:
	.\\gradlew.bat lint

type-check:
	.\\gradlew.bat compileDebugKotlin

test:
	.\\gradlew.bat testDebugUnitTest

test-e2e:
	.\\gradlew.bat testDebugUnitTest --rerun-tasks

coverage:
	.\\gradlew.bat jacocoTestReport

build:
	.\\gradlew.bat assembleDebug

sonar:
	.\\gradlew.bat jacocoTestReport
	sonar-scanner -Dsonar.qualitygate.wait=true

clean:
	.\\gradlew.bat clean
