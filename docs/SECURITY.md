# 🔐 Security Best Practices

Comprehensive security guide for protecting your IRIS setup.

## 1. Protect API Keys

### ✗ DON'T - Commit Keys to Repository

```bash
git add .env  # WRONG!
echo "$OPENAI_API_KEY" >> config.py  # WRONG!
```

### ✓ DO - Use Environment Variables

```bash
# Set environment variable
export OPENAI_API_KEY="sk-xxxx"

# IRIS reads from environment
python main.py
```

### ✓ DO - Use .env with .gitignore

```bash
# Create .env file with secrets
echo ".env" >> .gitignore
echo "credentials/" >> .gitignore

# Source .env before running
source .env
python main.py
```

### .env.example Template

```bash
# Share this EXAMPLE file (without secrets)
OPENAI_API_KEY=sk-your-key-here
GOOGLE_API_KEY=your-key-here
ENCRYPTION_KEY=your-key-here
```

---

## 2. Encrypt Sensitive Data

### Generate Encryption Key

```bash
# Generate secure key
python scripts/generate_encryption_key.py
# Add to .env as ENCRYPTION_KEY=...
```

### Encrypt/Decrypt Data

```python
from security.encryption import encrypt_aes, decrypt_aes

# Encrypt
user_email = "john@example.com"
encrypted = encrypt_aes(user_email)
print(encrypted)  # ➜ encrypted hex string

# Decrypt (only when needed)
decrypted = decrypt_aes(encrypted)
print(decrypted)  # ➜ john@example.com
```

### Automatic Encryption

IRIS automatically encrypts:
- User profiles
- Conversation history
- Login credentials
- Personal information

---

## 3. Voice Authentication

### Train Voice Profile

```bash
# Interactive voice training
python scripts/train_voice_profile.py

# Follow prompts to record voice samples
# Takes 2-3 minutes
```

### Enable Voice Auth

```bash
# In config.yaml
security:
  voice_auth_enabled: true
  voice_auth_threshold: 0.85  # 0.0-1.0, higher = stricter

# Or in .env
VOICE_AUTH_ENABLED=true
VOICE_AUTH_THRESHOLD=0.85
```

### How It Works

1. Voice samples stored in encrypted database
2. Voice biometric model trained locally
3. On startup, IRIS asks you to say a phrase
4. Accepts command only if voice matches (≥ threshold)

---

## 4. Manage Permissions

### Set Command Permissions

```python
from security.permission_manager import PermissionManager

perms = PermissionManager()

# Restrict dangerous operations
perms.set_permission(
    action="delete_files",
    resource="/",
    allowed=False
)

# Allow safe operations
perms.set_permission(
    action="open_app",
    resource="Slack",
    allowed=True
)
```

### Permission Types

| Action | Resource | Risk | Example |
|--------|----------|------|---------|
| delete_files | / or path | HIGH | Deny `/` |
| execute_command | cmd | HIGH | Verify before run |
| read_files | path | MEDIUM | Allow ~/Documents |
| open_app | app_name | LOW | Allow Slack, Chrome |
| call_api | api_name | MEDIUM | Monitor external calls |

### Default Permissions

```yaml
# Allowed by default
- open_app: [All apps]
- read_files: [~/Documents, ~/Downloads]
- system_info: [All]
- create_reminder: [All]

# Restricted by default
- delete_files: [None]
- modify_system: [None]
- access_credentials: [None]
```

---

## 5. Implement Audit Logging

### Enable Audit Logs

```bash
# In config.yaml or .env
ENABLE_AUDIT_LOGGING=true
```

### View Audit Logs

```python
from security.audit_logger import AuditLogger

audit = AuditLogger()

# Get recent events
events = audit.get_recent_events(limit=100)

for event in events:
    print(f"{event['timestamp']}: {event['action']} on {event['resource']}")
```

### Audit Log Structure

```python
{
    "timestamp": "2026-04-05T10:30:00Z",
    "user": "user@example.com",
    "action": "file_deletion",
    "resource": "/path/to/file",
    "status": "success",
    "ip_address": "192.168.1.100",
    "details": "Deleted report.pdf (2.3 MB)"
}
```

### Export Audit Logs

```bash
# Export to CSV
python scripts/export_audit_logs.py --format csv --output audit_logs.csv

# Export to JSON
python scripts/export_audit_logs.py --format json --output audit_logs.json
```

