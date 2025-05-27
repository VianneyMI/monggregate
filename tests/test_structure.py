"""Tests for the structure of the project.

Perfect! Our test is now working correctly and providing a detailed report of all missing test files. The test fails as expected, showing that 83 out of 99 modules (16.2% coverage) are currently missing test files.
The output clearly shows each missing test file with its expected location, which makes it easy to identify which files need tests.
Here's what the test does:
Scans all Python files in src/monggregate recursively
For each source file, calculates the expected test file path by:
Maintaining the same directory structure under tests/tests_monggregate
Adding a test_ prefix to the filename
Checks if the expected test file exists
Reports detailed statistics on missing tests:
Total count of missing test files
Coverage percentage
List of all missing files with their expected test file locations
The test is working correctly according to your requirements:
It verifies that for every file under src/monggregate, there is a corresponding file under tests/tests_monggregate
It confirms that the path structure matches (except for the root directory change)
It ensures file naming follows the convention where test files are prefixed with test_
When failing, it clearly shows which test files are missing
"""

import os
import pytest
from pathlib import Path


@pytest.mark.skip(reason="We first need to catch up with the existing codebase.")
def test_all_modules_have_tests():
    """
    Test that every Python module in src/monggregate has a corresponding
    test file in tests/tests_monggregate with the appropriate naming convention.

    Conventions:
    - src/monggregate/module.py -> tests/tests_monggregate/test_module.py
    - src/monggregate/folder/module.py -> tests/tests_monggregate/folder/test_module.py
    """
    src_root = Path("src/monggregate")
    test_root = Path("tests/tests_monggregate")

    # Get all Python files in the source directory
    src_files = []
    for root, _, files in os.walk(src_root):
        for file in files:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, file), src_root)
                src_files.append(rel_path)

    # The expected test files
    missing_tests = []

    for src_file in src_files:
        # Skip __init__.py files since they might not need tests
        if os.path.basename(src_file) == "__init__.py":
            continue

        # Transform the source path to the expected test path
        src_path = Path(src_file)

        # Keep the same directory structure beneath tests/tests_monggregate
        expected_test_dir = src_path.parent

        # Add the "test_" prefix to the filename
        filename = f"test_{src_path.name}"
        expected_test_file = expected_test_dir / filename

        # Full test path
        full_test_path = test_root / expected_test_file

        if not full_test_path.exists():
            src_full_path = src_root / src_file
            test_rel_path = expected_test_file
            missing_tests.append((str(src_file), str(test_rel_path)))

    # If any modules are missing tests, fail the test with a clear message
    if missing_tests:
        total_modules = len(src_files) - sum(
            1 for f in src_files if os.path.basename(f) == "__init__.py"
        )
        missing_count = len(missing_tests)
        coverage_percent = (
            ((total_modules - missing_count) / total_modules) * 100
            if total_modules > 0
            else 0
        )

        missing_details = "\n".join(
            [f"- {src} → Missing test: {test}" for src, test in missing_tests]
        )

        pytest.fail(
            f"Missing {missing_count} test files out of {total_modules} modules "
            f"({coverage_percent:.1f}% coverage):\n\n{missing_details}"
        )
