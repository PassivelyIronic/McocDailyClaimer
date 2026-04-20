# MCOC Daily Claimer

Automatyczny skrypt oparty na Pythonie i Playwright, który codziennie loguje się do sklepu internetowego Marvel Contest of Champions (MCOC) i odbiera darmowe nagrody (np. Daily Market Points, Daily/Weekly Crystals). 

Całość działa w chmurze dzięki **GitHub Actions** – skrypt uruchamia się samoczynnie w tle, jest w 100% darmowy i nie wymaga włączonego komputera. Po każdym uruchomieniu skrypt wysyła raport na Telegrama, a w razie błędu dołącza zrzut ekranu.

## Funkcje
* **W pełni automatyczny:** Działa według harmonogramu (domyślnie 20:05 polskiego czasu).
* **Inteligentny:** Klika tylko dostępne nagrody (ignoruje wyszarzone kafelki "SOLD OUT").
* **Powiadomienia Telegram:** Wiadomość o sukcesie (z liczbą klikniętych nagród) lub alert o błędzie ze zdjęciem przeglądarki, by łatwo namierzyć problem.
* **Bezpieczny:** Twoje dane logowania są przechowywane wyłącznie w szyfrowanych sekretach GitHuba.

---

## Jak uruchomić to na własnym koncie (Poradnik)

Aby użyć tego skryptu dla swojego konta Kabam, postępuj zgodnie z poniższymi krokami:

### 1. Zrób Fork repozytorium
Kliknij przycisk **Fork** w prawym górnym rogu tej strony, aby skopiować ten projekt na swoje własne konto GitHub.

### 2. Załóż bota na Telegramie (Powiadomienia)
1. Otwórz aplikację Telegram i znajdź bota o nazwie `@BotFather`.
2. Wyślij mu wiadomość `/newbot`, nadaj nazwę i skopiuj swój **API Token** (np. `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`).
3. Wyślij dowolną wiadomość do swojego nowo stworzonego bota (aby aktywować czat).
4. Otwórz w przeglądarce link: `https://api.telegram.org/bot<TWÓJ_TOKEN>/getUpdates` i poszukaj w tekście fragmentu `"chat":{"id":123456789`. Ta liczba to Twój **Chat ID**.

### 3. Skonfiguruj GitHub Secrets
Skrypt potrzebuje Twoich danych, aby móc działać. W swoim sforkowanym repozytorium wejdź w:
**Settings** -> **Secrets and variables** (po lewej stronie) -> **Actions**. 

Kliknij **New repository secret** i dodaj dokładnie te 4 zmienne:

| Nazwa (Name) | Wartość (Secret) |
| :--- | :--- |
| `LOGIN_EMAIL` | Twój e-mail używany do logowania w Kabam |
| `PASSWORD` | Twoje hasło do konta Kabam |
| `TELEGRAM_TOKEN` | Token bota z kroku 2 |
| `CHAT_ID` | Twój identyfikator czatu z kroku 2 |

### 4. Włącz GitHub Actions
GitHub domyślnie wyłącza automatyzacje w sforkowanych repozytoriach. 
1. Wejdź w zakładkę **Actions** na górnym pasku.
2. Kliknij zielony przycisk z napisem *"I understand my workflows, go ahead and enable them"*.

### 5. Przetestuj działanie
Aby nie czekać do wieczora, uruchom skrypt ręcznie:
1. W zakładce **Actions** wybierz z lewej strony **Daily Claim Automation**.
2. Kliknij szary przycisk **Run workflow** (po prawej stronie) i zatwierdź zielonym guzikiem.
3. Obserwuj swój telefon. W ciągu 1-2 minut powinieneś dostać wiadomość od swojego bota.

---

## Zmiana harmonogramu
Domyślnie skrypt uruchamia się codziennie 5 minut po pełnej rotacji sklepu. Jeśli chcesz zmienić godzinę, edytuj plik `.github/workflows/daily_claim.yml` i zmodyfikuj linijkę z harmonogramem `cron` (pamiętaj, że GitHub używa czasu UTC).

## Zastrzeżenie
Skrypt został stworzony w celach edukacyjnych i usprawniających codzienne zarządzanie kontem. Używaj na własną odpowiedzialność. Zmiany w kodzie HTML strony sklepu (redesign) mogą w przyszłości wymagać aktualizacji tzw. selektorów w pliku `main.py`.
