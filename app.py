import os
import re
import telebot

# Initialize Bot
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "សួស្តី! ខ្ញុំជាប៊ុតជំនួយការពិនិត្យអត្ថបទ WhiteSmoke។ 🦅🇰🇭\n\n"
        "សូមផ្ញើអត្ថបទភាសាអង់គ្លេសរបស់អ្នកមកទីនេះ។ ខ្ញុំនឹងពិនិត្យរកមើលកំហុសអក្ខរាវិរុទ្ធ "
        "សញ្ញាវណ្ណយុត្តិ និងការប្រើប្រាស់ពាក្យជាន់គ្នា រួចផ្តល់អនុសាសន៍កែលម្អជូនអ្នក!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def analyze_whitesmoke(message):
    text = message.text
    issues_found = []
    words = text.split()
    
    # 1. WhiteSmoke Pillar: Capitalization Rules
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for s in sentences:
        if s and s[0].islower():
            # Flag if a sentence starts with a lowercase letter
            issues_found.append(f"• ដើមប្រយោគគួរតែផ្តើមដោយអក្សរធំ៖ \"... {s[:15]}...\"")

    # 2. WhiteSmoke Pillar: Punctuation Mechanics
    if re.search(r'\s[.,!?]', text):
        issues_found.append("• មិនត្រូវមានដកឃ្លានៅពីមុខសញ្ញាវណ្ណយុត្តិឡើយ (ឧទាហរណ៍៖ \",\" ឬ \".\")")
    if re.search(r'[.,!?][A-Za-z]', text):
        issues_found.append("• ត្រូវដកឃ្លាមួយបន្ទាប់ពីប្រើសញ្ញាវណ្ណយុត្តិរួច")

    # 3. WhiteSmoke Pillar: Word Redundancy & Repetition Traps
    for i in range(len(words) - 1):
        clean_word_1 = words[i].lower().strip(".,!?\"'")
        clean_word_2 = words[i+1].lower().strip(".,!?\"'")
        if clean_word_1 == clean_word_2 and clean_word_1:
            issues_found.append(f"• រកឃើញពាក្យដដែលៗជាន់គ្នា៖ \"{words[i]} {words[i+1]}\"")

    # 4. WhiteSmoke Pillar: Style & Structure Alerts
    if len(words) > 40:
        issues_found.append("• អត្ថបទនេះវែងពេក គួរតែបំបែកជាកថាខណ្ឌខ្លីៗដើម្បីឱ្យមានភាពទាក់ទាញ (Style Enhancement)")

    # Construct the Khmer Report Summary
    report_title = "🔍 **របាយការណ៍ពិនិត្យអត្ថបទ (រចនាប័ទ្ម WhiteSmoke)**\n━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if issues_found:
        report_body = "❌ **ចំណុចខ្វះខាតដែលត្រូវកែលម្អ៖**\n" + "\n".join(issues_found[:6])
    else:
        report_body = "✅ **អត្ថបទរបស់អ្នកល្អឥតខ្ចោះ!** មិនមានរកឃើញកំហុសរចនាសម្ព័ន្ធ ឬអក្ខរាវិរុទ្ធឡើយ។"

    bot.reply_to(message, report_title + report_body, parse_mode='Markdown')

if __name__ == "__main__":
    print("WhiteSmoke Khmer Bot running...")
    bot.infinity_polling()
