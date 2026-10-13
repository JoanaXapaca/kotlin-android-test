QMS Software Validation



Standard: ISO 13485:2016 — SOP 4.1.6

Responsible: Joana Rego



1\. Validated Software

| Software | Version | Purpose | Validation |

| Jenkins | LTS | CI/CD orchestration | Tested on every build |

| SonarQube Community | 26.9 | Static analysis | Quality Gate configured |

| SonarScanner CLI | 8.1.0.6389 | Scanner | Tested locally |

| Git | 2.55 | Version control | Used in production |

| JDK | 21 | Runtime | Tests passed |

| Kotlin | 2.x | Language | Unit tests |

| Gradle | 9.6 | Build | Build validated |

| JaCoCo | 0.8.x | Coverage | 100% |

| Robolectric | 4.15.1 | E2E testing | 3 tests passing |

| Android SDK | 37.0 | Platform | Compilation success |

| Python | 3.14 | Report scripts | Manual validation |



2\. Integrity

| Software | Integrity check |

| Jenkins | Authentication via credentials |

| SonarQube | Token read from local file |

| Git | HTTPS + token |

| Gradle | gradle-wrapper.jar versioned |

| npm | Not applicable |



3\. Risks

| Risk | Mitigation |

| SonarQube Community does not detect injections | Complementary tools |

| Android SDK version incompatibility | Use stable API 37.0 |

| Gradle cache invalidation | Configuration cache enabled |

| Outdated dependencies | Periodic review |



4\. References

\- ISO 13485:2016 sec. 4.1.6

\- Quality Manual GlobeStar v01.47

