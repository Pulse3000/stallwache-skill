# 🤝 Contributing to Stallwache

Thank you for your interest in contributing to Stallwache! This document provides guidelines and instructions for contributing.

---

## 📋 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and constructive in all interactions
- Provide helpful feedback and suggestions
- Focus on the code, not the person
- Help others learn and grow
- Report inappropriate behavior to stallwache123@gmail.com

---

## 🚀 Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub
git clone https://github.com/YOUR_USERNAME/stallwache.git
cd stallwache
```

### 2. Create a Development Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix-name
```

### 3. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Development tools
```

### 4. Make Your Changes
- Write clean, readable code
- Follow Python PEP 8 style guide
- Add comments for complex logic
- Update documentation as needed

### 5. Test Your Changes
```bash
# Run tests
python -m pytest tests/

# Code style check
flake8 .

# Auto-format
black .
```

### 6. Commit Your Changes
```bash
git add .
git commit -m "feat: describe your changes"
# or
git commit -m "fix: describe the bug fix"
```

### 7. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 8. Create a Pull Request
- Go to GitHub and create a pull request
- Describe your changes clearly
- Reference any related issues
- Link to relevant documentation

---

## 🐛 Reporting Bugs

### Before Reporting
- Check if the bug has already been reported
- Try to reproduce on latest version
- Gather system information

### How to Report
1. Go to [Issues](https://github.com/stallwache/skill/issues)
2. Click "New Issue"
3. Choose "Bug report"
4. Fill out the template with:
   - **Title**: Clear, concise description
   - **Description**: What happened and what was expected
   - **Steps to reproduce**: Exact steps to trigger the bug
   - **Environment**: Python version, Docker version, OS
   - **Logs**: Error messages and logs

### Example
```
Title: Camera connection fails with timeout error

Description:
When starting Stallwache with RTSP URL rtsp://192.168.x.x:554/stream, 
the system fails to connect with "Connection timeout" error.

Steps to reproduce:
1. Set CAMERA_RTSP_URL in .env.production
2. Run docker-compose up -d
3. Check logs: docker logs stallwache

Environment:
- Python 3.10.4
- Docker 20.10.17
- Ubuntu 22.04
- Camera: Rollei Safetycam HD 20

Error logs:
[ERROR] RTSP connection timeout after 30 seconds
```

---

## 💡 Suggesting Enhancements

### Before Suggesting
- Check if feature already exists
- Check if similar feature is being worked on
- Think about use cases and benefits

### How to Suggest
1. Go to [Issues](https://github.com/stallwache/skill/issues)
2. Click "New Issue"
3. Choose "Feature request"
4. Fill out the template with:
   - **Title**: Clear feature description
   - **Problem**: What problem does it solve
   - **Proposed solution**: How should it work
   - **Alternatives**: Other approaches considered

### Example
```
Title: Add support for multiple cameras

Problem:
Currently Stallwache supports only one camera. For larger farms 
with multiple barns, users need multiple instances.

Proposed solution:
- Add CAMERA_LIST configuration (comma-separated URLs)
- Create separate detector process per camera
- Consolidate alerts in single Telegram chat

Benefits:
- Manage multiple cattle areas from one system
- More efficient resource usage
- Single point of monitoring
```

---

## 📝 Documentation Contributions

### Types of Documentation
- **Code comments** - Inline explanations
- **Docstrings** - Function/class documentation
- **README files** - Getting started guides
- **API docs** - Function reference
- **Troubleshooting** - Common issues & solutions
- **Tutorials** - Step-by-step guides

### Documentation Guidelines

#### Code Comments
```python
# Good: Explains the 'why'
# Temporal analysis: check if detection consistent across 5 frames
# to reduce false positives from single-frame noise
if frame_consistency > threshold:
    trigger_alert()

# Bad: States the obvious
# Increment counter
counter += 1
```

#### Docstrings
```python
def detect_calf(frame: np.ndarray) -> Dict:
    """
    Detect calf in a video frame using YOLOv8.
    
    Args:
        frame: Input image as numpy array (BGR format)
        
    Returns:
        Dictionary with keys:
        - 'detected' (bool): Whether a calf was detected
        - 'confidence' (float): Detection confidence (0-1)
        - 'bbox' (tuple): Bounding box coordinates
        
    Raises:
        ValueError: If frame is not valid image format
        
    Example:
        >>> result = detect_calf(frame)
        >>> if result['detected']:
        ...     print(f"Confidence: {result['confidence']}")
    """
```

#### README Contributions
- Add to table of contents
- Keep consistent with existing style
- Use clear headers and examples
- Include command outputs when relevant

---

## 🧪 Testing Guidelines

### Writing Tests
```python
# Good test structure
import pytest
from detector import detect_calf

