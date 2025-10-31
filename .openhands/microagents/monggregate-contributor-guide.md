---
name: Monggregate Contributor Guide
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers: []
---

# Monggregate Contributor Guide

This microagent provides comprehensive documentation and guidance for developers and AI Code Agents contributing to the Monggregate project - a Python library that simplifies MongoDB aggregation pipelines through an Object-Oriented Programming interface.

## 📋 Project Overview

**Monggregate** is a lightweight QueryBuilder for MongoDB aggregation pipelines that:
- Provides an OOP interface to MongoDB aggregation pipelines
- Is based on Pydantic and compatible with all MongoDB drivers and ODMs
- Enables pandas-style chaining of operations
- Integrates MongoDB documentation for quick reference
- Supports autocompletion for MongoDB features

**Current Version**: 0.22.1
**Python Requirements**: >=3.10
**License**: MIT
**Author**: Vianney Mixtur

## 🏗️ Repository Structure

```
monggregate/
├── .github/                    # GitHub workflows and CI/CD
│   └── workflows/
├── .openhands/                 # OpenHands microagents
│   └── microagents/
├── docs/                       # MkDocs documentation
│   ├── api.md
│   ├── contributing.md
│   ├── how-to/
│   ├── intro/
│   ├── reference/
│   └── tutorial/
├── requirements/               # Dependency management
│   ├── all.txt
│   ├── build.txt
│   ├── core.txt
│   ├── doc.txt
│   ├── linting.txt
│   ├── optional.txt
│   ├── testing.txt
│   └── typing.txt
├── src/monggregate/           # Main source code
│   ├── operators/             # MongoDB operators implementation
│   │   ├── accumulators/
│   │   ├── arithmetic/
│   │   ├── array/
│   │   ├── boolean/
│   │   ├── comparison/
│   │   ├── conditional/
│   │   ├── custom/
│   │   ├── data_size/
│   │   ├── date/
│   │   ├── objects/
│   │   ├── strings/
│   │   └── type_/
│   ├── search/                # Search functionality
│   │   ├── collectors/
│   │   ├── commons/
│   │   └── operators/
│   ├── stages/                # Pipeline stages
│   │   └── search/
│   ├── base.py
│   ├── dollar.py              # S and SS classes
│   ├── fields.py
│   ├── pipeline.py            # Main Pipeline class
│   └── utils.py
├── tests/                     # Test suite
│   ├── tests_docs/
│   ├── tests_legacy/
│   ├── tests_monggregate/
│   └── tests_operators/
├── pyproject.toml             # Project configuration
├── requirements.txt           # Dependencies
├── uv.lock                    # UV lock file
├── mkdocs.yml                 # Documentation config
├── mypy.ini                   # Type checking config
└── pytest.ini                # Testing config
```

## 🔧 Development Environment Setup

### Prerequisites
- Python 3.10 or higher
- Git
- UV (recommended) or pip for dependency management

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/VianneyMI/monggregate.git
   cd monggregate
   ```

2. **Install dependencies**:
   ```bash
   # Using UV (recommended)
   uv sync

   # Or using pip
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Install development dependencies**:
   ```bash
   # For testing
   pip install -r requirements/testing.txt
   
   # For linting
   pip install -r requirements/linting.txt
   
   # For documentation
   pip install -r requirements/doc.txt
   
   # Or install all dev dependencies
   pip install -r requirements/all.txt
   ```

## 🧪 Testing Guidelines

### Test Structure
- **Unit tests**: Located in `tests/tests_monggregate/`
- **Operator tests**: Located in `tests/tests_operators/`
- **Documentation tests**: Located in `tests/tests_docs/`
- **Legacy tests**: Located in `tests/tests_legacy/`

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/tests_monggregate/test_pipeline.py

# Run with coverage
pytest --cov=src/monggregate

