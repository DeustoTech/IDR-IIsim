# Testing and versioning

## Automated Testing

The model utilizes Continuous Integration (CI) with tests for units and integration using unittest, and it includes a minimum viable test case based on the cement example.

To improve robustness and transparency, we commit to the following:

* Code Coverage: A code coverage report will be generated and published with the CI results to clearly show the percentage of tested code.  
* Weird Input: The test suite will be expanded to include testing with "weird input" (e.g., boundary, zero, or highly improbable values) to ensure proper input checks are guaranteed.  
* Exception Handling: Tests for all ValueError exception handlings will be implemented to ensure that error paths are also correctly checked.

## Versioning

The model uses versioning, and we commit to following Semantic Versioning (SemVer) for future releases to clearly denote breaking (major), feature (minor), and patch (patch) changes. Dependency compatibility is explicitly handled via requirements.txt.