class TestDetector:
    def test_detect_calf_valid_frame(self):
        """Test detection with valid input."""
        frame = load_test_frame()
        result = detect_calf(frame)
        
        assert result['detected'] == True
        assert 0 <= result['confidence'] <= 1
        assert len(result['bbox']) == 4
    
    def test_detect_calf_invalid_frame(self):
        """Test detection with invalid input."""
        with pytest.raises(ValueError):
            detect_calf(None)
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_detector.py::TestDetector::test_detect_calf_valid_frame

# With coverage
pytest --cov=stallwache tests/
```

### Coverage Requirements
- Aim for >80% code coverage
- All public functions should have tests
- Test both happy path and error cases
- Include integration tests for components

---

## 📦 Code Style

### Python Style (PEP 8)

```python
# Imports: standard, third-party, local
import os
import sys
from typing import Dict, List

import cv2
import numpy as np

from stallwache.config import CONFIG

# Constants: UPPER_CASE
MAX_FRAME_QUEUE_SIZE = 100
DEFAULT_CONFIDENCE_THRESHOLD = 0.65

# Function naming: snake_case
def process_rtsp_stream(url: str) -> None:
    pass

# Class naming: PascalCase
class StreamProcessor:
    def __init__(self):
        pass

# Variable naming: snake_case
frame_buffer = []
confidence_threshold = 0.65

# Comments: explain WHY, not WHAT
# Consecutive detections improve accuracy
if consecutive_frames >= MIN_FRAMES:
    trigger_alert()
```

### Tools
```bash
# Code formatting
black . --line-length 88

# Style checking
flake8 . --max-line-length=88

# Type checking
mypy .

# All-in-one
pre-commit run --all-files
```

---

## 🔒 Security Guidelines

### Security Considerations
- Never commit credentials or secrets
- Use environment variables for sensitive data
- Validate all external inputs
- Follow OWASP guidelines
- Report security issues privately to: security@stallwache.dev

### Example
```python
# ❌ DON'T: Hardcode credentials
CAMERA_PASSWORD = "Stallwache123!"

# ✅ DO: Use environment variables
import os
CAMERA_PASSWORD = os.getenv("CAMERA_PASSWORD")
```

---

## 📚 Documentation Structure

```
docs/
├── README.md              # Main documentation
├── GETTING_STARTED.md     # Quick start guide
├── API.md                 # API reference
├── DEPLOYMENT.md          # Deployment guides
├── TROUBLESHOOTING.md     # Common issues
├── CONTRIBUTING.md        # This file
└── CHANGELOG.md           # Version history
```

---

## 🔄 Pull Request Process

### Before Submitting
- [ ] Fork the repository
- [ ] Create feature branch
- [ ] Make your changes
- [ ] Add/update tests
- [ ] Update documentation
- [ ] Run all tests: `pytest`
- [ ] Check code style: `flake8 .`
- [ ] Format code: `black .`

### PR Submission
- [ ] Clear title and description
- [ ] Link related issues
- [ ] Include screenshots/examples if relevant
- [ ] One feature per PR (avoid mixing)
- [ ] Keep commits clean and organized

### PR Template
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Related Issues
Fixes #123

## Testing
- [x] Tested locally
- [x] Added tests
- [x] All tests pass

## Documentation
- [x] Updated README
- [x] Updated docstrings
- [x] Added examples

## Checklist
- [x] Code follows style guidelines
- [x] Self-review completed
- [x] No new warnings generated
- [x] Documentation updated
```

---

## 📅 Development Workflow

```
1. Plan Phase
   - Discuss feature/bug in Issues
   - Get approval from maintainers
   - Break down into tasks

2. Development Phase
   - Create feature branch
   - Write code + tests
   - Keep commits clean
   - Update documentation

3. Review Phase
   - Submit pull request
   - Address feedback
   - Rebase if needed
   - Maintain discussion

4. Merge Phase
   - Final approval
   - Merge to main
   - Close related issues
   - Celebrate! 🎉
```

---

## 🏆 Recognition

We recognize and thank all contributors! 

Contributors are listed in:
- [CONTRIBUTORS.md](./CONTRIBUTORS.md)
- GitHub commit history
- Release notes

---

## 📞 Need Help?

### Resources
- 📖 [SKILL.md](./SKILL.md) - Technical documentation
- 💬 [GitHub Discussions](https://github.com/stallwache/skill/discussions) - Ask questions
- 🐛 [GitHub Issues](https://github.com/stallwache/skill/issues) - Report problems
- 📧 Email: stallwache123@gmail.com

### Common Questions

**Q: How do I get started with contributing?**  
A: Start with documentation updates or small bug fixes to get familiar with the process.

**Q: What if I don't know Python well?**  
A: Help with documentation! It's just as important as code.

**Q: Can I work on multiple features at once?**  
A: Please keep features separate - one PR per feature.

**Q: How long does PR review take?**  
A: Usually 2-5 days, but depends on complexity.

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Thank you for considering contributing to Stallwache! Your help makes this project better for everyone.

**Happy coding! 🐄**

---

**Version**: 1.0.0 | **Updated**: May 2026

Last updated: May 2026 | [Back to Main Repo](https://github.com/stallwache/skill)
