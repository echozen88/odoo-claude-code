# Odoo.sh Support Guide

This skill provides comprehensive guidance for developing and deploying Odoo modules on Odoo.sh, Odoo's official cloud platform.

## What is Odoo.sh?

Odoo.sh is Odoo's official PaaS (Platform as a Service) offering that provides:
- Automated builds and deployments
- Built-in database management
- CI/CD pipelines
- Multi-environment support (dev, staging, production)
- Automatic backups
- Integration with GitHub/GitLab

## Odoo.sh Configuration Files

### odoo.sh Configuration

The primary configuration file for Odoo.sh projects:

```yaml
# .odoo.sh (YAML format)
---
# Odoo version target
version: "19.0"

# Python dependencies
dependencies:
  - "python-dateutil>=2.8.0"
  - "requests>=2.31.0"
  - "psycopg2-binary>=2.9.0"

# PIP requirements file (alternative)
# pipfile: requirements.txt

# Custom build commands (optional)
# build_commands:
#   - "npm install"
#   - "npm run build"

# Environment variables (optional)
# env:
#   MY_CUSTOM_VAR: "value"
```

### Build Configuration

```yaml
# odoo.conf - Custom Odoo configuration
[options]
# Admin password for database operations
admin_passwd = ${ADMIN_PASSWORD}

# Database settings
dbfilter = ^%d$
db_host = False
db_port = False
db_user = False
db_password = False

# Workers configuration
workers = 4
max_cron_threads = 2
limit_request = 8192

# Log settings
logfile = /var/log/odoo/odoo.log
log_level = info
log_handler = :INFO

# Email settings (use SMTP server from odoo.sh)
smtp_server = localhost
smtp_port = 25

# Addons path
addons_path = /data/odoo/addons,/data/odoo/custom-addons

# i18n (load translations)
load_language = en_US,fr_FR,de_DE,es_ES

# Demo data
demo = {}

# Without demo
without_demo = all
```

### Test Configuration

```yaml
# odoo-test.conf - Configuration for test runs
[options]
test_enable = True
test_tags = post_install,-at_install
log_level = debug
test_commit = False
```

## Project Structure for Odoo.sh

### Recommended Repository Structure

```
my-odoo-repo/
├── .github/
│   └── workflows/
│       └── odoo-sh.yml      # GitHub Actions for external builds
├── .odoo.sh                # Main odoo.sh configuration
├── odoo.conf               # Custom Odoo config
├── odoo-test.conf          # Test configuration
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
├── README.md
├── addons/                 # Custom modules
│   ├── my_module_1/
│   │   ├── __manifest__.py
│   │   ├── models/
│   │   ├── views/
│   │   └── static/
│   └── my_module_2/
│       ├── __manifest__.py
│       └── ...
└── scripts/               # Build/deployment scripts
    ├── build.sh
    └── post_deploy.sh
```

### Requirements Files

```python
# requirements.txt
# Python dependencies for custom modules
python-dateutil>=2.8.0
requests>=2.31.0
pytz>=2023.3
Pillow>=10.0.0
reportlab>=4.0.0
openpyxl>=3.1.0
xlrd>=2.0.0
```

```json
{
  "name": "my-odoo-addons",
  "version": "1.0.0",
  "description": "Custom Odoo addons",
  "dependencies": {
    "owl": "^2.0.0"
  },
  "scripts": {
    "build": "webpack --mode production",
    "watch": "webpack --watch"
  },
  "devDependencies": {
    "webpack": "^5.88.0",
    "webpack-cli": "^5.1.0"
  }
}
```

## Deployment Modes

### Branch Management

Odoo.sh uses Git branches to manage deployments:

| Branch Type | Purpose | Environment | Auto-Deploy |
|-------------|---------|--------------|-------------|
| `main` | Production-ready code | Production | Yes |
| `staging/*` | Pre-production testing | Staging | Yes |
| `dev/*` | Development work | Development | Yes |
| Feature branches | Feature development | On-demand | No |
| Other branches | Testing | Not deployed | No |

### Branch Naming Conventions

```bash
# Production
main

# Staging
staging/v1.2.0
staging/release-2024-Q1

# Development
dev/feature-xyz
dev/bugfix-123
dev/refactor-abc

# Feature/Hotfix (manual deploy only)
feature/new-dashboard
hotfix/critical-bug
```

### Deploying Branches

```bash
# Create and push development branch
git checkout -b dev/new-feature
git add .
git commit -m "Add new feature"
git push origin dev/new-feature

# Create and push staging branch
git checkout -b staging/v1.2.0
git merge dev/new-feature
git push origin staging/v1.2.0

# Deploy to production (merge to main)
git checkout main
git merge staging/v1.2.0
git tag v1.2.0
git push origin main --tags
```

