# KUMSIYAT Telegram bot — starter package

This package contains the first working text-and-button version of the bot.

## Important
- No bot token is included. Keep your token private.
- Set the new/current token as an environment variable named `BOT_TOKEN` on the hosting service.
- Do not paste the token into chats or public files.
- Payment buttons are placeholders. They do not accept money yet.
- Product images and the approved KUMSI photo are not embedded yet; they must be added after the image files are available.

## Run
1. Install Python 3.10+.
2. Install dependencies: `pip install -r requirements.txt`
3. Set `BOT_TOKEN` in the hosting service's secret/environment-variable settings.
4. Start: `python bot.py`

The `/course`, `/suppliers`, `/currency`, and `/bundle` commands currently open the main menu. The inline buttons open the corresponding product pages.
