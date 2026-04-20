import os
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Błąd powiadomienia: {e}")

def send_telegram_photo(message, photo_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {"chat_id": CHAT_ID, "caption": message, "parse_mode": "HTML"}
    try:
        with open(photo_path, 'rb') as photo:
            requests.post(url, data=payload, files={'photo': photo})
    except Exception as e:
        print(f"Błąd wysyłania zdjęcia: {e}")

def main():
    page = None
    browser = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            print("1. Otwieranie strony głównej sklepu...")
            page.goto("https://store.playcontestofchampions.com/")
            page.wait_for_load_state('networkidle')
            
            print("2. Klikanie przycisku LOGIN na stronie głównej...")
            page.locator('.button-login').first.click()
            
            print("3. Logowanie na stronie Kabam...")
            page.wait_for_timeout(3000) 
            
            email_field = page.locator('input[name="email"], input[type="email"]').first
            email_field.wait_for(state="visible", timeout=15000)
            email_field.fill(LOGIN_EMAIL)
            
            password_field = page.locator('input[name="password"]').first
            password_field.wait_for(state="visible", timeout=15000)
            password_field.fill(PASSWORD)
            
            print("Klikam przycisk zatwierdzający (Submit)...")
            page.locator('#submit-button').click()
            
            print("4. Czekamy na powrót do sklepu...")
            page.wait_for_url("https://store.playcontestofchampions.com/**", timeout=30000)
            page.wait_for_load_state('networkidle')
            
            print("5. Przewijanie strony i szukanie darmowych nagród...")
            page.wait_for_selector('.item-card', timeout=15000)
            
            # scroll donw
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(3000) 
            
            free_buttons = page.locator('.item-action-free .primary-button').all()
            
            if not free_buttons:
                print("Nie znaleziono aktywnych przycisków 'FREE'.")
                send_telegram_message("⚠️ Skrypt zakończony. Sklep załadowany, ale nie było żadnych darmowych nagród do odebrania (wszystko to SOLD OUT).")
            else:
                claims_count = 0
                for btn in free_buttons:
                    try:
                        if btn.is_visible():
                            btn.scroll_into_view_if_needed()
                            page.wait_for_timeout(500)
                            
                            btn.click(force=True)
                            print("Kliknięto prawdziwy przycisk 'Free'!")
                            claims_count += 1
                            
                            page.wait_for_timeout(4000)
                    except Exception as btn_err:
                        print(f"Pominięto przycisk z powodu błędu: {btn_err}")
                
                send_telegram_message(f"✅ <b>Sukces!</b> Dzisiejsza akcja MCOC wykonana. Odebrano {claims_count} darmowych nagród!")

            browser.close()

    except Exception as e:
        error_msg = f"❌ <b>Błąd automatyzacji!</b>\n\nCoś poszło nie tak:\n<code>{str(e)}</code>"
        print(f"Wystąpił błąd: {e}")
        
        if page:
            try:
                screenshot_path = "error_screenshot.png"
                page.screenshot(path=screenshot_path)
                send_telegram_photo(error_msg, screenshot_path)
            except Exception as screenshot_err:
                print(f"Nie udało się zrobić screena: {screenshot_err}")
                send_telegram_message(error_msg)
        else:
            send_telegram_message(error_msg)
            
        if browser:
            browser.close()
        raise e

if __name__ == "__main__":
    main()