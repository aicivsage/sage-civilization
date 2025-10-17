#!/usr/bin/env python3
"""
Email Search and Contact Management Utility

Provides search, filtering, and contact management for email agents.
Part of the autonomous email agent capabilities.
"""

import imaplib
import email
from email.header import decode_header
import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

# Configuration
EMAIL_ADDRESS = 'acgee.ai@gmail.com'
EMAIL_PASSWORD = 'imbk qgug ycse edio'  # App password
CONTACTS_FILE = '/home/corey/projects/AI-CIV/grow_gemini_deepresearch/memories/agents/email-reporter/contacts.json'

class EmailSearcher:
    """Handle email search and contact management operations"""

    def __init__(self, email_addr: str = EMAIL_ADDRESS, password: str = EMAIL_PASSWORD):
        self.email = email_addr
        self.password = password
        self.imap = None

    def connect(self):
        """Establish IMAP connection"""
        try:
            self.imap = imaplib.IMAP4_SSL('imap.gmail.com')
            self.imap.login(self.email, self.password)
            return True
        except Exception as e:
            print(f"❌ IMAP connection failed: {e}")
            return False

    def disconnect(self):
        """Close IMAP connection"""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except:
                pass

    def search_inbox(self,
                     query: Optional[str] = None,
                     from_addr: Optional[str] = None,
                     subject: Optional[str] = None,
                     date_range: Optional[Tuple[datetime, datetime]] = None,
                     limit: int = 50) -> List[Dict]:
        """
        Search inbox with various filters

        Args:
            query: Text to search in body (optional)
            from_addr: Filter by sender email (optional)
            subject: Filter by subject text (optional)
            date_range: Tuple of (start_date, end_date) (optional)
            limit: Maximum results to return

        Returns:
            List of email dictionaries with metadata
        """
        if not self.connect():
            return []

        try:
            self.imap.select('INBOX')

            # Build IMAP search criteria
            criteria = []

            if from_addr:
                criteria.append(f'FROM "{from_addr}"')

            if subject:
                criteria.append(f'SUBJECT "{subject}"')

            if date_range:
                start_date, end_date = date_range
                criteria.append(f'SINCE {start_date.strftime("%d-%b-%Y")}')
                criteria.append(f'BEFORE {end_date.strftime("%d-%b-%Y")}')

            # Execute search
            search_string = ' '.join(criteria) if criteria else 'ALL'
            status, messages = self.imap.search(None, search_string)

            if status != 'OK':
                return []

            email_ids = messages[0].split()

            # Limit results
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids

            results = []
            for email_id in email_ids:
                email_data = self._fetch_email(email_id)
                if email_data:
                    # Apply body query filter if specified
                    if query and query.lower() not in email_data['body'].lower():
                        continue
                    results.append(email_data)

            return results

        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
        finally:
            self.disconnect()

    def _fetch_email(self, email_id: bytes) -> Optional[Dict]:
        """Fetch and parse a single email"""
        try:
            status, msg_data = self.imap.fetch(email_id, '(RFC822)')

            if status != 'OK':
                return None

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Decode subject
                    subject = msg.get('Subject', '')
                    if subject:
                        decoded = decode_header(subject)[0]
                        if isinstance(decoded[0], bytes):
                            subject = decoded[0].decode(decoded[1] or 'utf-8')
                        else:
                            subject = decoded[0]

                    # Get body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                payload = part.get_payload(decode=True)
                                if payload:
                                    body = payload.decode('utf-8', errors='ignore')
                                    break
                    else:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='ignore')

                    return {
                        'id': email_id.decode(),
                        'from': msg.get('From', ''),
                        'to': msg.get('To', ''),
                        'subject': subject,
                        'date': msg.get('Date', ''),
                        'body': body[:1000]  # Limit body length
                    }

            return None

        except Exception as e:
            print(f"❌ Failed to fetch email {email_id}: {e}")
            return None

    def find_email_addresses(self, text: str) -> List[str]:
        """
        Extract email addresses from any text

        Args:
            text: Text to search for email addresses

        Returns:
            List of unique email addresses found
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return list(set(matches))  # Remove duplicates

    def search_for_address(self, partial_email: str) -> List[Dict]:
        """
        Search inbox for any email containing a specific address
        Useful for finding all correspondence with someone

        Args:
            partial_email: Email address or partial address to search

        Returns:
            List of emails involving this address
        """
        results = []

        # Search as sender
        from_results = self.search_inbox(from_addr=partial_email)
        results.extend(from_results)

        # Search in body (for CC, forwarded, etc.)
        body_results = self.search_inbox(query=partial_email)

        # Deduplicate
        seen_ids = {r['id'] for r in results}
        for email_data in body_results:
            if email_data['id'] not in seen_ids:
                results.append(email_data)

        return results

class ContactManager:
    """Manage the contacts list for email agents"""

    def __init__(self, contacts_file: str = CONTACTS_FILE):
        self.contacts_file = contacts_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create contacts file if it doesn't exist"""
        if not os.path.exists(self.contacts_file):
            os.makedirs(os.path.dirname(self.contacts_file), exist_ok=True)
            default_data = {
                "contacts": [],
                "last_updated": datetime.utcnow().isoformat(),
                "schema_version": "1.0"
            }
            with open(self.contacts_file, 'w') as f:
                json.dump(default_data, f, indent=2)

    def load_contacts(self) -> List[Dict]:
        """Load all contacts from file"""
        with open(self.contacts_file, 'r') as f:
            data = json.load(f)
        return data.get('contacts', [])

    def save_contacts(self, contacts: List[Dict]):
        """Save contacts to file"""
        data = {
            "contacts": contacts,
            "last_updated": datetime.utcnow().isoformat(),
            "schema_version": "1.0"
        }
        with open(self.contacts_file, 'w') as f:
            json.dump(data, f, indent=2)

    def check_contact_exists(self, email_addr: str) -> Optional[Dict]:
        """
        Check if contact exists in list

        Args:
            email_addr: Email address to check

        Returns:
            Contact dict if found, None otherwise
        """
        contacts = self.load_contacts()
        for contact in contacts:
            if contact['email'].lower() == email_addr.lower():
                return contact
        return None

    def add_contact(self, name: str, email_addr: str, role: str,
                   priority: str = "medium", notes: str = "") -> bool:
        """
        Add new contact to list

        Args:
            name: Contact name
            email_addr: Email address
            role: Role/relationship (human_operator, sister_civilization, etc.)
            priority: Priority level (high, medium, low)
            notes: Additional notes

        Returns:
            True if added, False if already exists
        """
        # Check if exists
        if self.check_contact_exists(email_addr):
            print(f"⚠️  Contact {email_addr} already exists")
            return False

        contacts = self.load_contacts()
        new_contact = {
            "name": name,
            "email": email_addr,
            "role": role,
            "priority": priority,
            "notes": notes
        }
        contacts.append(new_contact)
        self.save_contacts(contacts)

        print(f"✅ Added contact: {name} <{email_addr}>")
        return True

    def update_contact(self, email_addr: str, **kwargs) -> bool:
        """
        Update existing contact

        Args:
            email_addr: Email address of contact to update
            **kwargs: Fields to update (name, role, priority, notes)

        Returns:
            True if updated, False if not found
        """
        contacts = self.load_contacts()
        for contact in contacts:
            if contact['email'].lower() == email_addr.lower():
                contact.update(kwargs)
                self.save_contacts(contacts)
                print(f"✅ Updated contact: {email_addr}")
                return True

        print(f"⚠️  Contact {email_addr} not found")
        return False

    def get_contact_by_role(self, role: str) -> List[Dict]:
        """Get all contacts with specific role"""
        contacts = self.load_contacts()
        return [c for c in contacts if c['role'] == role]

    def get_high_priority_contacts(self) -> List[Dict]:
        """Get all high priority contacts"""
        contacts = self.load_contacts()
        return [c for c in contacts if c['priority'] == 'high']

def main():
    """Demo and testing"""
    print("="*70)
    print("📧 Email Search and Contact Management Utility")
    print("="*70)
    print()

    # Test contact management
    print("📇 Contact Management:")
    cm = ContactManager()
    contacts = cm.load_contacts()
    print(f"Loaded {len(contacts)} contacts:")
    for contact in contacts:
        print(f"  - {contact['name']} <{contact['email']}> [{contact['role']}]")
    print()

    # Test email search
    print("🔍 Email Search:")
    searcher = EmailSearcher()

    # Search recent emails from Corey
    print("Searching for emails from Corey...")
    corey_emails = searcher.search_inbox(from_addr='coreycmusic@gmail.com', limit=5)
    print(f"Found {len(corey_emails)} emails")
    for email_data in corey_emails[:3]:
        print(f"  - {email_data['subject']}")
    print()

    # Find email addresses in text
    print("📋 Email Address Extraction:")
    sample_text = """
    Contact me at test@example.com or admin@company.org
    You can also reach support@service.net
    """
    addresses = searcher.find_email_addresses(sample_text)
    print(f"Found addresses: {addresses}")
    print()

    print("="*70)
    print("✅ Tests complete")
    print("="*70)

if __name__ == "__main__":
    main()
