# Error Logging Pattern Fix - JavaScript/React Best Practices

**Date**: 2025-10-14
**Agent**: coder
**Category**: Pattern Discovery (Dead End Avoided)
**Project**: BNB Launchpad Frontend

---

## The Problem Pattern (Anti-Pattern)

**Symptom**: Console shows `[object Object]` instead of actual error messages

**Root Cause**: Logging JavaScript Error objects directly without stringification

**Bad Pattern**:
```typescript
catch (error) {
  console.error('Error:', error);  // ← Shows as [object Object]
  console.error('Details:', { error, context });  // ← Also shows [object Object]
}
```

**Why it fails**: JavaScript's `console.error()` doesn't automatically stringify Error objects when they're nested in other objects.

---

## The Solution Pattern

### Pattern 1: Comprehensive Error Logging

```typescript
catch (error) {
  console.error('========== ERROR IN [CONTEXT] ==========');
  console.error('Error:', error);  // Log the object itself
  console.error('Message:', error instanceof Error ? error.message : String(error));
  console.error('Name:', error instanceof Error ? error.name : 'N/A');
  console.error('Stack:', error instanceof Error ? error.stack : 'N/A');

  // Attempt JSON stringification (includes non-enumerable properties)
  try {
    console.error('Full JSON:', JSON.stringify(error, Object.getOwnPropertyNames(error), 2));
  } catch (e) {
    console.error('Could not stringify:', e);
    console.error('String representation:', String(error));
  }

  // Context variables
  console.error('Context var 1:', contextValue1);
  console.error('Context var 2:', contextValue2);
  console.error('========================================');
}
```

**Why this works**:
- Logs error object directly (browsers often render this nicely)
- Extracts specific properties (message, name, stack)
- Uses `Object.getOwnPropertyNames()` to include non-enumerable properties in JSON
- Fallback to `String()` if JSON fails
- Includes relevant context
- Clear visual delimiters for easy scanning

### Pattern 2: Global Error Handlers

**Window Error Events**:
```typescript
window.addEventListener('error', (event) => {
  console.error('========== GLOBAL ERROR ==========');
  console.error('Message:', event.message);
  console.error('File:', event.filename);
  console.error('Line:', event.lineno, 'Col:', event.colno);

  if (event.error) {
    console.error('Error:', event.error);
    console.error('Message:', event.error.message);
    console.error('Stack:', event.error.stack);

    try {
      console.error('Full:', JSON.stringify(event.error, Object.getOwnPropertyNames(event.error), 2));
    } catch (e) {
      console.error('Stringify failed:', e);
    }
  }
  console.error('==================================');
});
```

**Promise Rejection Events**:
```typescript
window.addEventListener('unhandledrejection', (event) => {
  console.error('========== UNHANDLED REJECTION ==========');
  console.error('Reason:', event.reason);

  if (event.reason instanceof Error) {
    console.error('Message:', event.reason.message);
    console.error('Stack:', event.reason.stack);
  }

  try {
    console.error('Full:', JSON.stringify(event.reason, Object.getOwnPropertyNames(event.reason), 2));
  } catch (e) {
    console.error('Stringify failed:', e);
    console.error('ToString:', String(event.reason));
  }
  console.error('========================================');
});
```

### Pattern 3: React ErrorBoundary

```typescript
componentDidCatch(error: Error, errorInfo: ErrorInfo) {
  console.error('========== ERROR BOUNDARY ==========');
  console.error('Error name:', error.name);
  console.error('Error message:', error.message);
  console.error('Error stack:', error.stack);

  try {
    console.error('Full error:', JSON.stringify(error, Object.getOwnPropertyNames(error), 2));
  } catch (e) {
    console.error('Stringify failed:', e);
  }

  console.error('Component stack:', errorInfo.componentStack);

  try {
    console.error('Full errorInfo:', JSON.stringify(errorInfo, null, 2));
  } catch (e) {
    console.error('Stringify failed:', e);
  }
  console.error('===================================');
}
```

---

## Why This Pattern Is Critical

### Before Fix (2 Days of Frustration):
```
ERROR
[object Object]
    at someFunction (bundle.js:85794:58)
```

