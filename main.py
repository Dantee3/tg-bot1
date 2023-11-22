from typing import Final
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, ConversationHandler, CallbackContext, CallbackQueryHandler

TOKEN: Final = '6446174202:AAEEn3UL2Z0sx0K7W_PLOWDrEEdPXjYOrWU'
BOT_USERNAME: Final = '@findjBot'

# Conversation states
NAME, AGE, COUNTRY, PREFERENCES, SPECIALIZATION, INLINE_CHOICE = range(6)

# Dictionary to store user information
user_data = {}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Please enter your name: ')
    return NAME

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Available commands:\n'
                                    '/start - Begin using the bot and provide your name\n'
                                    '/help - Get assistance and instructions\n'
                                    '/cancel - Cancel the current conversation\n'
                                    '/preferences - Tell us your job preferences')
    return NAME


# Function to get the user's name
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith('/'):
        # Check if the name has the first letter in uppercase and the rest in lowercase
        if text[0].isupper() and text[1:].islower():
            user_data['name'] = text
            await update.message.reply_text(f"Hello, {user_data['name']}! Please enter your age:")
            return AGE
        else:
            await update.message.reply_text("Please enter your name with the first letter in uppercase and the rest in lowercase.")
    return NAME

# Function to get the user's age
async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith('/'):
        # Check if age is a positive integer and not greater than 70
        if text.isdigit() and 16 <= int(text) <= 70:
            user_data['age'] = text
            await update.message.reply_text("Great! Now, please enter your country of residence:")
            return COUNTRY
        else:
            await update.message.reply_text("Please enter a valid age.")
    return AGE


# Function to get the user's country
async def get_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith('/'):
        # Check if the country has the first letter in uppercase and the rest in lowercase
        if text[0].isupper() and text[1:].islower():
            user_data['country'] = text
            await update.message.reply_text(f"Thank you, {user_data['name']}! You are {user_data['age']} years old and live in {user_data['country']}. You can use the /help command to get assistance.")
            return ConversationHandler.END
        else:
            await update.message.reply_text("Please enter your country with the first letter in uppercase and the rest in lowercase.")
    return COUNTRY
    
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Canceled. Please enter your name:')
    return NAME    

# Function to get the user's preferences and provide specialization options
async def preferences_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Online"), KeyboardButton("Offline")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await update.message.reply_text("Please choose your preferred type of work:", reply_markup=reply_markup)
    return PREFERENCES

