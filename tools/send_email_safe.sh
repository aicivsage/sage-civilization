#!/bin/bash
# Safe Email Sender - Verifies address before sending
# Usage: ./tools/send_email_safe.sh recipient@example.com "Subject" "path/to/body.html"

set -e

if [ $# -lt 3 ]; then
    echo "Usage: $0 <to_email> <subject> <html_file>"
    echo ""
    echo "Examples:"
    echo "  $0 coreycmusic@gmail.com 'Subject' drafts/email.html"
    echo "  $0 'Corey' 'Subject' drafts/email.html  # Lookup by name"
    exit 1
fi

TO="$1"
SUBJECT="$2"
HTML_FILE="$3"

echo "🔍 Verifying email address..."
echo ""

# Verify address
if python3 tools/verify_email_address.py "$TO"; then
    echo ""
    echo "✅ Address verified - proceeding with send..."
    echo ""
    
    # Extract email if name was provided
    EMAIL=$(python3 tools/verify_email_address.py "$TO" 2>/dev/null | grep "Email:" | cut -d' ' -f2)
    if [ -z "$EMAIL" ]; then
        EMAIL="$TO"
    fi
    
    # Send email
    python3 tools/send_html_email.py --to "$EMAIL" --subject "$SUBJECT" --body "$(cat $HTML_FILE)"
else
    echo ""
    echo "❌ SEND ABORTED - Address not verified"
    echo ""
    echo "To send anyway (not recommended), use send_html_email.py directly:"
    echo "  python3 tools/send_html_email.py --to \"$TO\" --subject \"$SUBJECT\" --body \"\$(cat $HTML_FILE)\""
    exit 1
fi