# Run with HTML report
pytest --html=report.html
```

### Test Configuration
- **pytest.ini**: Contains pytest configuration
- **Coverage**: Configured to track coverage in `src/monggregate`
- **Test utilities**: Available in `tests/utils.py`

## 🔍 Code Quality Standards

### Linting and Formatting
The project uses multiple tools for code quality:

1. **Black**: Code formatting
   ```bash
   black src/ tests/
   ```

2. **Ruff**: Fast Python linter
   ```bash
   ruff check src/ tests/
   ruff format src/ tests/
   ```

3. **MyPy**: Static type checking
   ```bash
   mypy src/monggregate
   ```

### Type Hints
- **Required**: All public APIs must have type hints
- **Configuration**: See `mypy.ini` for type checking rules
- **Dependencies**: Uses `typing-extensions>=4.0` for compatibility

### Code Style Guidelines
- Follow PEP 8 standards
- Use descriptive variable and function names
- Add docstrings to all public classes and methods
- Keep functions focused and single-purpose
- Use type hints consistently

## 🏛️ Architecture Patterns

### Core Components

1. **Pipeline Class** (`pipeline.py`):
   - Main entry point for building aggregation pipelines
   - Supports method chaining (fluent interface)
   - Exports to MongoDB-compatible format

2. **Dollar Classes** (`dollar.py`):
   - `S`: Single dollar sign operations
   - `SS`: Double dollar sign operations
   - Provides MongoDB operator access

3. **Stages** (`stages/`):
   - Each MongoDB stage has its own class
   - Inherits from base stage class
   - Validates input parameters

4. **Operators** (`operators/`):
   - Organized by category (arithmetic, array, etc.)
   - Each operator is a separate class
   - Follows consistent interface pattern

### Design Patterns Used

1. **Builder Pattern**: Pipeline construction
2. **Factory Pattern**: Operator creation
3. **Strategy Pattern**: Different operator implementations
4. **Fluent Interface**: Method chaining for pipeline building

### Pydantic Integration
- All models inherit from Pydantic BaseModel
- Automatic validation and serialization
- Type safety and IDE support
- JSON schema generation

## 📝 Documentation Standards

### Documentation Structure
- **MkDocs**: Used for documentation generation
- **API Reference**: Auto-generated from docstrings
- **Tutorials**: Step-by-step guides
- **How-to Guides**: Problem-solving focused

### Writing Documentation
1. **Docstrings**: Use Google-style docstrings
2. **Examples**: Include practical examples
3. **Type Information**: Document parameter and return types
4. **Cross-references**: Link to related functionality

### Building Documentation
```bash
# Install documentation dependencies
pip install -r requirements/doc.txt

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

## 🔄 Contribution Workflow

