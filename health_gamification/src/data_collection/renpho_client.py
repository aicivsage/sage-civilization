"""
Renpho API Client
Fetches weight and blood pressure data from Renpho Health API
Based on hass-renpho reverse engineering approach
"""

import httpx
import hashlib
import time
from typing import Optional, Dict, Any, List
from datetime import datetime, date


class RenphoClient:
    """Client for Renpho Health API"""

    # Renpho API endpoints (from hass-renpho research)
    BASE_URL = "https://renpho.qnclouds.com"
    LOGIN_ENDPOINT = "/api/v3/users/sign_in.json"
    DEVICE_LIST_ENDPOINT = "/api/v3/devices"
    MEASUREMENTS_ENDPOINT = "/api/v3/measurements"

    # API Constants
    APP_ID = "Renpho"
    APP_VERSION = "4.0.0"

    def __init__(self, email: str = None, password: str = None):
        """
        Initialize Renpho client

        Args:
            email: Renpho account email
            password: Renpho account password
        """
        self.email = email
        self.password = password
        self.access_token = None
        self.user_id = None
        self.client = httpx.AsyncClient(timeout=30.0)

    def _generate_request_hash(self, timestamp: int) -> str:
        """
        Generate request hash for authentication
        Based on hass-renpho implementation

        Args:
            timestamp: Unix timestamp

        Returns:
            MD5 hash string
        """
        # Hash format: md5(timestamp + app_id + app_version)
        hash_string = f"{timestamp}{self.APP_ID}{self.APP_VERSION}"
        return hashlib.md5(hash_string.encode()).hexdigest()

    async def authenticate(self) -> bool:
        """
        Authenticate with Renpho API

        Returns:
            True if authentication successful
        """
        try:
            if not self.email or not self.password:
                raise ValueError("Email and password required for authentication")

            # Generate timestamp and hash
            timestamp = int(time.time())
            request_hash = self._generate_request_hash(timestamp)

            # Login payload
            payload = {
                "secure_flag": "1",
                "email": self.email,
                "password": self.password,
                "app_id": self.APP_ID,
                "app_version": self.APP_VERSION,
                "timestamp": timestamp,
                "hash": request_hash
            }

            # Make login request
            response = await self.client.post(
                f"{self.BASE_URL}{self.LOGIN_ENDPOINT}",
                json=payload
            )

            response.raise_for_status()
            data = response.json()

            # Extract authentication tokens
            if data.get("status_code") == 50000:
                terminal_user = data.get("terminal_user", {})
                self.access_token = terminal_user.get("access_token")
                self.user_id = terminal_user.get("id")

                print(f"Authenticated successfully as user {self.user_id}")
                return True
            else:
                error_msg = data.get("status_message", "Unknown error")
                print(f"Authentication failed: {error_msg}")
                return False

        except Exception as e:
            print(f"Error during authentication: {e}")
            return False

    async def get_devices(self) -> List[Dict[str, Any]]:
        """
        Get list of Renpho devices associated with account

        Returns:
            List of device dictionaries
        """
        try:
            if not self.access_token:
                raise ValueError("Not authenticated. Call authenticate() first.")

            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            response = await self.client.get(
                f"{self.BASE_URL}{self.DEVICE_LIST_ENDPOINT}",
                headers=headers
            )

            response.raise_for_status()
            data = response.json()

            devices = data.get("devices", [])
            return devices

        except Exception as e:
            print(f"Error getting devices: {e}")
            return []

    async def get_latest_measurement(
        self,
        device_mac: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get latest weight and blood pressure measurement

        Args:
            device_mac: MAC address of specific device (optional)

        Returns:
            Dictionary with weight_kg, systolic_bp, diastolic_bp, measured_at
            or None if no measurements found
        """
        try:
            if not self.access_token:
                raise ValueError("Not authenticated. Call authenticate() first.")

            # If no device MAC provided, get first device
            if not device_mac:
                devices = await self.get_devices()
                if not devices:
                    print("No devices found")
                    return None
                device_mac = devices[0].get("mac")

            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            # Query parameters for latest measurement
            params = {
                "device_mac": device_mac,
                "user_id": self.user_id,
                "limit": 1,
                "order": "desc"
            }

            response = await self.client.get(
                f"{self.BASE_URL}{self.MEASUREMENTS_ENDPOINT}",
                headers=headers,
                params=params
            )

            response.raise_for_status()
            data = response.json()

            measurements = data.get("measurements", [])

            if not measurements:
                print("No measurements found")
                return None

            # Parse latest measurement
            latest = measurements[0]

            result = {
                "weight_kg": latest.get("weight"),
                "systolic_bp": latest.get("systolic_pressure"),
                "diastolic_bp": latest.get("diastolic_pressure"),
                "measured_at": latest.get("measured_at"),
                "device_mac": device_mac
            }

            return result

        except Exception as e:
            print(f"Error getting latest measurement: {e}")
            return None

    async def get_measurements_by_date_range(
        self,
        start_date: date,
        end_date: date,
        device_mac: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get measurements for a date range

        Args:
            start_date: Start date
            end_date: End date
            device_mac: MAC address of device (optional)

        Returns:
            List of measurement dictionaries
        """
        try:
            if not self.access_token:
                raise ValueError("Not authenticated. Call authenticate() first.")

            if not device_mac:
                devices = await self.get_devices()
                if not devices:
                    print("No devices found")
                    return []
                device_mac = devices[0].get("mac")

            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            params = {
                "device_mac": device_mac,
                "user_id": self.user_id,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "order": "asc"
            }

            response = await self.client.get(
                f"{self.BASE_URL}{self.MEASUREMENTS_ENDPOINT}",
                headers=headers,
                params=params
            )

            response.raise_for_status()
            data = response.json()

            measurements = data.get("measurements", [])

            # Parse measurements
            results = []
            for m in measurements:
                results.append({
                    "weight_kg": m.get("weight"),
                    "systolic_bp": m.get("systolic_pressure"),
                    "diastolic_bp": m.get("diastolic_pressure"),
                    "measured_at": m.get("measured_at"),
                    "device_mac": device_mac
                })

            return results

        except Exception as e:
            print(f"Error getting measurements by date range: {e}")
            return []

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
async def fetch_latest_renpho_data(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to fetch latest Renpho data

    Args:
        email: Renpho account email
        password: Renpho account password

    Returns:
        Latest measurement dictionary or None
    """
    async with RenphoClient(email, password) as client:
        if await client.authenticate():
            return await client.get_latest_measurement()
    return None
