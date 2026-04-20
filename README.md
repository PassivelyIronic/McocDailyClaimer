# MCOC Daily Claimer

A Python script that automatically claims free rewards from the Marvel Contest of Champions webstore. It uses Playwright to navigate the site and runs on GitHub Actions, so it is free and works in the cloud without needing your computer to be on.

## Features
- Claims daily market points and crystals automatically.
- Runs every day at 18:05 UTC (20:05 CET).
- Sends a Telegram notification on success.
- Sends an error report with a screenshot if the script fails.

## Setup Instructions

1. **Fork the repository** to your own GitHub account.
2. **Create a Telegram Bot**:
   - Message `@BotFather` on Telegram to create a bot and get your **API Token**.
   - Send any message to your new bot.
   - Get your **Chat ID** by visiting: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`.
3. **Add GitHub Secrets**:
   In your forked repository, go to **Settings > Secrets and variables > Actions**. Create four **New repository secrets**:
   - `LOGIN_EMAIL`: Your Kabam account email.
   - `PASSWORD`: Your Kabam account password.
   - `TELEGRAM_TOKEN`: Your Telegram bot token.
   - `CHAT_ID`: Your Telegram chat ID.
4. **Enable Actions**: 
   Go to the **Actions** tab in your repository and click the button to enable workflows.

## Manual Test
To check if it works immediately:
- Go to the **Actions** tab.
- Select **Daily Claim Automation** from the left sidebar.
- Click **Run workflow** on the right side.
- Check your Telegram for a success message within 2 minutes.

## How it Works
The script logs into `store.playcontestofchampions.com`, scrolls through the store, and identifies items that have an active "Free" button. It ignores items already marked as "Sold Out."

## Disclaimer
This is an unofficial automation tool. Use it at your own risk. The author is not responsible for any issues with your Kabam account.
