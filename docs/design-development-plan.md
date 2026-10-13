Design and Development Plan



Project: Kotlin Android Test

Standard: ISO 13485:2016 - SOP 7.3.1

Version: 1.0.0

Author: Joana Rego



1\. Objective

This document defines the design and development plan for the project, including phases, responsibilities, inputs, and outputs of each phase, as required by ISO 13485:2016 section 7.3.1.



2\. Life Cycle

The life cycle follows the IEC 62304 model, adapted to the scope of this project.



| Phase | Description | Responsible |

| 1. Planning | Requirements definition | Product Management |

| 2. Design | Architecture and specification | R\&D |

| 3. Implementation | Coding | R\&D |

| 4. Verification | Unit tests and static analysis | R\&D + QA |

| 5. Validation | E2E tests and acceptance | QA |

| 6. Release | Git tag and APK publication | R\&D |

| 7. Maintenance | Post-release support | Technical Support |



3\. Pipeline Stages

| Stage | Tool | ISO Phase |

| Checkout | Git | All |

| Install | ./gradlew dependencies | Implementation |

| Lint | ./gradlew lint | Verification |

| Type-check | ./gradlew compileDebugKotlin | Verification |

| Unit Tests | ./gradlew testDebugUnitTest | Verification |

| E2E Tests | Robolectric (JVM) | Verification |

| Coverage | JaCoCo | Verification |

| SonarQube | SonarQube Community | Verification |

| Build | ./gradlew assembleDebug | Release |

| Audit Report | Python | All |



4\. Entry and Exit Criteria

| Phase | Entry | Exit | Criterion |

| Implementation | Approved requirement | Committed code | Git push |

| Verification | Committed code | Tests passed + Quality Gate | Coverage >= 80%, 0 Issues |

| Release | Verification passed | APK + Git tag | Quality Gate Passed |

| Maintenance | Bug report | Bug fix | New cycle |



5\. Responsibilities

| Role | Responsibility |

| R\&D | Implementation, unit tests, bug fixes |

| QA | Validation, E2E tests, Quality Gate review |

| Product Management | Requirements definition, release approval |

| Management Representative | Final approval |



6\. Tools Used

| Tool | Version | Purpose |

| Kotlin | 2.x | Language |

| JDK | 21 | Runtime |

| Android SDK | 37.0 | Android platform |

| Gradle | 9.6 | Build |

| JaCoCo | 0.8.x | Coverage |

| Robolectric | 4.15.1 | E2E testing |

| Jenkins | LTS | CI/CD orchestration |

| SonarQube | Community 26.9 | Static analysis |

| Git | 2.55 | Version control |



7\. Interface Management

| Interface | Responsible | How |

| R\&D <-> QA | Both | Pull Requests + Jenkins |

| QA <-> Product | QA lead | Management Review |

| Product <-> Customer | Sales | Jira |



8\. Plan Updates

This plan is reviewed at the start of each new feature, after each major release, or when there are significant changes to the QMS.



9\. References

\- ISO 13485:2016, section 7.3.1

\- IEC 62304 - Medical Device Software Life Cycle

\- Quality Manual GlobeStar v01.47