### Branch Strategy
- **main**: Stable release branch
- **feature/***: New feature development
- **bugfix/***: Bug fixes
- **docs/***: Documentation updates

### Pull Request Process
1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/your-feature-name`
3. **Make changes** following code quality standards
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Run full test suite**: `pytest`
7. **Run linting**: `ruff check && black --check .`
8. **Commit changes** with descriptive messages
9. **Push to your fork**
10. **Create pull request** to main branch

### Commit Message Format
```
type(scope): brief description

Detailed explanation if needed

- List specific changes
- Reference issues: Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🚀 Release Process

### Version Management
- **Tool**: bumpver (configured in pyproject.toml)
- **Pattern**: MAJOR.MINOR.PATCH
- **Files updated**: pyproject.toml, src/monggregate/__init__.py

### Release Steps
1. **Update version**: `bumpver update patch|minor|major`
2. **Update changelog**: Document changes in docs/changelog.md
3. **Create release tag**: Automatically done by bumpver
4. **Build package**: `python -m build`
5. **Upload to PyPI**: `twine upload dist/*`

## 🐛 Debugging Guidelines

### Common Issues
1. **Import errors**: Check PYTHONPATH and package installation
2. **Type errors**: Run mypy to catch type issues early
3. **Test failures**: Use pytest's verbose mode for details
4. **MongoDB connection**: Ensure test database is available

### Debugging Tools
- **pytest**: Use `-v` for verbose output, `-s` to see print statements
- **pdb**: Python debugger for step-through debugging
- **logging**: Use Python's logging module for debug output

## 🔐 Security Considerations

### Environment Variables
- **MongoDB URI**: Store in `.env` file (not committed)
- **API Keys**: Never commit to repository
- **Test Data**: Use sample databases, not production data

### Dependencies
- **Regular updates**: Keep dependencies current
- **Security scanning**: Monitor for vulnerabilities
- **Minimal dependencies**: Only include necessary packages

## 📊 Performance Guidelines

### Optimization Strategies
1. **Lazy evaluation**: Don't execute until needed
2. **Efficient operators**: Use appropriate MongoDB operators
3. **Index awareness**: Consider database indexes in pipeline design
4. **Memory usage**: Be mindful of large result sets

### Benchmarking
- **Test with realistic data sizes**
- **Compare with raw MongoDB queries**
- **Profile memory usage**
- **Monitor execution time**

## 🤝 Community Guidelines

### Communication
- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Code reviews**: Be constructive and respectful
- **Documentation**: Help improve documentation clarity

### Mentoring
- **New contributors**: Welcome and guide newcomers
- **Code reviews**: Explain reasoning behind suggestions
- **Knowledge sharing**: Document lessons learned
- **Best practices**: Share and discuss improvements

## 🔧 Implicit Rules and Conventions

### Code Organization
1. **One class per file** for operators and stages
2. **Consistent naming**: Use MongoDB terminology
3. **Import organization**: Group imports logically
4. **Error handling**: Use appropriate exception types

### Testing Conventions
1. **Test file naming**: `test_*.py` pattern
2. **Test class naming**: `Test*` pattern
3. **Test method naming**: `test_*` descriptive names
4. **Fixtures**: Use pytest fixtures for common setup

### Documentation Conventions
1. **API documentation**: Auto-generated from docstrings
2. **Examples**: Include in docstrings and separate files
3. **Cross-references**: Link related functionality
4. **Version compatibility**: Note version requirements

## 🎯 Software Engineering Best Practices

### Development Lifecycle

#### 1. Planning Phase
- **Requirements gathering**: Understand MongoDB features to implement
- **Design review**: Consider API consistency and usability
- **Architecture decisions**: Document major design choices
- **Timeline estimation**: Break work into manageable chunks

#### 2. Implementation Phase
- **Test-driven development**: Write tests before implementation
- **Incremental development**: Small, focused commits
- **Code reviews**: Peer review all changes
- **Continuous integration**: Automated testing on all changes

#### 3. Testing Phase
- **Unit testing**: Test individual components
- **Integration testing**: Test component interactions
- **End-to-end testing**: Test complete workflows
- **Performance testing**: Verify acceptable performance

#### 4. Deployment Phase
- **Staging environment**: Test in production-like environment
- **Gradual rollout**: Release to subset of users first
- **Monitoring**: Track metrics and errors
- **Rollback plan**: Be prepared to revert if needed

#### 5. Maintenance Phase
- **Bug fixes**: Address issues promptly
- **Security updates**: Keep dependencies current
- **Performance optimization**: Continuous improvement
- **Documentation updates**: Keep docs current

### Quality Assurance
1. **Automated testing**: Comprehensive test suite
2. **Code coverage**: Aim for high coverage
3. **Static analysis**: Use linting and type checking
4. **Security scanning**: Regular dependency audits
5. **Performance monitoring**: Track key metrics

### Collaboration Best Practices
1. **Clear communication**: Document decisions and rationale
2. **Knowledge sharing**: Regular team discussions
3. **Code ownership**: Shared responsibility for code quality
4. **Mentoring**: Help team members grow
5. **Continuous learning**: Stay updated with best practices

This microagent serves as a comprehensive guide for anyone contributing to the Monggregate project, ensuring consistent development practices and high-quality contributions.