Design Validation Plan



Project: Kotlin Android Test

Standard: ISO 13485:2016 - SOP 7.3.6



1\. Objective

Validate that the software meets user requirements in a simulated environment. The real clinical environment is out of scope.



2\. Validation Environment

| Item | Description |

| Operating system | Windows 11 |

| Runtime | JDK 21 |

| Framework | Android SDK 37.0 |

| Testing tool | Robolectric 4.15.1 |

| User | Developer / QA |

| Scenario | Simulated Android environment |



3\. E2E Tests

| ID | Test | Scenario | Acceptance Criterion |

| E2E-01 | MainActivity start | Robolectric.buildActivity | App starts without crashing |

| E2E-02 | Calculator add in Android | calculator.add(2, 3) | Returns 5 |

| E2E-03 | Calculator subtract in Android | calculator.subtract(10, 4) | Returns 6 |



4\. Limitations

Validation in a real clinical environment is not applicable to this pipeline test project. The real product, ConnexALL, is validated at the customer site.

Robolectric simulates the Android environment on the JVM but does not replace instrumented tests on a real device or emulator. For UI-level validation, additional instrumented tests would be required.