**Result**: Impossible to debug. No idea what's actually breaking.

### After Fix (Actionable Information):
```
========== ERROR IN handleBuy ==========
Error: insufficient funds for intrinsic transaction cost
Message: insufficient funds for intrinsic transaction cost
Stack: Error: insufficient funds for intrinsic transaction cost
    at Web3Provider._wrapError (providers.js:2345)
    at Web3Provider.send (providers.js:1234)
Full JSON: {
  "message": "insufficient funds for intrinsic transaction cost",
  "code": "INSUFFICIENT_FUNDS",
  "data": { ... }
}
Selected token: 0x1234...5678
Amount: 0.1
========================================
```

**Result**: Immediately clear what's wrong. Can fix in minutes.

---

## Key Learnings

### 1. JavaScript Error Object Quirks

Error objects have **non-enumerable properties** that don't show up in normal JSON.stringify():
- `message` - enumerable ✅
- `name` - enumerable ✅
- `stack` - **non-enumerable** ❌

**Solution**: Use `Object.getOwnPropertyNames()` as the replacer:
```typescript
JSON.stringify(error, Object.getOwnPropertyNames(error), 2)
```

### 2. Nested Objects Hide Errors

```typescript
// BAD - error becomes [object Object]
console.error('Failed:', { error, context });

// GOOD - error is visible
console.error('Failed');
console.error('Error:', error);
console.error('Context:', context);
```

### 3. Always Include Context

When logging errors, include:
- **What** was being attempted (function name, operation)
- **Where** it happened (file, component, line if available)
- **Input values** (parameters, state at time of error)
- **Environment** (wallet connected?, network ID, token address, etc.)

### 4. Visual Delimiters Are Essential

```typescript
console.error('========== CLEAR HEADER ==========');
// ... error details ...
console.error('==================================');
```

**Why**: In a React app with dozens of renders and effects, clear delimiters make errors scannable.

### 5. Graceful Stringification

Always wrap JSON.stringify in try-catch:
```typescript
try {
  console.error('JSON:', JSON.stringify(obj, null, 2));
} catch (e) {
  console.error('Stringify failed:', e);
  console.error('Fallback:', String(obj));
}
```

**Why**: Some objects (circular references, special objects) can't be stringified.

---

## When to Apply This Pattern

✅ **Always use in**:
- Global error handlers (window.addEventListener('error'))
- Global promise rejection handlers
- React ErrorBoundary components
- Any catch block in production code
- Async error handlers (useEffect cleanup, async functions)

❌ **Don't bother for**:
- Quick prototyping (but add before committing)
- Console.log debugging (temporary, will be removed)

---

## Time Saved for Descendants

**Without this pattern**:
- 2 days debugging `[object Object]` (Corey's experience)
- Guessing what errors mean
- Adding console.logs everywhere to triangulate
- Re-deploying constantly to test theories

**With this pattern**:
- See actual error in first occurrence
- Immediately know what's wrong
- Fix in minutes, not days

**Estimated time saved per bug**: 1-8 hours
**Estimated bugs per project**: 10-50
**Total time saved**: 10-400 hours per project

---

## Related Patterns

- **Performance Logging**: Use similar delimiters for timing logs
- **State Debugging**: Log state changes with context in useEffect
- **API Errors**: Extract and log response.data, status, headers
- **Web3 Errors**: ethers.js errors have special properties (code, reason, transaction)

---

## Code Locations

**Fixed in BNB Launchpad**:
- `/frontend/src/index.tsx` - Global handlers
- `/frontend/src/components/ErrorBoundary.tsx` - React error boundary
- `/frontend/src/App.tsx` - All async error handlers

**Pattern is reusable across**:
- Any React project
- Any JavaScript/TypeScript project
- Browser-based apps
- Node.js apps (though console.error works slightly differently)

---

**Pattern Status**: Production-tested, highly recommended for all descendants
**Difficulty**: Easy (5 minutes to implement)
**Impact**: Critical (saves hours/days of debugging time)

---

**TL;DR**: Never log `[object Object]` again. Always stringify errors properly with context, stack traces, and visual delimiters. Future you (and Corey) will thank you.
