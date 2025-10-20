# HCGateway Deployment Preparation - 2025-10-18

## Context

Prepared HCGateway deployment for Corey's health gamification system. HCGateway is a REST API bridge that allows backend systems to access Android Health Connect data, replacing direct Renpho and Google Fit API integrations.

## What I Did

### 1. Repository Setup
- Cloned HCGateway from https://github.com/ShuchirJ/HCGateway
- Location: `/home/corey/projects/AI-CIV/HCGateway/`
- Reviewed architecture (Flask API + MongoDB + React Native mobile app)
- Analyzed API endpoints (v2: login, refresh, fetch, push, delete)

### 2. Configuration Files Created

**api/.env** (environment configuration):
- Template with all required variables
- Clear instructions for each setting
- MongoDB URI format documented
- Firebase Project ID placeholder
- Ready for Corey to customize

**docker-compose.yml** (already existed):
- Uses official HCGateway Docker image
- MongoDB included
- Port 6644 for API
- Volumes for service-account.json and database

### 3. Deployment Automation

**deploy.sh** (executable deployment script):
- Prerequisites checking (Docker, Docker Compose)
- Configuration validation (.env, service-account.json)
- Automated deployment (docker-compose up)
- Health checks (verify containers running)
- User-friendly output with colors
- Error handling and warnings

Features:
- Detects missing Firebase credentials (creates placeholder)
- Warns about default passwords
- Verifies API responds after deployment
- Provides management commands for logs/restart

### 4. Documentation Created

**DEPLOYMENT_SETUP_GUIDE.md** (comprehensive guide):
- Architecture diagram
- Prerequisites checklist
- Firebase setup walkthrough (step-by-step)
- Environment configuration instructions
- Two deployment options (Docker vs manual)
- Mobile app setup (pre-built APK vs custom build)
- Security considerations (production recommendations)
- API endpoints summary
- Integration overview
- Troubleshooting section
- Decision matrix (public vs self-hosted)

**INTEGRATION_PLAN.md** (backend integration):
- Current architecture analysis
- New architecture proposal
- Complete HCGatewayClient class template (ready to use)
- Data format transformation logic
- HealthDataPipeline updates
- Configuration changes needed
- Testing strategy
- Migration plan (parallel run → switchover → deprecate)
- Fallback strategy
- Implementation tasks breakdown

**QUICK_START.md** (5-minute guide):
- Two fast-track options
- Minimal steps to get running
- Decision matrix
- Common issues & solutions
- Integration code snippet

**COREY_ACTION_ITEMS.md** (next steps):
- Clear decision point (public vs self-hosted)
- Pros/cons for each option
- Specific action items for Corey
- What I need to proceed
- Testing checklist
- Questions to answer

## Key Technical Insights

### HCGateway Architecture
```
Corey's Phone (Android)
    ↓ (Health Connect API)
React Native Mobile App (syncs every 2 hours)
    ↓ (REST API + Firebase push)
Flask API Server (Python 3.13)
    ↓ (Fernet encryption)
MongoDB (encrypted storage)
    ↓ (REST API)
Our health_gamification Backend
```

### Security Model
- Data encrypted before storage (Fernet encryption)
- Passwords hashed with Argon2 (never plaintext)
- Bearer token authentication (12-hour expiry)
- Refresh token mechanism
- Per-user encryption keys (derived from password hash)

### API v2 Endpoints
- `POST /api/v2/login` → Get access token
- `POST /api/v2/refresh` → Refresh expired token
- `POST /api/v2/fetch/<dataType>` → Retrieve health data
- `PUT /api/v2/push/<dataType>` → Write health data (requires Firebase)
- `DELETE /api/v2/delete/<dataType>` → Delete health data (requires Firebase)

Supported data types: weight, bloodPressure, steps, heartRate, sleep, 30+ others

### Data Flow
1. Mobile app reads from Health Connect (Renpho, Google Fit, etc.)
2. App encrypts data using user's password-derived key
3. App sends to API server via REST
4. API stores encrypted data in MongoDB
5. Our backend authenticates and retrieves data
6. API decrypts data before returning (using same password-derived key)

### Integration Strategy

**Current (health_gamification):**
```python
renpho_client.get_weight()
renpho_client.get_blood_pressure()
google_fit_client.get_steps()
```

**New (unified):**
```python
hcgateway_client.fetch_weight()
hcgateway_client.fetch_blood_pressure()
hcgateway_client.fetch_steps()
```

**Benefits:**
- One API for all health data
- Android Health Connect is source of truth
- Auto-sync (mobile app handles it)
- Extensible (easy to add more data types)
- No need for Renpho API key or Google Fit OAuth

## Decisions Made

1. **Deployment Method:** Docker Compose (recommended)
   - Automated setup
   - MongoDB included
   - Easy management
   - Alternative: Manual Python deployment documented

2. **Configuration Approach:** Template-based
   - Created .env template with clear instructions
   - Corey provides: Firebase credentials, MongoDB password
   - Sensible defaults for everything else

3. **Documentation Strategy:** Layered
   - QUICK_START.md for fast-track
   - DEPLOYMENT_SETUP_GUIDE.md for comprehensive
   - INTEGRATION_PLAN.md for backend work
   - COREY_ACTION_ITEMS.md for decision-making

4. **Migration Path:** Parallel run → switchover
   - Keep old RenphoClient/GoogleFitClient initially
   - Run both data sources in parallel
   - Validate data quality matches
   - Switch over once proven
   - Deprecate old clients

## Decisions Deferred (Awaiting Corey)

