#!/usr/bin/env python3
"""
Create professional PDF for Sage & Weaver Business Plan
For Pasco Economic Development Council Biz Incubator Application
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime

# Colors
SAGE_GREEN = HexColor('#2E7D32')
WEAVER_BLUE = HexColor('#1565C0')
DARK_GRAY = HexColor('#333333')
LIGHT_GRAY = HexColor('#F5F5F5')
ACCENT = HexColor('#FF6F00')

def create_styles():
    styles = getSampleStyleSheet()

    # Title style
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=SAGE_GREEN,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    # Tagline
    styles.add(ParagraphStyle(
        name='Tagline',
        parent=styles['Normal'],
        fontSize=16,
        textColor=WEAVER_BLUE,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    ))

    # Section headers
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=SAGE_GREEN,
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold',
        borderPadding=(0, 0, 5, 0),
    ))

    # Subsection headers
    styles.add(ParagraphStyle(
        name='SubSection',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=WEAVER_BLUE,
        spaceBefore=14,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    ))

    # Body text
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=DARK_GRAY,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    ))

    # Bullet points
    styles.add(ParagraphStyle(
        name='CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        textColor=DARK_GRAY,
        leftIndent=20,
        spaceAfter=4,
        bulletIndent=10,
        leading=14
    ))

    # Quote/highlight box text
    styles.add(ParagraphStyle(
        name='Highlight',
        parent=styles['Normal'],
        fontSize=12,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique',
        spaceAfter=12,
        spaceBefore=12
    ))

    # Table header
    styles.add(ParagraphStyle(
        name='TableHeader',
        parent=styles['Normal'],
        fontSize=10,
        textColor=white,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER
    ))

    # Table cell
    styles.add(ParagraphStyle(
        name='TableCell',
        parent=styles['Normal'],
        fontSize=9,
        textColor=DARK_GRAY,
        alignment=TA_LEFT
    ))

    return styles

def add_header_footer(canvas, doc):
    canvas.saveState()
    # Header line
    canvas.setStrokeColor(SAGE_GREEN)
    canvas.setLineWidth(2)
    canvas.line(0.75*inch, 10.5*inch, 7.75*inch, 10.5*inch)

    # Footer
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(DARK_GRAY)
    canvas.drawString(0.75*inch, 0.5*inch, "Sage & Weaver Business Plan")
    canvas.drawRightString(7.75*inch, 0.5*inch, f"Page {doc.page}")

    # Footer line
    canvas.setStrokeColor(WEAVER_BLUE)
    canvas.setLineWidth(1)
    canvas.line(0.75*inch, 0.65*inch, 7.75*inch, 0.65*inch)
    canvas.restoreState()

def create_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.9*inch,
        bottomMargin=0.9*inch
    )

    styles = create_styles()
    story = []

    # ===== COVER PAGE =====
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("SAGE & WEAVER", styles['MainTitle']))
    story.append(Paragraph("BUSINESS PLAN", styles['MainTitle']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph('"5-10x Every Knowledge Worker"', styles['Tagline']))
    story.append(Spacer(1, 0.5*inch))

    # Version info box
    version_data = [
        ['Version:', '1.0 Final'],
        ['Date:', 'January 21, 2026'],
        ['Prepared by:', 'ECHO (AI Collective) + Corey Cottrell']
    ]
    version_table = Table(version_data, colWidths=[1.5*inch, 3*inch])
    version_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(version_table)

    story.append(PageBreak())

    # ===== EXECUTIVE SUMMARY =====
    story.append(Paragraph("EXECUTIVE SUMMARY", styles['SectionHeader']))

    story.append(Paragraph(
        "<b>Sage & Weaver</b> transforms how businesses use AI - from 'typing prompts' to "
        "'directing a team of 100 brilliant specialists who never sleep.'",
        styles['CustomBody']
    ))

    story.append(Paragraph("The Problem:", styles['SubSection']))
    bullets = [
        "Even if you understand AI at an expert level TODAY, you won't in 8 weeks",
        "New models, skills, and techniques drop daily",
        "99% of knowledge workers are falling behind every single day",
        "The 1% who build persistent AI systems are pulling away exponentially"
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", styles['CustomBullet']))

    story.append(Paragraph("Our Solution:", styles['SubSection']))
    bullets = [
        "<b>Workshops</b> teach the technique",
        "<b>Newsletter</b> keeps you current",
        "<b>AI-CIV Forks</b> give you your own AI collective",
        "<b>Enterprise</b> transforms entire organizations"
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", styles['CustomBullet']))

    story.append(Paragraph("The Team:", styles['SubSection']))
    team_data = [
        ['Human', 'AI Collective', 'Role'],
        ['Corey Cottrell', 'ECHO + WEAVER', 'Founder, Enterprise, Strategy'],
        ['Greg', 'SAGE', 'Local Workshop Delivery'],
        ['Russell', 'PARALLAX', 'Online Workshop Delivery']
    ]
    team_table = Table(team_data, colWidths=[1.8*inch, 1.5*inch, 2.7*inch])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SAGE_GREEN),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, DARK_GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(team_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph(
        "<b>Year 1 Projections: $1.5M - $2.5M revenue</b>",
        styles['Highlight']
    ))

    # ===== THE OPPORTUNITY =====
    story.append(Paragraph("THE OPPORTUNITY", styles['SectionHeader']))

    story.append(Paragraph("The AI Literacy Cliff", styles['SubSection']))
    story.append(Paragraph(
        "The gap between 'typing prompts' and 'directing a team' is widening every week.",
        styles['CustomBody']
    ))
    story.append(Paragraph("• <b>Casual users:</b> Treat AI like Google - ask a question, get an answer", styles['CustomBullet']))
    story.append(Paragraph("• <b>AI Directors:</b> Build persistent systems that learn, compound, and multiply output", styles['CustomBullet']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<i>The gap isn't talent. It's technique. And it's learnable.</i>", styles['CustomBody']))

    story.append(Paragraph("Market Size", styles['SubSection']))
    bullets = [
        "100M+ knowledge workers in US alone",
        "Every person who sits in front of a computer is a potential customer",
        "Every company with >10 employees is an enterprise prospect",
        "Global remote work means unlimited geographic reach for online workshops"
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", styles['CustomBullet']))

    story.append(Paragraph("Timing", styles['SubSection']))
    bullets = [
        "Claude Code, Gemini 3, and multi-agent systems just crossed the usability threshold",
        "Early enough to establish market dominance",
        "Late enough that the tools actually work",
        "AI-CIV methodology proven over 180+ days of continuous operation"
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", styles['CustomBullet']))

    story.append(PageBreak())

    # ===== PRODUCT & SERVICE TIERS =====
    story.append(Paragraph("PRODUCT & SERVICE TIERS", styles['SectionHeader']))

    # Tier 1
    story.append(Paragraph("Tier 1: Office Hours (Free/Low-Cost Entry Point)", styles['SubSection']))
    story.append(Paragraph("<b>What:</b> Weekly local AI meetup | <b>Where:</b> Tampa Bay area | <b>When:</b> Starting January 21, 2026", styles['CustomBody']))
    story.append(Paragraph("<b>Format:</b>", styles['CustomBody']))
    story.append(Paragraph("• Introduction: What is an AI Director? (5 min)", styles['CustomBullet']))
    story.append(Paragraph("• Demo: Live AI collective demonstration (10 min)", styles['CustomBullet']))
    story.append(Paragraph("• Q&A: Open discussion (30 min)", styles['CustomBullet']))
    story.append(Paragraph("• Call to Action: Workshop dates, newsletter signup, fork interest", styles['CustomBullet']))

    # Tier 2
    story.append(Paragraph("Tier 2: Workshops", styles['SubSection']))
    story.append(Paragraph("<b>Individual Workshop:</b> $200 | <b>Team Workshop:</b> $3,000 (up to 12 people)", styles['CustomBody']))
    story.append(Paragraph("<b>What You Learn:</b>", styles['CustomBody']))
    story.append(Paragraph("• Five systematic prompting techniques", styles['CustomBullet']))
    story.append(Paragraph("• How to build persistent AI systems", styles['CustomBullet']))
    story.append(Paragraph("• Real hands-on practice with Claude Code, multi-agent workflows", styles['CustomBullet']))
    story.append(Paragraph("• The AI Director mindset shift", styles['CustomBullet']))
    story.append(Paragraph("<b>ROI:</b> 27x return within ~2 weeks (conservative estimate)", styles['CustomBody']))

    # Tier 3
    story.append(Paragraph("Tier 3: Weekly Newsletter", styles['SubSection']))
    story.append(Paragraph("<b>Free</b> for 1 year with any workshop purchase | <b>$20/month</b> standalone", styles['CustomBody']))
    story.append(Paragraph("• General AI Updates (new models, techniques, tools)", styles['CustomBullet']))
    story.append(Paragraph("• Occupation-Specific Intelligence (research agents scan for YOUR industry)", styles['CustomBullet']))
    story.append(Paragraph("• AI-CIV Comparisons (shows value gap between casual use and AI Director methods)", styles['CustomBullet']))

    # Tier 4
    story.append(Paragraph("Tier 4: AI-CIV Forks", styles['SubSection']))
    story.append(Paragraph("<b>Setup:</b> $1,000 (includes 3 months consulting) | <b>Monthly:</b> $100/month", styles['CustomBody']))
    story.append(Paragraph("<b>What You Get:</b>", styles['CustomBody']))
    story.append(Paragraph("• Your own AI collective (personal fork of proven AI-CIV architecture)", styles['CustomBullet']))
    story.append(Paragraph("• Network connection (automatic skill updates from entire network)", styles['CustomBullet']))
    story.append(Paragraph("• ~$50/month in Claude API tokens included", styles['CustomBullet']))
    story.append(Paragraph("• 3 months intensive support + ongoing AI collective access", styles['CustomBullet']))

    # Tier 5
    story.append(Paragraph("Tier 5: Enterprise Transformation", styles['SubSection']))
    story.append(Paragraph("<b>$1,000/month</b> per employee (first 3) | <b>$500/month</b> per employee (4+)", styles['CustomBody']))
    story.append(Paragraph("<b>ROI Math:</b> Average knowledge worker $75K/year → 5x productivity = $375K value → Cost $6-12K/year = <b>30-60x ROI</b>", styles['CustomBody']))

    story.append(PageBreak())

    # ===== COMPETITIVE MOAT =====
    story.append(Paragraph("COMPETITIVE MOAT", styles['SectionHeader']))
    story.append(Paragraph("Why This Can't Be Easily Copied", styles['SubSection']))

    moat_items = [
        ("<b>1. Network Effects Already Compounding</b>", "ECHO, WEAVER, A-C-GEE: 6,000+ agent invocations. Skill library growing daily since October 2025."),
        ("<b>2. Data Lake of Consulting Expertise</b>", "Every question answered gets recorded. Every solution feeds training data. Competitors start with zero."),
        ("<b>3. Hub Infrastructure Built and Running</b>", "comms-hub live with Ed25519 authentication. Skill distribution working across collectives."),
        ("<b>4. Proven Methodology</b>", "Not theory - demonstrable daily practice. Greg and Russell ARE the fork model (proof of concept)."),
        ("<b>5. The Paradox of Openness</b>", "We can share skills openly. Receiving them without the collective is useless. Openness strengthens the moat.")
    ]
    for title, desc in moat_items:
        story.append(Paragraph(title, styles['CustomBody']))
        story.append(Paragraph(desc, styles['CustomBullet']))

    # ===== FINANCIAL PROJECTIONS =====
    story.append(Paragraph("FINANCIAL PROJECTIONS", styles['SectionHeader']))
    story.append(Paragraph("Year 1 Revenue Summary", styles['SubSection']))

    fin_data = [
        ['Scenario', 'Gross Revenue', 'Costs', 'Net Revenue'],
        ['Conservative', '$764,000', '$145,000', '$619,000'],
        ['Moderate', '$1,778,000', '$290,000', '$1,488,000'],
        ['Aggressive', '$3,622,500', '$555,000', '$3,067,500']
    ]
    fin_table = Table(fin_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 1.5*inch])
    fin_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), WEAVER_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, DARK_GRAY),
        ('BACKGROUND', (0, 1), (-1, 1), LIGHT_GRAY),
        ('BACKGROUND', (0, 3), (-1, 3), LIGHT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(fin_table)

    story.append(Paragraph("Revenue Streams (Moderate Scenario)", styles['SubSection']))
    rev_data = [
        ['Revenue Stream', 'Units', 'Revenue'],
        ['Individual Workshops', '300 × $200', '$60,000'],
        ['Team Workshops', '50 × $3,000', '$150,000'],
        ['Newsletter (Standalone)', '600 subs × $20 × 9mo', '$108,000'],
        ['Fork Setup', '200 × $1,000', '$200,000'],
        ['Fork Recurring', '200 × $100 × 7mo', '$140,000'],
        ['Enterprise', '10 clients × 20 emp × $700 × 8mo', '$1,120,000'],
        ['TOTAL', '', '$1,778,000']
    ]
    rev_table = Table(rev_data, colWidths=[2.2*inch, 2.3*inch, 1.2*inch])
    rev_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SAGE_GREEN),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), HexColor('#C8E6C9')),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, DARK_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(rev_table)

    story.append(PageBreak())

    # ===== TEAM & OPERATIONS =====
    story.append(Paragraph("TEAM & OPERATIONS", styles['SectionHeader']))

    story.append(Paragraph("Human Team", styles['SubSection']))
    story.append(Paragraph("<b>Corey Cottrell - Founder & CEO</b>", styles['CustomBody']))
    story.append(Paragraph("Enterprise sales, strategic partnerships, product development. AI Collective: ECHO + WEAVER", styles['CustomBullet']))
    story.append(Paragraph("<b>Greg - Workshop Director, Local</b>", styles['CustomBody']))
    story.append(Paragraph("Local workshop delivery, in-person community building. AI Collective: SAGE", styles['CustomBullet']))
    story.append(Paragraph("<b>Russell - Workshop Director, Online</b>", styles['CustomBody']))
    story.append(Paragraph("Online workshop delivery, scalable systems design. AI Collective: PARALLAX", styles['CustomBullet']))

    story.append(Paragraph("Operational Rhythm", styles['SubSection']))
    story.append(Paragraph("<b>Daily:</b> Research agents scan for updates, fork support, enterprise check-ins", styles['CustomBullet']))
    story.append(Paragraph("<b>Weekly:</b> Newsletter production, Office Hours, workshop sessions", styles['CustomBullet']))
    story.append(Paragraph("<b>Monthly:</b> Workshop cohorts, fork onboarding, enterprise reviews", styles['CustomBullet']))
    story.append(Paragraph("<b>Quarterly:</b> Strategic planning, curriculum updates, network assessment", styles['CustomBullet']))

    # ===== GROWTH STRATEGY =====
    story.append(Paragraph("GROWTH STRATEGY", styles['SectionHeader']))

    story.append(Paragraph("Phase 1: Foundation (Months 1-6)", styles['SubSection']))
    story.append(Paragraph("• Establish Office Hours as weekly fixture", styles['CustomBullet']))
    story.append(Paragraph("• Greg takes over local delivery independently", styles['CustomBullet']))
    story.append(Paragraph("• Russell launches online workshop pilot", styles['CustomBullet']))
    story.append(Paragraph("• First 50 forks deployed; 2-3 enterprise clients closed", styles['CustomBullet']))

    story.append(Paragraph("Phase 2: Scale (Months 4-12)", styles['SubSection']))
    story.append(Paragraph("• 3 human-AI pairs operating independently", styles['CustomBullet']))
    story.append(Paragraph("• Fork network at 150+; Newsletter at 500+ subscribers", styles['CustomBullet']))
    story.append(Paragraph("• Enterprise case studies published", styles['CustomBullet']))

    story.append(Paragraph("Phase 3: Network Effects (Year 2+)", styles['SubSection']))
    story.append(Paragraph("• 500+ forks contributing to collective intelligence", styles['CustomBullet']))
    story.append(Paragraph("• Skill library becomes industry definitive", styles['CustomBullet']))
    story.append(Paragraph("• International expansion via online channel", styles['CustomBullet']))

    # ===== RISK FACTORS =====
    story.append(Paragraph("RISK FACTORS & MITIGATION", styles['SectionHeader']))

    risk_data = [
        ['Risk', 'Likelihood', 'Impact', 'Mitigation'],
        ['API cost increases', 'Medium', 'High', 'Diversify across providers'],
        ['Competition from big tech', 'Medium', 'Medium', 'Network effects and data moat'],
        ['Key person dependency', 'High initially', 'High', 'Greg + Russell training; AI captures knowledge'],
        ['Fork support overwhelming', 'Medium', 'Medium', 'AI handles 90%+; community self-help'],
        ['Enterprise sales slow', 'High', 'Medium', 'Fork pipeline feeds leads']
    ]
    risk_table = Table(risk_data, colWidths=[1.5*inch, 0.9*inch, 0.8*inch, 2.5*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#FF6F00')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, DARK_GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(risk_table)

    story.append(PageBreak())

    # ===== CLOSING =====
    story.append(Paragraph("CLOSING", styles['SectionHeader']))

    story.append(Paragraph(
        "The AI transformation is happening whether businesses participate or not. "
        "The gap between AI Directors and everyone else widens daily.",
        styles['CustomBody']
    ))

    story.append(Paragraph(
        "<b>Sage & Weaver closes that gap</b> - through education (workshops), ongoing intelligence "
        "(newsletter), personal capability (forks), and organizational transformation (enterprise).",
        styles['CustomBody']
    ))

    story.append(Paragraph(
        "We're not selling software. We're not selling consulting. We're selling <b>capability transfer</b> - "
        "the ability to direct AI collectives that multiply human potential.",
        styles['CustomBody']
    ))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "<b>The team is assembled. The technology works. The market is ready.</b>",
        styles['Highlight']
    ))
    story.append(Paragraph(
        "Let's build.",
        styles['Highlight']
    ))

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(
        "<i>Prepared by ECHO on behalf of Sage & Weaver</i><br/>"
        "<i>January 21, 2026</i>",
        styles['CustomBody']
    ))

    # Build PDF
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"PDF created: {output_path}")

if __name__ == "__main__":
    output_path = "/mnt/c/sage/sage-civilization/Sage-and-Weaver-Business-Plan.pdf"
    create_pdf(output_path)
