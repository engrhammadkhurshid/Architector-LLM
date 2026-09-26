# 🚀 Architector-LLM v2.0.0 Quick Start Guide

## For Users

### Installation

```bash
code --install-extension architector-llm-2.0.0.vsix
```

### First Launch

1. **Setup Wizard appears automatically**
2. **Choose LLM Provider:**
   - **Local (Ollama)** - Free, requires 3.8GB download
   - **Cloud API** - Instant, requires API key

3. **If Cloud API:**
   - Select provider (DeepSeek, OpenAI, or Claude)
   - Get API key from provider website
   - Enter and verify key

4. **Research Participation (Optional):**
   - Read consent dialog
   - Provide professional information
   - Or skip to use without analytics

5. **Start using:**
   - Click "Architector" in status bar
   - Or: Command Palette → "Architector: Generate Architecture Documentation"

### API Keys

Get your API keys here:
- **DeepSeek:** https://platform.deepseek.com/api_keys
- **OpenAI:** https://platform.openai.com/api-keys
- **Claude:** https://console.anthropic.com/settings/keys

### Commands

- `Architector: Generate Architecture Documentation` - Generate docs
- `Architector: Check Dependencies` - Verify tools
- `Architector: About Architector-LLM` - Info & credits
- `Architector: View Privacy Policy` - See privacy policy
- `Architector: Withdraw Research Consent` - Opt out of research
- `Architector: Update Developer Information` - Update info
- `Architector: Export Analytics Data` - Export your data

---

## For Researcher (Hammad)

### Setup Analytics Backend

1. **Install dependencies:**
```bash
pip install flask flask-cors
```

2. **Run analytics server:**
```bash
python analytics_backend.py
```

3. **Update extension URLs:**

Edit [setupWizard.ts](vscode-extension/src/setupWizard.ts) and [developerInfo.ts](vscode-extension/src/analytics/developerInfo.ts):

```typescript
// Change this:
await fetch('https://research.nust.edu.pk/architector/register', ...)

// To your local server:
await fetch('http://localhost:5000/architector/register', ...)
```

4. **Test data collection:**
- Install extension
- Complete setup wizard with research consent
- Generate documentation
- Check `analytics_data/` folder for logs

### View Statistics

**Web endpoint:**
```
http://localhost:5000/architector/stats
```

**Local files:**
```
analytics_data/participants.jsonl - Developer information
analytics_data/sessions.jsonl    - Usage sessions
```

### For Production

Deploy backend to NUST server:

```bash
# Using gunicorn (production)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 analytics_backend:app

# Or use NUST's recommended deployment method
```

Update extension URLs to:
```
https://research.nust.edu.pk/architector/register
https://research.nust.edu.pk/architector/analytics
https://research.nust.edu.pk/architector/delete
```

Rebuild extension:
```bash
cd vscode-extension
npm run compile
cd ..
npx vsce package
```

---

## Testing Checklist

### Test API Integration

- [ ] Install v2.0.0
- [ ] Setup wizard appears
- [ ] Select DeepSeek API
- [ ] Enter API key
- [ ] Key validation works
- [ ] Generate docs with API
- [ ] Success message shows
- [ ] Switch to different provider in settings
- [ ] Regenerate docs with new provider

### Test Analytics

- [ ] Complete consent dialog
- [ ] Provide developer information
- [ ] Generate documentation
- [ ] Check analytics backend logs
- [ ] Verify data in sessions.jsonl
- [ ] Export analytics from extension
- [ ] View stats endpoint
- [ ] Withdraw consent
- [ ] Verify data deleted

### Test Ollama (Backward Compatibility)

- [ ] Select Ollama in wizard
- [ ] Generate docs (should work as v1.0)
- [ ] No API key required
- [ ] Local model used

---

## Configuration

### Extension Settings

`File > Preferences > Settings > Search "Architector"`

```json
{
  "architector.llmProvider": "deepseek",  // or "ollama", "openai", "claude"
  "architector.outputDirectory": "docs/arch"
}
```

### Backend Environment Variables

```bash
# LLM Provider
export LLM_PROVIDER=deepseek  # or ollama, openai, claude

# API Keys (for cloud providers)
export DEEPSEEK_API_KEY=sk-...
export OPENAI_API_KEY=sk-...
export CLAUDE_API_KEY=sk-ant-...

# Ollama (if using local)
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=deepseek-coder:6.7b
```

---

## Troubleshooting

### Setup wizard doesn't appear
```
Command Palette → "Architector: Generate Architecture Documentation"
Wizard will run if not completed
```

### API key invalid
```
1. Get new key from provider website
2. Command Palette → "Architector: Generate Architecture Documentation"
3. Extension will prompt for key
```

### Analytics not working
```
1. Check analytics backend is running
2. View browser console for errors
3. Check local logs: ~/.vscode/extensions/.../analytics/
```

### Want to switch providers
```
1. File > Preferences > Settings
2. Search "architector.llmProvider"
3. Change to desired provider
4. Generate docs (will prompt for API key if needed)
```

---

## Files Reference

**Extension:**
- `architector-llm-2.0.0.vsix` - Main package (265KB)
- `V2_IMPLEMENTATION_COMPLETE.md` - Full documentation
- `PRIVACY_POLICY.md` - Privacy policy

**Backend:**
- `analytics_backend.py` - Analytics server
- `backend/src/llm/client.py` - Multi-provider LLM client

**Source:**
- `vscode-extension/src/setupWizard.ts` - Setup wizard
- `vscode-extension/src/apiKeyManager.ts` - API key management
- `vscode-extension/src/analytics/developerInfo.ts` - Consent & developer info
- `vscode-extension/src/analytics/telemetry.ts` - Usage analytics

---

## Support

**Issues?** Contact: engr.hammadkhurshid@gmail.com  
**GitHub:** https://github.com/engrhammadkhurshid/architector-llm  
**Documentation:** See V2_IMPLEMENTATION_COMPLETE.md

---

## Quick Commands Summary

```bash
# Install extension
code --install-extension architector-llm-2.0.0.vsix

# Run analytics backend
python analytics_backend.py

# View stats
curl http://localhost:5000/architector/stats

# Rebuild extension (after changes)
cd vscode-extension && npm run compile && cd .. && npx vsce package
```

---

**🎉 You're all set! Start generating architecture documentation!**
