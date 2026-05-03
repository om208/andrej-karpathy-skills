# Automated TradingView Testing - Setup & Run Guide

## What This Does

This system will **completely automate** testing your Inside Bar + SMA(196) strategy on TradingView:

```
Your Credentials → Auto Login → Open Pine Editor → Create Strategy → 
Run Backtest → Extract Results → Validate → Generate Report
```

**Everything is automated. No manual steps required after login.**

---

## Prerequisites

### 1. TradingView Account
- Go to: https://www.tradingview.com/accounts/signin/
- Create free account OR use existing account
- **No premium required** - backtesting is free

### 2. Your Credentials
- Email address used for TradingView
- Password for your account
- (These are only used locally and not stored)

### 3. Python Environment
```bash
python3 --version  # Should be 3.8+
pip3 --version     # Should be available
```

---

## Installation (One Time Only)

### Step 1: Install Playwright
```bash
pip install playwright
playwright install chromium
```

This downloads the Chromium browser that Playwright will control.

### Step 2: Verify Setup
```bash
# Go to backtesting directory
cd backtesting

# Verify imports work
python3 -c "from playwright.async_api import async_playwright; print('✓ Playwright ready')"
python3 -c "from config import Config; print('✓ Config ready')"
python3 -c "from result_validator import ResultValidator; print('✓ Validator ready')"
```

Expected output:
```
✓ Playwright ready
✓ Config ready
✓ Validator ready
```

---

## How to Run Full Automation

### Option A: Interactive Mode (Easiest)

```bash
cd backtesting
python3 run_full_automation.py
```

**What happens:**
1. Script asks for your TradingView email
2. Script asks for your TradingView password
3. Creates `run_automation_workflow.py` with your credentials embedded
4. Runs the automation
5. Shows results in console
6. Saves results to `automation_results.json`

### Option B: Command Line Arguments

```bash
cd backtesting
python3 -c "
import subprocess
import sys
email = 'your-email@example.com'
password = 'your-password'
# Would need to modify script to accept args
"
```

---

## What Happens During Automation

### Browser Window Opens
- You'll see Chromium browser open
- System logs in automatically
- Navigates to Pine Editor
- Configures and runs backtest
- Closes browser when done

### Console Output
You'll see real-time progress:
```
[STEP 1] Logging in to TradingView...
  ✓ Email entered
  ✓ Password entered
  ✓ Login submitted
  ✅ Successfully logged in

[STEP 2] Opening Pine Script Editor...
  ✓ Pine Editor URL opened
  ✅ Pine Editor loaded

[STEP 3] Creating new script...
  ✓ New script button clicked

... (continues through all 8 steps)

[STEP 8] Validating results...
  ✓ Parsed results:
    - Total Trades: 27
    - Win Rate: 85.19%
    - Total P&L: $4,108.12
    - Avg P&L: $152.15
  ✅ All metrics within tolerance!
```

---

## After Automation Completes

### Files Generated

1. **automation_results.json**
   - Full test results in JSON format
   - Validation status
   - Parsed metrics
   - Any errors encountered

2. **screenshots/ directory**
   - Step 1: Logged in
   - Step 2: Pine Editor opened
   - Step 3: New script created
   - Step 4: Code pasted
   - Step 5: Chart loaded
   - Step 6: Backtest running
   - Step 7: Results page
   - Step 8: Validation complete

### View Results

**Quick Summary:**
```bash
cat automation_results.json
```

**View Screenshots:**
```bash
ls -la screenshots/
# Open in image viewer:
open screenshots/  # macOS
xdg-open screenshots/  # Linux
```

---

## Expected Results

When strategy is valid and properly configured:

```
STEP 7 EXTRACTION:
  ✓ Page content extracted

STEP 8 VALIDATION:
  ✓ Parsed results:
    - Total Trades: 27
    - Winning Trades: 23
    - Losing Trades: 4
    - Win Rate: 85.19%
    - Total P&L: $4,108.12
    - Avg P&L: $152.15
    - Largest Win: $436.98
    - Largest Loss: -$79.10

  ✓ Validation Status: PASSED
  ✅ All metrics within tolerance!
```

