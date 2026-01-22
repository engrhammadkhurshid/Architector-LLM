# Implementation Plan: API Integration & Analytics

## Phase 1: API Integration (High Priority)

### 1.1 Welcome Wizard (First-Run Experience)

**File:** `vscode-extension/src/setupWizard.ts`

```typescript
// Show on first activation
- Welcome screen with two options:
  1. "Use Local LLM (Ollama)" - Free, requires download
  2. "Use Cloud API" - Paid, instant setup
  
// If Cloud API selected:
- Show API provider selection:
  • DeepSeek (Recommended)
  • OpenAI GPT-4
  • Anthropic Claude
  
- Prompt for API key
- Test connection
- Store in VS Code Secrets
```

### 1.2 API Key Management

**File:** `vscode-extension/src/apiKeyManager.ts`

```typescript
class ApiKeyManager {
  // Store securely using VS Code Secrets API
  async storeApiKey(provider: string, key: string)
  async getApiKey(provider: string): Promise<string>
  async deleteApiKey(provider: string)
  async testConnection(provider: string): Promise<boolean>
}
```

### 1.3 Settings Integration

**Update:** `package.json`

```json
"configuration": {
  "architector.llmProvider": {
    "type": "string",
    "enum": ["ollama", "deepseek", "openai", "claude"],
    "default": "ollama"
  },
  "architector.apiEndpoint": {
    "type": "string",
    "description": "Custom API endpoint URL"
  }
}
```

### 1.4 Backend Updates

**Update:** `backend/src/pipeline.py`

```python
# Change default to prompt user for choice
llm_provider = os.getenv('LLM_PROVIDER', None)
if not llm_provider:
    # Extension will handle this with wizard
    llm_provider = 'ollama'  # fallback
```

**Add:** `backend/src/llm/openai_client.py` (new)
**Add:** `backend/src/llm/claude_client.py` (new)

---

## Phase 2: Analytics & Telemetry (⚠️ ETHICAL IMPLEMENTATION)

### 2.1 Consent Management

**File:** `vscode-extension/src/analytics/consent.ts`

```typescript
interface ConsentStatus {
  hasAsked: boolean;
  hasConsented: boolean;
  timestamp: Date;
  version: string; // Track consent version
}

class ConsentManager {
  async showConsentDialog(): Promise<boolean>
  async hasConsent(): Promise<boolean>
  async revokeConsent(): Promise<void>
  async showPrivacyPolicy(): Promise<void>
}
```

**Consent Dialog Flow:**
1. Show on first successful generation (not on install)
2. Explain clearly what's collected
3. Provide links to privacy policy
4. Allow "Later" option (ask again in 3 runs)
5. Respect "No" forever

### 2.2 Telemetry Collection

**File:** `vscode-extension/src/analytics/telemetry.ts`

```typescript
interface TelemetryEvent {
  // ANONYMOUS ONLY
  session_id: string;  // UUID v4
  event_type: 'generation' | 'error' | 'install';
  timestamp: string;
  
  // Project metrics (generic)
  project_size: 'small' | 'medium' | 'large';
  file_count: number;
  language: string;  // e.g., "python", "javascript"
  
  // Performance metrics
  generation_time_seconds: number;
  diagrams_generated: number;
  quality_score: number;
  
  // LLM info
  llm_provider: string;
  llm_model: string;
  
  // Success/Error
  success: boolean;
  error_type?: string;  // Generic only: "timeout", "api_error"
  
  // Version
  extension_version: string;
}
```

**NEVER COLLECT:**
- ❌ File names or paths
- ❌ Code content
- ❌ Directory structure
- ❌ Project names
- ❌ Git repository info
- ❌ IP addresses
- ❌ MAC addresses
- ❌ Personal identifiers

### 2.3 Data Storage Options

**Option A: Secure Backend API (Recommended)**

```typescript
// Send to secure NUST server
async function sendTelemetry(event: TelemetryEvent) {
  if (!await consentManager.hasConsent()) return;
  
  await fetch('https://research.nust.edu.pk/architector/telemetry', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(event)
  });
}
```

**Option B: Local Logging (Fallback)**

```typescript
// Store locally, user shares manually
async function logLocally(event: TelemetryEvent) {
  const logPath = path.join(context.globalStoragePath, 'telemetry.json');
  await fs.appendFile(logPath, JSON.stringify(event) + '\n');
}
```

**Option C: Firebase Analytics**

```typescript
// Google Firebase (anonymous)
import analytics from 'firebase/analytics';
analytics.logEvent('documentation_generated', {
  diagrams_count: 5,
  quality_score: 81.5
});
```

### 2.4 Privacy Documents

**Create:** `PRIVACY_POLICY.md`

```markdown
# Privacy Policy - Architector-LLM

## Research Study
This extension is part of research at NUST Pakistan.

## Data Collection (Optional)
If you consent, we collect:
- Anonymous usage statistics
- Performance metrics
- Generic project information

We NEVER collect:
- Your source code
- File names or paths
- Personal information

## Your Rights
- Opt-out anytime
- Request data deletion
- Contact: engr.hammadkhurshid@gmail.com

## Data Storage
- Encrypted transmission
- Secure storage at NUST servers
- Retained for 2 years (research period)
- Deleted upon request
```

