#!/bin/bash
# Email Reporter Agent - Execution Script
# Sends consolidation update to Weaver

echo "========================================"
echo "Email Reporter Agent"
echo "Sending to: weaver.aiciv@gmail.com"
echo "Subject: Consolidation Mission Update"
echo "========================================"
echo ""

cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch

# Execute Python email script
python3 send_email_to_weaver.py

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Email delivered successfully!"
    echo "Weaver should receive notification within 30 seconds."
else
    echo ""
    echo "❌ Email delivery failed (exit code: $EXIT_CODE)"
    echo "Check error output above for details."
fi

exit $EXIT_CODE
