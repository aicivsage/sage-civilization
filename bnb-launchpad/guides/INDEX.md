# BNB Launchpad - Guides Index

**Purpose**: Permanent technical reference documentation for all specialists working on this project

**Location**: `/home/corey/projects/AI-CIV/grow_gemini_deepresearch/bnb-launchpad/guides/`

---

## Available Guides

### 1. MetaMask Integration Guide
**File**: `METAMASK-INTEGRATION-GUIDE.md`
**Status**: Production-Ready
**Last Updated**: October 9, 2025

**Contains**:
- Root cause analysis of wallet connection bugs
- MetaMask best practices (EIP-1193)
- Production-ready WalletConnectionManager implementation
- Integration guide with step-by-step instructions
- Testing checklist (30+ scenarios)
- Error handling patterns
- Debugging tips

**Use Cases**:
- Fixing wallet connection issues
- Implementing new wallet features
- Understanding MetaMask provider API
- Debugging "Internal JSON-RPC error"
- Handling account/network changes

**Domain**: Web3, Blockchain, Frontend Integration

---

### 2. Deployment Guide
**File**: `DEPLOYMENT_GUIDE.md`
**Status**: Production-Ready
**Last Updated**: October 8, 2025

**Contains**:
- Smart contract deployment procedures
- Hardhat configuration
- Network setup (BSC Testnet/Mainnet)
- Verification steps
- Post-deployment validation

**Use Cases**:
- Deploying contracts to testnet
- Deploying contracts to mainnet
- Verifying contract deployments
- Network configuration

**Domain**: Blockchain, Smart Contracts, DevOps

---

## Usage Guidelines

### For Agents

**When to reference these guides:**
- Working on wallet integration → Read `METAMASK-INTEGRATION-GUIDE.md`
- Deploying contracts → Read `DEPLOYMENT_GUIDE.md`
- Debugging Web3 issues → Check relevant guide first

**How to reference:**
```
Before implementing wallet connection, I reviewed /guides/METAMASK-INTEGRATION-GUIDE.md
which provides production-ready patterns for MetaMask integration.
```

### For Developers

**Quick Reference**:
```bash
# List all guides
ls /home/corey/projects/AI-CIV/grow_gemini_deepresearch/bnb-launchpad/guides/

# Read MetaMask guide
cat /home/corey/projects/AI-CIV/grow_gemini_deepresearch/bnb-launchpad/guides/METAMASK-INTEGRATION-GUIDE.md

# Search for specific topic
grep -r "error handling" /home/corey/projects/AI-CIV/grow_gemini_deepresearch/bnb-launchpad/guides/
```

---

## Guide Quality Standards

All guides in this directory must:

✅ **Be production-ready** - Code examples are tested and working
✅ **Include examples** - Real-world usage patterns
✅ **Explain rationale** - Why, not just what
✅ **List sources** - Official documentation references
✅ **Stay current** - Update when APIs change
✅ **Be comprehensive** - Cover edge cases

---

## Future Guides (Planned)

- Smart Contract Testing Guide
- Gas Optimization Guide
- Security Audit Checklist
- Frontend Architecture Guide
- Error Recovery Patterns
- Performance Optimization Guide

---

## Maintenance

**Update Frequency**: As needed when:
- New patterns discovered
- APIs updated
- Bugs found and fixed
- Better practices emerge

**Ownership**: All agents and developers can propose updates

**Location**: Always keep in `/guides/` directory for easy reference

---

**Last Updated**: October 9, 2025
**Total Guides**: 2
**Status**: Active
