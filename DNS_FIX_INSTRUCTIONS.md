# 🔧 DNS Fix for Supabase Access in India

## Problem
Supabase is blocked/restricted in India, causing DNS resolution failures.

## Solution
Change your DNS to Google DNS or Cloudflare DNS to bypass the block.

---

## Option 1: Run PowerShell Script (Easiest)

1. **Open PowerShell as Administrator**
   - Right-click Start → Windows PowerShell (Admin)

2. **Run the fix script:**
   ```powershell
   cd "C:\Users\24r11\OneDrive\Desktop\breath analyser\Breath-Analyzser"
   .\fix_dns.ps1
   ```

3. **Restart backend:**
   - The script will change DNS to Google DNS (8.8.8.8)
   - Flush DNS cache
   - Test Supabase connection

---

## Option 2: Manual DNS Change (Windows)

1. **Open Network Settings**
   - Press `Win + R`
   - Type: `ncpa.cpl`
   - Press Enter

2. **Select your active network adapter**
   - Right-click → Properties

3. **Configure IPv4**
   - Select "Internet Protocol Version 4 (TCP/IPv4)"
   - Click Properties

4. **Change DNS servers:**
   - Select "Use the following DNS server addresses"
   - Preferred DNS: `8.8.8.8`
   - Alternate DNS: `8.8.4.4`
   - Click OK

5. **Flush DNS cache:**
   ```cmd
   ipconfig /flushdns
   ```

---

## Option 3: Use Cloudflare DNS (Alternative)

Same steps as above, but use:
- Preferred DNS: `1.1.1.1`
- Alternate DNS: `1.0.0.1`

---

## Option 4: Use VPN

If DNS change doesn't work:
1. Install a VPN (ProtonVPN, Windscribe - free options)
2. Connect to a server outside India
3. Restart backend

---

## Verify Fix

After changing DNS, test the connection:

```powershell
# Test DNS resolution
nslookup db.tmavkmymbdcmugunjtle.supabase.co

# Test connection
ping db.tmavkmymbdcmugunjtle.supabase.co
```

If you see an IP address, DNS is working!

---

## Restart Backend

After fixing DNS:

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Then refresh localhost:5174 and authentication should work!

---

## Quick Test

```bash
cd backend
python test_db.py
```

Should show: `✅ Database connected!`

---

## If Still Not Working

1. **Restart your computer** (to apply DNS changes)
2. **Disable antivirus/firewall temporarily**
3. **Use mobile hotspot** (bypasses ISP restrictions)
4. **Contact your ISP** (they might be blocking Supabase)

---

**Status:** DNS fix ready to apply!
