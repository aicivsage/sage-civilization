# Build Recipes Memory

**Purpose**: Store gradle configurations that work reliably

**Structure**: Each recipe is a working gradle snippet with:
- Header comment explaining what it sets up
- Full configuration code
- Dependency versions that work together
- Common issues and solutions
- Last verified date

**Retrieval Protocol**: When generating build.gradle.kts files, use these recipes as templates.

**File Naming**: `[feature]-setup.gradle.kts` (e.g., `compose-material3-setup.gradle.kts`, `hilt-dependencies.gradle.kts`)

---

This directory represents battle-tested build configurations - versions and setups proven to work.
