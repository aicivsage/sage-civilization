# Health Gamification System

**Version:** 1.0 (Phase 1 Complete)
**Status:** Foundation Ready for Credential Setup

## Overview

Health gamification system that tracks weight, blood pressure, and step count from Renpho and Google Fit APIs, calculates daily health scores, and builds a simulated investment portfolio based on health performance.

## Current Status: Phase 1 Complete

Phase 1 provides the foundational infrastructure:
- SQLite database with full schema
- Encrypted credential storage
- Renpho API client (ready for authentication)
- Google Fit API client (ready for OAuth setup)
- Database initialization and testing scripts

## Directory Structure

```
health_gamification/
├── data/                    # SQLite database storage
├── credentials/             # Encrypted API credentials
├── backups/                 # Database backups
├── src/
│   ├── data_collection/     # API clients (Renpho, Google Fit)
│   ├── scoring/             # Health scoring engine (Phase 2)
│   ├── database/            # Database manager and schema
│   ├── telegram/            # Telegram notifications (Phase 3)
│   ├── security/            # Credentials encryption
│   └── portfolio/           # Portfolio simulation (Phase 2)
├── scripts/                 # Utility scripts
├── tests/                   # Test suite
└── requirements.txt         # Python dependencies
```

## Quick Start

### 1. Install Dependencies

```bash
cd health_gamification
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python scripts/initialize_database.py
```

This creates `data/health.db` with all tables and default configuration.

### 3. Run Tests

```bash
python tests/test_phase1.py
```

Verifies all Phase 1 components are working correctly.

## Database Schema

### Tables

1. **health_metrics** - Daily measurements (weight, BP, steps)
2. **health_scores** - Daily scores and running balance
3. **achievements** - Milestones and badges
4. **audit_log** - Complete audit trail
5. **system_config** - Configuration and thresholds

### Default Configuration

- Target weight: 105 kg
- Baseline weight: 115 kg
- Target BP: 120/80
- Daily steps goal: 10,000
- Portfolio investment: $1 per health point

## API Integration (Next Step)

### Renpho Setup

1. Store credentials:
```python
from src.security import store_credentials

store_credentials("renpho", {
    "email": "your_email@example.com",
    "password": "your_password"
})
```

2. Test connection:
```python
from src.data_collection import RenphoClient

async with RenphoClient() as client:
    # Load credentials from storage
    creds = retrieve_credentials("renpho")
    client.email = creds["email"]
    client.password = creds["password"]

    # Authenticate
    if await client.authenticate():
        data = await client.get_latest_measurement()
        print(data)
```

### Google Fit Setup

1. Create OAuth2 credentials in Google Cloud Console
2. Enable Fitness API
3. Store client credentials:
```python
store_credentials("google_fit", {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret"
})
```

4. Complete OAuth flow (see `src/data_collection/google_fit_client.py`)

## Security

- All credentials encrypted using Fernet (AES-128)
- Encryption key stored in `credentials/.encryption_key` (600 permissions)
- Credential files stored with 600 permissions (owner-only access)
- Full audit log of all database operations

## Phase 2 (Not Yet Implemented)

- Health scoring engine
- Portfolio simulation
- Automated data collection
- Daily scoring automation

## Phase 3 (Not Yet Implemented)

- Telegram notifications
- Daily score reports
- Achievement alerts
- Portfolio performance summaries

## Testing

Phase 1 tests verify:
- ✓ Database operations (insert, query, update)
- ✓ Credential encryption/decryption
- ✓ API client stubs (hash generation, OAuth URL)
- ✓ Configuration management
- ✓ Audit logging

## Files Created

**Database:**
- `src/database/schema.sql` - Complete database schema
- `src/database/health_db.py` - Async database manager
- `src/database/__init__.py` - Module exports

**Security:**
- `src/security/credentials_manager.py` - Credential encryption
- `src/security/__init__.py` - Module exports

**Data Collection:**
- `src/data_collection/renpho_client.py` - Renpho API client
- `src/data_collection/google_fit_client.py` - Google Fit API client
- `src/data_collection/__init__.py` - Module exports

**Scripts:**
- `scripts/initialize_database.py` - Database setup
- `tests/test_phase1.py` - Phase 1 test suite

**Configuration:**
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Next Steps

1. **Obtain Credentials:**
   - Renpho account email/password
   - Google Cloud OAuth2 client ID/secret

2. **Test API Connections:**
   - Authenticate with Renpho
   - Complete Google Fit OAuth flow
   - Verify data retrieval

3. **Build Phase 2:**
   - Scoring engine implementation
   - Portfolio simulation logic
   - Automated data collection

4. **Build Phase 3:**
   - Telegram integration
   - Notification system
   - Daily automation

## Dependencies

- `aiosqlite` - Async SQLite database
- `cryptography` - Credential encryption
- `httpx` - Async HTTP client
- `python-dateutil` - Date utilities
- `pytest` - Testing framework (optional)

## License

Internal A-C-Gee civilization project.
