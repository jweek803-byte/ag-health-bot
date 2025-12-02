# Центр Здоровья AG - Telegram Bot

## Overview
A fully-featured Telegram bot for "Центр Здоровья AG" (AG Health Center) with Russian-language interface. The bot provides product catalog, appointment booking, health recommendations, and admin notifications.

## Project Structure
- `bot.py` - Main bot application with all features
- `users.json` - User database (auto-created)
- `post_index.json` - Daily post tracking
- Image assets: `eye.jpg`, `expert.jpg`, `hydrogen.jpg`, `belt.jpg`, `relax.jpg`, `kenta.jpg`
- `.env` - Environment variables (contains TELEGRAM_BOT_TOKEN)

## How to Run
The bot runs automatically via the configured workflow: `python bot.py`
- Uses polling to receive messages from Telegram
- Runs 24/7 with automatic restart

## Features
✅ **6-Item Product Catalog**
- Массажёр для глаз (Eye Massager)
- Health Expert 25 (Physio Device)
- Водородная колба (Hydrogen Generator)
- Лазерный пояс Body Belt (Laser Belt)
- Турмалиновый ковёр Relax (Tourmaline Mat)
- Kenta (Shockwave Massager)

✅ **10 Health Conditions Database**
- Артроз, Артрит, Диабет, Катаракта, Бессонница
- Головные боли, Варикоз, Лимфостаз, Остеохондроз, Жировой гепатоз
- Each with symptoms, consequences, and equipment recommendations

✅ **7-Day Appointment Booking System**
- Hourly slots 9am-4pm
- Date and time selection
- Admin notifications on bookings

✅ **Order System**
- One-click ordering for products
- Admin alerts with customer info
- User database tracking

✅ **30-Day Content Calendar**
- Daily educational posts for channel
- Auto-scheduled posting at 10:00
- Topics: health tips, product benefits, lifestyle advice

✅ **Channel Integration**
- Link to https://t.me/AG_HealthCenter
- Subscription prompts in bot

## Configuration
- **Admin ID:** 1690527494
- **Channel:** @AG_HealthCenter
- **Token:** TELEGRAM_BOT_TOKEN (stored in secrets)

## Dependencies
- pytelegrambotapi (telebot)
- python-dotenv

## Status
✅ **PRODUCTION READY**
- All features implemented and tested
- Bot is stable and running 24/7
- Ready for deployment

## Recent Changes (December 1, 2025)
- Fixed file corruption issues
- Removed unused pytz dependencies
- Cleaned up scheduler code
- All features verified and working

## Next Steps
1. Publish the project to make it live with permanent URL
2. Test bot with real Telegram users
3. Monitor admin notifications for orders/bookings