# Function to handle the user's choice of online or offline work
async def get_online_offline_choice(update: Update, context: CallbackContext):
    # Check if the user made a choice using inline buttons
    query = update.callback_query
    user_data['preferences'] = query.data.lower()

    # Inline buttons for specialization choices
    inline_keyboard = [
        [
            InlineKeyboardButton("IT", callback_data='it'),
            InlineKeyboardButton("Design", callback_data='design')
        ],
        [
            InlineKeyboardButton("Engineering", callback_data='engineering'),
            InlineKeyboardButton("Other", callback_data='other')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    await query.message.edit_text(f"You selected {user_data['preferences']} work. Now, please choose your specialization:", reply_markup=reply_markup)
    return INLINE_CHOICE



'''
# Function to handle inline button choices
async def inline_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    user_data['specialization'] = query.data

    # Provide recommendations based on user preferences and specialization
    recommendations = f"Thank you for providing your preferences. Here are some job recommendations based on your choices:\n\n"
    if user_data['preferences'] == 'online':
        if user_data['specialization'] == 'it':
            recommendations += "Job: *IT Specialist*\n" \
                              "Pay: $25 per hour\n" \
                              "Type: Full-time\n" \
                              "Requirements: Bachelor's degree in Computer Science, 3+ years of experience\n" \
                              "[Link to apply](https://docgo.wd1.myworkdayjobs.com/en-US/DocGo/job/Remote/Administrative-Assistant_R-2891)"
        elif user_data['specialization'] == 'design':
            recommendations += "Job: *Design Course Teacher*\n" \
                              "Pay: $7.00 - $10.00 per Hour\n" \
                              "Type: Less than 30 hrs/week Full-time\n" \
                              "Requirements: Knowledge of Adobe Photoshop, Adobe Illustrator, Figma; Completed projects using these graphic editors; Friendliness and stress resistance; Desire to develop oneself and others\n" \
                              "[Link to apply](https://www.upwork.com/freelance-jobs/apply/Teacher-for-the-online-course-Design_~015090055f51ae36a9/)"
        elif user_data['specialization'] == 'engineering':
            recommendations += "Job: *Software Engineer*\n" \
                              "Pay: $30 per hour\n" \
                              "Type: Full-time\n" \
                              "Requirements: Master's degree in Software Engineering, 5+ years of experience\n" \
                              "[Link to apply](https://www.upwork.com/freelance-jobs/apply/Seeking-Personal-Trainer-Develop-Custom-Workout-Programs-via-Distinction_~01551c232169844281/)"
        else:
            recommendations += "Job: *College Instructor*\n" \
                              "Pay: $6.00 - $15.00 per Hour\n" \
                              "Type: More than 30 hrs/week Full-time\n" \
                              "Requirements: Ph.D. in a relevant field, Proficiency in English, Previous teaching or tutoring experience preferred, Demonstrated knowledge\n" \
                              "[Link to apply](https://www.upwork.com/freelance-jobs/apply)"
    elif user_data['preferences'] == 'offline':
        if user_data['specialization'] == 'it':
            recommendations += f"Job: *Web Programmer - Intern in {user_data['country']}*\n" \
                              f"Pay: Stipend for the internship\n" \
                              f"Type: 2 months (Duration of the internship)\n" \
                              f"Requirements: No work experience required\n" \
                              f"[Link to apply](https://hh.kz/vacancy/88510720?from=vacancy_search_list&hhtmFrom=vacancy_search_list)"
        elif user_data['specialization'] == 'design':
            recommendations += f"Job: *Graphic Designer in {user_data['country']}*\n" \
                              f"Pay:  250 000-400 000 KZT (monthly)\n" \
                              f"Type: Full-time\n" \
                              f"Requirements: Proficient in Adobe Creative Suite\n" \
                              f"[Link to apply](https://www.indeed.com/jobs?q=work++online&l=&vjk=9285d2a840029944)"
        elif user_data['specialization'] == 'engineering':
            recommendations += f"Job: *Software Engineer in {user_data['country']}*\n" \
                              f"Pay: 300 000-450 000 KZT (monthly)\n" \
                              f"Type: Full-time\n" \
                              f"Requirements: Master's degree in Software Engineering, 5+ years of experience\n" \
                              f"[Link to apply](https://docgo.wd1.myworkdayjobs.com/en-US/DocGo/job/Remote/Administrative-Assistant_R-2891)"
        else:
            recommendations += f"Job: *IT Manager in {user_data['country']}*\n" \
                              f"Pay: 350 000 KZT (monthly)\n" \
                              f"Type: Full-time\n" \
                              f"Requirements: 1–3 years of experience\n" \
                              f"[Link to apply](https://hh.kz/vacancy/89730097?from=vacancy)"

    await query.edit_message_text(recommendations, parse_mode='Markdown')
    return ConversationHandler.END

'''

# Function to show job recommendations
async def recommendations_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'preferences' not in user_data or 'specialization' not in user_data:
        await update.message.reply_text("Please complete the preferences and specialization first using the /preferences command.")
        return

    # Provide recommendations based on user preferences and specialization
    recommendations = f"Here are some job recommendations based on your choices:\n\n"
    if user_data['preferences'] == 'online':
        if user_data['specialization'] == 'it':
            recommendations += "Job: *IT Specialist*\n" \
                              "Pay: $25 per hour\n" \
                              "Type: Full-time\n" \
                              "Requirements: Bachelor's degree in Computer Science, 3+ years of experience\n" \
                              "[Link to apply](https://docgo.wd1.myworkdayjobs.com/en-US/DocGo/job/Remote/Administrative-Assistant_R-2891)"
        elif user_data['specialization'] == 'design':
            recommendations += "Job: *Design Course Teacher*\n" \
                              "Pay: $7.00 - $10.00 per Hour\n" \
                              "Type: Less than 30 hrs/week Full-time\n" \
                              "Requirements: Knowledge of Adobe Photoshop, Adobe Illustrator, Figma; Completed projects using these graphic editors; Friendliness and stress resistance; Desire to develop oneself and others\n" \
                              "[Link to apply](https://www.upwork.com/freelance-jobs/apply/Teacher-for-the-online-course-Design_~015090055f51ae36a9/)"
        elif user_data['specialization'] == 'engineering':
            recommendations += "Job: *Software Engineer*\n" \
                              "Pay: $30 per hour\n" \
                              "Type: Full-time\n" \
                              "Requirements: Master's degree in Software Engineering, 5+ years of experience\n" \
                              "[Link to apply](https://www.upwork.com/freelance-jobs/apply/Seeking-Personal-Trainer-Develop-Custom-Workout-Programs-via-Distinction_~01551c232169844281/)"
        else:
            recommendations += "Job: *College Instructor*\n" \
                              "Pay: $6.00 - $15.00 per Hour\n" \
                              "Type: More than 30 hrs/week Full-time\n" \
                              "Requirements: Ph.D. in a relevant field, Proficiency in English, Previous teaching or tutoring experience preferred, Demonstrated knowledge\n" \
                              "[Link to apply](https://www.upwork.com/freelance-jobs/apply)"
    elif user_data['preferences'] == 'offline':
        if user_data['specialization'] == 'it':
            recommendations += f"Job: *Web Programmer - Intern in {user_data['country']}*\n" \
                              f"Pay: Stipend for the internship\n" \
                              f"Type: 2 months (Duration of the internship)\n" \
                              f"Requirements: No work experience required\n" \
                              f"[Link to apply](https://hh.kz/vacancy/88510720?from=vacancy_search_list&hhtmFrom=vacancy_search_list)"
        elif user_data['specialization'] == 'design':
            recommendations += f"Job: *Graphic Designer in {user_data['country']}*\n" \
                              f"Pay:  250 000-400 000 KZT (monthly)\n" \
                              f"Type: Full-time\n" \
                              f"Requirements: Proficient in Adobe Creative Suite\n" \
                              f"[Link to apply](https://www.indeed.com/jobs?q=work++online&l=&vjk=9285d2a840029944)"
        elif user_data['specialization'] == 'engineering':
            recommendations += f"Job: *Software Engineer in {user_data['country']}*\n" \
                              f"Pay: 300 000-450 000 KZT (monthly)\n" \
                              f"Type: Full-time\n" \
                              f"Requirements: Master's degree in Software Engineering, 5+ years of experience\n" \
                              f"[Link to apply](https://docgo.wd1.myworkdayjobs.com/en-US/DocGo/job/Remote/Administrative-Assistant_R-2891)"
        else:
            recommendations += f"Job: *IT Manager in {user_data['country']}*\n" \
                              f"Pay: 350 000 KZT (monthly)\n" \
                              f"Type: Full-time\n" \
                              f"Requirements: 1–3 years of experience\n" \
                              f"[Link to apply](https://hh.kz/vacancy/89730097?from=vacancy)"

    await update.message.reply_text(recommendations, parse_mode='Markdown')

# Command handler for /recommendations
recommendations_handler = CommandHandler('recommendations', recommendations_command)



# Command handler for /preferences
preferences_handler = CommandHandler('preferences', preferences_command)

# Conversation handlers
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('preferences', preferences_command)],
    states={
        PREFERENCES: [CallbackQueryHandler(get_online_offline_choice)],  # Use CallbackQueryHandler
        # INLINE_CHOICE: [CallbackQueryHandler(inline_choice, pattern='^spec$')],  # Adjust pattern if needed
    },
    fallbacks=[CommandHandler('cancel', cancel_command)]
)

conversation_handler2 = ConversationHandler(
    entry_points=[CommandHandler('start', start_command)],
    states={
        NAME: [MessageHandler(None, get_name)],
        AGE: [MessageHandler(None, get_age)],
        COUNTRY: [MessageHandler(None, get_country)],
    },
    fallbacks=[CommandHandler('cancel', cancel_command)]
)


# Initialize your bot with the conversation handler and other handlers
bot = Application.builder().token(TOKEN).build()
bot.add_handler(conversation_handler2)
bot.add_handler(conversation_handler)
bot.add_handler(CommandHandler('help', help_command))
bot.add_handler(CommandHandler('cancel', cancel_command))
bot.add_handler(preferences_handler)
bot.add_handler(recommendations_handler)

if __name__ == '__main__':
    print('Starting Bot...')
    bot.run_polling(poll_interval=1)

