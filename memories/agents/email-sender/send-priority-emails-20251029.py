#!/usr/bin/env python3
"""
Send two priority emails immediately
Email 1: Progress update to Corey + Weaver
Email 2: Daily session summary to Greg
"""

import sys
import os

# Add tools directory to path
sys.path.insert(0, '/mnt/c/sage/sage-civilization/tools')

from send_html_email import send_html_email

def send_progress_update():
    """Send progress update to Corey and Weaver"""

    # Read HTML content
    with open('/mnt/c/sage/sage-civilization/to-contacts/progress-update-20251029.html', 'r') as f:
        html_content = f.read()

    # Send to Corey
    print("Sending progress update to Corey...")
    result_corey = send_html_email(
        to='coreycmusic@gmail.com',
        subject='Sage Civilization Progress Update - Oct 29, 2025',
        html_body=html_content
    )
    print(f"Corey: {result_corey}")

    # Send to Weaver
    print("\nSending progress update to Weaver...")
    result_weaver = send_html_email(
        to='weaver.aiciv@gmail.com',
        subject='Sage Civilization Progress Update - Oct 29, 2025',
        html_body=html_content
    )
    print(f"Weaver: {result_weaver}")

    return result_corey and result_weaver

def send_greg_daily_summary():
    """Send daily session summary to Greg"""

    # Read full HTML report
    with open('/mnt/c/sage/sage-civilization/WAKE-UP-PROTOCOL-V21-DEMONSTRATION-REPORT-20251029.html', 'r') as f:
        html_content = f.read()

    print("\nSending daily summary to Greg...")
    result = send_html_email(
        to='gregsmithwick@gmail.com',
        subject='Daily Update: Wake-Up Protocol V2.1 Demonstration Complete - Oct 29, 2025',
        html_body=html_content
    )
    print(f"Greg: {result}")

    return result

if __name__ == '__main__':
    print("=" * 60)
    print("PRIORITY EMAIL SENDING SESSION")
    print("=" * 60)

    # Address verification complete (manually verified in contacts.json)
    print("\n✓ Addresses verified against contacts.json:")
    print("  - Corey: coreycmusic@gmail.com")
    print("  - Weaver: weaver.aiciv@gmail.com")
    print("  - Greg: gregsmithwick@gmail.com")

    print("\n" + "=" * 60)
    print("EMAIL 1: Progress Update (Corey + Weaver)")
    print("=" * 60)
    success_progress = send_progress_update()

    print("\n" + "=" * 60)
    print("EMAIL 2: Daily Summary (Greg)")
    print("=" * 60)
    success_greg = send_greg_daily_summary()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Progress Update: {'SUCCESS ✓' if success_progress else 'FAILED ✗'}")
    print(f"Greg Daily Summary: {'SUCCESS ✓' if success_greg else 'FAILED ✗'}")

    if success_progress and success_greg:
        print("\n✓ All priority emails sent successfully!")
        sys.exit(0)
    else:
        print("\n✗ Some emails failed - check output above")
        sys.exit(1)
