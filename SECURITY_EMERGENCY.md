# 🚨 SECURITY EMERGENCY - IMMEDIATE ACTION REQUIRED

**Date:** March 24, 2026  
**Severity:** CRITICAL  
**Status:** ACTIVE BREACH

---

## ⚠️ CONFIRMED EXPOSURE

Your Google Cloud service account private key is **PUBLICLY VISIBLE** in git history.

**Exposed File:** `backend/scripts/ee-credentials.json.json`  
**Exposed In Commits:** f5d5aa6, 65b5305  
**Project:** bhu-hack  
**Service Account:** breath-analyzer-backend@bhu-hack.iam.gserviceaccount.com

---

## 🔥 IMMEDIATE ACTIONS (Do This NOW - 15 minutes)

### Step 1: Revoke the Compromised Service Account (5 min)

```bash
# Go to Google Cloud Console
# https://console.cloud.google.com/iam-admin/serviceaccounts?project=bhu-hack

# 1. Find: breath-analyzer-backend@bhu-hack.iam.gserviceaccount.com
# 2. Click the 3 dots menu
# 3. Click "Delete" or "Disable"
# 4. Confirm deletion
```

**OR via command line:**
```bash
gcloud iam service-accounts delete \
  breath-analyzer-backend@bhu-hack.iam.gserviceaccount.com \
  --project=bhu-hack
```

### Step 2: Create New Service Account (5 min)

```bash
# Create new service account
gcloud iam service-accounts create vayu-backend-v2 \
  --display-name="VayuDrishti Backend v2" \
  --project=bhu-hack

# Grant Earth Engine permissions
gcloud projects add-iam-policy-binding bhu-hack \
  --member="serviceAccount:vayu-backend-v2@bhu-hack.iam.gserviceaccount.com" \
  --role="roles/earthengine.viewer"

# Create new key
gcloud iam service-accounts keys create new-credentials.json \
  --iam-account=vayu-backend-v2@bhu-hack.iam.gserviceaccount.com \
  --project=bhu-hack

# Move to correct location (NOT in git!)
mv new-credentials.json backend/app/services/ee-credentials.json
```

### Step 3: Remove from Git History (5 min)

```bash
# Remove the exposed file from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/scripts/ee-credentials.json.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (WARNING: This rewrites history)
git push origin --force --all
git push origin --force --tags

# Clean up local refs
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

**ALTERNATIVE (Safer):** Use BFG Repo-Cleaner
```bash
# Download BFG
# https://rtyley.github.io/bfg-repo-cleaner/

# Remove the file
java -jar bfg.jar --delete-files ee-credentials.json.json

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push origin --force --all
```

---

## 🛡️ PREVENT FUTURE EXPOSURES (Do This Next - 10 minutes)

### Step 4: Update .gitignore

```bash
# Add to .gitignore
cat >> .gitignore << EOF

