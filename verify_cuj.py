from playwright.sync_api import sync_playwright

def run_cuj(page):
    page.goto("http://localhost:8501")
    page.wait_for_timeout(2000)

    # We just want to check that the UI renders and no syntax error prevents it from running.
    # The loading spinners are visible only when an async AI operation is performed.
    # We will just verify it loaded properly.
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    import os
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    os.makedirs("/home/jules/verification/videos", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
