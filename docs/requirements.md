Requirements Specification



Project: Kotlin Android Test

Standard: ISO 13485:2016 - SOP 7.3.2

Version: 1.0.0



1\. Functional Requirements

| ID | Requirement | Priority | Status |

| REQ-01 | `Calculator.add(a, b)` returns the sum of two integers | High | Implemented |

| REQ-02 | `Calculator.subtract(a, b)` returns the difference between two integers | High | Implemented |

| REQ-03 | The Android application starts without crashing | High | Implemented |

| REQ-04 | The application runs on Android API 24+ | High | Implemented |



2\. Non-Functional Requirements

| ID | Requirement | Metric | Status |

| NFR-01 | Test coverage >= 80% | SonarQube | 100% |

| NFR-02 | Quality Gate Passed | SonarQube | OK |

| NFR-03 | 0 Issues | SonarQube | OK |

| NFR-04 | 0 Vulnerabilities | SonarQube | OK |

| NFR-05 | Pipeline time < 10 min | Jenkins | \~5 min |

| NFR-06 | Lint without errors | ./gradlew lint | 0 issues |



3\. Regulatory Requirements

| ID | Requirement | Standard | Status |

| REG-01 | Test traceability | ISO 13485 sec. 7.3.5 | OK |

| REG-02 | Mandatory Quality Gate | FDA (SaMD) | OK |

| REG-03 | Audit records | ISO 13485 sec. 4.2.5 | OK |

| REG-04 | Version control | ISO 13485 sec. 4.2.4 | OK |

| REG-05 | Static analysis | OWASP Top 10 | Partial |



4\. Security Requirements

| ID | Requirement | OWASP Category | Status |

| SEC-01 | No injections | A03 | Community does not detect |

| SEC-02 | No hardcoded credentials | A02 | OK |

| SEC-03 | Updated dependencies | A06 | OK |



5\. Out of Scope

UI testing with Espresso, network communication, data persistence, user authentication.



6\. References

\- ISO 13485:2016 sec. 7.3.2

\- Quality Manual GlobeStar v01.47

\- OWASP Top 10 (2021)

