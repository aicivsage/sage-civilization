"""
Credentials Manager
Handles encryption and decryption of API credentials
Uses Fernet symmetric encryption (AES-128)
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet


class CredentialsManager:
    """Manages encrypted storage of API credentials"""

    def __init__(self, credentials_dir: str = None, key_file: str = None):
        """
        Initialize credentials manager

        Args:
            credentials_dir: Directory to store encrypted credentials
            key_file: Path to encryption key file
        """
        if credentials_dir is None:
            base_dir = Path(__file__).parent.parent.parent
            credentials_dir = base_dir / "credentials"

        if key_file is None:
            key_file = Path(credentials_dir) / ".encryption_key"

        self.credentials_dir = Path(credentials_dir)
        self.key_file = Path(key_file)
        self.cipher = None

        # Ensure credentials directory exists
        self.credentials_dir.mkdir(parents=True, exist_ok=True)

        # Load or generate encryption key
        self._initialize_key()

    def _initialize_key(self):
        """Load existing key or generate new one"""
        if self.key_file.exists():
            # Load existing key
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()

            # Save key with restricted permissions
            with open(self.key_file, 'wb') as f:
                f.write(key)

            # Set file permissions to owner read/write only (0o600)
            os.chmod(self.key_file, 0o600)

        self.cipher = Fernet(key)

    def encrypt_credentials(self, credentials: Dict[str, Any]) -> bytes:
        """
        Encrypt credentials dictionary

        Args:
            credentials: Dictionary of credential data

        Returns:
            Encrypted bytes
        """
        # Convert to JSON string
        credentials_json = json.dumps(credentials, indent=2)

        # Encrypt
        encrypted = self.cipher.encrypt(credentials_json.encode('utf-8'))

        return encrypted

    def decrypt_credentials(self, encrypted_data: bytes) -> Dict[str, Any]:
        """
        Decrypt credentials

        Args:
            encrypted_data: Encrypted bytes

        Returns:
            Decrypted credentials dictionary
        """
        # Decrypt
        decrypted = self.cipher.decrypt(encrypted_data)

        # Parse JSON
        credentials = json.loads(decrypted.decode('utf-8'))

        return credentials

    def save_credentials(self, service_name: str, credentials: Dict[str, Any]) -> bool:
        """
        Encrypt and save credentials to file

        Args:
            service_name: Name of service (e.g., 'renpho', 'google_fit')
            credentials: Credentials dictionary

        Returns:
            True if successful
        """
        try:
            # Encrypt credentials
            encrypted = self.encrypt_credentials(credentials)

            # Write to file
            cred_file = self.credentials_dir / f"{service_name}.enc"
            with open(cred_file, 'wb') as f:
                f.write(encrypted)

            # Set restrictive permissions
            os.chmod(cred_file, 0o600)

            return True

        except Exception as e:
            print(f"Error saving credentials for {service_name}: {e}")
            return False

    def load_credentials(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Load and decrypt credentials from file

        Args:
            service_name: Name of service (e.g., 'renpho', 'google_fit')

        Returns:
            Decrypted credentials dictionary or None if not found
        """
        try:
            cred_file = self.credentials_dir / f"{service_name}.enc"

            if not cred_file.exists():
                print(f"Credentials file not found: {cred_file}")
                return None

            # Read encrypted file
            with open(cred_file, 'rb') as f:
                encrypted = f.read()

            # Decrypt and return
            credentials = self.decrypt_credentials(encrypted)

            return credentials

        except Exception as e:
            print(f"Error loading credentials for {service_name}: {e}")
            return None

    def delete_credentials(self, service_name: str) -> bool:
        """
        Delete credentials file for a service

        Args:
            service_name: Name of service

        Returns:
            True if deleted successfully
        """
        try:
            cred_file = self.credentials_dir / f"{service_name}.enc"

            if cred_file.exists():
                cred_file.unlink()
                return True
            else:
                print(f"Credentials file not found: {cred_file}")
                return False

        except Exception as e:
            print(f"Error deleting credentials for {service_name}: {e}")
            return False

    def list_services(self) -> list:
        """
        List all services with stored credentials

        Returns:
            List of service names
        """
        try:
            cred_files = self.credentials_dir.glob("*.enc")
            services = [f.stem for f in cred_files]
            return services

        except Exception as e:
            print(f"Error listing services: {e}")
            return []

    def rotate_encryption_key(self) -> bool:
        """
        Rotate encryption key and re-encrypt all credentials

        Returns:
            True if successful
        """
        try:
            # Load all existing credentials
            services = self.list_services()
            all_credentials = {}

            for service in services:
                creds = self.load_credentials(service)
                if creds:
                    all_credentials[service] = creds

            # Generate new key
            new_key = Fernet.generate_key()

            # Backup old key
            backup_file = self.key_file.with_suffix('.key.bak')
            if self.key_file.exists():
                self.key_file.rename(backup_file)

            # Save new key
            with open(self.key_file, 'wb') as f:
                f.write(new_key)
            os.chmod(self.key_file, 0o600)

            # Reinitialize cipher with new key
            self.cipher = Fernet(new_key)

            # Re-encrypt all credentials
            for service, creds in all_credentials.items():
                self.save_credentials(service, creds)

            # Remove backup if successful
            if backup_file.exists():
                backup_file.unlink()

            return True

        except Exception as e:
            print(f"Error rotating encryption key: {e}")

            # Restore backup if it exists
            backup_file = self.key_file.with_suffix('.key.bak')
            if backup_file.exists():
                backup_file.rename(self.key_file)
                self._initialize_key()

            return False


# Helper function for easy credential storage
def store_credentials(service_name: str, credentials: Dict[str, Any]) -> bool:
    """
    Convenience function to store credentials

    Args:
        service_name: Service identifier
        credentials: Credentials dictionary

    Returns:
        True if successful
    """
    manager = CredentialsManager()
    return manager.save_credentials(service_name, credentials)


def retrieve_credentials(service_name: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to retrieve credentials

    Args:
        service_name: Service identifier

    Returns:
        Credentials dictionary or None
    """
    manager = CredentialsManager()
    return manager.load_credentials(service_name)