---

## 6. Regular Backups

### Automated Backups

```bash
# In config.yaml
storage:
  backup:
    enabled: true
    frequency: "daily"
    retention_days: 30
```

### Manual Backup

```bash
python scripts/backup_data.py

# Creates: backups/backup_2026-04-05_143000.tar.gz
```

### Verify Backup

```bash
# List backup contents
tar -tzf backups/backup_2026-04-05.tar.gz

# Test restore
mkdir /tmp/test_restore
tar -xzf backups/backup_2026-04-05.tar.gz -C /tmp/test_restore
ls /tmp/test_restore/
```

### Restore from Backup

```bash
# Stop IRIS
pkill -f "python main.py"

# Restore
tar -xzf backups/backup_2026-04-05.tar.gz -C ./

# Restart
python main.py
```

---

## 7. Secure Credential Storage

### macOS Keychain (Recommended)

```python
from security.secure_storage import KeychainStorage

keychain = KeychainStorage()

# Store credentials securely
keychain.store("gmail_password", "my_secure_password")

# Retrieve when needed
password = keychain.retrieve("gmail_password")

# Delete when done
keychain.delete("gmail_password")
```

### Linux: GNOME Keyring

```python
from security.secure_storage import GnomeKeyringStorage

keyring = GnomeKeyringStorage()
keyring.store("slack_token", "xoxb-xxxx")
token = keyring.retrieve("slack_token")
```

### Encrypted File Storage

```python
from security.secure_storage import EncryptedStorage

storage = EncryptedStorage(encryption_key="your-key")
storage.store("api_key", "sk-xxxx")
api_key = storage.retrieve("api_key")
```

---

## 8. Secure Communication

### HTTPS/TLS

```bash
# When using cloud providers, ensure HTTPS
OPENAI_API_URL=https://api.openai.com  # ✓ HTTPS

# Never use HTTP for sensitive data
OPENAI_API_URL=http://api.openai.com   # ✗ Insecure
```

### VPN (Optional)

```bash
# For enhanced privacy, use VPN
# IRIS connections will be tunneled through VPN
```

---

## 9. Network Security

### Firewall

```bash
# Restrict Ollama to localhost only
# In ollama serve output: Listen on 127.0.0.1:11434

# Never expose Ollama to network
# ✗ OLLAMA_HOST=0.0.0.0:11434  (Dangerous!)
# ✓ OLLAMA_HOST=127.0.0.1:11434  (Safe)
```

### Local-Only Mode

```yaml
# Recommended configuration
llm:
  provider: "ollama"
  ollama:
    host: "127.0.0.1"  # Localhost only
    port: 11434

# No internet communication needed
```

---

## 10. Data Privacy

### What Data Is Collected

**Collected (when enabled)**:
- Voice commands (transcribed text)
- Conversation history
- User preferences
- Interaction patterns

**NOT Collected**:
- Personal financial information
- Passwords (stored encrypted only)
- Browsing history (unless explicitly enabled)
- Email content (summaries only)

### Data Deletion

```python
from brain.memory_manager import MemoryManager

memory = MemoryManager()

# Delete specific data
memory.delete("user_preference")

# Clear conversation history
memory.clear_conversation_history()

# Clear all personal data
memory.clear_all()
```

### GDPR Compliance

```bash
# Export personal data (GDPR data portability)
python scripts/export_user_data.py --output user_data.json

# Delete all personal data (GDPR right to be forgotten)
python scripts/delete_user_data.py --confirm
```

---

## Security Checklist

- [ ] API keys stored in .env (not in code)
- [ ] .env added to .gitignore
- [ ] Encryption key generated and stored securely
- [ ] Voice authentication enabled
- [ ] Permissions configured appropriately
- [ ] Audit logging enabled
- [ ] Backups configured and tested
- [ ] Firewalls restricting Ollama to localhost
- [ ] HTTPS used for cloud providers
- [ ] Regular security updates applied

---

## Reporting Security Issues

Found a security vulnerability? **Please don't open a public issue.**

Instead:
1. Email security@iris-assistant.dev
2. Include detailed description
3. Include steps to reproduce
4. Allow 48 hours for response

---

See [Configuration](CONFIGURATION.md) for security settings and [Troubleshooting](TROUBLESHOOTING.md) for security issues.
