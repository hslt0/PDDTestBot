import time
from playwright.sync_api import sync_playwright

def solve_test(start_theme=10, end_theme=149):
    with sync_playwright() as p:
        print("Connecting to Edge...")
        browser_main = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        ctx_main = browser_main.contexts[0]
        page_main = ctx_main.pages[0] if ctx_main.pages else ctx_main.new_page()
        
        browser_test = p.chromium.launch(headless=True)
        
        for theme in range(start_theme, end_theme + 1):
            part = 1
            while True:
                url = f"https://vodiy.ua/pdr/test/?complect=6&theme={theme}&part={part}"
                print(f"\n>>> Theme {theme}, Page {part}")
                page_main.goto(url)
                
                try:
                    page_main.wait_for_selector(".ticketpage", timeout=10000)
                except:
                    print(f"Page timeout, skipping...")
                    break

                is_empty = page_main.locator(".empty-state-v2").is_visible()
                questions_locator = page_main.locator(".ticketpage_ul > li")
                
                if is_empty or questions_locator.count() == 0:
                    print(f"Theme {theme} (part {part}) is empty. Skipping...")
                    break # Переходимо до наступної ТЕМИ

                questions = questions_locator.all()
                print(f"Found {len(questions)} questions.")

                for i in range(len(questions)):
                    radios = page_main.locator(f".ticketpage_ul > li:nth-child({i+1}) input[type='radio']").all()
                    aids = [radio.get_attribute("data-aid") for radio in radios]
                    
                    correct_aid = None
                    print(f"Q{i+1}", end=" ", flush=True)
                    
                    for aid in aids:
                        ctx_guess = browser_test.new_context()
                        page_guess = ctx_guess.new_page()
                        try:
                            page_guess.goto(url)
                            with page_guess.expect_response(lambda r: "/loganswer/" in r.url, timeout=5000) as resp:
                                page_guess.locator(f"input[data-aid='{aid}']").dispatch_event("click")
                            
                            if resp.value.json().get("is_correct"):
                                correct_aid = aid
                                ctx_guess.close()
                                break
                        except: pass
                        ctx_guess.close()
                    
                    if correct_aid:
                        page_main.locator(f"input[data-aid='{correct_aid}']").dispatch_event("click")
                        print("✔", end=" ", flush=True)
                        time.sleep(0.3)
                    else:
                        print("✖", end=" ", flush=True)

                next_exists = page_main.locator(f"a[href*='part={part + 1}']").count() > 0
                if not next_exists:
                    break
                part += 1
                
        browser_test.close()
        browser_main.disconnect()

if __name__ == "__main__":
    solve_test(start_theme=121, end_theme=149)