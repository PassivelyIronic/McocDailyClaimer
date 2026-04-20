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

def main():
    try:
        with sync_playwright() as p:
            # Uruchamiamy przeglądarkę
            browser = p.chromium.launch(headless=True)
            # Ustawiamy rozdzielczość i User-Agent (żeby strona nie myślała że to bot)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            print("1. Otwieranie strony głównej sklepu...")
            page.goto("https://store.playcontestofchampions.com/")
            page.wait_for_load_state('networkidle')
            
            print("2. Szukanie przycisku logowania...")
            # Szuka przycisku/linku zawierającego tekst "Log in" lub "Login"
            login_button = page.get_by_text("Log in", exact=False).first
            login_button.click()
            
            print("3. Logowanie na stronie Kabam...")
            # Wpisujemy email i hasło - te selektory [type="email"] są uniwersalne
            page.locator('input[type="email"]').fill(LOGIN_EMAIL)
            page.locator('input[type="password"]').fill(PASSWORD)
            page.locator('button[type="submit"]').click()
            
            print("4. Czekamy na powrót do sklepu...")
            # Czekamy, aż url znowu zmieni się na sklep (po zalogowaniu)
            page.wait_for_url("https://store.playcontestofchampions.com/**", timeout=30000)
            page.wait_for_load_state('networkidle')
            
            print("5. Przewijanie strony i szukanie darmowych nagród...")
            # Scrollujemy lekko w dół, żeby upewnić się, że wszystko się załadowało
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(3000) # Czekamy 3 sekundy
            
            # Szukamy wszystkich elementów zawierających słowo "Free"
            # Może to wymagać drobnej poprawki, jeśli gra używa grafiki zamiast tekstu
            free_buttons = page.get_by_text("Free", exact=False).all()
            
            if not free_buttons:
                print("Nie znaleziono przycisków 'Free'. Być może już odebrane, lub strona ładuje się wolniej.")
                send_telegram_message("⚠️ Skrypt zakończony, ale nie znaleziono żadnych darmowych nagród (przycisków 'Free').")
            else:
                claims_count = 0
                for btn in free_buttons:
                    try:
                        if btn.is_visible():
                            btn.click()
                            print("Kliknięto 'Free'!")
                            claims_count += 1
                            # WAŻNE: W wielu grach po kliknięciu "Free" wyskakuje okienko, gdzie trzeba kliknąć "Claim" lub "OK".
                            # Jeśli na tej stronie tak jest, musimy dodać tutaj kod klikający w to okienko, np:
                            # page.get_by_text("Claim", exact=False).first.click()
                            
                            page.wait_for_timeout(2000) # Przerwa między kliknięciami
                    except Exception as btn_err:
                        print(f"Pominięto przycisk z powodu błędu: {btn_err}")
                
                send_telegram_message(f"✅ <b>Sukces!</b> Dzisiejsza akcja MCOC wykonana. Kliknięto {claims_count} darmowych nagród.")

            browser.close()

    except Exception as e:
        error_msg = f"❌ <b>Błąd automatyzacji!</b>\n\nSkrypt napotkał problem:\n<code>{str(e)}</code>"
        send_telegram_message(error_msg)
        raise e

if __name__ == "__main__":
    main()