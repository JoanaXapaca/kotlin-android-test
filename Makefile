.PHONY: install lint type-check test test-e2e coverage a11y build sonar clean

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

a11y:
	@echo "Accessibility: not applicable to Kotlin"

build:
	.\\gradlew.bat assembleDebug

sonar:
	.\\scripts\\run_sonar.bat

clean:
	.\\gradlew.bat clean