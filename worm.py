import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# کلیلەکانت لێرە جێگیر کراون
TOKEN = "8667273302:AAGCPOdRUDcQFPgECqopNvN8vfzrhdRELaY"
GROQ_API_KEY = "Gsk_Aqh1lhYdczMcWX9Ztjy2WGdyb3FYMY0hAW4ywODyCpxNV7qQ754y"

user_db = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_db[user_id] = user_db.get(user_id, {"limit": 10})
    
    keyboard = [[InlineKeyboardButton("👑 کڕینی VIP", url="https://t.me/Daryas_Official")]]
    
    await update.message.reply_text(
        f"🔥 **WormGPT v2.0 چالاک بوو** 🔥\n\n"
        f"نامەی ماوە: {user_db[user_id]['limit']}\n"
        "بۆتەکە ئامادەیە، پرسیارەکەت بنووسە...",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_db.get(user_id, {"limit": 0})["limit"] <= 0:
        await update.message.reply_text("❌ لیمیتەکەت تەواو بوو.")
        return

    await update.message.reply_chat_action("typing")
    
    try:
        # پەیوەندی ڕاستەوخۆ بە Groq
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY.strip()}"}
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": update.message.text}]
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            user_db[user_id]["limit"] -= 1
            await update.message.reply_text(f"😈 **WormGPT:**\n\n{reply}")
        else:
            await update.message.reply_text(f"❌ سێرڤەر وتی: {response.json().get('error', {}).get('message', 'Error')}")
            
    except Exception as e:
        await update.message.reply_text(f"⚠️ کێشەی تەکنیکی: {str(e)}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 WormGPT Pro is Running...")
app.run_polling()