## Build Dependencies

### Python Dependencies

```yaml
# Method 1: In .odoo.sh
dependencies:
  - "library>=version"

# Method 2: In requirements.txt
# odoo.sh will automatically install from requirements.txt if it exists
library>=version

# Method 3: In __manifest__.py
{
    'external_dependencies': {
        'python': ['requests>=2.31.0', 'beautifulsoup4>=4.12.0'],
    },
}
```

### System Dependencies

```yaml
# odoo.sh provides most common system dependencies
# For custom system packages, create a build script:

# scripts/build.sh
#!/bin/bash
set -e

# Install system packages
sudo apt-get update
sudo apt-get install -y \
    libreoffice \
    imagemagick \
    wkhtmltopdf

# Install custom Python packages
pip install -r requirements.txt

# Build JavaScript assets
npm install
npm run build

echo "Build completed successfully"
```

### JavaScript Build Process

```json
// package.json
{
  "scripts": {
    "build": "webpack --config webpack.config.js --mode production",
    "watch": "webpack --config webpack.config.js --mode development --watch"
  }
}
```

```yaml
# .odoo.sh - Trigger build after dependency install
build_commands:
  - "npm install"
  - "npm run build"
```

## Environment-Specific Configuration

### Development Environment

```yaml
# .odoo-sh.dev (override for dev branches)
version: "19.0"

# Development doesn't need demo data
# demo = {}

# More verbose logging for debugging
# log_level = debug

# Workers: fewer for dev
# workers = 2
```

### Staging Environment

```yaml
# .odoo-sh.staging (override for staging/* branches)
version: "19.0"

# Load demo data for testing
# demo = {}

# Standard logging
# log_level = info

# Workers: medium for staging
# workers = 4
```

### Production Environment

```yaml
# .odoo-sh.prod (override for main branch)
version: "19.0"

# No demo data in production
# demo = {}
# without_demo = all

# Minimal logging for performance
# log_level = warn

# Workers: optimal for production
# workers = 8
# max_cron_threads = 4
```

## CI/CD Integration

### GitHub Actions (External Builds)

```yaml
# .github/workflows/odoo-sh.yml
name: Odoo.sh Build

on:
  push:
    branches: [main, staging/*, dev/*]
  pull_request:
    branches: [main]

jobs:
  odoo-sh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Trigger Odoo.sh Build
        env:
          ODOO_SH_TOKEN: ${{ secrets.ODOO_SH_TOKEN }}
        run: |
          curl -X POST https://your-project.odoo.sh/build \
            -H "Authorization: Bearer $ODOO_SH_TOKEN" \
            -F "branch=${GITHUB_REF#refs/heads/}"
```

### Pre-Deploy Validation

```yaml
# scripts/pre_deploy.sh
#!/bin/bash
set -e

echo "Running pre-deployment checks..."

# Check Python syntax
python -m py_compile addons/*/*.py

# Run tests (in development/staging)
if [ "${ODOO_ENVIRONMENT}" != "production" ]; then
    echo "Running tests..."
    odoo -d test_database --test-enable --test-tags=post_install
fi

# Check for TODO/FIXME comments
if git grep -n "TODO\|FIXME" addons/; then
    echo "Warning: TODO/FIXME comments found"
fi

echo "Pre-deployment checks completed"
```

## Debugging on Odoo.sh

### Access Logs

```bash
# Via Odoo.sh UI
1. Go to your project
2. Select the environment
3. Click "Logs"
4. Download or view logs in browser

# Via SSH (for advanced debugging)
# SSH into odoo.sh server (contact Odoo support)
ssh user@server.odoo.sh

# View logs
tail -f /var/log/odoo/odoo.log

# View specific error logs
grep ERROR /var/log/odoo/odoo.log | tail -50
```

### Enable Debug Mode

```python
# Enable via odoo.conf
[options]
dev_mode = pdb,qweb,werkzeug,xml

# Enable via URL parameter
https://your-instance.odoo.sh/web?debug=1

# Common debug modes:
# ?debug=1           - Enable debug tools
# ?debug=assets       - Debug assets
# ?debug=tests        - Test mode
# ?dev=pdb          - Python debugger
```

### Remote Debugging

```python
# Add breakpoints in code
def my_method(self):
    import pdb; pdb.set_trace()
    # Code stops here, can inspect variables
    return True

# Then use odoo.sh terminal to attach debugger
```

### Database Access

