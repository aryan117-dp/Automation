import json
from playwright.sync_api import sync_playwright

def post_instagram_reel(json_file_path, video_path, caption_text):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False) 
        context = browser.new_context()

        # 1. Load and inject cookies
        with open(json_file_path, 'r') as f:
            raw_cookies = json.load(f)
            
        formatted_cookies = []
        for cookie in raw_cookies:
            clean_cookie = {
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                'domain': cookie.get('domain'),
                'path': cookie.get('path', '/'),
                'secure': cookie.get('secure', True),
                'httpOnly': cookie.get('httpOnly', True),
                'sameSite': 'Lax'
            }
            if 'expirationDate' in cookie:
                clean_cookie['expires'] = cookie['expirationDate']
            formatted_cookies.append(clean_cookie)

        context.add_cookies(formatted_cookies)
        
        # 2. Go to Instagram
        page = context.new_page()
        page.goto("https://www.instagram.com/")
        page.wait_for_selector("svg[aria-label='Home']", timeout=15000)
        print("Logged in successfully!")

        # ---------------------------------------------------------
        # NEW FIX 1: Handle the "Turn on Notifications" popup
        # ---------------------------------------------------------
        print("Checking for Notifications popup...")
        try:
            # Waits up to 5 seconds for the "Not Now" button to appear
            page.get_by_role("button", name="Not Now").click(timeout=5000)
            print("Dismissed notifications popup.")
        except:
            print("No notifications popup appeared. Moving on.")

        # 3. Click the "Create" button on the sidebar
        print("Clicking Create...")
        page.locator("svg[aria-label='New post']").click()

        # 4. Upload the Video File
        print("Uploading video...")
        page.wait_for_selector("input[type='file']", state="attached")
        page.locator("input[type='file']").set_input_files(video_path)

        # ---------------------------------------------------------
        # NEW FIX 2: Handle the "Video posts are now shared as reels" popup
        # ---------------------------------------------------------
        print("Checking for Reels 'OK' popup...")
        try:
            # Waits up to 5 seconds for the "OK" button
            page.get_by_role("button", name="OK").click(timeout=5000)
            print("Clicked OK on Reels info popup.")
        except:
            print("No Reels info popup appeared. Moving on.")

        # 5. Handle Video Ratio / Formatting (Clicking 'Next')
        print("Clicking Next (Crop step)...")
        page.get_by_role("button", name="Next").click()

        print("Clicking Next (Edit step)...")
        page.get_by_role("button", name="Next").click()

        # 6. Add Caption
        print("Writing caption...")
        page.wait_for_selector('div[aria-label="Write a caption..."]')
        page.locator('div[aria-label="Write a caption..."]').fill(caption_text)

        # 7. Share the Post
        print("Sharing...")
        page.get_by_role("button", name="Share").click()

        # 8. Wait for completion
        print("Waiting for upload to finish (this might take a minute)...")
        page.get_by_text("Your post has been shared.").wait_for(timeout=60000)
        
        print("Reel posted successfully!")
        
        page.wait_for_timeout(3000) 
        browser.close()

if __name__ == "__main__":
    post_instagram_reel(
        json_file_path="insta_cookie.json", 
        video_path="output.mp4", 
        caption_text="#fyp #memes #funnyreels"
    )
