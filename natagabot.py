# pylint:disable=E0633
import telebot
from telebot import types
import requests
import json
from bs4 import BeautifulSoup

admin_chat_id = 5321637533

dev = types.InlineKeyboardButton(text="𝑴𝒊𝒏𝒊𝒂 𝑨𝒈𝒓𝒊𝒄𝒖𝒍𝒕𝒖𝒓𝒆🌸🌾 ", url='https://t.me/+rbphVRSaWD9mNjg8')
btn = types.InlineKeyboardMarkup()
btn.row_width = 1
btn.add(dev)

token = "6410467729:AAE35oFq2b1ogyxZMIlA_VbYC60DKJB9neY"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton('𓆩⋆ ׅᎯL ׅG̸E🅽ᎬRᎪⱠ ׅ⋆𓆪', url='https://t.me/BO_R0'),
                  types.InlineKeyboardButton('𝑴𝒊𝒏𝒊𝒂 𝑨𝒈𝒓𝒊𝒄𝒖𝒍𝒕𝒖𝒓𝒆☘️', url='https://t.me/+rbphVRSaWD9mNjg8'))

    bot.reply_to(message, f"- أهلاً بك عزيزي [{message.from_user.first_name}](tg://user?id={message.from_user.id}) 👋.\n"
                      f"- في بوت [{bot.get_me().first_name}](https://t.me/{bot.get_me().username}) للحصول على النتيجة.\n"
                      f"- يمكنك استخدام البوت للحصول على نتيجة كلية الزراعة جامعة المنيا.\n"
                      , parse_mode='Markdown', reply_markup=keyboard)
    bot.reply_to(message, "برجاء ادخال id (كود الطالب )🆔:")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if not message.text.isdigit():
        return

    chat_id = message.chat.id
    bot.reply_to(message, "برجاء ادخال الباسورد :")
    bot.register_next_step_handler(message, send_sms, chat_id, message.text)

def send_sms(message, chat_id, number):
    text = message.text

    url1 = "http://credit.minia.edu.eg/studentLogin"
    headers1 = {
        "Host": "credit.minia.edu.eg",
        "Connection": "keep-alive",
        "Content-Length": "72",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://credit.minia.edu.eg",
        "Referer": "http://credit.minia.edu.eg/static/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    data = {
        "UserName": number,
        "Password": text,
        "sysID": "313.",
        "UserLang": "E",
        "userType": "2",
    }

    try:
        response = requests.post(url1, headers=headers1, data=data, timeout=10)

        if not response.ok:
            bot.reply_to(message, "توجد مشكلة في الموقع. الرجاء المحاولة مرة أخرى لاحقًا.❌")
            return

        if "LoginOK" in response.text and json.loads(response.text)["rows"][0]["row"]["LoginOK"] == "True":
            bot.reply_to(message, "تم تسجيل الدخول بنجاح ✅")
            cookies = response.headers["Set-Cookie"]
        else:
            bot.reply_to(message, "برجاء التأكد من كود الطالب وكلمة المرور ثم أعد المحاولة مرة أخرى ❌")
            return

        # ... (بقية الكود كما هو)
    
    except requests.Timeout:
        bot.reply_to(message, " الموقع لا يعمل برجاء المحاولة مرة اخري لاحقاً❌")
        return

    url = "http://credit.minia.edu.eg/getJCI"
    headers = {
        "Host": "credit.minia.edu.eg",
        "Connection": "keep-alive",
        "Content-Length": "223",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://credit.minia.edu.eg",
        "Referer": "http://credit.minia.edu.eg/static/PortalStudent.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": cookies
    }
    payload = {
        "param0": "Reports.RegisterCert",
        "param1": "getTranscript",
        "param2": '{"crsReplaceHide":"true","ShowDetails":"true","portalFlag":"true","RegType":"student","AppType":"result"}'
    }
    response1 = requests.post(url, headers=headers, data=payload).text
    soup = BeautifulSoup(response1, 'html.parser')
    json_text = soup.get_text()
    data2 = json.loads(json_text)
    
    calculate_and_send_course_info(chat_id, data2)

def calculate_and_send_course_info(chat_id, data2):
    # الدورة الأولى (2022-2023)
    first_semester_2022_2023 = data2["StuSemesterData"][0]["Semesters"][0]
    total_credits_2022_2023, message_2022_2023 = print_course_info(first_semester_2022_2023["Courses"], "اولي ترم اول (2022-2023)")
    bot.send_message(chat_id, message_2022_2023)
    bot.send_message(chat_id, f"\nالساعات المسجلة: {first_semester_2022_2023['RegHrs']}        الساعات الحاصل عليها: {first_semester_2022_2023['EarnedHrs']}\nالمعدل الفصلي: {first_semester_2022_2023['GPA']}        المعدل التراكمي: {first_semester_2022_2023['CurrGPA']}")

    # الدورة الثانية (2022-2023)
    second_semester_2022_2023 = data2["StuSemesterData"][0]["Semesters"][1]
    total_credits_2022_2023 += print_course_info(second_semester_2022_2023["Courses"], "اولي ترم تاني (2022-2023)")[0]
    message_2022_20232= "\n\n" + print_course_info(second_semester_2022_2023["Courses"], "اولي ترم تاني (2022-2023)")[1]
    bot.send_message(chat_id, message_2022_20232)

    bot.send_message(chat_id, f"\nالساعات المسجلة: {second_semester_2022_2023['RegHrs']}        الساعات الحاصل عليها: {second_semester_2022_2023['EarnedHrs']}\nالمعدل الفصلي: {second_semester_2022_2023['GPA']}        المعدل التراكمي: {second_semester_2022_2023['CurrGPA']}")

    # الدورة الأولى (2023-2024)
    first_semester_2023_2024 = data2["StuSemesterData"][1]["Semesters"][0]
    total_credits_2023_2024, message_2023_2024 = print_course_info(first_semester_2023_2024["Courses"], "تانية ترم اول (2023-2024)")
    bot.send_message(chat_id, message_2023_2024)
    bot.send_message(chat_id, f"\nالساعات المسجلة: {first_semester_2023_2024['RegHrs']}        الساعات الحاصل عليها: {first_semester_2023_2024['EarnedHrs']}\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}")

def print_course_info(course_data, semester_name):
    message_text = f"\n{semester_name}:\n"
    message_text += "اسم المقرر  | الساعات المعتمدة | التقدير |\n"
    message_text += "--------------------------------------------\n"
    total_credits = 0

    for course in course_data:
        course_name = course["CourseName"]
        course_code = course["CourseCode"]
        course_credit = int(course["CourseCredit"])
        grade = course.get("Grade", "unannounced")
        total_credits += course_credit
        message_text += f"•{course_name} 🔸 {course_credit} 🔸{grade} \n"

    return total_credits, message_text

bot.polling()