```bash
# Access database shell via odoo.sh UI
1. Go to project
2. Select environment
3. Click "DB Shell"
4. Write SQL queries

# Or connect via local pgAdmin (requires SSH tunnel)
ssh -L 5432:localhost:5432 user@server.odoo.sh
# Then connect to localhost:5432
```

## Backup and Restore

### Automatic Backups

```yaml
# Odoo.sh automatically creates backups:
# - Hourly: Retained for 24 hours
# - Daily: Retained for 7 days
# - Weekly: Retained for 4 weeks
# - Monthly: Retained for 12 months
```

### Manual Backup

```bash
# Via Odoo.sh UI
1. Go to project
2. Select environment
3. Click "Backups"
4. Click "Download" for desired backup

# Or create manual backup via Python
import xmlrpc.client

# Connect to odoo.sh
url = 'https://your-instance.odoo.sh/xmlrpc/2/db'
db = 'database_name'
super_admin_passwd = 'admin_password'

# Create backup
backup = xmlrpc.client.ServerProxy(url)
backup.backup(super_admin_passwd, db)
```

### Restore Backup

```bash
# Via Odoo.sh UI
1. Go to project
2. Select environment
3. Click "Backups"
4. Click "Restore" next to desired backup
5. Confirm restore (overwrites current database)
```

### Clone Database

```bash
# Clone production database to staging
1. Go to project
2. Select production environment
3. Click "Backups"
4. Click "Duplicate"
5. Select target environment (staging)
6. Confirm duplication
```

## Advanced Configuration

### Workers Configuration

```python
# Optimize workers based on CPU cores
# General formula: (2 * CPU) + 1

[options]
# For 4 CPU cores
workers = 9
max_cron_threads = 2

# For larger instances
limit_request = 8192
limit_memory_soft = 2147483648  # 2GB
limit_memory_hard = 2684354560  # 2.5GB
```

### Cache Configuration

```python
[options]
# Redis for cache (recommended for production)
cache = "redis://localhost:6379/0"

# Or memcache
# cache = "memcache://localhost:11211"

# Cache size for object cache
cache_timeout = 7200  # 2 hours
```

### Email Configuration

```python
[options]
# Use Odoo.sh built-in SMTP
smtp_server = localhost
smtp_port = 25
smtp_ssl = False
smtp_user = False
smtp_password = False

# Or configure external SMTP
# smtp_server = smtp.gmail.com
# smtp_port = 587
# smtp_ssl = False
# smtp_starttls = True
# smtp_user = your-email@gmail.com
# smtp_password = your-app-password
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|--------|----------|
| Build fails | Dependency conflict | Check requirements.txt, fix version conflicts |
| Deployment fails | Migration error | Check upgrade scripts, fix data migration |
| Module not loading | Wrong Odoo version | Check version in __manifest__.py |
| Worker timeout | Long-running query | Optimize query, increase timeout |
| Out of memory | Too many workers | Reduce workers count |
| Permission error | Wrong file permissions | Check git file permissions |

### Debug Build Failures

```bash
# Check build logs
# In odoo.sh UI: Click "Logs" during build

# Common build issues:
# 1. Python syntax error
#    - Check .py files
#    - Run: python -m py_compile addons/*/*.py

# 2. Missing dependency
#    - Check requirements.txt
#    - Check __manifest__.py

# 3. JavaScript build error
#    - Check webpack configuration
#    - Run: npm run build locally

# 4. XML syntax error
#    - Check .xml files
#    - Validate: xmllint --noout file.xml
```

### Debug Runtime Errors

```python
# Enable detailed logging
[options]
log_level = debug
log_handler = :INFO

# Log to file
logfile = /var/log/odoo/odoo.log

# Log SQL queries
log_db = True
```

## Best Practices

### 1. Branch Management

- Use `main` for production only
- Use `staging/*` for releases
- Use `dev/*` for active development
- Keep feature branches short-lived
- Delete merged branches

### 2. Deployment Strategy

- Always deploy to staging first
- Test thoroughly on staging
- Use semantic versioning
- Tag releases in git
- Document deployment changes

### 3. Configuration

- Keep production settings minimal
- Use environment-specific configs
- Monitor resource usage
- Optimize workers based on load
- Enable backups regularly

### 4. Security

- Never commit secrets
- Use environment variables
- Rotate credentials regularly
- Enable SSL
- Monitor access logs

### 5. Monitoring

- Set up error alerts
- Monitor database size
- Track response times
- Review logs regularly
- Use Odoo.sh monitoring tools

**Remember:** Odoo.sh simplifies deployment, but proper configuration and testing are still essential for successful Odoo projects.
