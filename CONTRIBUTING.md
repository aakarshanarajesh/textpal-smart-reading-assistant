# Contributing to TextPal

Thank you for your interest in contributing to TextPal! Here are guidelines to help you get started.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/your-username/smart_textpal.git
   cd smart_textpal
   ```

3. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Setting Up Your Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Run the application
python app.py
```

### Code Style

We follow PEP 8 style guidelines. Before submitting:

```bash
# Format your code
black .

# Check for style issues
flake8 .

# Run linter
pylint utils/ app.py
```

### Testing

Run tests before submitting:
```bash
pytest
pytest --cov=utils  # With coverage
```

## Making Changes

1. **Keep changes focused**: One feature per branch
2. **Write clear commit messages**:
   ```
   feat: Add new feature description
   fix: Fix bug description
   docs: Update documentation
   style: Code style improvements
   refactor: Refactor existing code
   test: Add tests
   ```

3. **Update documentation** if needed
4. **Add tests** for new features

## Submitting Changes

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots if UI changes

3. **Address review comments** promptly

## Feature Ideas

Some areas where contributions are welcome:

- [ ] Additional language support for translation
- [ ] More input file formats (DOCX, PPT)
- [ ] Advanced reading statistics
- [ ] Mobile application
- [ ] Improved UI/UX
- [ ] Performance optimizations
- [ ] Additional accessibility features
- [ ] API documentation
- [ ] Unit tests expansion

## Reporting Bugs

When reporting bugs, include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, browser)
- Error logs/screenshots

## Questions?

Feel free to:
- Create an GitHub issue for discussion
- Email the project maintainers
- Join our community discussions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing! 🚀**