# Service Account Keys (NEVER COMMIT THESE!)
*credentials*.json
*-credentials.json
*.json.json
*service-account*.json
*serviceaccount*.json
key.json
keys/*.json

# Environment Files
.env
.env.*
!.env.example
!.env.template

EOF
```

### Step 5: Add Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check for potential secrets
if git diff --cached --name-only | grep -E '\.(json|env)$'; then
    echo "⚠️  WARNING: You're about to commit JSON or ENV files!"
    echo "   Make sure they don't contain secrets."
    echo ""
    echo "   Files:"
    git diff --cached --name-only | grep -E '\.(json|env)$'
    echo ""
    read -p "   Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Commit aborted"
        exit 1
    fi
fi

# Check for private keys
if git diff --cached | grep -i "PRIVATE KEY"; then
    echo "🚨 CRITICAL: Private key detected in commit!"
    echo "❌ Commit aborted"
    exit 1
fi

# Check for common secret patterns
if git diff --cached | grep -E "(api[_-]?key|secret|password|token).*[:=].*['\"]?[a-zA-Z0-9]{20,}"; then
    echo "⚠️  WARNING: Potential secret detected!"
    echo "❌ Commit aborted"
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Step 6: Install git-secrets

```bash
# Install git-secrets
# Windows (via Chocolatey)
choco install git-secrets

# Or download from: https://github.com/awslabs/git-secrets

# Initialize
git secrets --install
git secrets --register-aws

# Add custom patterns
git secrets --add 'PRIVATE KEY'
git secrets --add 'credentials'
git secrets --add '[a-zA-Z0-9]{32,}'
```

---

## 📊 DAMAGE ASSESSMENT

### What Was Exposed:
- ✅ Google Cloud Service Account Private Key
- ✅ Project ID: bhu-hack
- ✅ Service Account Email
- ✅ Client ID

### What Was NOT Exposed:
- ✅ WAQI API Token (in .env, not committed)
- ✅ Supabase credentials (in .env, not committed)
- ✅ Database passwords (in .env, not committed)

### Potential Impact:
- ❌ Anyone with the key can access your Google Earth Engine
- ❌ Potential unauthorized API usage
- ❌ Potential data access
- ❌ Potential cost implications

### Likelihood of Exploitation:
- **Medium** - File is in public repo
- **Low** - Requires knowledge of what to do with it
- **Time Sensitive** - The longer it's exposed, the higher the risk

---

## ✅ VERIFICATION CHECKLIST

After completing all steps:

- [ ] Old service account deleted/disabled
- [ ] New service account created
- [ ] New credentials file created (NOT in git)
- [ ] File removed from git history
- [ ] Force pushed to remote
- [ ] .gitignore updated
- [ ] Pre-commit hook installed
- [ ] git-secrets installed
- [ ] Backend tested with new credentials
- [ ] Old credentials confirmed non-functional

---

## 🔍 HOW TO CHECK IF YOU'RE SAFE

### Test 1: Check Git History
```bash
# This should return NOTHING
git log --all --full-history --source -- "*credentials*.json"
```

### Test 2: Check Remote Repository
```bash
# Go to GitHub/GitLab
# Search for: "PRIVATE KEY"
# Should find: 0 results
```

### Test 3: Test Old Credentials
```bash
# Try using old credentials (should FAIL)
# If it works, the key is still active - DELETE IT!
```

---

## 📞 IF YOU NEED HELP

### Google Cloud Support
- Console: https://console.cloud.google.com/support
- Phone: Check your GCP console for support number

### GitHub Support (if repo is on GitHub)
- https://support.github.com/
- Can help remove sensitive data from public repos

---

## 📝 INCIDENT REPORT

**Date Discovered:** March 24, 2026  
**Discovered By:** Kiro AI Security Audit  
**Exposure Duration:** Unknown (at least since commit f5d5aa6)  
**Action Taken:** [Fill in after completing steps]  
**Verification:** [Fill in after testing]  
**Status:** [OPEN / RESOLVED]

---

## 🎓 LESSONS LEARNED

1. **Never commit credentials** - Even in scripts folder
2. **Use .gitignore properly** - Add patterns BEFORE committing
3. **Use environment variables** - For all secrets
4. **Use secret managers** - Google Secret Manager, AWS Secrets Manager
5. **Scan before commit** - Use git-secrets or similar tools
6. **Regular audits** - Check what's in git periodically

---

## 🔐 BEST PRACTICES GOING FORWARD

### For Credentials:
1. Store in Google Secret Manager
2. Load at runtime from environment
3. Never hardcode in files
4. Rotate regularly (every 90 days)

### For Git:
1. Use pre-commit hooks
2. Use git-secrets
3. Review diffs before committing
4. Never force push without review

### For Team:
1. Train on security practices
2. Code review all commits
3. Automated security scanning
4. Incident response plan

---

**PRIORITY:** CRITICAL  
**ACTION REQUIRED:** IMMEDIATE  
**ESTIMATED TIME:** 30 minutes

**DO THIS NOW!**
