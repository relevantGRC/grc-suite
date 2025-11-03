# Contributing to AWS Automated Access Review

Thank you for your interest in contributing to AWS Automated Access Review! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check the [GitHub Issues](https://github.com/ajy0127/aws_automated_access_review/issues) to see if the issue has already been reported.
2. If not, create a new issue with a descriptive title and detailed description.
3. Include steps to reproduce the issue, expected behavior, and actual behavior.
4. Add relevant screenshots or logs if applicable.

### Submitting Changes

1. Fork the repository.
2. Create a new branch from `main` for your changes:
   ```
   git checkout -b feature/your-feature-name
   ```
3. Make your changes, following the coding conventions below.
4. Add tests for your changes.
5. Ensure all tests pass:
   ```
   ./scripts/run_tests.sh
   ```
6. Commit your changes with a clear commit message:
   ```
   git commit -m "Add feature: your feature description"
   ```
7. Push your branch to your fork:
   ```
   git push origin feature/your-feature-name
   ```
8. Create a pull request to the `main` branch of the original repository.

## Coding Conventions

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
- Use 4 spaces for indentation (not tabs).
- Use snake_case for function and variable names.
- Use CamelCase for class names.
- Maximum line length is 88 characters (we use Black formatter).
- Add docstrings for all functions, classes, and modules.

### Shell Scripts

- Include a shebang line: `#!/bin/bash`
- Use 2 spaces for indentation.
- Include helpful comments.
- Add error handling with appropriate exit codes.

### Testing

- Write unit tests for all new functionality.
- Ensure tests are deterministic and don't rely on external services.
- Mock AWS services using appropriate testing tools.

## Pull Request Process

1. Update the README.md with details of changes to the interface, if applicable.
2. Update the documentation in the `docs/` directory if needed.
3. The version number in VERSION file will be updated according to [Semantic Versioning](https://semver.org/).
4. Your pull request will be reviewed by at least one maintainer.
5. Once approved, your pull request will be merged.

## Development Setup

See the [README.md](README.md) for instructions on setting up your development environment.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE).

Thank you for contributing to AWS Automated Access Review! 
