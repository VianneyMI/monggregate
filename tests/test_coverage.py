"""Tests for the structure of the project.

This test checks that every Python module in src/monggregate has a corresponding
test file in tests/tests_monggregate with the appropriate naming convention.

Conventions:
- src/monggregate/module.py -> tests/tests_monggregate/test_module.py
- src/monggregate/subpackage/module.py -> tests/tests_monggregate/tests_subpackage/test_module.py
"""

import os
from pathlib import Path

import pytest


def get_python_files(directory: Path) -> list[str]:
    """Get all Python files in the given directory recursively.

    This function uses os.walk which yields a 3-tuple for each directory it visits:
    - root: The path to the directory
    - dirs: List of subdirectories in the directory
    - files: List of files in the directory

    Example of os.walk output:
    For a structure like:
        src/
        └── monggregate/
            ├── __init__.py
            ├── base.py
            └── stages/
                ├── __init__.py
                └── match.py

    os.walk would yield:
    1. ("src/monggregate", ["stages"], ["__init__.py", "base.py"])
    2. ("src/monggregate/stages", [], ["__init__.py", "match.py"])

    Args:
        directory: Path to the root directory to search in

    Returns:
        List of relative paths to Python files from the root directory
    """
    python_files = []
    for folder, _, files in os.walk(directory):
        if folder != "__pycache__":
            for file in files:
                if file.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(folder, file), directory)
                    python_files.append(rel_path)
    return python_files


def get_expected_test_path(src_file: str, test_root: Path) -> Path:
    """Convert a source file path to its expected test file path.

    Args:
        src_file: Relative path to the source file from src/monggregate
        test_root: Root directory for tests (tests/tests_monggregate)

    Returns:
        Path to where the test file should be located

    Example:
        src_file = "stages/match.py"
        test_root = Path("tests/tests_monggregate")
        -> returns Path("tests/tests_monggregate/tests_stages/test_match.py")
    """
    src_path = Path(src_file)

    # Add the "test_" prefix to the filename
    test_filename = f"test_{src_path.name}"

    # Add 'tests_' prefix to each directory part
    test_path_parts = []
    for part in src_path.parent.parts:
        test_path_parts.append(f"tests_{part}" if part else part)

    # Construct the full test path
    test_path = test_root / Path(*test_path_parts) / test_filename

    return test_path


def find_missing_tests(src_files: list[str], test_root: Path) -> list[tuple[str, str]]:
    """Find source files that don't have corresponding test files.

    Args:
        src_files: List of relative paths to source files
        test_root: Root directory for tests

    Returns:
        List of tuples (source_file, expected_test_file) for missing tests
    """
    missing_tests = []

    for src_file in src_files:
        # Skip __init__.py files since they might not need tests
        if os.path.basename(src_file) == "__init__.py":
            continue

        expected_test_path = get_expected_test_path(src_file, test_root)

        if not expected_test_path.exists():
            test_rel_path = expected_test_path.relative_to(test_root)
            missing_tests.append((str(src_file), str(test_rel_path)))

    return missing_tests


def calculate_coverage_stats(
    src_files: list[str], missing_tests: list[tuple[str, str]]
) -> tuple[int, int, float]:
    """Calculate test coverage statistics.

    Args:
        src_files: List of all source files
        missing_tests: List of files missing tests

    Returns:
        Tuple of (total_modules, missing_count, coverage_percentage)
    """
    total_modules = len(src_files) - sum(
        1 for f in src_files if os.path.basename(f) == "__init__.py"
    )
    missing_count = len(missing_tests)
    coverage_percent = (
        ((total_modules - missing_count) / total_modules) * 100
        if total_modules > 0
        else 0
    )

    return total_modules, missing_count, coverage_percent


def generate_error_message(
    total_modules: int,
    missing_count: int,
    coverage_percent: float,
    missing_tests: list[tuple[str, str]],
) -> str:
    """Generate an error message for missing test files.

    Args:
        total_modules: Total number of modules
        missing_count: Number of missing test files
        coverage_percent: Coverage percentage
        missing_tests: List of files missing tests

    Returns:
        Error message for missing test files
    """
    error_msg = (
        f"Missing {missing_count} test files out of {total_modules} modules "
        f"({coverage_percent:.1f}% coverage):\n\n"
    )
    if missing_tests:
        error_msg += "\n".join(
            [f"- {src} → Missing test: {test}" for src, test in missing_tests]
        )
    return error_msg


def test_all_modules_have_tests() -> None:
    """Test that every Python module in src/monggregate has a corresponding
    test file in tests/tests_monggregate with the appropriate naming convention.

    Conventions:
    - src/monggregate/module.py -> tests/tests_monggregate/test_module.py
    - src/monggregate/subpackage/module.py -> tests/tests_monggregate/tests_subpackage/test_module.py
    """
    src_root = Path("src/monggregate")
    test_root = Path("tests/tests_monggregate")

    # Get all Python files in the source directory containing the code to be tested
    src_files = get_python_files(src_root)

    # Find which test files are missing
    missing_tests = find_missing_tests(src_files, test_root)

    # Calculate coverage statistics
    total_modules, missing_count, coverage_percent = calculate_coverage_stats(
        src_files, missing_tests
    )

    # Format error message if needed
    error_msg = generate_error_message(
        total_modules, missing_count, coverage_percent, missing_tests
    )

    assert not missing_tests, error_msg
