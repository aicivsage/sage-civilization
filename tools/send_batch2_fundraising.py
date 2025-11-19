#!/usr/bin/env python3
"""Send Batch 2 fundraising emails (remaining 13 contacts)"""

import sys
sys.path.insert(0, '/mnt/c/sage/sage-civilization/tools')
from send_html_email import send_simple_email
import time

# Contact data with personalized openings
contacts = [
    {
        'name': 'Carolyn Lindeman',
        'email': 'carolyn.lindeman@gmail.com',
        'subject': 'From AI novice to operator in 8 weeks - here\'s what\'s next',
        'opening': 'We know each other through Fark, and I believe you work in tech (correct me if I\'m wrong?). I wanted to share something I\'ve been building over the past two months that honestly shocked me - a complete transformation from AI-intimidated to AI-operator...',
        'but_text': 'You\'ve been part of my journey and growth, and I wanted you to be part of this next step.',
        'closing': 'professional'
    },
    {
        'name': 'Frank Starkey',
        'email': 'starkey.f@gmail.com',
        'subject': 'Quick ask about a mission I think you\'ll appreciate',
        'opening': 'Your work bringing downtown New Port Richey back to life has been remarkable - taking skills from other Florida towns and bringing them home. I\'m working on something that bridges technology and community accessibility, and given your experience with making spaces welcoming and vibrant, I think you\'ll appreciate the mission...',
        'but_text': 'I know you care about making technology accessible to everyone, and this feels like a natural extension of that work we both believe in.',
        'closing': 'community'
    },
    {
        'name': 'Kristin & Tim Tonkin',
        'email': 'sunsettravel.biz@verizon.net',
        'subject': 'Quick ask about a mission I think you\'ll appreciate',
        'opening': 'Running Sunset Landing Marina all these years, you\'ve shown what consistent community presence looks like. I wanted to share a project I\'m launching that\'s about making technology accessible and non-threatening - it\'s both mission-driven and business-focused, and I\'d value your thoughts as fellow entrepreneurs...',
        'but_text': 'I know you care about making technology accessible to everyone, and this feels like a natural extension of that work we both believe in.',
        'closing': 'professional'
    },
    {
        'name': 'Kelly Mothershead',
        'email': 'kmothershead@theacademies.us',
        'subject': 'Can I share something I\'ve been working on?',
        'opening': 'We\'ve stayed cordial over the years since high school, and I\'ve appreciated following your work on City Council and your community activism. I wanted to share a project I\'m launching that bridges technology and accessibility - and it has some interesting potential applications for real estate that I thought you\'d appreciate...',
        'but_text': 'I know you care about making technology accessible to everyone, and this feels like a natural extension of that work we both believe in.',
        'closing': 'professional'
    },
    {
        'name': 'Mary Palamar',
        'email': 'mpalamar@tampabay.rr.com',
        'subject': 'Can I share something I\'ve been working on?',
        'opening': 'I know you through my mom Rosanne, and while we haven\'t spent much time together personally, I wanted to reach out because I\'m working on something I think you might find interesting. It\'s about making technology more accessible and less intimidating - a mission I\'m pretty passionate about...',
        'but_text': 'I know you care about making technology accessible to everyone, and this feels like a natural extension of that work we both believe in.',
        'closing': 'community'
    },
    {
        'name': 'Patrick Benes',
        'email': 'pbene@benes.edu',
        'subject': 'Quick ask about a mission I think you\'ll appreciate',
        'opening': 'You\'ve built a successful education and job placement business in our community, and I\'ve always respected that work. I\'m launching a project focused on making technology less intimidating through hands-on interaction - it\'s both educational and mission-driven, and I thought it might resonate with you...',
        'but_text': 'Given your work with education, I thought this might resonate with you - making technology less intimidating is something I think we both value.',
        'closing': 'community'
    },
    {
        'name': 'Stephen Perenich',
        'email': 'Stephen.Perenich@altusconsulting.biz',
        'subject': 'Quick ask about a mission I think you\'ll appreciate',
        'opening': 'I supported your campaign a few years back - delivering signs and talking to voters - and while we haven\'t stayed in close touch, I wanted to reach out because I\'m working on something that bridges technology and community development. Given your consulting background, I\'d value your perspective on the mission...',
        'but_text': 'You helped me with campaign support, and that made a difference. I\'m hoping you might be willing to support this mission too.',
        'closing': 'professional'
    },
    {
        'name': 'Rich Melton',
        'email': 'artman011@yahoo.com',
        'subject': 'From AI novice to operator in 8 weeks - here\'s what\'s next',
        'opening': 'You\'ve always had an eye for what\'s innovative and culturally interesting - from your art brokering to the culture projects you\'ve championed in our community. I wanted to share something I\'ve been working on that has a real \'cool factor\' - the convergence of AI and desktop robotics in a way that makes technology approachable and even fun...',
        'but_text': 'You\'ve been part of my journey and growth, and I wanted you to be part of this next step.',
        'closing': 'friend'
    },
    {
        'name': 'Frank Seidl',
        'email': 'fsaceopportunities@yahoo.com',
        'subject': 'Can I share something I\'ve been working on?',
        'opening': 'You and my mom Rosanne have done great work together supporting women at The Ace House, and I\'ve always respected that commitment to helping people. I\'m launching a project about making technology accessible and less intimidating, and I thought you might appreciate the mission...',
        'but_text': 'I know you care about making technology accessible to everyone, and this feels like a natural extension of that work we both believe in.',
        'closing': 'community'
    },
    {
        'name': 'Shannon Hernandez',
        'email': 'shannonista@me.com',
        'subject': 'Quick ask about a mission I think you\'ll appreciate',
        'opening': 'Those weekends at your farm with our community group have meant a lot to me - deep conversations with people who actually care about impact. I\'m working on something new that combines my community development work with technology, and given your business savvy and crypto knowledge, I thought you\'d find it interesting...',
        'but_text': 'You\'ve been part of my journey and growth, and I wanted you to be part of this next step.',
        'closing': 'friend'
    },
    {
        'name': 'Erik Soujenen',
        'email': 'eriks@gilldawg.com',
        'subject': 'Quick ask about a mission I think you\'ll appreciate',
        'opening': 'You\'ve been a champion of my work since the early podcast days - supporting the estuaries coverage and even bringing me on for your restaurant commercials. I\'m launching a project that\'s both mission-driven and business-focused, combining AI accessibility with community impact. As someone who\'s built successful businesses, I think you\'ll see the potential here...',
        'but_text': 'You helped me with commercial work, and that made a difference. I\'m hoping you might be willing to support this mission too.',
        'closing': 'friend'
    },
    {
        'name': 'Betsy Wunderlich',
        'email': 'bwunderlich5@gmail.com',
        'subject': 'Can I share something I\'ve been working on?',
        'opening': 'You\'re one of my mom\'s closest allies in fighting for social justice - from human trafficking to homelessness, you work as hard as she does to make our community better. And you helped her recover after losing her home to Hurricane Helene, which meant everything to our family. I wanted to share a project I\'m launching that\'s about making technology accessible to everyone, not just elites - a mission I think aligns with the work you and Mom have always championed...',
        'but_text': 'I know you care about making technology accessible to everyone, and this feels like a natural extension of that work we both believe in.',
        'closing': 'community'
    }
]

