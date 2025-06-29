# Contributing to FinHealth Bot

Thank you for your interest in contributing to the FinHealth Bot project! We welcome contributions from the community to help us improve and grow. Please follow these guidelines to contribute effectively.

## How Can I Contribute?

### Reporting Bugs

If you encounter a bug in the project, please report it by opening an issue with the following details:
- **Title**: A concise title for the bug.
- **Description**: A clear description of the issue.
- **Steps to Reproduce**: Detailed steps to reproduce the bug.
- **Expected Behavior**: What you expected to happen.
- **Actual Behavior**: What actually happened.
- **Additional Context**: Include any error messages or screenshots.

### Suggesting Features

We are always looking to improve our project. If you have a feature suggestion, please open an issue describing the feature with:
- **Title**: A concise title for the feature.
- **Description**: A clear and detailed description of the feature.
- **Context**: Why you think this feature would be beneficial.
- **Implementation Ideas**: If applicable, ideas for how the feature could be implemented.

### Code Contributions

#### Code Style
- **Follow PEP 8** for Python code.
- Ensure all your code has clear and concise docstrings.

#### Setup Development Environment
1. **Fork the repository** on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/hospital-price-chatbot.git
   cd hospital-price-chatbot
   ```
3. **Set up a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # macOS/Linux
   .\env\Scripts\activate  # Windows
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Create a new branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Making Changes
- Make small, manageable commits with clear, descriptive commit messages.
- Ensure your changes do not break any existing functionality.
- Follow relevant documentation practices.

#### Running Tests
- Please ensure all tests pass before submitting a pull request:
  ```bash
  pytest tests/
  ```

#### Pull Request Process
1. Ensure that your changes are up to date with the main branch.
   ```bash
   git fetch upstream
   git merge upstream/main
   ```
2. Submit a pull request with a clear description of the changes.
3. Reference any related issues in your pull request.
4. A project maintainer will review your submission and may ask follow-up questions.

### Code of Conduct

Please note that FinHealth Bot has adopted a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure an inclusive and respectful community. By participating in this project, you agree to abide by its terms.

---

Thank you for your contributions! Your efforts help make FinHealth Bot better for everyone! If you have any questions, feel free to reach out to the repository maintainers.
