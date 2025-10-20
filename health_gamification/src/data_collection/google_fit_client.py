"""
Google Fit API Client
Fetches step count data from Google Fit using Fitness API
Uses OAuth2 authentication
"""

import httpx
import json
from typing import Optional, Dict, Any
from datetime import datetime, date, timedelta
from pathlib import Path


class GoogleFitClient:
    """Client for Google Fit Fitness API"""

    # Google Fit API endpoints
    FITNESS_API_BASE = "https://www.googleapis.com/fitness/v1/users/me"
    DATASOURCES_ENDPOINT = f"{FITNESS_API_BASE}/dataSources"
    DATASETS_ENDPOINT = f"{FITNESS_API_BASE}/dataSources/{{dataSourceId}}/datasets/{{startTime}}-{{endTime}}"

    # Data source for step count (aggregated)
    STEP_COUNT_DELTA = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"

    # OAuth2 endpoints
    OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"

    # Scopes required
    SCOPES = [
        "https://www.googleapis.com/auth/fitness.activity.read",
        "https://www.googleapis.com/auth/fitness.location.read"
    ]

    def __init__(self, client_id: str = None, client_secret: str = None, credentials_path: str = None):
        """
        Initialize Google Fit client

        Args:
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            credentials_path: Path to stored OAuth2 credentials (access/refresh tokens)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.credentials_path = credentials_path
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
        self.client = httpx.AsyncClient(timeout=30.0)

    def get_oauth_url(self, redirect_uri: str = "http://localhost:8080") -> str:
        """
        Generate OAuth2 authorization URL

        Args:
            redirect_uri: OAuth2 redirect URI (must match Google Cloud Console config)

        Returns:
            Authorization URL to visit in browser
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.SCOPES),
            "access_type": "offline",  # Request refresh token
            "prompt": "consent"
        }

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.OAUTH_AUTH_URL}?{query_string}"

    async def exchange_code_for_tokens(
        self,
        authorization_code: str,
        redirect_uri: str = "http://localhost:8080"
    ) -> bool:
        """
        Exchange authorization code for access and refresh tokens

        Args:
            authorization_code: Code from OAuth redirect
            redirect_uri: Must match the one used in authorization

        Returns:
            True if successful
        """
        try:
            payload = {
                "code": authorization_code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code"
            }

            response = await self.client.post(self.OAUTH_TOKEN_URL, data=payload)
            response.raise_for_status()

            data = response.json()

            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")

            # Calculate expiry time
            expires_in = data.get("expires_in", 3600)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)

            # Save credentials if path provided
            if self.credentials_path:
                self._save_credentials()

            return True

        except Exception as e:
            print(f"Error exchanging authorization code: {e}")
            return False

    async def refresh_access_token(self) -> bool:
        """
        Refresh access token using refresh token

        Returns:
            True if successful
        """
        try:
            if not self.refresh_token:
                raise ValueError("No refresh token available")

            payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token"
            }

            response = await self.client.post(self.OAUTH_TOKEN_URL, data=payload)
            response.raise_for_status()

            data = response.json()

            self.access_token = data.get("access_token")

            # Calculate new expiry
            expires_in = data.get("expires_in", 3600)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)

            # Save updated credentials
            if self.credentials_path:
                self._save_credentials()

            return True

        except Exception as e:
            print(f"Error refreshing access token: {e}")
            return False

    def _save_credentials(self):
        """Save OAuth2 credentials to file"""
        credentials = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_expiry": self.token_expiry.isoformat() if self.token_expiry else None,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        Path(self.credentials_path).parent.mkdir(parents=True, exist_ok=True)

        with open(self.credentials_path, 'w') as f:
            json.dump(credentials, f, indent=2)

    def _load_credentials(self) -> bool:
        """Load OAuth2 credentials from file"""
        try:
            if not self.credentials_path or not Path(self.credentials_path).exists():
                return False

            with open(self.credentials_path, 'r') as f:
                credentials = json.load(f)

            self.access_token = credentials.get("access_token")
            self.refresh_token = credentials.get("refresh_token")
            self.client_id = credentials.get("client_id")
            self.client_secret = credentials.get("client_secret")

            expiry_str = credentials.get("token_expiry")
            if expiry_str:
                self.token_expiry = datetime.fromisoformat(expiry_str)

            return True

        except Exception as e:
            print(f"Error loading credentials: {e}")
            return False

    async def authenticate(self) -> bool:
        """
        Authenticate with Google Fit API
        Loads existing credentials or prompts for OAuth flow

        Returns:
            True if authenticated
        """
        # Try loading existing credentials
        if self._load_credentials():
            # Check if token expired
            if self.token_expiry and datetime.now() >= self.token_expiry:
                print("Access token expired, refreshing...")
                return await self.refresh_access_token()
            return True

        print("No valid credentials found. OAuth flow required.")
        print(f"Visit this URL to authorize: {self.get_oauth_url()}")
        print("After authorization, use exchange_code_for_tokens() with the code.")
        return False

    async def get_daily_steps(self, target_date: date) -> Optional[int]:
        """
        Get total steps for a specific day

        Args:
            target_date: Date to query

        Returns:
            Total step count or None
        """
        try:
            if not self.access_token:
                raise ValueError("Not authenticated. Call authenticate() first.")

            # Convert date to nanoseconds (Google Fit uses nanoseconds)
            start_time = int(datetime.combine(target_date, datetime.min.time()).timestamp() * 1e9)
            end_time = int(datetime.combine(target_date, datetime.max.time()).timestamp() * 1e9)

            # Build endpoint URL
            url = self.DATASETS_ENDPOINT.format(
                dataSourceId=self.STEP_COUNT_DELTA,
                startTime=start_time,
                endTime=end_time
            )

            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            response = await self.client.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            # Sum all step count values
            total_steps = 0
            for point in data.get("point", []):
                for value in point.get("value", []):
                    if value.get("intVal"):
                        total_steps += value["intVal"]

            return total_steps

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                # Token expired, try to refresh
                print("Access token expired, attempting refresh...")
                if await self.refresh_access_token():
                    # Retry the request
                    return await self.get_daily_steps(target_date)
            print(f"HTTP error getting daily steps: {e}")
            return None

        except Exception as e:
            print(f"Error getting daily steps: {e}")
            return None

    async def get_steps_range(
        self,
        start_date: date,
        end_date: date
    ) -> Dict[str, int]:
        """
        Get steps for a date range

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            Dictionary mapping date strings to step counts
        """
        results = {}

        current_date = start_date
        while current_date <= end_date:
            steps = await self.get_daily_steps(current_date)
            if steps is not None:
                results[current_date.isoformat()] = steps

            current_date += timedelta(days=1)

        return results

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    async def __aenter__(self):
        """Context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close()


# Convenience function
async def fetch_google_fit_steps(target_date: date, credentials_path: str) -> Optional[int]:
    """
    Convenience function to fetch steps from Google Fit

    Args:
        target_date: Date to query
        credentials_path: Path to OAuth2 credentials file

    Returns:
        Step count or None
    """
    async with GoogleFitClient(credentials_path=credentials_path) as client:
        if await client.authenticate():
            return await client.get_daily_steps(target_date)
    return None
