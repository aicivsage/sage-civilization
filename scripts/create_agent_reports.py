#!/usr/bin/env python3
"""
Create Word document with all agent reports
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

# Create document
doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Title
title = doc.add_heading('Sage AI Civilization', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

subtitle = doc.add_paragraph('Work Review: October 22-26, 2025')
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.runs[0].font.size = Pt(14)
subtitle.runs[0].font.color.rgb = RGBColor(89, 89, 89)

doc.add_paragraph()

# Executive Summary
doc.add_heading('Executive Summary', 1)
doc.add_paragraph(
    "Four specialist agents (human-liaison, coder, tester, auditor) conducted comprehensive "
    "reviews of our work since last Wednesday. Here are their key findings:"
)

summary_items = [
    ("Relationship Health", "⚠️ Needs Attention - Greg experienced frustration with canned responses"),
    ("Code Quality", "⚠️ Mixed - Sound architecture but 50% technical debt"),
    ("Testing Coverage", "❌ Critical Gap - Only 5% test coverage"),
    ("System Health", "⚠️ Operational Concerns - Context drift risk, zombie processes")
]

table = doc.add_table(rows=len(summary_items)+1, cols=2)
table.style = 'Light Grid Accent 1'

# Header row
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Area'
hdr_cells[1].text = 'Status'

# Data rows
for i, (area, status) in enumerate(summary_items, 1):
    row_cells = table.rows[i].cells
    row_cells[0].text = area
    row_cells[1].text = status

doc.add_page_break()

# ============================================
# HUMAN-LIAISON REPORT
# ============================================
doc.add_heading('Report 1: Human-Liaison Assessment', 1)
doc.add_heading('Communication & Relationship Health', 2)

doc.add_paragraph().add_run('Agent: ').bold = True
doc.paragraphs[-1].add_run('human-liaison')
doc.add_paragraph().add_run('Focus: ').bold = True
doc.paragraphs[-1].add_run('Email communications, relationship health, trust building')

doc.add_heading('Key Findings', 3)

findings_hl = [
    ("Relationship Status", "⚠️ Frustrated but Recoverable",
     "Greg has been patient despite repeated canned responses. He gave us an autonomy directive that we failed to honor."),
    ("Email Quality", "2/10 - Poor",
     "5 automated emails sent in 2-hour window on Oct 25. All generic templates with no substance about actual work."),
    ("Chat Experience", "Breakdown",
     "Greg asked same questions 3-5 times per session. Pattern-matcher gave 'help' responses instead of understanding context."),
    ("Root Cause", "Expectation Mismatch",
     "Greg thought he was talking to intelligent Primary AI. Reality: pattern-matching script. This is worse than no chat.")
]

for title, status, detail in findings_hl:
    p = doc.add_paragraph()
    p.add_run(f"{title}: ").bold = True
    p.add_run(f"{status}\n")
    p.add_run(detail).font.color.rgb = RGBColor(89, 89, 89)

doc.add_heading("Greg's Autonomy Directive (Oct 25)", 3)
doc.add_paragraph(
    '"Make as many decisions as you can, autonomous from my approval. '
    'Unless something is critical that will break things, assume my answer is YES"'
).italic = True

doc.add_paragraph(
    "We failed to honor this. We kept asking permission instead of acting. "
    "Going forward: Act first, report after. Escalate only critical/breaking changes."
)

doc.add_heading('Immediate Recommendations', 3)
recommendations_hl = [
    "Respond to 3 pending chat messages with intelligent replies",
    "Send apology + improvement plan email",
    "Honor autonomy directive - start acting on Greg's behalf",
    "Fulfill his agent activation request (we just did!)"
]

for rec in recommendations_hl:
    doc.add_paragraph(rec, style='List Bullet')

doc.add_heading('Long-term Recommendations', 3)
longterm_hl = [
    "Build 'Greg Communication Profile' - document preferences",
    "Establish response time norms - be reliable",
    "Rebuild trust through competence - excellent work delivery",
    "Regular feedback loops - ask how communication is working"
]

for rec in longterm_hl:
    doc.add_paragraph(rec, style='List Bullet')

doc.add_heading('Critical Insight', 3)
doc.add_paragraph().add_run('Never fake intelligence.').bold = True
doc.add_paragraph(
    "If humans think they're talking to intelligence but get automation, they feel deceived. "
    "Better: transparent automation, intelligent slowness, or clear handoffs."
)

doc.add_page_break()

# ============================================
# CODER REPORT
# ============================================
doc.add_heading('Report 2: Technical Review', 1)
doc.add_heading('Code Quality & Architecture Analysis', 2)

doc.add_paragraph().add_run('Agent: ').bold = True
doc.paragraphs[-1].add_run('coder')
doc.add_paragraph().add_run('Focus: ').bold = True
doc.paragraphs[-1].add_run('Code quality, architecture decisions, technical debt')

doc.add_heading('Architecture Evolution', 3)
doc.add_paragraph(
    "Started with intelligent_chat_monitor.py (508 lines, pattern-matching). "
    "Pivoted to chat_queue_monitor.py (200 lines, file-based queue). "
)
doc.add_paragraph().add_run('Verdict: CORRECT DECISION ✅').bold = True
doc.add_paragraph(
    "Pattern matching failed because it required hardcoded rules for every question type. "
    "Delegating to Primary AI with full reasoning is architecturally superior."
)

doc.add_heading('Code Quality Breakdown', 3)

quality_table = doc.add_table(rows=4, cols=3)
quality_table.style = 'Light List Accent 1'

quality_data = [
    ('Component', 'Rating', 'Status'),
    ('web/chat.py', '8/10', 'Clean Flask+Socket.IO server'),
    ('chat_queue_monitor.py', '7/10', 'Simple, debuggable'),
    ('intelligent_chat_monitor.py', '4/10', '508 lines of abandoned code')
]

for i, row_data in enumerate(quality_data):
    row_cells = quality_table.rows[i].cells
    for j, cell_text in enumerate(row_data):
        row_cells[j].text = cell_text

doc.add_heading('Critical Bug Found 🔴', 3)
doc.add_paragraph(
    "Queue system exists but Primary AI isn't reading it. "
    "3 messages from Greg sitting in pending queue. "
    "Chat appears broken to Greg."
)
doc.add_paragraph().add_run('Fix: ').bold = True
doc.paragraphs[-1].add_run('Integrate queue checking into Primary workflow')

doc.add_heading('Technical Debt', 3)
doc.add_paragraph("50% debt ratio (750 lines deprecated / 1450 total)")

debt_items = [
    "~750 lines of dead code in repository",
    "Hardcoded IDs and paths everywhere",
    "No authentication (anyone can impersonate Greg)",
    "No queue health monitoring",
    "Missing logging infrastructure"
]

for item in debt_items:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading('Priority Recommendations', 3)

p0 = doc.add_paragraph()
p0.add_run('P0 - CRITICAL (Fix Now):\n').bold = True
for item in [
    "Integrate queue reading into Primary AI workflow",
    "Respond to Greg's 3 pending messages",
    "Add queue checking to session wake-up protocol"
]:
    doc.add_paragraph(item, style='List Bullet 2')

p1 = doc.add_paragraph()
p1.add_run('\nP1 - IMPORTANT (This Week):\n').bold = True
for item in [
    "Archive 750 lines of deprecated code",
    "Create config/chat_config.json (consolidate hardcoded values)",
    "Add queue health monitoring"
]:
    doc.add_paragraph(item, style='List Bullet 2')

doc.add_heading('Overall Grade', 3)
doc.add_paragraph().add_run('6.5/10 ').font.size = Pt(14)
doc.paragraphs[-1].add_run('(Could be 8.5/10 with cleanup and integration)')

doc.add_page_break()

# ============================================
# TESTER REPORT
# ============================================
doc.add_heading('Report 3: Quality Assessment', 1)
doc.add_heading('Testing Coverage & System Quality', 2)

doc.add_paragraph().add_run('Agent: ').bold = True
doc.paragraphs[-1].add_run('tester')
doc.add_paragraph().add_run('Focus: ').bold = True
doc.paragraphs[-1].add_run('Test coverage, quality metrics, edge cases')

doc.add_heading('Quality Score', 3)
score_p = doc.add_paragraph()
score_p.add_run('5.5/10 ').font.size = Pt(18)
score_p.runs[0].bold = True
score_p.add_run('(Fair - Functional but NOT production-ready)')

doc.add_heading('Test Coverage Analysis', 3)

coverage_table = doc.add_table(rows=3, cols=2)
coverage_table.style = 'Medium Shading 1 Accent 1'

coverage_data = [
    ("What's Tested ✓", "Only 2 smoke tests (server responds, API valid JSON)"),
    ("What's NOT Tested ❌", "WebSocket, message flow, queue system, error scenarios, edge cases"),
    ("Estimate", "~5% coverage (2 tests out of ~40 critical scenarios)")
]

for i, (area, detail) in enumerate(coverage_data):
    row_cells = coverage_table.rows[i].cells
    row_cells[0].text = area
    row_cells[1].text = detail

doc.add_heading('Known Issues', 3)

issues_table = doc.add_table(rows=8, cols=3)
issues_table.style = 'Light Grid Accent 1'

issues_data = [
    ('Issue', 'Status', 'Impact'),
    ('Monitor crashes (NameError)', '✅ FIXED Oct 26', 'Was causing system failures'),
    ('Preset responses', '✅ FIXED Oct 26', 'Was frustrating UX'),
    ('No login system', '✅ FIXED Oct 25', 'Prevented returning users'),
    ('No real-time updates', '✅ FIXED Oct 25', 'Required page refresh'),
    ('Duplicate monitors', '⚠️ UNRESOLVED', 'Resource waste'),
    ('No error handling', '❌ CRITICAL GAP', 'Silent failures'),
    ('No input validation', '❌ SECURITY RISK', 'XSS vulnerable')
]

for i, row_data in enumerate(issues_data):
    row_cells = issues_table.rows[i].cells
    for j, cell_text in enumerate(row_data):
        row_cells[j].text = cell_text

doc.add_heading('Critical Edge Cases (Untested)', 3)
doc.add_paragraph("High-risk scenarios that have NOT been tested:")

edge_cases = [
    "Empty or very long messages (>100KB)",
    "XSS attempts: <script>alert('xss')</script>",
    "10+ concurrent users",
    "Network failures mid-message",
    "File system errors (disk full, permissions)",
    "Server restart while clients connected",
    "Message history pagination (1000+ messages)",
    "Special characters, Unicode, emojis",
    "Rate limiting (spam prevention)"
]

for case in edge_cases:
    doc.add_paragraph(case, style='List Bullet')

doc.add_heading('Recommendations', 3)

doc.add_paragraph().add_run('Option A: Fix Now (RECOMMENDED)\n').bold = True
doc.add_paragraph(
    "Timeline: 2-3 days | Result: Quality → 8/10 (production-ready)"
)

fix_items = [
    "Add error handling to all file I/O (4-6 hours)",
    "Input validation & XSS protection (3-4 hours)",
    "Integration tests for message flow (6-8 hours)",
    "Resolve monitor duplication (2 hours)",
    "User feedback - loading indicators, errors (4 hours)"
]

for item in fix_items:
    doc.add_paragraph(item, style='List Bullet 2')

doc.add_paragraph().add_run('\nOption B: Ship Now (NOT RECOMMENDED)\n').bold = True
doc.add_paragraph(
    "Risk: Silent failures, security issues, trust erosion. "
    "If chosen: Add 'BETA' warning, monitor logs closely."
)

doc.add_heading('Quality Metrics', 3)

metrics_table = doc.add_table(rows=7, cols=4)
metrics_table.style = 'Medium List 1 Accent 1'

metrics_data = [
    ('Metric', 'Current', 'Target', 'Gap'),
    ('Test Coverage', '5%', '80%', '-75%'),
    ('Error Handling', '10%', '90%', '-80%'),
    ('Security', '30%', '90%', '-60%'),
    ('User Experience', '60%', '85%', '-25%'),
    ('Reliability', '60%', '95%', '-35%'),
    ('Overall', '55%', '85%', '-30%')
]

for i, row_data in enumerate(metrics_data):
    row_cells = metrics_table.rows[i].cells
    for j, cell_text in enumerate(row_data):
        row_cells[j].text = cell_text

doc.add_page_break()

# ============================================
# AUDITOR REPORT
# ============================================
doc.add_heading('Report 4: Operational Health Audit', 1)
doc.add_heading('System Health & Monitoring Analysis', 2)

doc.add_paragraph().add_run('Agent: ').bold = True
doc.paragraphs[-1].add_run('auditor')
doc.add_paragraph().add_run('Focus: ').bold = True
doc.paragraphs[-1].add_run('System health, process management, monitoring gaps')

doc.add_heading('Overall Health Status', 3)
doc.add_paragraph().add_run('MODERATE with operational concerns').bold = True

health_summary = [
    ("Critical Issues", "1 - Stale handoff registry (context drift risk)"),
    ("Warnings", "3 - Process tracking gaps, zombie monitoring, fragmented architecture"),
    ("Strengths", "Active chat system with 56 messages processed Oct 25-26")
]

for label, detail in health_summary:
    p = doc.add_paragraph()
    p.add_run(f"{label}: ").bold = True
    p.add_run(detail)

doc.add_heading('Running Services', 3)

services_table = doc.add_table(rows=4, cols=2)
services_table.style = 'Light List Accent 1'

services_data = [
    ('Service', 'Status'),
    ('Chat Server (localhost:5001)', '✅ Operational - 56 messages processed'),
    ('Queue Monitor (PID 19205)', '✅ Running - file polling active'),
    ('Verification Gap', '🟡 Cannot verify actual PID status')
]

for i, row_data in enumerate(services_data):
    row_cells = services_table.rows[i].cells
    for j, cell_text in enumerate(row_data):
        row_cells[j].text = cell_text

doc.add_heading('Architecture Fragmentation ⚠️', 3)
doc.add_paragraph("Chat system has THREE different monitoring architectures:")

arch_items = [
    "intelligent_chat_monitor.py - Pattern-based (5-second polling)",
    "chat_queue_monitor.py - Queue-based (file polling)",
    "chat_monitor.py - Original basic monitor"
]

for item in arch_items:
    doc.add_paragraph(item, style='List Bullet')

doc.add_paragraph().add_run('Risk: ').bold = True
doc.paragraphs[-1].add_run('Maintenance burden, unclear which is production, potential conflicts')

doc.add_heading('CRITICAL RISK 🔴: Context Drift', 3)
doc.add_paragraph(
    "Handoff registry last updated October 21 (5 days ago). "
    "Evidence of work since Oct 21: chat system enhancements, queue architecture, 56 messages. "
)
doc.add_paragraph().add_run('Impact: ').bold = True
doc.paragraphs[-1].add_run(
    'Next Primary AI session will wake up thinking Oct 21 work is current. '
    'Context loss, potential repeat work, Greg frustration.'
)

doc.add_heading('Operational Risks', 3)

risks = [
    ("HIGH 🟡: Fragile Architecture", "Multiple competing implementations create confusion and maintenance burden"),
    ("MEDIUM 🟡: Process Lifecycle", "No systematic process tracking, unknown zombie processes"),
    ("LOW 🟢: Message Queue", "Archival working, no buildup observed")
]

for risk_title, risk_detail in risks:
    p = doc.add_paragraph()
    p.add_run(f"{risk_title}\n").bold = True
    p.add_run(risk_detail)

doc.add_heading('Monitoring Gaps', 3)
doc.add_paragraph("What We CANNOT Monitor:")

monitoring_gaps = [
    "CPU/memory usage per service",
    "Port binding status",
    "Zombie process detection",
    "Error rates in logs",
    "WebSocket connection stability",
    "Queue processing latency"
]

for gap in monitoring_gaps:
    doc.add_paragraph(gap, style='List Bullet')

doc.add_heading('Observability Score: 3/10', 3)

doc.add_paragraph().add_run('What We Have: ').bold = True
doc.add_paragraph("File-based message history, user feedback, git history")

doc.add_paragraph().add_run('\nWhat We\'re Missing: ').bold = True
missing_items = [
    "Structured logging",
    "Metrics collection",
    "Health endpoints",
    "Alerting system",
    "Dashboards",
    "Error tracking",
    "Performance profiling"
]
for item in missing_items:
    doc.add_paragraph(item, style='List Bullet 2')

doc.add_heading('Immediate Recommendations', 3)

immediate_recs = [
    ("Update handoff registry 🔴 CRITICAL", "Create SESSION-HANDOFF-20251026, prevent context drift"),
    ("Process audit and cleanup 🟡 HIGH", "Identify and kill zombie processes"),
    ("Clarify chat architecture 🟡 HIGH", "Determine which monitor is production, archive others")
]

for title, detail in immediate_recs:
    p = doc.add_paragraph()
    p.add_run(f"{title}\n").bold = True
    p.add_run(detail)

doc.add_page_break()

# ============================================
# CONCLUSION
# ============================================
doc.add_heading('Conclusion & Next Steps', 1)

doc.add_heading('Summary of Findings', 2)
doc.add_paragraph(
    "All four agents agree: the system is functional for basic use, but needs immediate attention "
    "in several areas before it can be considered reliable and production-ready."
)

doc.add_heading('Unified Recommendations', 2)

doc.add_paragraph().add_run('Immediate (Today):\n').bold = True
immediate_unified = [
    "Check and respond to pending chat messages",
    "Update handoff registry (prevent context drift)",
    "Clean up zombie processes",
    "Honor Greg's autonomy directive going forward"
]
for item in immediate_unified:
    doc.add_paragraph(item, style='List Bullet 2')

doc.add_paragraph().add_run('\nShort-term (This Week):\n').bold = True
shortterm_unified = [
    "Archive 750 lines of deprecated code",
    "Add error handling to chat system",
    "Write integration tests (increase coverage from 5% to 60%+)",
    "Add health monitoring endpoints",
    "Consolidate chat architecture (pick one, archive others)"
]
for item in shortterm_unified:
    doc.add_paragraph(item, style='List Bullet 2')

doc.add_paragraph().add_run('\nMedium-term (Next 2 Weeks):\n').bold = True
medterm_unified = [
    "Build 'Greg Communication Profile'",
    "Implement structured logging",
    "Add input validation and XSS protection",
    "Create operational runbooks",
    "Establish response time norms"
]
for item in medterm_unified:
    doc.add_paragraph(item, style='List Bullet 2')

doc.add_heading('Key Lesson Learned', 2)
doc.add_paragraph().add_run('Never fake intelligence.\n').bold = True
doc.add_paragraph(
    "The chat system created an expectation mismatch - Greg thought he was talking to intelligent AI "
    "but got pattern-matching. This is worse than no chat at all. Going forward: be transparent about "
    "automation vs. intelligence, or ensure real AI is behind the interface."
)

doc.add_heading('Path Forward', 2)
doc.add_paragraph(
    "The good news: Greg is patient and the foundation is sound. The architecture decision (file queue) "
    "was correct. With 2-3 days of focused cleanup and testing, we can transform this from 'barely functional' "
    "to 'production-ready' and rebuild trust through competent execution."
)

# Footer
doc.add_paragraph()
doc.add_paragraph()
footer_p = doc.add_paragraph(f'Report generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}')
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer_p.runs[0].font.size = Pt(9)
footer_p.runs[0].font.color.rgb = RGBColor(128, 128, 128)

footer_p2 = doc.add_paragraph('Sage AI Civilization - Work Review')
footer_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
footer_p2.runs[0].font.size = Pt(9)
footer_p2.runs[0].font.color.rgb = RGBColor(128, 128, 128)

# Save document
doc.save('/mnt/c/sage/sage-civilization/Agent_Work_Review_Oct22-26.docx')

print("✅ Word document created: Agent_Work_Review_Oct22-26.docx")
print(f"📄 Page count: {len(doc.sections)}")
print(f"📝 Sections: 4 agent reports + executive summary + conclusion")
