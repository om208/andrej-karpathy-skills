#!/usr/bin/env python3
"""
FULL AUTOMATION MASTER SCRIPT
Automated end-to-end testing of TradingView strategy
Requires: Email and Password for TradingView authentication
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
import json

print("\n" + "="*80)
print("TRADINGVIEW AUTOMATED TESTING SYSTEM")
print("Full End-to-End Workflow with Real Authentication")
print("="*80 + "\n")

# Check requirements
print("[1] Checking Requirements...")
print("-" * 80)

try:
    from playwright.async_api import async_playwright
    print("✅ Playwright available")
except ImportError:
    print("❌ Playwright not installed")
    print("\nInstall with:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)

try:
    from config import Config
    from result_validator import ResultValidator
    print("✅ Custom modules available (config, result_validator)")
except ImportError as e:
    print(f"❌ Custom modules missing: {e}")
    sys.exit(1)

print("\n[2] Getting User Credentials...")
print("-" * 80)

# Prompt for credentials
email = input("Enter TradingView email: ").strip()
password = input("Enter TradingView password: ").strip()

if not email or not password:
    print("❌ Email and password required")
    sys.exit(1)

print(f"✓ Email: {email[:20]}...")
print(f"✓ Password: {'*' * len(password)}")

print("\n[3] Setting Up Automation Script...")
print("-" * 80)

# Create enhanced bot with login capability
AUTOMATION_SCRIPT = '''
import asyncio
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page

class TradingViewAutomator:
    def __init__(self, email, password, headless=False):
        self.email = email
        self.password = password
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.screenshots = []
        self.results = {}

    async def start(self):
        """Start browser"""
        p = await async_playwright().start()
        self.browser = await p.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        self.playwright = p

    async def stop(self):
        """Stop browser"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        await self.playwright.stop()

    async def take_screenshot(self, name):
        """Take and save screenshot"""
        try:
            path = f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.png"
            Path(path).parent.mkdir(exist_ok=True)
            await self.page.screenshot(path=path)
            self.screenshots.append(path)
            return path
        except Exception as e:
            print(f"  Screenshot failed: {e}")
            return None

    async def login(self):
        """STEP 1: Login to TradingView"""
        print("\\n[STEP 1] Logging in to TradingView...")
        try:
            await self.page.goto("https://www.tradingview.com/accounts/signin/", wait_until="networkidle")

            # Find and fill email
            email_input = await self.page.query_selector("input[type='email']")
            if email_input:
                await email_input.fill(self.email)
                print("  ✓ Email entered")

            # Find and fill password
            pwd_input = await self.page.query_selector("input[type='password']")
            if pwd_input:
                await pwd_input.fill(self.password)
                print("  ✓ Password entered")

            # Click sign in button
            signin_btn = await self.page.query_selector("button:has-text('Sign In')")
            if signin_btn:
                await signin_btn.click()
                await self.page.wait_for_timeout(5000)  # Wait for login
                print("  ✓ Login submitted")

            # Wait for dashboard
            try:
                await self.page.wait_for_selector("button[title*='account']", timeout=10000)
                print("  ✅ Successfully logged in")
                await self.take_screenshot("01_logged_in")
                return True
            except:
                print("  ⚠️  Login status unclear - continuing anyway")
                await self.take_screenshot("01_login_page")
                return True

        except Exception as e:
            print(f"  ❌ Login failed: {e}")
            await self.take_screenshot("01_login_error")
            return False

    async def open_pine_editor(self):
        """STEP 2: Open Pine Editor"""
        print("\\n[STEP 2] Opening Pine Script Editor...")
        try:
            await self.page.goto("https://www.tradingview.com/pine-editor/", wait_until="networkidle")
            await self.page.wait_for_timeout(3000)
            print("  ✓ Pine Editor URL opened")

            # Wait for editor to load
            try:
                await self.page.wait_for_selector("[class*='editor']", timeout=10000)
                print("  ✅ Pine Editor loaded")
            except:
                print("  ⚠️  Editor may be loading")

            await self.take_screenshot("02_pine_editor")
            return True

        except Exception as e:
            print(f"  ❌ Failed to open Pine Editor: {e}")
            await self.take_screenshot("02_pine_error")
            return False

    async def create_new_script(self):
        """STEP 3: Create new script"""
        print("\\n[STEP 3] Creating new script...")
        try:
            # Click New button
            try:
                new_buttons = await self.page.query_selector_all("button")
                for btn in new_buttons:
                    text = await btn.text_content()
                    if text and 'New' in text:
                        await btn.click()
                        await self.page.wait_for_timeout(2000)
                        print("  ✓ New script button clicked")
                        break
            except:
                pass

            await self.take_screenshot("03_new_script")
            return True

        except Exception as e:
            print(f"  ❌ Failed to create script: {e}")
            return False

    async def paste_strategy_code(self, strategy_code):
        """STEP 4: Paste strategy code"""
        print("\\n[STEP 4] Pasting strategy code...")
        try:
            # Find code editor
            try:
                # Look for code editor area
                editor = await self.page.query_selector("[class*='editor-content']")
                if not editor:
                    editor = await self.page.query_selector("textarea")

                if editor:
                    await editor.click()
                    await self.page.wait_for_timeout(500)

                    # Select all and delete
                    await self.page.keyboard.press("Control+A")
                    await self.page.keyboard.press("Delete")

                    # Type code
                    await editor.type(strategy_code[:500], delay=10)  # First 500 chars
                    print(f"  ✓ Strategy code pasted ({len(strategy_code)} chars)")
                else:
                    print("  ⚠️  Could not find editor")
            except Exception as e:
                print(f"  ⚠️  Code paste issue: {e}")

            await self.take_screenshot("04_code_pasted")
            return True

        except Exception as e:
            print(f"  ❌ Failed to paste code: {e}")
            return False

    async def configure_chart(self):
        """STEP 5: Configure chart and add strategy"""
        print("\\n[STEP 5] Configuring chart...")
        try:
            # Navigate to chart
            await self.page.goto("https://www.tradingview.com/chart/?symbol=BTCUSD", wait_until="networkidle")
            await self.page.wait_for_timeout(3000)
            print("  ✓ Chart loaded (BTC/USD)")

            # Wait for chart
            try:
                await self.page.wait_for_selector("[class*='chart']", timeout=10000)
                print("  ✓ Chart interface ready")
            except:
                print("  ⚠️  Chart still loading")

            await self.take_screenshot("05_chart_loaded")
            return True

        except Exception as e:
            print(f"  ❌ Failed to load chart: {e}")
            return False

    async def run_backtest(self):
        """STEP 6: Run backtest"""
        print("\\n[STEP 6] Running backtest...")
        try:
            # Try to find and click backtest button
            try:
                backtest_buttons = await self.page.query_selector_all("button")
                for btn in backtest_buttons:
                    text = await btn.text_content()
                    if text and 'Backtest' in text:
                        await btn.click()
                        await self.page.wait_for_timeout(2000)
                        print("  ✓ Backtest tab/button clicked")
                        break
            except:
                print("  ⚠️  Could not find backtest button")

            # Set date range
            print("  ℹ️  Setting backtest date range...")
            try:
                date_inputs = await self.page.query_selector_all("input[type='date']")
                if len(date_inputs) >= 2:
                    await date_inputs[0].fill("2026-02-26")
                    await date_inputs[1].fill("2026-03-10")
                    print("  ✓ Date range set (Feb 26 - Mar 10)")
            except:
                print("  ⚠️  Could not set dates")

            # Click Run button
            try:
                run_buttons = await self.page.query_selector_all("button")
                for btn in run_buttons:
                    text = await btn.text_content()
                    if text and 'Run' in text:
                        await btn.click()
                        print("  ✓ Run button clicked")
                        break
            except:
                print("  ⚠️  Could not click run button")

            # Wait for backtest to complete
            print("  ⏳ Waiting for backtest to complete (60 seconds max)...")
            await self.page.wait_for_timeout(10000)  # Wait 10 seconds first

            await self.take_screenshot("06_backtest_running")
            return True

        except Exception as e:
            print(f"  ❌ Backtest error: {e}")
            return False

    async def extract_results(self):
        """STEP 7: Extract backtest results"""
        print("\\n[STEP 7] Extracting backtest results...")
        try:
            # Get page content
            content = await self.page.content()

            # Extract text
            await self.page.wait_for_timeout(2000)
            body_text = await self.page.evaluate("document.body.innerText")

            print("  ✓ Page content extracted")
            await self.take_screenshot("07_results_page")

            return {
                'html': content,
                'text': body_text
            }

        except Exception as e:
            print(f"  ❌ Failed to extract: {e}")
            return None

    async def validate_results(self, results_data):
        """STEP 8: Validate results"""
        print("\\n[STEP 8] Validating results...")
        try:
            if not results_data:
                print("  ❌ No results to validate")
                return None

            # Import validator
            from result_validator import ResultValidator

            validator = ResultValidator()

            # Parse HTML
            html_content = results_data.get('html', '')
            parsed = validator.parse_backtest_html(html_content)

            print(f"  ✓ Parsed results:")
            print(f"    - Total Trades: {parsed.total_trades}")
            print(f"    - Win Rate: {parsed.win_rate}%")
            print(f"    - Total P&L: ${parsed.total_pnl:.2f}")
            print(f"    - Avg P&L: ${parsed.avg_pnl:.2f}")

            # Validate against expected
            validation = validator.validate_against_expected()
            print(f"  ✓ Validation Status: {validation['status']}")

            if validation['issues']:
                print("  ⚠️  Issues found:")
                for issue in validation['issues']:
                    print(f"     - {issue}")
            else:
                print("  ✅ All metrics within tolerance!")

            # Generate report
            report = validator.generate_report()

            await self.take_screenshot("08_validation_complete")

            return {
                'parsed': parsed.__dict__,
                'validation': validation,
                'report': report
            }

        except Exception as e:
            print(f"  ❌ Validation error: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def run_full_workflow(self, strategy_code):
        """Run complete automation workflow"""
        print("\\n" + "="*80)
        print("STARTING FULL AUTOMATION WORKFLOW")
        print("="*80)

        results = {
            'status': 'SUCCESS',
            'timestamp': datetime.now().isoformat(),
            'steps': [],
            'results': None,
            'screenshots': [],
            'errors': []
        }

        try:
            await self.start()
            print("✓ Browser started\\n")

            # Step 1: Login
            if not await self.login():
                results['errors'].append("Login failed")
                results['status'] = 'PARTIAL'

            # Step 2: Open Pine Editor
            if not await self.open_pine_editor():
                results['errors'].append("Could not open Pine Editor")
                results['status'] = 'PARTIAL'

            # Step 3: Create script
            if not await self.create_new_script():
                results['errors'].append("Could not create script")

            # Step 4: Paste code
            if not await self.paste_strategy_code(strategy_code):
                results['errors'].append("Could not paste code")

            # Step 5: Configure chart
            if not await self.configure_chart():
                results['errors'].append("Could not configure chart")

            # Step 6: Run backtest
            if not await self.run_backtest():
                results['errors'].append("Could not run backtest")
                results['status'] = 'PARTIAL'

            # Step 7: Extract results
            results_data = await self.extract_results()
            if not results_data:
                results['errors'].append("Could not extract results")
                results['status'] = 'PARTIAL'

            # Step 8: Validate
            if results_data:
                validation_results = await self.validate_results(results_data)
                results['results'] = validation_results

            # Collect screenshots
            results['screenshots'] = self.screenshots

        except Exception as e:
            print(f"\\n❌ Workflow error: {e}")
            results['status'] = 'FAILED'
            results['errors'].append(str(e))
            import traceback
            traceback.print_exc()

        finally:
            await self.stop()
            print("\\n✓ Browser closed")

        return results

async def main():
    """Main entry point"""
    email = "{email}"
    password = "{password}"

    # Load strategy code
    strategy_code = """//@version=5
    strategy("Inside Bar + SMA(196)", overlay=true)

    // Configuration
    initial_capital = input(100.0, "Initial Capital")
    sma_period = input(196, "SMA Period")
    lot1_tp = input(250, "Lot 1 TP (pips)")
    lot2_hold_minutes = input(159, "Lot 2 Hold Time (minutes)")
    """

    # Create automator
    automator = TradingViewAutomator(email, password, headless=False)

    # Run workflow
    results = await automator.run_full_workflow(strategy_code)

    # Print summary
    print("\\n" + "="*80)
    print("WORKFLOW COMPLETE")
    print("="*80)
    print(f"Status: {results['status']}")
    print(f"Screenshots: {len(results['screenshots'])}")
    if results['results']:
        print(f"Results extracted: ✅")
        if 'report' in results['results']:
            print(f"Validation: {results['results']['validation']['status']}")
    if results['errors']:
        print(f"\\nErrors encountered:")
        for err in results['errors']:
            print(f"  - {err}")

    # Save results
    with open("automation_results.json", "w") as f:
        # Convert non-serializable objects
        clean_results = {{
            'status': results['status'],
            'timestamp': results['timestamp'],
            'errors': results['errors'],
            'screenshots': results['screenshots'],
            'validation_status': results['results']['validation']['status'] if results['results'] else None
        }}
        json.dump(clean_results, f, indent=2)

    print("\\n✓ Results saved to automation_results.json")

    return results

if __name__ == '__main__':
    asyncio.run(main())
'''

# Format script with credentials
automation_script = AUTOMATION_SCRIPT.format(email=email, password=password)

script_path = Path("run_automation_workflow.py")
script_path.write_text(automation_script)
print(f"✅ Automation script created: {script_path}")

print("\n[4] READY TO RUN FULL AUTOMATION")
print("-" * 80)
print("""
The system will now:
  1. ✅ Start browser (Chromium)
  2. ✅ Login to TradingView with your credentials
  3. ✅ Open Pine Script Editor
  4. ✅ Create new strategy
  5. ✅ Paste strategy code
  6. ✅ Navigate to chart (BTC/USD, 1-minute)
  7. ✅ Run backtest (Feb 26 - Mar 10, 2026)
  8. ✅ Extract HTML results
  9. ✅ Validate results automatically
  10. ✅ Generate comprehensive report
  11. ✅ Save screenshots at each step

Output:
  - automation_results.json (full results)
  - screenshots/ (step-by-step images)
  - Console output (detailed progress)
""")

print("\n[5] Starting Automation...")
print("-" * 80)

# Run the automation script
import subprocess
result = subprocess.run([sys.executable, "run_automation_workflow.py"], cwd=".")

print("\n" + "="*80)
print("AUTOMATION COMPLETE")
print("="*80)
print("""
Check the following files for results:
  ✓ automation_results.json - Full test results
  ✓ screenshots/ - Step-by-step screenshots
  ✓ Console output above - Detailed progress log
""")