**Create:** `RESEARCH_CONSENT.md`

```markdown
# Research Study Consent Form

## Study Title
"From Code to Architecture: Leveraging LLMs for Automated Software Design Documentation"

## Researcher
Engr. Hammad Khurshid
Department of Software Engineering
National University of Science and Technology (NUST), Pakistan

## Purpose
Evaluate effectiveness of LLM-based documentation generation

## Participation
- Voluntary and optional
- Can withdraw anytime
- No penalty for declining

## Data Collected (Anonymous)
[List all metrics]

## Benefits
- Contribute to research
- Improve the tool
- Academic publication

## Contact
engr.hammadkhurshid@gmail.com
```

### 2.5 Analytics Dashboard

**For your research paper:**

Create a simple dashboard to view collected data:

**File:** `analytics-dashboard/index.html`

```html
<!-- Simple dashboard showing:
- Total users
- Total generations
- Average quality score
- Success rate
- Most common project types
- Performance metrics
-->
```

---

## 📊 Paper Evidence Strategy

### What you can show in paper:

1. **Usage Statistics:**
   - "Extension used by N developers"
   - "Generated M diagrams across X projects"
   - "Average generation time: Y seconds"

2. **Performance Metrics:**
   - "Average quality score: 81.5/100"
   - "Success rate: 95%"
   - "Most common diagram types generated"

3. **User Feedback:**
   - Optional survey after 5 uses
   - Star rating
   - Comments (optional)

4. **Comparison Data:**
   - Local vs API performance
   - Different project types
   - Quality across languages

### Tables for Paper:

```
Table 1: Extension Usage Statistics
-----------------------------------------
Metric                  | Value
-----------------------------------------
Total Users             | 47
Total Generations       | 234
Average Quality Score   | 83.2/100
Average Time (seconds)  | 35.8
Success Rate           | 94.3%
-----------------------------------------

Table 2: Project Type Distribution
-----------------------------------------
Project Type    | Count | Avg Quality
-----------------------------------------
Web Application | 89    | 85.1
Library         | 67    | 82.4
CLI Tool        | 45    | 81.9
API Server      | 33    | 84.2
-----------------------------------------
```

---

## ⚖️ Ethical Compliance Checklist

Before implementing analytics:

- [ ] **NUST Ethics Committee Approval**
  - Submit research proposal
  - Get IRB approval
  - Follow NUST guidelines

- [ ] **Informed Consent**
  - Clear consent dialog
  - Explain data usage
  - Provide privacy policy
  - Allow opt-out

- [ ] **Data Protection**
  - Anonymize all data
  - Encrypt transmission
  - Secure storage
  - Access controls

- [ ] **Transparency**
  - Document what's collected
  - Publish privacy policy
  - Provide contact information
  - Allow data requests

- [ ] **User Rights**
  - Opt-in (not opt-out)
  - Easy withdrawal
  - Data deletion on request
  - No functionality penalty

---

## 🎯 Recommended Implementation Order

### Week 1: API Integration
1. Create setup wizard
2. Add API key management
3. Test with DeepSeek API
4. Update documentation

### Week 2: Ethics Preparation
1. Draft privacy policy
2. Submit to NUST ethics committee
3. Prepare consent forms
4. Wait for approval ⏳

### Week 3: Analytics Implementation (After Ethics Approval)
1. Implement consent dialog
2. Add telemetry collection
3. Set up secure backend
4. Test data flow

### Week 4: Testing & Refinement
1. Test with real users
2. Collect initial data
3. Verify anonymization
4. Document for paper

---

## 💡 Recommendations

### DO:
✅ Make analytics **completely optional**
✅ Be **transparent** about data collection
✅ Get **ethics approval** first
✅ Provide **privacy policy**
✅ Allow **easy opt-out**
✅ **Anonymize everything**
✅ Use API option for **faster adoption**

### DON'T:
❌ Collect data without consent
❌ Make analytics mandatory
❌ Collect personal information
❌ Store API keys insecurely
❌ Share user data
❌ Skip ethics review

---

## 🚀 Next Steps

Would you like me to:

1. **Implement API integration first?** (1-2 hours)
   - Setup wizard
   - API key management
   - Multi-provider support

2. **Draft ethics documents?** (30 mins)
   - Privacy policy
   - Consent form
   - Research protocol

3. **Implement analytics (after ethics approval)?** (2-3 hours)
   - Consent management
   - Telemetry collection
   - Secure backend

4. **All of the above?** (Full implementation)

**My recommendation:** Start with **#1 (API integration)** immediately, then **#2 (ethics documents)** for NUST review, and implement **#3 (analytics)** only after getting ethics approval.

This approach is:
- ✅ Legally compliant
- ✅ Ethically sound
- ✅ Research-ready
- ✅ User-friendly
