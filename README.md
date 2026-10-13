Kotlin Android Test

Android/Kotlin demonstration project for the CI/CD pipeline, used as a base to replicate across other technologies.



Pipeline

Runs on Jenkins, with the following stages:

1\. Checkout — clones the Git repository

2\. Install — `./gradlew dependencies`

3\. Lint — `./gradlew lint`

4\. Type-check — `./gradlew compileDebugKotlin`

5\. Unit Tests — `./gradlew testDebugUnitTest`

6\. E2E Tests — Robolectric (JVM-based)

7\. Coverage — JaCoCo report

8\. SonarQube — `sonar-scanner -Dsonar.qualitygate.wait=true`

9\. Build — `./gradlew assembleDebug`

10\. Audit Report — `python scripts/generate\_report.py`



Trigger: Poll SCM every 5 minutes. Every push to the `main` branch triggers the pipeline.



Running locally



Requirements:

\- JDK 21

\- Android SDK (API 37.0)

\- Gradle (via wrapper)



Environment variables:

\- `JAVA\_HOME` = JDK 21 installation path

\- `ANDROID\_SDK\_ROOT` = Android SDK path



Commands:

| Command | What it does |

| `make install` | Downloads dependencies |

| `make lint` | Runs Android Lint |

| `make type-check` | Compiles Kotlin sources |

| `make test` | Runs unit tests |

| `make test-e2e` | Runs E2E tests (Robolectric) |

| `make coverage` | Generates JaCoCo report |

| `make build` | Builds debug APK |

| `make sonar` | Runs SonarQube analysis |

| `make clean` | Removes build artifacts |



Before pushing, run:

```bash

make lint

make test

make coverage

make build

Interpreting results

Jenkins:



Green: pipeline passed



Red: some stage failed; check Console Output



Artifacts: APK + reports archived on each build



SonarQube:



Dashboard: http://localhost:9000/dashboard?id=kotlin-android-test



Quality Gate must be Passed



Coverage is read from app/build/reports/jacoco/jacocoTestReport/jacocoTestReport.xml



Stack

Layer	Technology

Language	Kotlin 2.x

Runtime	JDK 21

Platform	Android SDK 37.0

Build	Gradle 9.6

Unit Tests	JUnit 4

E2E Tests	Robolectric 4.15.1

Coverage	JaCoCo

Lint	Android Lint

CI/CD	Jenkins

Static analysis	SonarQube



Structure

kotlin-android-test/

├── app/

│   ├── src/

│   │   ├── main/java/com/connexall/kotlintest/

│   │   │   ├── Calculator.kt

│   │   │   ├── MainActivity.kt

│   │   │   └── ui/theme/

│   │   ├── test/java/com/connexall/kotlintest/

│   │   │   ├── CalculatorTest.kt

│   │   │   └── MainActivityE2ETest.kt

│   │   └── androidTest/

│   └── build.gradle.kts

├── docs/

│   ├── design-development-plan.md

│   ├── requirements.md

│   ├── traceability-matrix.md

│   ├── qms-software-validation.md

│   ├── validation-plan.md

│   └── design-file/

│       └── README.md

├── scripts/

│   ├── generate\_report.py

│   └── run\_sonar.bat

├── Jenkinsfile

├── Makefile

├── sonar-project.properties

├── build.gradle.kts

├── settings.gradle.kts

├── gradlew / gradlew.bat

└── reports/   (generated)



Notes

Robolectric is used for E2E tests instead of an Android emulator (faster, no emulator required in CI).



JaCoCo is configured to exclude UI components (MainActivity, theme/) from coverage — only logic code counts.



The Sonar token is read from C:\\Users\\jrego\\sonar-token.txt via scripts/run\_sonar.bat.



JAVA\_HOME must point to JDK 21 (not JDK 25) for Android Gradle Plugin compatibility.



The Android SDK must be installed via Android Studio or command-line tools.



Quality Gate is enforced with sonar.qualitygate.wait=true.

