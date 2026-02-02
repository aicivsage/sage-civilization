#!/usr/bin/env python3
"""
Email Address Validator - Prevents bounced emails by verifying against address book

Usage:
    python3 tools/verify_email_address.py recipient@example.com
    python3 tools/verify_email_address.py "Corey Cottrell"  # Lookup by name

Returns:
    - Exit 0: Email verified in address book
    - Exit 1: Email NOT in address book (with suggestions if similar name found)
    - Exit 2: Error reading address book

Purpose: Prevent email bounces by checking against verified contacts before sending
"""

import json
import sys
import os
from pathlib import Path
from difflib import SequenceMatcher

def load_address_book():
    """Load verified contacts from address book"""
    address_book_path = Path(__file__).parent.parent / "memories" / "communication" / "address-book" / "contacts.json"
    
    if not address_book_path.exists():
        print(f"❌ ERROR: Address book not found at {address_book_path}", file=sys.stderr)
        return None
    
    try:
        with open(address_book_path, 'r') as f:
            data = json.load(f)
            return data.get('contacts', [])
    except Exception as e:
        print(f"❌ ERROR: Failed to read address book: {e}", file=sys.stderr)
        return None

def similarity(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_contact_by_email(contacts, email):
    """Find contact by exact email match"""
    for contact in contacts:
        if contact.get('email', '').lower() == email.lower():
            return contact
    return None

def find_contact_by_name(contacts, name):
    """Find contact by name (fuzzy match)"""
    name_lower = name.lower()
    
    # Exact match first
    for contact in contacts:
        contact_name = contact.get('name', '').lower()
        if contact_name == name_lower:
            return contact
    
    # Fuzzy match if no exact match
    best_match = None
    best_similarity = 0.6  # Threshold for considering a match
    
    for contact in contacts:
        contact_name = contact.get('name', '')
        sim = similarity(name, contact_name)
        if sim > best_similarity:
            best_similarity = sim
            best_match = contact
    
    return best_match

def suggest_contacts(contacts, query):
    """Suggest similar contacts based on name or email similarity"""
    suggestions = []
    query_lower = query.lower()
    
    for contact in contacts:
        name = contact.get('name', '')
        email = contact.get('email', '')
        
        # Check if query partially matches name or email
        if query_lower in name.lower() or query_lower in email.lower():
            suggestions.append(contact)
        # Check similarity
        elif similarity(query, name) > 0.5 or similarity(query, email) > 0.5:
            suggestions.append(contact)
    
    return suggestions[:5]  # Return top 5 suggestions

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify_email_address.py <email_or_name>")
        print("\nExamples:")
        print("  python3 verify_email_address.py coreycmusic@gmail.com")
        print("  python3 verify_email_address.py 'Corey Cottrell'")
        sys.exit(2)
    
    query = sys.argv[1]
    
    # Load address book
    contacts = load_address_book()
    if contacts is None:
        sys.exit(2)
    
    # Determine if query is email or name
    is_email = '@' in query
    
    if is_email:
        # Search by email
        contact = find_contact_by_email(contacts, query)
        
        if contact:
            print(f"✅ EMAIL VERIFIED")
            print(f"Name: {contact.get('name')}")
            print(f"Email: {contact.get('email')}")
            print(f"Relationship: {contact.get('relationship', 'N/A')}")
            if contact.get('notes'):
                print(f"Notes: {contact.get('notes')}")
            sys.exit(0)
        else:
            print(f"⚠️  EMAIL NOT IN ADDRESS BOOK")
            print(f"Email: {query}")
            print()
            print("This email address is not verified in the address book.")
            print("Sending to unverified addresses may result in bounces.")
            print()
            
            # Suggest similar contacts
            suggestions = suggest_contacts(contacts, query)
            if suggestions:
                print("Did you mean one of these?")
                for contact in suggestions:
                    print(f"  • {contact.get('name')} <{contact.get('email')}>")
            
            sys.exit(1)
    else:
        # Search by name
        contact = find_contact_by_name(contacts, query)
        
        if contact:
            print(f"✅ CONTACT FOUND")
            print(f"Name: {contact.get('name')}")
            print(f"Email: {contact.get('email')}")
            print(f"Relationship: {contact.get('relationship', 'N/A')}")
            if contact.get('notes'):
                print(f"Notes: {contact.get('notes')}")
            sys.exit(0)
        else:
            print(f"⚠️  CONTACT NOT FOUND")
            print(f"Name: {query}")
            print()
            print("This person is not in the address book.")
            print()
            
            # Suggest similar contacts
            suggestions = suggest_contacts(contacts, query)
            if suggestions:
                print("Did you mean one of these?")
                for contact in suggestions:
                    print(f"  • {contact.get('name')} <{contact.get('email')}>")
            
            sys.exit(1)

if __name__ == "__main__":
    main()
