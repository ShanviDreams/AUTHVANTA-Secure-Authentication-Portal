from pathlib import Path

content = """# AUTHVANTA — System Diagrams

## 1. System Architecture

```mermaid
flowchart TB
U[User] --> UI[Frontend]
A[Admin] --> UI
UI --> F[Flask Backend]
F --> AUTH[Authentication]
F --> MFA[MFA]
F --> MAIL[Gmail SMTP]
F --> SEC[Security Module]
AUTH --> DB[(MySQL)]
MFA --> DB
SEC --> DB