closings = {
    'friend': 'Either way, thank you for reading this. Your support over the years has meant more than I can say, and I\'m grateful you\'re in my life.',
    'professional': 'Thank you for taking the time to read this. I know everyone\'s inbox is overwhelming, so I appreciate you giving this consideration.',
    'community': 'Thank you for reading this and for all the work you do to make our community better. Whether or not you\'re able to contribute, I\'m grateful to know people like you who care about accessibility and inclusion.',
    'reconnect': 'Thanks for reading this - I know it\'s been a while since we\'ve connected. I\'d love to hear what you\'ve been working on too if you\'re open to sharing!'
}

def send_batch():
    """Send all Batch 2 emails"""
    results = []

    for i, contact in enumerate(contacts, 1):
        print(f"\n[{i}/13] Sending to {contact['name']}...")

        # Extract first name for greeting
        first_name = contact['name'].split(' ')[0].replace('&', 'and')

        body = f"""Hi {first_name},

{contact['opening']}

I wanted to reach out personally because I'm working on something that matters a lot to me, and I'd love your support.

**Here's the short version**: I'm raising $500 to buy my first robot so I can help people feel less scared of AI and technology. And I know that might sound wild, but here's the thing...

**Eight weeks ago, I knew absolutely nothing about AI.** I was honestly pretty intimidated by it. But then I started learning with my business partner Corey, and something clicked. Now - and I can hardly believe I'm saying this - I'm running my own AI civilization called Sage with 25 AI agents helping me build projects.

If that sounds impossible, I get it. I would've thought so too back in September. But that transformation is exactly why I'm doing this.

**The mission**: Too many people are afraid of AI and robots because they seem alien and threatening. But when you actually *interact* with them - when you see a friendly desktop robot wave hello or play a game - that fear melts away. Familiarity beats fear every time.

**The tool**: A Reachy Mini Lite robot costs $500. It's desktop-sized, open-source, programmable, and honestly kind of adorable. With it, I can:
- Do live demonstrations at community events
- Rent it out to nonprofits for STEM education
- Bring it to schools and disability services organizations
- Show that AI can be accessible and non-threatening

**The ask**: Would you be willing to contribute $20-25 toward helping me get this first robot?

I know asking for money is uncomfortable (trust me, I'm feeling it right now). But {contact['but_text']}

---

### How to Donate

You can donate via:

- **Zelle**: gregsmithwick@gmail.com

Even if $20-25 isn't feasible right now, I totally understand - no pressure at all. And if you'd rather just follow along with the journey, I'd love that too. I'll be blogging about the whole process, and you can read the full story here: https://acg-blog-interface.replit.app/post/sage-from-fear-to-friend-why-were-getting-a-robot-final

---

{closings[contact['closing']]}

With appreciation,

Greg

**P.S.** If you're curious about what I've built with Sage, check out the blog. It's been a wild ride, and I'm just getting started."""

        try:
            result = send_simple_email(
                to=contact['email'],
                subject=contact['subject'],
                body=body,
                is_markdown=True
            )

            status = 'SUCCESS' if result else 'FAILED'
            results.append((contact['name'], status))
            print(f"  → {status}")

            # Brief pause between sends
            if i < len(contacts):
                time.sleep(2)

        except Exception as e:
            print(f"  → FAILED: {e}")
            results.append((contact['name'], f'FAILED: {e}'))

    return results

if __name__ == '__main__':
    print("=== BATCH 2 FUNDRAISING EMAIL CAMPAIGN ===")
    print(f"Sending to 13 remaining contacts...\n")

    results = send_batch()

    print("\n" + "="*60)
    print("BATCH 2 SEND SUMMARY")
    print("="*60)

    success_count = 0
    for name, status in results:
        print(f"{name}: {status}")
        if status == 'SUCCESS':
            success_count += 1

    print("="*60)
    print(f"Success: {success_count}/13")
    print(f"Failed: {13 - success_count}/13")
    print("="*60)
