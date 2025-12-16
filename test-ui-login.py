import asyncio
import sys
from playwright.async_api import async_playwright
import json

async def test_login_flow():
    """Test the complete login flow in the UI"""
    
    async with async_playwright() as p:
        print("=" * 50)
        print("Testing Login Flow in UI")
        print("=" * 50)
        print()
        
        # Launch browser
        print("[Step 1] Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate to frontend
            print("[Step 2] Navigating to frontend (http://localhost:4200)...")
            response = await page.goto("http://localhost:4200", wait_until="networkidle")
            
            if response.status != 200:
                print(f"❌ Failed to load page. Status: {response.status}")
                return False
            
            print("✓ Page loaded successfully")
            
            # Check if Login button exists
            print("[Step 3] Checking for Login button...")
            login_button = page.locator("button:has-text('Login')")
            count = await login_button.count()
            
            if count == 0:
                print("❌ Login button not found")
                await page.screenshot(path="/tmp/page_before_login.png")
                print("Screenshot saved: /tmp/page_before_login.png")
                return False
            
            print(f"✓ Found {count} Login button(s)")
            
            # Click Login button
            print("[Step 4] Clicking Login button...")
            await login_button.first.click()
            await page.wait_for_timeout(500)  # Wait for modal to open
            
            # Check if modal opened
            print("[Step 5] Verifying login modal opened...")
            modal = page.locator(".modal-content")
            if not await modal.is_visible():
                print("❌ Login modal did not open")
                await page.screenshot(path="/tmp/page_modal_fail.png")
                return False
            
            print("✓ Login modal opened")
            
            # Check for Test Login button
            print("[Step 6] Looking for 'Test Login' button...")
            test_login_btn = page.locator("button:has-text('Test Login')")
            if await test_login_btn.count() == 0:
                print("❌ Test Login button not found")
                # Try alternative selectors
                all_buttons = page.locator("button")
                button_count = await all_buttons.count()
                print(f"Found {button_count} total buttons on modal")
                for i in range(button_count):
                    text = await all_buttons.nth(i).text_content()
                    print(f"  Button {i}: {text}")
                await page.screenshot(path="/tmp/page_buttons.png")
                return False
            
            print("✓ Test Login button found")
            
            # Click Test Login button
            print("[Step 7] Clicking 'Test Login' button...")
            await test_login_btn.first.click()
            
            # Wait for authentication to complete
            print("[Step 8] Waiting for authentication...")
            await page.wait_for_timeout(2000)
            
            # Check console for errors
            print("[Step 9] Checking for console errors...")
            console_messages = []
            page.on("console", lambda msg: console_messages.append({"type": msg.type, "text": msg.text}))
            
            # Check if navigated to dashboard
            print("[Step 10] Verifying navigation to dashboard...")
            current_url = page.url
            print(f"Current URL: {current_url}")
            
            if "/dashboard" in current_url:
                print("✓ Successfully navigated to dashboard")
                
                # Check for dashboard content
                dashboard = page.locator(".dashboard-container")
                if await dashboard.is_visible():
                    print("✓ Dashboard content is visible")
                    
                    # Get page title
                    title = await page.title()
                    print(f"Page title: {title}")
                    
                    # Take screenshot
                    await page.screenshot(path="/tmp/dashboard_success.png")
                    print("Screenshot saved: /tmp/dashboard_success.png")
                    
                    return True
                else:
                    print("❌ Dashboard container not visible")
                    await page.screenshot(path="/tmp/dashboard_fail.png")
                    return False
            else:
                print("❌ Did not navigate to dashboard")
                await page.screenshot(path="/tmp/navigation_fail.png")
                
                # Check for error message
                error_msg = page.locator(".error-message")
                if await error_msg.is_visible():
                    error_text = await error_msg.text_content()
                    print(f"Error message visible: {error_text}")
                
                return False
                
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            await page.screenshot(path="/tmp/error_screenshot.png")
            return False
        finally:
            await browser.close()

async def main():
    print("\n" + "=" * 50)
    print("UI LOGIN FLOW TEST")
    print("=" * 50 + "\n")
    
    success = await test_login_flow()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ LOGIN FLOW TEST PASSED")
        print("=" * 50)
        return 0
    else:
        print("❌ LOGIN FLOW TEST FAILED")
        print("=" * 50)
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
