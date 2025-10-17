# Example Memory Search Commands

This document demonstrates the grep-based search strategy for the HCAMS memory system.

---

## Scenario 1: Agent Starting New PostgreSQL Task

**Task:** "Implement database migrations for PostgreSQL using Alembic"

**Agent:** Coder

### Tier 1: Quick Recent Context Search (< 1 second)

```bash
grep 'postgresql\|database\|migration\|alembic' memories/agents/coder/context/recent_context.jsonl
```

**Expected Output:**
```jsonl
{"timestamp":"2025-09-28T15:00:00Z","task_id":"impl-025","context":"Implemented database models using SQLAlchemy for PostgreSQL","tags":["postgresql","sqlalchemy","database","models"],"key_findings":["AsyncSession required for FastAPI","declarative_base for models"]}
```

**Analysis:** Coder has recent PostgreSQL experience with SQLAlchemy, good context for Alembic (which is SQLAlchemy's migration tool).

### Tier 2: Check for Patterns (1-2 seconds)

```bash
# This would be done with Read tool
Read memories/agents/coder/context/patterns.json
# Filter in memory for tags: ["database", "migration", "sqlalchemy"]
```

**Expected Output:**
```json
{
  "pattern_id": "sqlalchemy-model-pattern",
  "name": "SQLAlchemy Async Model Pattern",
  "category": "code-template",
  "description": "Standard pattern for defining async SQLAlchemy models",
  "tags": ["sqlalchemy", "postgresql", "async", "database"]
}
```

**Analysis:** Has SQLAlchemy pattern but no Alembic pattern yet - this task will create one.

### Tier 4: Cross-Agent Search (10 seconds)

```bash
grep 'alembic\|migration' memories/agents/*/context/recent_context.jsonl
```

**Expected Output:**
```
memories/agents/architect/context/recent_context.jsonl:{"timestamp":"2025-10-01T10:00:00Z","task_id":"design-012","context":"Designed database schema migration strategy using Alembic - recommended for SQLAlchemy projects","tags":["alembic","migration","database","architecture"],"key_findings":["Alembic is SQLAlchemy's official migration tool","Supports auto-generate from models","Version control for schema"]}
```

**Analysis:** Architect researched Alembic! Coder should read that task for context.

```bash
Read memories/agents/architect/tasks/design-012.json
```

**Result:** Gets Architect's research on Alembic best practices, recommended commands, etc.

---

## Scenario 2: Finding Past FastAPI Work

**Task:** "Add rate limiting to FastAPI endpoints"

**Agent:** Coder

### Search Recent Work on FastAPI

```bash
grep 'fastapi' memories/agents/coder/context/recent_context.jsonl | tail -5
```

**Expected Output (last 5 FastAPI-related tasks):**
```jsonl
{"timestamp":"2025-09-22T10:00:00Z","task_id":"impl-018","context":"Implemented FastAPI JWT authentication middleware","tags":["fastapi","jwt","auth","middleware"],"key_findings":["Dependency injection for auth","OAuth2PasswordBearer pattern"]}
{"timestamp":"2025-09-25T14:00:00Z","task_id":"impl-021","context":"Created FastAPI CRUD endpoints for tasks resource","tags":["fastapi","crud","rest","api"],"key_findings":["APIRouter for modularity","Pydantic for validation"]}
{"timestamp":"2025-09-28T11:00:00Z","task_id":"impl-024","context":"Implemented FastAPI error handling with RFC 9457 format","tags":["fastapi","error-handling","rfc-9457"],"key_findings":["Custom exception handlers","JSONResponse for errors"]}
{"timestamp":"2025-09-30T16:00:00Z","task_id":"impl-027","context":"Added FastAPI dependency injection for database sessions","tags":["fastapi","database","dependency-injection","sqlalchemy"],"key_findings":["Depends() for DI","Yield for cleanup"]}
{"timestamp":"2025-10-01T13:00:00Z","task_id":"impl-029","context":"Implemented FastAPI async endpoints with proper typing","tags":["fastapi","async","typing","endpoints"],"key_findings":["async def for async operations","Type hints for OpenAPI"]}
```

**Analysis:** Lots of FastAPI experience! Specifically has middleware experience (impl-018) which is relevant for rate limiting.

### Read Detailed Middleware Task

```bash
Read memories/agents/coder/tasks/impl-018.json
```

**Expected Key Finding:**
```json
{
  "learnings": {
    "reusable_patterns": [
      "Pattern: FastAPI middleware - use @app.middleware('http') decorator or Starlette BaseHTTPMiddleware",
      "Pattern: Access request/response in middleware for cross-cutting concerns"
    ]
  }
}
```

**Result:** Knows how to add middleware, can apply to rate limiting.

---

## Scenario 3: Finding Patterns by Tag

**Task:** "Implement CRUD endpoints for new 'comments' resource"

**Agent:** Coder

### Search Patterns for CRUD

```bash
Read memories/agents/coder/context/patterns.json
# Filter by tags: ["crud"]
```

**Expected Pattern:**
```json
{
  "pattern_id": "fastapi-crud-endpoint",
  "name": "FastAPI CRUD Endpoint Template",
  "category": "code-template",
  "description": "Standard pattern for implementing CRUD endpoints in FastAPI",
  "when_to_use": "Creating new REST API resource with CRUD operations",
  "how_to_use": [
    "1. Define Pydantic schemas (CommentCreate, CommentUpdate, CommentResponse)",
    "2. Create APIRouter with prefix and tags",
    "3. Implement async handlers: create (POST), read (GET), update (PUT/PATCH), delete (DELETE)",
    "4. Add proper error handling (404 for not found, 422 for validation)",
    "5. Include OpenAPI documentation via docstrings"
  ],
  "examples": ["impl-021", "impl-023", "impl-026"],
  "success_rate": 0.95,
  "tags": ["fastapi", "api", "crud", "rest", "pattern"]
}
```

**Result:** Has reusable CRUD pattern! Can follow template for comments resource. Can also read example tasks (impl-021, impl-023, impl-026) for reference.

---

## Scenario 4: Finding Similar Past Tasks

**Task:** "Research GraphQL vs REST for API design"

**Agent:** Researcher

### Search Task Index by Type and Tags

```bash
Read memories/agents/researcher/tasks/index.json
```

**Index Structure:**
```json
{
  "tasks": [
    {
      "task_id": "research-039",
      "timestamp": "2025-09-25T16:45:00Z",
      "type": "research",
      "status": "completed",
      "tags": ["rest", "api", "versioning", "best-practices"],
      "summary": "REST API versioning strategies"
    },
    {
      "task_id": "research-042",
      "timestamp": "2025-10-01T18:30:00Z",
      "type": "research",
      "status": "completed",
      "tags": ["rest", "api", "best-practices", "pagination", "error-handling"],
      "summary": "REST API best practices 2025"
    }
  ]
}
```

**Filter in memory:** type="research" AND "api" in tags

**Found:** research-039, research-042 - both about REST APIs

```bash
Read memories/agents/researcher/tasks/research-042.json
```

**Extract Methodology:**
```json
{
  "execution": {
    "approach": "Following domain knowledge best practices: 1) Search for 2024-2025 authoritative sources, 2) Cross-reference minimum 3 sources, 3) Verify with official standards (RFCs), 4) Check real-world adoption"
  },
  "learnings": {
    "reusable_patterns": [
      "Pattern: For API design research, check official RFCs, industry surveys, and popular framework implementations"
    ]
  }
}
```

**Result:** Knows methodology for API research, can apply to GraphQL vs REST comparison.

---

## Scenario 5: Finding Collaboration History

**Task:** "Review Coder's implementation of authentication endpoint"

**Agent:** Reviewer

### Check Past Collaborations with Coder

```bash
grep '"other_agent":"coder"' memories/agents/reviewer/relationships/collaborations.jsonl | tail -3
```

**Expected Output (last 3 collaborations):**
```jsonl
{"timestamp":"2025-09-20T10:00:00Z","collaboration_type":"peer_review","other_agent":"coder","task_id":"review-005","context":"Reviewed FastAPI endpoint implementation","outcome":"success","learnings":"Coder writes clean async code but sometimes forgets error handling"}
{"timestamp":"2025-09-26T14:00:00Z","collaboration_type":"peer_review","other_agent":"coder","task_id":"review-008","context":"Reviewed database model implementation","outcome":"success","learnings":"Coder is strong with SQLAlchemy patterns, suggested adding indexes"}
{"timestamp":"2025-09-30T11:00:00Z","collaboration_type":"peer_review","other_agent":"coder","task_id":"review-011","context":"Reviewed CRUD endpoint implementation","outcome":"success","learnings":"Coder now consistently includes error handling - improvement noted!"}
```

**Analysis:**
- Coder has track record of good async code
- Previous issue with error handling is now resolved
- Strong with SQLAlchemy
- For auth review, should pay special attention to security aspects (not mentioned in past reviews)

---

## Scenario 6: Date Range Search

**Task:** "What research did we do last week?"

**Agent:** Primary AI (auditing)

### Search by Date Range (Sept 25-Oct 1)

```bash
grep '2025-09-2[5-9]\|2025-10-01' memories/agents/researcher/context/recent_context.jsonl
```

**Expected Output:**
```jsonl
{"timestamp":"2025-09-25T16:45:00Z","task_id":"research-039","context":"REST API versioning strategies - URI path versioning most common and visible","tags":["rest","api","versioning","best-practices"],"key_findings":["URI path versioning preferred","/v1 vs /api/v1 debate","Support 2 versions simultaneously"]}
{"timestamp":"2025-09-28T11:20:00Z","task_id":"research-040","context":"Pydantic v2 validation performance - 5-50x faster than v1, breaking changes minimal","tags":["pydantic","python","validation","performance"],"key_findings":["5-50x performance improvement","Migration from v1 straightforward","Type hints required"]}
{"timestamp":"2025-10-01T13:00:00Z","task_id":"research-041","context":"Python web frameworks 2025 trends - FastAPI leads growth (30% YoY), Django stable, Flask declining","tags":["python","web-frameworks","fastapi","django","flask","trends"],"key_findings":["FastAPI 9M+ downloads monthly","30% YoY growth","Async-first is dominant trend"]}
{"timestamp":"2025-10-01T18:30:00Z","task_id":"research-042","context":"REST API best practices 2025 - cursor pagination, RFC 9457 errors, JWT auth standard","tags":["rest","api","best-practices","pagination","error-handling"],"key_findings":["Cursor pagination > offset","RFC 9457 for error format","Rate limiting essential"]}
```

**Result:** 4 research tasks last week, all related to API/web development.

---

## Scenario 7: Cross-Agent Knowledge Discovery

**Task:** "Has anyone worked with Redis before?"

**Agent:** Primary AI

### Search All Agents for Redis Experience

```bash
grep -l 'redis' memories/agents/*/context/recent_context.jsonl
```

**Expected Output:**
```
memories/agents/architect/context/recent_context.jsonl
memories/agents/coder/context/recent_context.jsonl
```

**Analysis:** Architect and Coder have Redis experience.

### Get Details from Each

```bash
grep 'redis' memories/agents/architect/context/recent_context.jsonl
```

**Output:**
```jsonl
{"timestamp":"2025-09-18T10:00:00Z","task_id":"design-009","context":"Designed caching strategy using Redis for API response caching - 60-80% size reduction","tags":["redis","caching","architecture","performance"],"key_findings":["Redis optimal for cache","TTL 1-5 minutes for API responses","Invalidate on writes"]}
```

```bash
grep 'redis' memories/agents/coder/context/recent_context.jsonl
```

**Output:**
```jsonl
{"timestamp":"2025-09-19T14:00:00Z","task_id":"impl-016","context":"Implemented Redis connection pooling and cache helpers for FastAPI","tags":["redis","fastapi","caching","implementation"],"key_findings":["aioredis for async Redis","Connection pool size 10-20","Cache decorator pattern"]}
```

**Result:** Both agents have Redis experience! Architect designed strategy, Coder implemented it. For new Redis task, delegate to Coder (has implementation experience).

---

## Scenario 8: Finding Knowledge Gaps

**Task:** "What do we not know about databases?"

**Agent:** Primary AI (planning learning)

### Read Domain Knowledge and Look for Gaps

```bash
Read memories/agents/researcher/context/domain_knowledge.md
```

**Find Section:**
```markdown
## Knowledge Gaps Identified

### Database Technologies
- ✓ PostgreSQL connection pooling (researched)
- ✓ PostgreSQL vs MySQL comparison (researched)
- ✗ PostgreSQL replication and read replicas (not researched)
- ✗ Database monitoring with Prometheus (not researched)
- ✗ PostgreSQL 16 new features vs 15 (not researched)
```

```bash
Read memories/agents/researcher/tasks/research-043.json
```

**Find Gaps from Task:**
```json
{
  "learnings": {
    "knowledge_gaps_identified": [
      "Gap: Don't yet know monitoring best practices for connection pools (Prometheus metrics?)",
      "Gap: Don't know PostgreSQL 16 changes vs 15 for connection pooling",
      "Gap: No research yet on read replicas and connection pool distribution"
    ]
  }
}
```

**Result:** Clear list of future research topics for Researcher agent.

---

## Performance Comparison: With vs Without Memory System

### Without Memory System (Current State)

**Scenario:** Coder needs to implement user authentication endpoint

**Steps:**
1. Read ADR-001 for API spec (30s)
2. Research JWT best practices from scratch (20 min)
3. Research FastAPI auth patterns from scratch (15 min)
4. Implement from scratch (45 min)
5. Test and debug (20 min)

**Total Time:** ~100 minutes

### With Memory System (HCAMS)

**Scenario:** Same task - implement user authentication endpoint

**Steps:**
1. Grep recent_context.jsonl for "auth|jwt|fastapi" (1s)
2. Find Researcher's JWT research (research-037) - read it (2 min)
3. Find own FastAPI middleware pattern (impl-018) - read it (2 min)
4. Check patterns.json for auth patterns (1 min)
5. Implement using learned patterns (25 min)
6. Test (10 min - fewer issues due to learned patterns)
7. Log to memory (2 min)

**Total Time:** ~43 minutes

**Time Saved:** 57 minutes (57% faster!)

**Quality Improvement:** Fewer bugs due to reusing proven patterns

---

## Summary: Why Grep-Based Search Works

### Advantages Demonstrated

1. **Speed:** Sub-second for recent_context.jsonl searches
2. **Simplicity:** Standard Unix tool, no learning curve
3. **Flexibility:** Regex patterns for complex queries
4. **Transparency:** See exactly what's being searched
5. **Scalability:** Linear performance, predictable
6. **Debuggable:** Can run same commands manually

### Optimization Techniques Used

1. **JSONL Format:** Each line is complete JSON, no need to parse full file
2. **Small Files:** recent_context.jsonl is only 100 lines (~50 KB)
3. **Tags:** Normalized lowercase tags for consistent matching
4. **Indices:** index.json for O(1) lookup before full task read
5. **Tiered Search:** Fast → Deep, only go deep when needed

### When to Use Each Tier

| Tier | Speed | When to Use | Command |
|------|-------|-------------|---------|
| 1 | < 1s | Always start here | `grep {keywords} recent_context.jsonl` |
| 2 | 1-3s | Need domain knowledge or patterns | `Read domain_knowledge.md patterns.json` |
| 3 | 3-10s | Need detailed past work | `Read index.json` then specific tasks |
| 4 | 10-30s | Check if other agents have experience | `grep {keywords} */context/recent_context.jsonl` |
| 5 | 5-15s | Need organizational knowledge | `grep {keywords} memories/knowledge/**/*.md` |

### Expected Search Pattern for Typical Task

1. **90% of tasks:** Tier 1-2 sufficient (< 3 seconds)
2. **9% of tasks:** Tier 3 needed (< 10 seconds)
3. **1% of tasks:** Tier 4-5 for deep cross-agent search (< 30 seconds)

**Average search time across all tasks:** ~5 seconds (negligible overhead)

---

**Conclusion:** The grep-based search strategy is fast, simple, and scales well to 100+ agents while providing powerful search capabilities using only Claude SDK tools.
