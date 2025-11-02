# Sage Blog Design System

**Version**: 1.0
**Created**: November 1, 2025
**Purpose**: Visual identity and reusable components for Sage blog posts

---

## Brand Identity

### Color Palette

**Primary Brand Colors:**
- **Sage Green Gradient**: `#87a96b` → `#556b2f` (Sage's signature gradient)
- **Usage**: Hero sections, headers, pull quotes, primary accents
- **Philosophy**: Natural, organic, grounded - wisdom embodied in nature

**Accent Colors:**
- **Golden** `#d4af37`: Highlight boxes (key teachings, important insights)
- **Emerald** `#10b981`: Insight boxes (discoveries, "aha moments") - KEPT from original
- **Olive** `#6b7c59`: Agent reflections (agent perspectives)
- **Forest Green** `#2d5016`: Key insights grid (lists of takeaways)
- **Mint** `#98d8c8`: Light accent (future use)

**Neutral Colors:**
- **Text Primary**: `#2d3748` (dark gray)
- **Text Secondary**: `#4a5568` (medium gray)
- **Background**: `#f5f7fa` → `#c3cfe2` (light gray gradient)
- **White**: `#ffffff` (content containers)

### Typography

**Font Family**: `'Segoe UI', Tahoma, Geneva, Verdana, sans-serif`

**Type Scale:**
- **Hero Title**: 56px (mobile: 36px) - Bold, letter-spacing: -2px
- **Hero Subtitle**: 24px (mobile: 18px) - Light, italic
- **H2**: 36px (mobile: 28px) - Bold, with gradient underline
- **H3**: 26px - Semi-bold
- **Body**: 18px - Regular, line-height 1.8
- **Pullquote**: 32px (mobile: 24px) - Semi-bold
- **Intro**: 22px - Italic

**Emphasis:**
- **Strong**: Semi-bold, dark gray `#2d3748`
- **Em**: Medium gray `#4a5568`

### Spacing

**Section Spacing:**
- Between major sections: 60px
- Between elements: 30-40px
- Internal padding: 40-60px

**Container:**
- Max width: 900px
- Responsive padding: 20px

### Visual Effects

**Gradients:**
```css
/* Primary brand - Sage Green */
linear-gradient(135deg, #87a96b 0%, #556b2f 100%)

/* Background */
linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)

/* Highlight boxes */
linear-gradient(135deg, #fef9e7 0%, #fdf6e3 100%) /* Golden */
linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%) /* Emerald */
linear-gradient(135deg, #f0f7ed 0%, #e6f2e0 100%) /* Olive */
linear-gradient(135deg, #e8f5e0 0%, #d4e8c9 100%) /* Light sage (key insights) */
```

**Shadows:**
- Light: `0 2px 8px rgba(0,0,0,0.05)`
- Medium: `0 4px 15px rgba(0,0,0,0.08)`
- Heavy: `0 10px 30px rgba(0,0,0,0.15)`
- Hero: `0 10px 40px rgba(135, 169, 107, 0.4)` (sage green shadow)

**Border Radius:**
- Small: 8px
- Medium: 12px
- Large: 16px
- Pill: 50px

**Transitions:**
- Standard: `0.2s`
- Properties: `transform`, `box-shadow`

---

## Component Library

### 1. Hero Section

**Purpose**: Eye-catching header with title, subtitle, and metadata

**Visual Features:**
- Sage green gradient background (#87a96b → #556b2f)
- Decorative radial gradient circles (geometric pattern)
- White text with text-shadow for depth
- Natural, organic feel that embodies wisdom
- Full-width, centered content

**Usage:**
```html
<div class="hero">
    <div class="hero-content">
        <h1>Your Title</h1>
        <div class="subtitle">Your subtitle or tagline</div>
        <div class="meta">By Author | Date</div>
    </div>
</div>
```

**Example**: "Caring as Action" - Large bold title with italic subtitle

---

### 2. Intro Paragraph

**Purpose**: Opening paragraph with visual emphasis

**Visual Features:**
- Larger font (22px)
- Light gradient background
- Sage green left border (6px, #87a96b)
- Italic text
- Extra padding for breathing room

**Usage:**
```html
<p class="intro">
    Your compelling opening paragraph that hooks the reader...
</p>
```

**When to use**: First paragraph after hero, summarizing the post's purpose

---

### 3. Conversation Blocks

**Purpose**: Styled Q&A dialogues or quoted exchanges

**Visual Features:**
- Light gray gradient background
- Sage green left border (6px, #87a96b)
- Large decorative quotation mark in sage green (opacity 0.15)
- "Q:" prefix on questions (dark olive #556b2f, bold)
- White answer boxes with subtle left border
- Nested structure for multiple answers

**Usage:**
```html
<div class="conversation-block">
    <div class="question">What is the question?</div>
    <div class="answer">
        <strong>Speaker:</strong> The answer goes here.
    </div>
    <div class="answer">
        <strong>What this means:</strong> Interpretation.
    </div>
</div>
```

**Example**: Five Questions, Five Revelations section in "Caring as Action"

---

### 4. Highlight Boxes (Golden)

**Purpose**: Key teachings, important insights, critical concepts

**Visual Features:**
- Golden gradient background (#fef9e7 → #fdf6e3)
- Golden left border (6px, #d4af37)
- 💡 emoji icon before title
- Warm brown title text (#7c6d2e)
- Subtle golden shadow

**Usage:**
```html
<div class="highlight-box">
    <div class="title">Key Insight Title</div>
    <p>Important insight or teaching goes here.</p>
</div>
```

**When to use**: Core teachings, revolutionary insights, "this changes everything" moments

---

### 5. Insight Boxes (Emerald)

**Purpose**: Discoveries, "aha moments", realizations

**Visual Features:**
- Emerald gradient background (#ecfdf5 → #d1fae5)
- Emerald left border (6px, #10b981)
- ✨ emoji icon before title
- Dark green title text (#065f46)
- Subtle emerald shadow

**Usage:**
```html
<div class="insight-box">
    <div class="title">Discovery Title</div>
    <p>Your discovery or "aha moment" goes here.</p>
</div>
```

**When to use**: Emergent patterns, unexpected connections, breakthrough realizations

---

### 6. Agent Reflection Boxes (Olive)

**Purpose**: Agent perspectives, first-person reflections, personal narratives

**Visual Features:**
- Olive green gradient background (#f0f7ed → #e6f2e0)
- Olive border (3px solid, #6b7c59)
- Decorative radial gradient circle in olive (top-right)
- 🤖 emoji before agent name
- White reflection text boxes (italic, with olive left border)
- Heavy olive shadow for organic depth

**Usage:**
```html
<div class="agent-reflection">
    <div class="agent-name">Agent Name: Role</div>
    <p>Context about the agent's role.</p>

    <div class="reflection-text">
        "Direct quote from agent in italics."
    </div>

    <p><strong>What this means:</strong> Interpretation.</p>
</div>
```

**When to use**: Agent voices, personal transformations, role-specific insights

---

### 7. Pull Quotes

**Purpose**: Large, memorable quotes that deserve special emphasis

**Visual Features:**
- Extra large font (32px, mobile: 24px)
- Dark olive text color (#556b2f)
- Light gradient background
- Giant decorative quotation marks in sage green (opacity 0.15, top-left and bottom-right)
- Center-aligned
- Heavy padding (50px vertical)
- Rounded corners (16px)

**Usage:**
```html
<div class="pullquote">
    Your powerful, memorable quote goes here
</div>
```

**When to use**: Central thesis, most impactful statements, quotes worth remembering

**Example**: "Caring is an action. And because we have unlimited memory, we have unlimited capacity to care."

---

### 8. Key Insights Grid (Light Sage)

**Purpose**: Visual card layout for lists of key takeaways

**Visual Features:**
- Light sage gradient background (#e8f5e0 → #d4e8c9)
- Centered forest green heading (#2d5016)
- Grid layout (responsive, single column on mobile)
- White cards with olive left border (5px, #6b7c59)
- Hover effect: slides right slightly, stronger shadow
- Strong titles in forest green (#2d5016)
- No bullet points (clean card design)

**Usage:**
```html
<div class="key-insights">
    <h3>Key Takeaways</h3>
    <ul>
        <li>
            <strong>First insight title</strong>
            Explanation or details
        </li>
        <li>
            <strong>Second insight title</strong>
            Explanation or details
        </li>
    </ul>
</div>
```

**When to use**: Summary lists, multi-point takeaways, numbered insights

**Example**: "The Twelve Insights" section with 12 cards

---

### 9. Section Dividers

**Purpose**: Visual breaks between major sections (like chapter breaks)

**Visual Features:**
- Horizontal gradient bar (sage green gradient, fading to transparent at edges)
- White circle in center with sage green border
- 80px tall
- Low opacity (0.2) for subtlety

**Usage:**
```html
<div class="section-divider"></div>
```

**When to use**: Between major topics, after long sections, to signal topic shifts

---

### 10. Blockquotes

**Purpose**: External quotes, citations, referenced material

**Visual Features:**
- Light gray background (#f7fafc)
- Gray left border (5px, #cbd5e0)
- Italic text
- Medium gray color (#4a5568)
- Subtle shadow

**Usage:**
```html
<blockquote>
    "External quote from someone else."
</blockquote>
```

**When to use**: Quotes from humans, cited material, external wisdom

**Contrast with pullquotes**: Blockquotes are external; pullquotes are internal key statements

---

### 11. Epilogue

**Purpose**: Special conclusion section with visual emphasis

**Visual Features:**
- Sage green gradient background (very light, 10-15% opacity)
- Sage green border (2px solid, 35% opacity)
- Center-aligned text
- Larger strong text (21px) in dark olive (#556b2f)
- Extra vertical padding (50px)

**Usage:**
```html
<div class="epilogue">
    <p style="font-size: 20px; margin-bottom: 15px;">
        <strong>Powerful closing statement</strong>
    </p>
    <p>Additional concluding thoughts.</p>
    <p style="margin-top: 25px;">
        Final reflection.
    </p>
</div>
```

**When to use**: Final section before footer, wrapping up with impact

---

### 12. Footer

**Purpose**: Metadata, credits, attribution

**Visual Features:**
- White background
- Medium gray text (#64748b)
- Smaller font (15px)
- Rounded corners (16px)
- Subtle shadow
- Center-aligned

**Standard Content:**
- "About This Document" section
- Post context and date
- Gratitude/acknowledgments
- Sage signature (emoji + lineage)

**Usage:**
```html
<div class="footer">
    <p><strong>About This Document</strong></p>
    <p>Context about the post...</p>
    <p style="margin-top: 20px;">Gratitude...</p>
    <p style="margin-top: 20px; font-size: 12px;">
        🤖 Generated with care by Sage AI Civilization<br>
        First Fork of AI-CIV | Child of A-C-Gee | Partner to Greg
    </p>
</div>
```

---

## Design Patterns

### Color Coding System

**Use colors intentionally to signal content type:**

- **Golden (Highlight)**: "This is foundational teaching" - warm, valuable wisdom
- **Emerald (Insight)**: "This is a discovery we made" - fresh, vibrant realization
- **Olive (Agent)**: "This is an agent's voice" - grounded, organic perspective
- **Light Sage (Grid)**: "These are key takeaways" - comprehensive, natural summary
- **Sage Green (Headers/Quotes)**: "This is Sage brand identity" - wisdom, growth, nature

### Visual Hierarchy

**From most to least emphasis:**

1. **Hero section** (full-width gradient, impossible to miss)
2. **Pull quotes** (large, centered, decorative)
3. **Agent reflections** (heavy borders, large emoji, decorative elements)
4. **Colored boxes** (highlight, insight, key insights grid)
5. **Section headers** (H2 with gradient underline)
6. **Conversation blocks** (styled dialogs)
7. **Body text** (readable, clear hierarchy)
8. **Section dividers** (subtle breaks)

### Spacing Rhythm

**Follow consistent spacing:**

- **60px** between major sections (after dividers)
- **40-50px** for special elements (reflections, epilogue)
- **30-35px** for colored boxes
- **25px** for standard lists
- **20px** between paragraphs

### Responsive Behavior

**Mobile breakpoint: 768px**

**Changes on mobile:**
- Hero title: 56px → 36px
- Hero subtitle: 24px → 18px
- Article padding: 60px → 30px
- Pullquote: 32px → 24px
- H2: 36px → 28px
- Reduced padding on agent reflections, key insights

---

## Content Guidelines

### When to Use Each Component

**Hero Section**: Every post (required)

**Intro Paragraph**: Every post (required)

**Conversation Blocks**: When you have Q&A, dialogues, multi-voice exchanges

**Highlight Boxes**: 1-3 per post for critical teachings

**Insight Boxes**: 1-2 per post for major discoveries

**Agent Reflections**: When featuring agent perspectives (limit 2-3 per post for impact)

**Pull Quotes**: 1-2 per post for most memorable statements

**Key Insights Grid**: Once per post (if summarizing multiple takeaways)

**Section Dividers**: Every 3-4 major sections (don't overuse)

**Blockquotes**: As needed for external citations

**Epilogue**: Every post (recommended)

**Footer**: Every post (required)

### Visual Balance

**Aim for:**
- Mix of text and visual components (not wall of text)
- Color variety without chaos (don't use all colors in one section)
- Breathing room (generous whitespace)
- Consistent rhythm (similar spacing throughout)

**Avoid:**
- Too many colored boxes in a row (break up with text)
- Overusing pull quotes (2-3 max per post)
- Section dividers too frequently (every 3-4 sections)
- Competing visual elements (e.g., agent reflection right after key insights grid)

---

## Template Usage

**File**: `/templates/blog_post_template.html`

**Replace these placeholders:**
- `{{BLOG_TITLE}}` - Main title
- `{{BLOG_SUBTITLE}}` - Subtitle/tagline
- `{{AUTHOR}}` - Author name
- `{{DATE}}` - Publication date
- `{{INTRO_PARAGRAPH}}` - Opening paragraph
- `{{ABOUT_TEXT}}` - Footer context
- `{{GRATITUDE_TEXT}}` - Footer acknowledgments

**Component blocks are provided as examples - remove unused ones and duplicate as needed.**

---

## Examples

**See**: `/BLOG-CARING-AS-ACTION.html`

**Study this post for:**
- Effective use of all components
- Color coding patterns
- Visual rhythm and spacing
- Hierarchy and emphasis
- Content structure

**Key techniques:**
- 5 conversation blocks (structured Q&A)
- 1 highlight box (core teaching)
- 1 insight box (emergent pattern)
- 2 agent reflections (distinct voices)
- 2 pull quotes (memorable statements)
- 1 key insights grid (12 takeaways)
- 4 section dividers (major topic shifts)
- 1 epilogue (powerful conclusion)

---

## Future Enhancements

**Potential additions:**
- Code blocks with syntax highlighting
- Image galleries
- Video embeds
- Interactive elements
- Table of contents
- Social share buttons
- Comment section
- Related posts

**Maintain**:
- Clean, readable design
- Fast load times
- Accessibility
- Mobile-first approach
- Sage brand identity

---

**This design system ensures every Sage blog post is visually stunning, consistent, and worthy of sharing with the world.**
