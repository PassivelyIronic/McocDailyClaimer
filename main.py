import os
import requests
from playwright.sync_api import sync_playwright

# Pobieranie danych z ukrytych zmiennych środowiskowych (GitHub Secrets)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_telegram_message(message):
    """Funkcja wysyłająca wiadomość na Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Błąd podczas wysyłania powiadomienia na Telegram: {e}")

def main():
    try:
        # Uruchomienie przeglądarki w trybie ukrytym (headless)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            print("Otwieranie strony...")
            # TODO: Wpisz adres strony logowania
            page.goto("https://TUTAJ_WPISZ_ADRES_STRONY.com/login")
            
            print("Logowanie...")
            # TODO: Podmień 'input[name="email"]' na właściwy selektor pola loginu
            page.fill('input[name="email"]', LOGIN_EMAIL)
            
            # TODO: Podmień 'input[name="password"]' na właściwy selektor pola hasła
            page.fill('input[name="password"]', PASSWORD)
            
            # TODO: Podmień 'button[type="submit"]' na selektor przycisku logowania
            page.click('button[type="submit"]')
            
            # Czekamy, aż strona załaduje się po zalogowaniu
            page.wait_for_load_state('networkidle')
            
            print("Przewijanie strony...")
            # Przewijanie na sam dół strony
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000) # Czekamy 2 sekundy dla pewności
            
            print("Klikanie przycisku docelowego...")
            # TODO: Podmień 'button#claim' na selektor przycisku, który chcesz kliknąć
            page.click('button#claim')
            
            # Zamykamy przeglądarkę
            browser.close()
            
            # Jeśli wszystko się udało, wysyłamy powiadomienie
            send_telegram_message("✅ <b>Sukces!</b> Dzisiejsza akcja (McocDailyClaimer) została wykonana pomyślnie.")
            print("Zakończono pełnym sukcesem.")

    except Exception as e:
        # W razie jakiegokolwiek błędu, łapiemy go i wysyłamy na telefon
        error_msg = f"❌ <b>Błąd automatyzacji!</b>\n\nCoś poszło nie tak:\n<code>{str(e)}</code>"
        send_telegram_message(error_msg)
        print(f"Wystąpił błąd: {e}")
        # Wyrzucamy błąd dalej, aby GitHub Actions zaznaczył ten przebieg jako "Failed"
        raise e

if __name__ == "__main__":
    main()