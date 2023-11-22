from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Update
from aiogram.dispatcher.dispatcher import Dispatcher as BaseDispatcher

API_TOKEN = '6304558758:AAGboh7HJ6kNJ0BawGdaQwcfCBmNJsL8D9M'
BOT_USERNAME = '@findjBotaskjdh'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Define a dictionary to store user data
user_data = {}

@dp.message_handler(commands=['start'])
async def preferences_command(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text) for text in ["Online", "Offline"]]
    keyboard.add(*buttons)

    await message.answer("Please choose your preferred type of work:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text.lower() in ["online", "offline"])
async def get_online_offline_choice(message):
    preferences = message.text.lower()

    # Store the user's preferences
    user_data['preferences'] = preferences

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    specialization_buttons = [
        InlineKeyboardButton(text, callback_data=text.lower()) for text in ["IT", "Design", "Engineering", "Other"]
    ]
    inline_keyboard.add(*specialization_buttons)

    await message.answer(f"You selected {preferences} work. Now, please choose your specialization:", reply_markup=inline_keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data.lower() in ["it", "design", "engineering", "other"])
async def get_specialization_choice(callback_query):
    specialization = callback_query.data.lower()

    # Store the user's specialization
    user_data['specialization'] = specialization

    # Call the recommendations function
    await recommendations_command(callback_query.message)

async def recommendations_command(message):
    if 'preferences' not in user_data or 'specialization' not in user_data:
        await message.reply_text("Please complete the preferences and specialization first using the /preferences command.")
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

    await message.reply_text(recommendations, parse_mode='Markdown')

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