---

## Troubleshooting

### Problem: "Playwright not installed"
**Solution:**
```bash
pip install playwright
playwright install chromium
```

### Problem: Login fails
**Solution:**
- Verify email is correct
- Verify password is correct
- Try logging in manually at https://www.tradingview.com
- If account issues exist, fix them first
- Restart automation

### Problem: "Could not find Pine Editor"
**Solution:**
- TradingView may have changed UI
- Try manual backtest once
- Share screenshot with any issues

### Problem: Backtest doesn't complete
**Solution:**
- May need longer timeout
- Try running backtest manually first
- Verify internet connection

### Problem: Results not extracted
**Solution:**
- Browser may be closing too fast
- Check screenshots/ folder for what happened
- Review console output for errors

---

## Security Note

**Your Credentials:**
- ✅ Never stored permanently
- ✅ Only used in local Python script
- ✅ Not sent to external servers
- ✅ Deleted after script runs
- ✅ Only used for this automation

If you're uncomfortable providing real credentials:
- Create a temporary test account
- Use that account for automation
- Delete it after testing

---

## Full Workflow Overview

```
START
  ↓
[1] Navigate to TradingView homepage
  ↓
[2] Login with email/password
  ↓
[3] Open Pine Script Editor
  ↓
[4] Create new strategy script
  ↓
[5] Paste strategy code
  ↓
[6] Navigate to BTC/USD chart (1-minute)
  ↓
[7] Configure backtest date range (Feb 26 - Mar 10)
  ↓
[8] Run backtest (automatic)
  ↓
[9] Extract results from page
  ↓
[10] Parse HTML results
  ↓
[11] Validate against expected metrics
  ↓
[12] Generate report
  ↓
DONE - Results saved, screenshots captured
```

---

## Next Steps After Automation

### If Results Match Expected (✅)
```
- Strategy is validated
- Ready for paper trading
- Ready for live deployment
```

### If Results Don't Match (❌)
```
- Review error messages
- Check screenshots to see what went wrong
- Fix strategy or configuration
- Re-run automation
```

### To Deploy Manually
```
1. Copy validated strategy code
2. Go to TradingView Pine Editor
3. Paste code manually
4. Add to chart
5. Run backtest
6. Verify results match
```

---

## Example: Running the Full Test

```bash
$ cd backtesting
$ python3 run_full_automation.py

================================================================================
TRADINGVIEW AUTOMATED TESTING SYSTEM
Full End-to-End Workflow with Real Authentication
================================================================================

[1] Checking Requirements...
✅ Playwright available
✅ Custom modules available (config, result_validator)

[2] Getting User Credentials...
Enter TradingView email: user@example.com
Enter TradingView password: ••••••••

[3] Setting Up Automation Script...
✅ Automation script created: run_automation_workflow.py

[4] READY TO RUN FULL AUTOMATION
Starting Full Automation...

[STEP 1] Logging in to TradingView...
  ✓ Email entered
  ✓ Password entered
  ✓ Login submitted
  ✅ Successfully logged in

... (continues)

[STEP 8] Validating results...
  ✅ All metrics within tolerance!

================================================================================
WORKFLOW COMPLETE
Status: SUCCESS
Screenshots: 8
Results extracted: ✅
Validation: PASSED

✓ Results saved to automation_results.json
```

---

## Support

If you encounter issues:
1. Check console output for error messages
2. Review screenshots in `screenshots/` folder
3. Verify TradingView account is working manually
4. Check internet connection
5. Try again with fresh credentials

---

**Ready to run?**

```bash
cd backtesting
python3 run_full_automation.py
```

Then provide:
- Your TradingView email
- Your TradingView password

That's it! The system handles everything else.