1. **Public vs Self-Hosted:**
   - Option A: Use public server (api.hcgateway.shuchir.dev) - faster, less private
   - Option B: Self-host - more private, requires Firebase setup
   - Recommendation: Start with A, migrate to B later

2. **Firebase Configuration:**
   - Need service-account.json from Corey's Firebase project
   - Need Firebase Project ID
   - Required for self-hosted deployment
   - Not needed if using public server

3. **MongoDB Password:**
   - Template uses placeholder
   - Need Corey to choose secure password
   - Must match between .env and docker-compose.yml

4. **Mobile App Build:**
   - Option A: Use pre-built APK (connects to public server)
   - Option B: Build custom APK (connects to self-hosted server)
   - Requires Node.js, Android Studio if building custom

5. **Integration Timeline:**
   - When to implement HCGatewayClient?
   - Parallel testing duration?
   - When to deprecate old clients?

## Files Created (Absolute Paths)

1. `/home/corey/projects/AI-CIV/HCGateway/DEPLOYMENT_SETUP_GUIDE.md` (5221 bytes)
2. `/home/corey/projects/AI-CIV/HCGateway/api/.env` (1493 bytes)
3. `/home/corey/projects/AI-CIV/HCGateway/deploy.sh` (3782 bytes, executable)
4. `/home/corey/projects/AI-CIV/HCGateway/INTEGRATION_PLAN.md` (15147 bytes)
5. `/home/corey/projects/AI-CIV/HCGateway/QUICK_START.md` (3556 bytes)
6. `/home/corey/projects/AI-CIV/HCGateway/COREY_ACTION_ITEMS.md` (5502 bytes)

## Next Steps

**For Coder (me):**
1. Await Corey's decision (public vs self-hosted)
2. If self-hosted chosen, await Firebase credentials
3. Implement HCGatewayClient class (template ready)
4. Update HealthDataPipeline to use HCGatewayClient
5. Write tests for new integration
6. Run parallel testing (old vs new data sources)

**For Corey:**
1. Review COREY_ACTION_ITEMS.md
2. Choose deployment option
3. If self-hosted: Complete Firebase setup, provide credentials
4. If public server: Download APK, install, create account
5. Confirm deployment approach

## Patterns Discovered

### Deployment Script Best Practices
- Check prerequisites before running (docker, docker-compose)
- Validate configuration files exist
- Warn about placeholder values (don't fail, give choice)
- Use colors for better UX (green success, yellow warning, red error)
- Provide management commands at end
- Test deployed services before declaring success

### Documentation Layering
- **Quick start:** 5-minute version for fast-track users
- **Comprehensive guide:** All details, all options, all edge cases
- **Integration guide:** Technical implementation, code templates
- **Action items:** Decision points, next steps, clear asks

### API Client Design Pattern
```python
class APIClient:
    def __init__(self, base_url, username, password):
        self.token = None
        self.token_expiry = None

    def authenticate(self):
        """Get initial token"""

    def refresh_auth(self):
        """Refresh expired token"""

    def _ensure_authenticated(self):
        """Check token validity, auto-refresh"""

    def _make_request(self, endpoint, **kwargs):
        """Authenticated request wrapper"""

    def fetch_resource(self, ...):
        """Public method for resource access"""
```

### Data Transformation Pattern
```python
def _transform_data(self, external_format):
    """Convert external API format to internal standard"""
    return {
        'timestamp': parse(external['start']),
        'value': external['data']['measurement']['value'],
        'source': self._extract_source(external['app'])
    }
```

## Learnings

1. **HCGateway solves multi-source problem:**
   - Instead of separate APIs for Renpho, Google Fit, etc.
   - Android Health Connect is universal data store
   - One API to rule them all

2. **Mobile app is key component:**
   - Handles sync automatically (every 2 hours)
   - Deals with Health Connect permissions
   - Encrypts data before sending
   - Pre-built APK available (public server) or build custom (self-hosted)

3. **Firebase is optional but important:**
   - Required for push notifications (manual sync trigger)
   - Required for remote delete
   - NOT required for read-only access
   - Can deploy without it (limited functionality)

4. **Security is built-in:**
   - Fernet encryption (symmetric)
   - Key derived from user password
   - Data encrypted at rest in MongoDB
   - Bearer token auth (12-hour expiry)

5. **Two deployment paths have tradeoffs:**
   - Public server: Zero setup, less privacy, instant
   - Self-hosted: More setup, full control, better privacy
   - Can migrate from public → self-hosted later

## Open Questions

1. **Data retention policy:** How long to keep health data in MongoDB?
2. **Backup strategy:** Should we backup MongoDB health data?
3. **Additional metrics:** Beyond weight/BP/steps, what else to track?
4. **Server location:** Localhost only or deploy to VPS for remote access?
5. **Monitoring:** Should we set up health checks/alerts for HCGateway API?

## Related Work

- **health_gamification backend:** Will integrate with this
- **Renpho integration:** Will be replaced by HCGateway
- **Google Fit integration:** Will be replaced by HCGateway
- **Points calculation:** Unchanged (just different data source)

## References

- HCGateway GitHub: https://github.com/ShuchirJ/HCGateway
- API Documentation: https://hcgateway.shuchir.dev/
- Android Health Connect: https://developer.android.com/health-and-fitness/guides/health-connect

## Success Criteria

- [ ] HCGateway server deployed and running
- [ ] Mobile app syncing data from Health Connect
- [ ] API returning weight, BP, steps data
- [ ] HCGatewayClient implemented and tested
- [ ] HealthDataPipeline using new client
- [ ] Data quality matches old sources
- [ ] Old clients deprecated
- [ ] Corey's health gamification system working end-to-end

**Status:** Preparation complete, awaiting Corey's configuration decisions.
