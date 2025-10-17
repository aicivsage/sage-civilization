# Enhanced UX Fork - Quick Start Guide

Get the Enhanced UX fork running in 5 minutes.

## Prerequisites

- Node.js v18+ installed
- MetaMask wallet extension
- Git

## Quick Installation

### 1. Clone and Navigate

```bash
cd /home/corey/projects/AI-CIV/grow_gemini_deepresearch/bnb-launchpad/experimental-forks/enhanced-ux
```

### 2. Install Dependencies

```bash
# Frontend
cd frontend
npm install

# Backend (in new terminal)
cd backend
npm install
```

### 3. Configure Environment

```bash
# Frontend
cd frontend
cp .env.example .env
# .env already has correct defaults for local development

# Backend
cd backend
cp .env.example .env
# .env already has BSC Testnet configuration
```

### 4. Start Servers

```bash
# Terminal 1: Backend
cd backend
npm run dev

# Terminal 2: Frontend
cd frontend
npm start
```

### 5. Open Browser

Navigate to: http://localhost:3000

## First Time Usage

1. **Connect Wallet**
   - Click "Connect Wallet" in top right
   - Approve MetaMask connection
   - App will switch to BSC Testnet automatically

2. **Load Tokens**
   - Click "Load Tokens" in token selector
   - Wait for tokens to appear (5-10 seconds)

3. **Select a Token**
   - Click on any token from the list
   - Price chart will start updating in real-time

4. **Make a Trade**
   - Switch to "Buy" or "Sell" tab
   - Enter amount
   - Click button and confirm in MetaMask

## Troubleshooting

### Backend Won't Start

```bash
# Check if port 4000 is in use
lsof -i :4000

# Kill process if needed
kill -9 <PID>
```

### Frontend Won't Connect to Backend

Check `.env` file:
```env
REACT_APP_WS_URL=http://localhost:4000
```

### MetaMask Not Switching Network

Manually switch to BSC Testnet in MetaMask settings.

### No Tokens Appearing

- Verify backend is running
- Check backend console for RPC errors
- Ensure factory address is correct in `.env`

## Production Deployment

See `README.md` for full deployment instructions.

## Links

- Implementation Plan: `IMPLEMENTATION_PLAN.md`
- Full Documentation: `README.md`
- Main Project: `../../README.md`
