Traceability Matrix



Project: Kotlin Android Test

Standard: ISO 13485:2016 — SOP 7.3.2 + 7.3.5



Requirement -> Test Matrix

| Requirement | Description | Test | File | Status |

| REQ-01 | Integer addition | `add\_withPositiveNumbers\_returnsSum` | CalculatorTest.kt | OK |

| REQ-01 | Addition with negatives | `add\_withNegativeNumbers\_returnsSum` | CalculatorTest.kt | OK |

| REQ-01 | Addition with zero | `add\_withZero\_returnsSameNumber` | CalculatorTest.kt | OK |

| REQ-02 | Integer subtraction | `subtract\_withPositiveNumbers\_returnsDifference` | CalculatorTest.kt | OK |

| REQ-02 | Subtraction with negatives | `subtract\_withNegativeNumbers\_returnsDifference` | CalculatorTest.kt | OK |

| REQ-02 | Subtraction with zero | `subtract\_withZero\_returnsSameNumber` | CalculatorTest.kt | OK |

| REQ-03 | App starts without crashing | `e2e001\_mainActivityStartsWithoutCrashing` | MainActivityE2ETest.kt | OK |

| NFR-01 | Coverage >= 80% | JaCoCo report | Pipeline | 100% |

| NFR-02 | Quality Gate | SonarQube | Pipeline | OK |

| REG-01 | Traceability | HTML report | generate\_report.py | OK |

| REG-03 | Audit records | archiveArtifacts | Jenkinsfile | OK |



E2E Tests

| ID | Test | File | Status |

| E2E-01 | MainActivity starts without crashing | MainActivityE2ETest.kt | OK |

| E2E-02 | Calculator works in Android context | MainActivityE2ETest.kt | OK |

| E2E-03 | Calculator subtract works in Android context | MainActivityE2ETest.kt | OK |



References

\- ISO 13485:2016 sec. 7.3.2 (Inputs) and sec. 7.3.5 (Verification)

\- Quality Manual GlobeStar v01.47

