# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- Initial release of Budgt.sh
- Modern Terminal User Interface for expense tracking
- Account management (Cash, Bank Account, Credit Card, Savings)
- Transaction tracking (Income, Expenses, Transfers)
- Category management with visual indicators
- Financial insights with weekly summaries and trends
- Multiple theme support
- Local SQLite database storage
- Comprehensive input validation
- Security features and data protection
- UV and Homebrew installation support

### Features
- **Account Management**: Create and manage multiple accounts
- **Transaction Tracking**: Record income, expenses, and transfers
- **Category System**: Organized expense categories with colors
- **Insights Dashboard**: Weekly spending analysis and trends
- **Theme Support**: Multiple color schemes
- **Keyboard Shortcuts**: Efficient navigation and actions
- **Data Security**: Local storage with user privacy protection

### Security
- SQL injection protection via SQLAlchemy ORM
- Input validation and sanitization
- Safe YAML configuration loading
- No network communication - purely local application
- Comprehensive error handling without information disclosure

### Installation Methods
- UV package manager support
- Homebrew formula
- pipx isolated installation
- Standard pip installation
- Source installation

### Technical Details
- Python 3.8+ support
- Built with Textual framework
- SQLAlchemy ORM for database operations
- Rich terminal formatting
- Plotext for data visualization
- YAML configuration management
