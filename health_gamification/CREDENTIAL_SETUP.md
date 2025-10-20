# Credential Setup Guide

This guide walks through setting up API credentials for Renpho and Google Fit.

## Prerequisites

- Renpho account (email/password)
- Google Cloud project with Fitness API enabled
- Python virtual environment activated

## Step 1: Activate Virtual Environment

```bash
cd health_gamification
source venv/bin/activate
```

## Step 2: Store Renpho Credentials

Create a Python script to store your Renpho credentials securely:

```python
#!/usr/bin/env python3
"""Store Renpho credentials"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from security import store_credentials

# Replace with your actual Renpho credentials
renpho_creds = {
    "email": "your_email@example.com",
    "password": "your_password"
}

if store_credentials("renpho", renpho_creds):
    print("✓ Renpho credentials stored successfully")
    print("Credentials encrypted in: credentials/renpho.enc")
else:
    print("✗ Failed to store credentials")
```

Save as `scripts/store_renpho_creds.py` and run:

```bash
python scripts/store_renpho_creds.py
```

## Step 3: Test Renpho Connection

```python
#!/usr/bin/env python3
"""Test Renpho API connection"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from security import retrieve_credentials
from data_collection import RenphoClient

async def test_renpho():
    # Load credentials
    creds = retrieve_credentials("renpho")
    if not creds:
        print("✗ No credentials found")
        return

    # Create client
    async with RenphoClient(creds["email"], creds["password"]) as client:
        # Authenticate
        print("Authenticating with Renpho...")
        if await client.authenticate():
            print("✓ Authentication successful!")

            # Get latest measurement
            print("\nFetching latest measurement...")
            data = await client.get_latest_measurement()

            if data:
                print(f"✓ Latest measurement:")
                print(f"  Weight: {data['weight_kg']} kg")
                print(f"  Blood Pressure: {data['systolic_bp']}/{data['diastolic_bp']}")
                print(f"  Measured at: {data['measured_at']}")
            else:
                print("✗ No measurements found")
        else:
            print("✗ Authentication failed")

if __name__ == "__main__":
    asyncio.run(test_renpho())
```

Save as `scripts/test_renpho.py` and run:

```bash
python scripts/test_renpho.py
```

## Step 4: Google Cloud Setup

### 4.1 Create OAuth2 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable **Fitness API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Fitness API"
   - Click "Enable"

4. Create OAuth2 credentials:
   - Navigate to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Health Gamification"
   - Click "Create"
   - Download JSON file (contains client_id and client_secret)

### 4.2 Store Google Fit Credentials

```python
#!/usr/bin/env python3
"""Store Google Fit OAuth2 credentials"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from security import store_credentials

# Replace with values from downloaded JSON
google_fit_creds = {
    "client_id": "your_client_id.apps.googleusercontent.com",
    "client_secret": "your_client_secret"
}

if store_credentials("google_fit", google_fit_creds):
    print("✓ Google Fit credentials stored successfully")
    print("Credentials encrypted in: credentials/google_fit.enc")
else:
    print("✗ Failed to store credentials")
```

Save as `scripts/store_google_fit_creds.py` and run:

```bash
python scripts/store_google_fit_creds.py
```

### 4.3 Complete OAuth Flow

```python
#!/usr/bin/env python3
"""Complete Google Fit OAuth2 flow"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from security import retrieve_credentials
from data_collection import GoogleFitClient

async def oauth_flow():
    # Load credentials
    creds = retrieve_credentials("google_fit")
    if not creds:
        print("✗ No credentials found")
        return

    # Create client
    oauth_creds_path = Path(__file__).parent.parent / "credentials" / "google_fit_oauth.json"
    client = GoogleFitClient(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        credentials_path=str(oauth_creds_path)
    )

    # Get OAuth URL
    print("=" * 60)
    print("Google Fit OAuth2 Authorization")
    print("=" * 60)
    print("\n1. Visit this URL in your browser:")
    print(f"\n{client.get_oauth_url()}\n")
    print("2. Authorize the application")
    print("3. Copy the authorization code from the redirect URL")
    print("   (It will be in the URL parameter 'code=')")
    print("\n" + "=" * 60)

    # Get code from user
    auth_code = input("\nEnter authorization code: ").strip()

    # Exchange for tokens
    print("\nExchanging code for tokens...")
    if await client.exchange_code_for_tokens(auth_code):
        print("✓ OAuth2 tokens obtained successfully!")
        print(f"✓ Tokens saved to: {oauth_creds_path}")
    else:
        print("✗ Failed to exchange authorization code")

    await client.close()

if __name__ == "__main__":
    asyncio.run(oauth_flow())
```

Save as `scripts/google_fit_oauth.py` and run:

```bash
python scripts/google_fit_oauth.py
```

### 4.4 Test Google Fit Connection

```python
#!/usr/bin/env python3
"""Test Google Fit API connection"""

import asyncio
import sys
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_collection import GoogleFitClient

async def test_google_fit():
    oauth_creds_path = Path(__file__).parent.parent / "credentials" / "google_fit_oauth.json"

    async with GoogleFitClient(credentials_path=str(oauth_creds_path)) as client:
        # Authenticate
        print("Authenticating with Google Fit...")
        if await client.authenticate():
            print("✓ Authentication successful!")

            # Get today's steps
            today = date.today()
            print(f"\nFetching steps for {today}...")
            steps = await client.get_daily_steps(today)

            if steps is not None:
                print(f"✓ Steps today: {steps:,}")
            else:
                print("✗ No step data found")
        else:
            print("✗ Authentication failed")
            print("Run scripts/google_fit_oauth.py first to authorize")

if __name__ == "__main__":
    asyncio.run(test_google_fit())
```

Save as `scripts/test_google_fit.py` and run:

```bash
python scripts/test_google_fit.py
```

## Security Notes

- All credentials are encrypted using Fernet (AES-128)
- Encryption key stored in `credentials/.encryption_key` with 600 permissions
- Credential files stored in `credentials/*.enc` with 600 permissions
- **NEVER commit credentials/ directory to git** (.gitignore configured)
- Keep encryption key backed up securely (lose it = lose all credentials)

## Troubleshooting

### Renpho Issues

**Authentication fails:**
- Verify email/password are correct
- Check if Renpho changed API endpoints (see `src/data_collection/renpho_client.py`)
- Try logging into Renpho app to ensure account is active

**No measurements found:**
- Ensure you have synced scale recently
- Check device MAC address is correct
- Verify measurements exist in Renpho app

### Google Fit Issues

**OAuth flow fails:**
- Ensure redirect URI is exactly `http://localhost:8080`
- Check Fitness API is enabled in Google Cloud Console
- Verify OAuth consent screen is configured

**No step data:**
- Ensure Google Fit app has step data
- Check date range is correct
- Verify Fitness API permissions granted

**Token expired:**
- Client automatically refreshes tokens
- If refresh fails, re-run OAuth flow

## Next Steps

Once credentials are working:
1. Test full data collection cycle
2. Populate initial health metrics manually
3. Build Phase 2 scoring engine
4. Set up automated daily data collection

## File Locations

- Encrypted credentials: `credentials/*.enc`
- Encryption key: `credentials/.encryption_key`
- OAuth tokens: `credentials/google_fit_oauth.json`
- Database: `data/health.db`

All credential files are git-ignored for security.
