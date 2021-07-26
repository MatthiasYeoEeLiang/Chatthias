import telebot
import pymysql
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from telegram_bot_calendar import WMonthTelegramCalendar, LSTEP
import time


#Telegram API Token
API_KEY = "APIKEY"
bot = telebot.TeleBot(API_KEY)

#SQL connection
mypass = "PW"
mydatabase = "DB"

con = pymysql.connect(host="localhost", user="root", password=mypass, database=mydatabase)
cur = con.cursor()
userTable = "users"

#MEMORY SPACE
places = ["TechnoEdge", "Deck", "FoodClique", "Frontier", "Bistro Box", "Central Square", "Spinelli",
            "Fine Food", "Flavours"]
placesDES = ["TechnoEdgeDES", "DeckDES", "FoodCliqueDES", "FrontierDES", "Bistro BoxDES", "Central SquareDES",
            "Fine FoodDES", "FlavoursDES"]
pax = ["2"]
timeslots = ["12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00", "17:00:00", "18:00:00"]

#Location Keyboard
placekeyboard = telebot.types.InlineKeyboardMarkup(row_width=7)
technoedge = telebot.types.InlineKeyboardButton(text="TechnoEdge", callback_data='TechnoEdge')
deck = telebot.types.InlineKeyboardButton(text="Deck", callback_data='Deck')
foodclique = telebot.types.InlineKeyboardButton(text="FoodClique", callback_data='FoodClique')
frontier = telebot.types.InlineKeyboardButton(text="Frontier", callback_data='Frontier')
centralsquare = telebot.types.InlineKeyboardButton(text="Central Square", callback_data="Central Square")
finefood = telebot.types.InlineKeyboardButton(text="Fine Food", callback_data="Fine Food")
flavours = telebot.types.InlineKeyboardButton(text="Flavours", callback_data="Flavours")
placekeyboard.add(technoedge)
placekeyboard.add(deck)
placekeyboard.add(foodclique)
placekeyboard.add(frontier)
placekeyboard.add(centralsquare)
placekeyboard.add(finefood)
placekeyboard.add(flavours)

#Location Description (DES) Keyboard
placeDESkeyboard = telebot.types.InlineKeyboardMarkup(row_width=7)
technoedgeDES = telebot.types.InlineKeyboardButton(text="TechnoEdge", callback_data='TechnoEdgeDES')
deckDES = telebot.types.InlineKeyboardButton(text="Deck", callback_data='DeckDES')
foodcliqueDES = telebot.types.InlineKeyboardButton(text="FoodClique", callback_data='FoodCliqueDES')
frontierDES = telebot.types.InlineKeyboardButton(text="Frontier", callback_data='FrontierDES')
centralsquareDES = telebot.types.InlineKeyboardButton(text="Central Square", callback_data="Central SquareDES")
finefoodDES = telebot.types.InlineKeyboardButton(text="Fine Food", callback_data="Fine FoodDES")
flavoursDES = telebot.types.InlineKeyboardButton(text="Flavours", callback_data="FlavoursDES")
placeDESkeyboard.add(technoedgeDES)
placeDESkeyboard.add(deckDES)
placeDESkeyboard.add(foodcliqueDES)
placeDESkeyboard.add(frontierDES)
placeDESkeyboard.add(centralsquareDES)
placeDESkeyboard.add(finefoodDES)
placeDESkeyboard.add(flavoursDES)

#Pax Keyboard
paxkeyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
two = telebot.types.InlineKeyboardButton(text="2", callback_data='2')
paxkeyboard.add(two)

#CancelBooking Keyboard
cancelbookingkeyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
cancelbooking = telebot.types.InlineKeyboardButton(text="Cancel Booking", callback_data="cancelbooking")
keepbooking= telebot.types.InlineKeyboardButton(text="Keep Booking", callback_data="keepbooking")
cancelbookingkeyboard.add(cancelbooking)
cancelbookingkeyboard.add(keepbooking)

#ContinueSession Keyboard
continuesessionkeyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
continuesession = telebot.types.InlineKeyboardButton(text="Continue from where I left off", callback_data="continue")
restart= telebot.types.InlineKeyboardButton(text="Restart Session", callback_data="restart")
continuesessionkeyboard.add(continuesession)
continuesessionkeyboard.add(restart)

#FOR STARTING
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Chatthias helps to arrange lunch meals to meet new people in NUS with your "
                                "desired dining location"
                                "\n \nIf you're lost and hungry, you can control me by using these commands"
                                "\n \n/start - starts the bot to find a match for you"
                                "\n \n/help - find out commands"
                                "\n \n/showbookings - shows your booked details"
                                "\n \n/cancelbookings - cancel your current booking and start a new session"
                                "\n \n/locations - learn more about the dining locations and where it is located"
                                "\n \n/showmyhistory - shows previous bookings and paired users")

    completedbooking = "SELECT * FROM chatthias.users WHERE EXISTS (SELECT * FROM chatthias.users WHERE username = " \
                       + "'" + message.from_user.username + "'" + " AND location IS NOT NULL AND pax IS NOT NULL AND " \
                                                                "date IS NOT NULL AND timeslot IS NOT NULL)"
    incompletebooking = "SELECT * FROM chatthias.users WHERE EXISTS (SELECT * FROM chatthias.users WHERE username = " \
                        + "'" + message.from_user.username + "'" + " AND location IS NULL OR pax IS NULL" \
                                                                 " OR date IS NULL OR timeslot IS NULL)"
    if (cur.execute(completedbooking)):
        bot.send_message(message.chat.id, "You already have a completed booking under your username. "
                                          "Would you like to review your booking?"
                                          "\n \n/showbookings - show all booking details under you"
                                          "\n \n/cancelbookings - cancel current booking and start a new session")

    elif (cur.execute(incompletebooking)):
        bot.send_message(message.chat.id, "You have an incomplete booking. Would you like to continue from where you "
                                          "left off or do you want to restart the whole session?",
                                          reply_markup=continuesessionkeyboard)
    else:
        bot.send_message(message.chat.id, "Thank you for using me. Select a place that you want to dine at",
                     reply_markup=placekeyboard)

@bot.message_handler(commands=['showmyhistory'])
def showmyhistory(message):
    bot.send_message(message.chat.id, "Here are your previous bookings. You can see your previous details "
                                      "selected! You can contact the users that you once paired with!")
    sql = "SELECT * FROM chatthias.history WHERE username = " + "'" +message.from_user.username+ "'" + "ORDER BY id DESC"
    cur.execute(sql)
    data = cur.fetchall()
    counter = 10
    for i in range(counter):
        try:
            bot.send_message(message.chat.id, "Booking ID: " + str(data[i][0]) +
                        "\n \nDate and Time Registered: " + str(data[i][6]) +
                        "\n \nBooking Username: " + data[i][1] +
                        "\n \nLocation, Date and Time Booked: " + data[i][2] + ", " + data[i][4] + " " + data[i][5] +
                        "\n \nPaired with username: @" + data[i][7])

        except IndexError:
            break
    bot.send_message(message.chat.id, "Use /help for more commands or /start to start finding a lunch date!")

@bot.message_handler(commands=['showbookings'])
def showbookings(message):
    completedbooking = "SELECT * FROM chatthias.users WHERE EXISTS (SELECT * FROM chatthias.users WHERE username = " \
                       + "'" + message.from_user.username + "'" + " " \
                        "AND location IS NOT NULL AND pax IS NOT NULL AND " \
                        "date IS NOT NULL AND timeslot IS NOT NULL)"
    if cur.execute(completedbooking):
        showbookingssql = "SELECT * FROM chatthias.users WHERE username = " + "'" + message.from_user.username + "'"
        cur.execute(showbookingssql)
        bookings = cur.fetchall()
        bot.send_message(message.chat.id, "Hello " + '*'+message.from_user.username+'*' + ". Thank you for "
                                                                                          "using Chatthias."
                                          "\n \nHere are your booking details:"
                                          "\n \nLocation: " + bookings[0][1] +
                                          "\n \nPax: " + bookings[0][2] +
                                          "\n \nDate: " + bookings[0][3] +
                                          "\n \nTimeslot: " + bookings[0][4], parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "You have no bookings! Use /start to start making one now.")

@bot.message_handler(commands=['cancelbookings'])
def cancelbookings(message):
    completedbooking = "SELECT * FROM chatthias.users WHERE EXISTS (SELECT * FROM chatthias.users WHERE username = " \
                       + "'" + message.from_user.username + "'" + \
                       " AND location IS NOT NULL AND pax IS NOT NULL AND " \
                       "date IS NOT NULL AND timeslot IS NOT NULL)"
    if cur.execute(completedbooking):
        showbookingssql = "SELECT * FROM chatthias.users WHERE username = " + "'" + message.from_user.username + "'"
        cur.execute(showbookingssql)
        bookings = cur.fetchall()
        userlocation = bookings[0][1]
        userpax = bookings[0][2]
        userdate = bookings[0][3]
        usertimeslot = bookings[0][4]
        bot.send_message(message.chat.id, "Hello " + '*' + message.from_user.username
                        + '*' + ". Thank you for " "using Chatthias."
                        "\n \nHere are your booking details:"
                        "\n \nLocation: " + userlocation +
                        "\n \nPax: " + userpax +
                        "\n \nDate: " + userdate +
                        "\n \nTimeslot: " + usertimeslot, parse_mode='Markdown')
        bot.send_message(message.chat.id, "Do you want to cancel this booking?", reply_markup=cancelbookingkeyboard)
    else:
        bot.send_message(message.chat.id, "You have no bookings! Use /start to start making one now.")

@bot.message_handler(commands=['locations'])
def locations(message):
    bot.send_message(message.chat.id, "Select a location to find out more about it!", reply_markup=placeDESkeyboard)

@bot.message_handler(commands=['cancelsearch'])
def cancelsearch(message):
    # Deleting Current Record
    deletesql = "DELETE FROM chatthias.users WHERE username = " + "'" + message.from_user.username + "'"
    cur.execute(deletesql)
    con.commit()
    bot.send_message(message.chat.id, "Search has been cancelled! Use /start to start a new booking")

#TO CATCH INVALID COMMANDS
@bot.message_handler(func=lambda message: message)
def handle_random(message):
    bot.send_message(message.chat.id, "Chatthias helps to arrange lunch meals to meet new people in NUS with your "
                                "desired dining location and timeslot"
                                "\n \nIf you're lost and hungry, you can control me by using these commands"
                                "\n \n/start - starts the bot to find a match for you"
                                "\n \n/showbookings - shows your booked details"
                                "\n \n/cancelbookings - cancel your current booking and start a new session"
                                "\n \n/locations - learn more about the dining locations and where it is located"
                                "\n \n/showmyhistory - shows previous bookings and paired users")

@bot.callback_query_handler(func=WMonthTelegramCalendar.func())
def calendar(c):
    result, key, step = WMonthTelegramCalendar(min_date=date.today(),
                                               max_date= date.today() + relativedelta(weeks=+3)).process(c.data)
    if not result and key:
        bot.edit_message_text("Select your desired date", c.message.chat.id, c.message.message_id,
            reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected '*'{result.strftime('%d/%m/%Y')}'*'",
                              c.message.chat.id, c.message.message_id, parse_mode='Markdown')
        timeslotkeyboard = telebot.types.InlineKeyboardMarkup(row_width=5)
        if result.strftime("%Y/%m/%d") <= datetime.now().strftime("%Y/%m/%d"):
            twelvePM = telebot.types.InlineKeyboardButton(text="12:00PM", callback_data="12:00:00")
            onePM = telebot.types.InlineKeyboardButton(text="1:00PM", callback_data="13:00:00")
            twoPM = telebot.types.InlineKeyboardButton(text="2:00PM", callback_data="14:00:00")
            threePM = telebot.types.InlineKeyboardButton(text="3:00PM", callback_data="15:00:00")
            fourPM = telebot.types.InlineKeyboardButton(text="4:00PM", callback_data="16:00:00")
            fivePM = telebot.types.InlineKeyboardButton(text="5:20PM", callback_data="17:00:00")
            sixPM = telebot.types.InlineKeyboardButton(text="6:00PM", callback_data="18:00:00")
            if (datetime.now().strftime("%H:%M:%S") < "12:00:00"):
                timeslotkeyboard.add(twelvePM)
            if (datetime.now().strftime("%H:%M:%S") < "13:00:00"):
                timeslotkeyboard.add(onePM)
            if (datetime.now().strftime("%H:%M:%S") < "14:00:00"):
                timeslotkeyboard.add(twoPM)
            if (datetime.now().strftime("%H:%M:%S") < "15:00:00"):
                timeslotkeyboard.add(threePM)
            if (datetime.now().strftime("%H:%M:%S") < "16:00:00"):
                timeslotkeyboard.add(fourPM)
            if (datetime.now().strftime("%H:%M:%S") < "17:00:00"):
                timeslotkeyboard.add(fivePM)
            if (datetime.now().strftime("%H:%M:%S") < "18:00:00"):
                timeslotkeyboard.add(sixPM)
        else:
            twelvePM = telebot.types.InlineKeyboardButton(text="12:00PM", callback_data="12:00:00")
            onePM = telebot.types.InlineKeyboardButton(text="1:00PM", callback_data="13:00:00")
            twoPM = telebot.types.InlineKeyboardButton(text="2:00PM", callback_data="14:00:00")
            threePM = telebot.types.InlineKeyboardButton(text="3:00PM", callback_data="15:00:00")
            fourPM = telebot.types.InlineKeyboardButton(text="4:00PM", callback_data="16:00:00")
            fivePM = telebot.types.InlineKeyboardButton(text="5:00PM", callback_data ="17:00:00")
            sixPM = telebot.types.InlineKeyboardButton(text="6:00PM", callback_data="18:00:00")
            timeslotkeyboard.add(twelvePM)
            timeslotkeyboard.add(onePM)
            timeslotkeyboard.add(twoPM)
            timeslotkeyboard.add(threePM)
            timeslotkeyboard.add(fourPM)
            timeslotkeyboard.add(fivePM)
            timeslotkeyboard.add(sixPM)

        #Update SQL
        sql = "UPDATE chatthias.users SET date = " + "'" + result.strftime("%d/%m/%Y") + "'" + " WHERE username = " \
              + "'" + c.from_user.username + "'"
        cur.execute(sql)
        con.commit()
        showbookingssql = "SELECT * FROM chatthias.users WHERE username = " + "'" + c.from_user.username + "'"
        cur.execute(showbookingssql)
        bookings = cur.fetchall()
        userdate = bookings[0][3]
        datetimebooked = datetime.strptime(userdate, '%d/%m/%Y')

        if (datetime.now() < datetimebooked):
            bot.send_message(c.message.chat.id, "Choose your preferred timeslot", reply_markup=timeslotkeyboard)

        else:
            # Deleting Current Record
            deletesql = "DELETE FROM chatthias.users WHERE username = " + "'" + c.from_user.username + "'"
            cur.execute(deletesql)
            con.commit()
            bot.send_message(c.message.chat.id, "There are no timeslots left for this day. I shall "
                                                "restart your booking")
            bot.send_message(c.message.chat.id, "Thank you for using me. Select a place that you want to dine at",
                             reply_markup=placekeyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback(query):
    data = query.data
    if data in places:
        bot.answer_callback_query(query.id, "Choosing Location... " + data.upper())
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.id, reply_markup=None)
        bot.send_message(query.message.chat.id, "You selected to dine at " + '*'+data+'*', parse_mode='Markdown')
        bot.send_message(query.message.chat.id, "Select the number of pax you would want to dine with",
                         reply_markup=paxkeyboard)
        #Update SQL
        sql = "INSERT INTO chatthias.users (username, location) VALUES (%s, %s)"
        values = (query.from_user.username, data)
        cur.execute(sql, values)
        con.commit()

    elif data in pax:
        bot.answer_callback_query(query.id, "Choosing Pax Number... " + data.upper())
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.id, reply_markup=None)
        bot.send_message(query.message.chat.id, "You selected to dine with " + '*'+data+'*' + " people",
                         parse_mode='Markdown')
        calendar, step = WMonthTelegramCalendar(min_date=date.today(), max_date= date.today()
                                                                                 + relativedelta(weeks=+3)).build()
        bot.send_message(query.message.chat.id, "Select your desired date to dine", reply_markup=calendar)

        #Update SQL
        sql = "UPDATE chatthias.users SET pax = " +data+ " WHERE username = " + "'" +query.from_user.username+ "'"
        cur.execute(sql)
        con.commit()

    elif data in timeslots:
        bot.answer_callback_query(query.id, "Choosing Timeslot... " + data.upper())
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.id, reply_markup=None)
        bot.send_message(query.message.chat.id, "You selected " + '*'+data+'*', parse_mode='Markdown')

        #Update SQL
        sql = "UPDATE chatthias.users SET timeslot = " + "'" +data+ "'" + " WHERE username = " + "'" \
              +query.from_user.username+ "'"
        cur.execute(sql)
        con.commit()

        timeregistered = "UPDATE chatthias.users SET timeregistered = " + "'" \
                         +(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))+\
                         "'" + " WHERE username = " + "'" +query.from_user.username+"'"
        cur.execute(timeregistered)
        con.commit()

        showbookingssql = "SELECT * FROM chatthias.users WHERE username = " + "'" + query.from_user.username + "'"
        cur.execute(showbookingssql)
        bookings = cur.fetchall()
        userlocation = bookings[0][1]
        userpax = bookings[0][2]
        userdate = bookings[0][3]
        usertimeslot = bookings[0][4]
        usertimeregistered = bookings[0][5]

        bot.send_message(query.message.chat.id,
                        "Congratulations! Your booking has been successfully recorded!"
                        "\n \nHere are your booking details:"
                        "\n \nLocation: " + userlocation +
                        "\n \nPax: " + userpax +
                        "\n \nDate: " + userdate +
                        "\n \nTimeslot: " + usertimeslot, parse_mode='Markdown')
        bot.send_message(query.message.chat.id, "Chatthias will start searching a match for you using these details. "
                                                "I will notify you again when I find a match!"
                                                "\n \n/cancelsearch - cancels your current search "
                                                "and starts a new session")
        time_now = datetime.now()
        datetimebooked = datetime.strptime(userdate + " " + usertimeslot, '%d/%m/%Y %H:%M:%S')
        t = int((datetimebooked - time_now).total_seconds())
        if t < 0:
            # Deleting Current Record
            deletesql = "DELETE FROM chatthias.users WHERE username = " + "'" + query.from_user.username + "'"
            cur.execute(deletesql)
            con.commit()
            bot.send_message(query.message.chat.id, "Invalid Time! Restart your booking!",
                             reply_markup=placekeyboard)
        while t > 0:
            print(t)
            t -= 1
            time.sleep(2)
            count = "SELECT COUNT(username) FROM chatthias.users " \
                    "WHERE location = " + "'" +userlocation+ "'" "AND pax = " + "'" +userpax+ "'" + \
                    "AND date = " + "'" +userdate+ "'" \
                    + "AND timeslot = " + "'" +usertimeslot+ "'"
            cur.execute(count)
            con.commit()
            if cur.fetchall()[0][0] > 1:
                currentusernamesql = "SELECT * FROM chatthias.users " \
                                     "WHERE username = " + "'" +query.from_user.username+ "'"
                if cur.execute(currentusernamesql) == 1:
                    usernamessql = "SELECT username FROM chatthias.users " \
                                    "WHERE pax = " + "'" +userpax+ "'" + "AND date = " + "'" +userdate+ "'" \
                                    + "AND timeslot = " + "'" +usertimeslot+ "'"
                    cur.execute(usernamessql)
                    usernames = list(cur.fetchall())
                    usernames.remove(((query.from_user.username),))
                    bot.send_message(query.message.chat.id, "I found a match!")
                    bot.send_message(query.message.chat.id, "I paired you up with @" + usernames[0][0] +
                                     "\n \nPlease contact your lunch date at @" + usernames[0][0] +
                                     "\n \nThank you for using Chatthias. Come again when you're hungry!")
                    sql = "INSERT INTO chatthias.history (username, " \
                          "location, pax, date, timeslot, timeregistered, userpaired) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    values = (query.from_user.username, userlocation, userpax, userdate, usertimeslot,
                              usertimeregistered, usernames[0][0])
                    cur.execute(sql, values)
                    con.commit()
                    # Deleting Current Record
                    time.sleep(10)
                    deletesql = "DELETE FROM chatthias.users WHERE username = " + "'" + query.from_user.username + "'" \
                                + "OR username = " + "'" + usernames[0][0] + "'"
                    cur.execute(deletesql)
                    con.commit()
                    break
            if t == 0:
                bot.send_message(query.message.chat.id, "Sorry! No lunch dates to be found! Your booking has been removed."
                                                        "\n \nUse /start to start a new session. "
                                                        "Thank you for using Chatthias!")
                deletesql = "DELETE FROM chatthias.users WHERE username = " + "'" + query.from_user.username + "'"
                cur.execute(deletesql)
                con.commit()

    elif data == 'cancelbooking':
        bot.answer_callback_query(query.id, "Cancelling Booking... ")
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.id, reply_markup=None)
        bot.send_message(query.message.chat.id, "Your booking has been cancelled. "
                            "You can start another booking with /start"
                            "\n \nThank you for supporting Chatthias.")
        #Deleting Current Record
        deletesql = "DELETE FROM chatthias.users WHERE username = " + "'" +query.from_user.username+ "'"
        cur.execute(deletesql)
        con.commit()
    elif data == 'continue':
        locationnotdone = "SELECT * FROM chatthias.users WHERE EXISTS " \
                          "(SELECT * FROM chatthias.users WHERE username = " + "'" \
                          + query.from_user.username + "'" + " AND location IS NULL)"
        paxnotdone = "SELECT * FROM chatthias.users WHERE EXISTS " \
                     "(SELECT * FROM chatthias.users WHERE username = " + "'" + \
                     query.from_user.username + "'" + " AND pax IS NULL)"
        datenotdone = "SELECT * FROM chatthias.users WHERE EXISTS " \
                      "(SELECT * FROM chatthias.users WHERE username = " + "'" + \
                      query.from_user.username + "'" + " AND date IS NULL)"
        timeslotnotdone = "SELECT * FROM chatthias.users WHERE EXISTS " \
                          "(SELECT * FROM chatthias.users WHERE username = " + "'" + \
                          query.from_user.username + "'" + " AND timeslot IS NULL)"
        if cur.execute(locationnotdone):
            bot.send_message(query.message.chat.id, "Thank you for using me. Select a place that you want to dine at",
                             reply_markup=placekeyboard)
        elif cur.execute(paxnotdone):
            bot.send_message(query.message.chat.id, "Select the number of pax you would want to dine with",
                             reply_markup=paxkeyboard)
        elif cur.execute(datenotdone) or cur.execute(timeslotnotdone):
            calendar, step = WMonthTelegramCalendar(min_date=date.today(),
                                                    max_date=date.today()
                                                    +relativedelta(weeks=+3)).build()
            bot.send_message(query.message.chat.id, "Select your desired date to dine", reply_markup=calendar)

    elif data == 'restart':
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.id, reply_markup=None)
        #Deleting Current Record
        deletesql = "DELETE FROM chatthias.users WHERE username = " + "'" +query.from_user.username+ "'"
        cur.execute(deletesql)
        con.commit()
        bot.send_message(query.message.chat.id, "Thank you for using me. Select a place that you want to dine at",
                         reply_markup=placekeyboard)
    elif data in placesDES:
        bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.id, reply_markup=None)
        if data == "TechnoEdgeDES":
            bot.send_message(query.message.chat.id, "TechnoEdge is a newly-renovated canteen at NUS Engineering. "
                                                    "Popular food choices include Western Fare, Vegetarian Food, "
                                                    "Indian Cuisine, Ramen & Fish Soup!"
                                                    "\n \nLocation: 2 Engineering Drive 4, S117584")
        elif data == "DeckDES":
            bot.send_message(query.message.chat.id, "Deck is located in the canteen at NUS Arts. "
                                                    "Popular food choices include their Mala and Pasta and "
                                                    "affordable CSSR. "
                                                    "There are around 13 stalls and it has a seating capacity of 1018!"
                                                    "\n \nLocation: NUS Computing Drive. The Deck Level 2")
        elif data == "FoodCliqueDES":
            bot.send_message(query.message.chat.id, "FoodClique is located at PGPR. Popular food choices "
                                                    "include Tian Tian Chicken Rice and Astons Express. "
                                                    "There are around 13 stalls and it has a seating capacity of 318!"
                                                    "\n \nLocation: 2 College Ave WWest, "
                                                    "Level 2 Stephen Riady Centre, S138607")
        elif data == "FrontierDES":
            bot.send_message(query.message.chat.id, "Frontier is located in the canteen at NUS Science. "
                                                    "Popular food choices include Chicken Rice and Western Cuisine. "
                                                    "There are around 15 stalls and it has a seating capacity of 700!"
                                                    "\n \nLocation: 12 Science Drive 2, S117549")
        elif data == "Central SquareDES":
            bot.send_message(query.message.chat.id, "Central Square is located in the Yusof Ishak House. "
                                                    "There are around 11 stalls and it has a seating capacity of 363!"
                                                    "\n \nLocation: 31 Lower Kent Ridge Rd, S119078")
        elif data == "Fine FoodDES":
            bot.send_message(query.message.chat.id, "Fine Food is one of the many food outlets located in NUS UTown. "
                                                    "There are around 14 stalls and it has a seating capacity of 410!"
                                                    "\n \nLocation: NUS, 1 Create Way, Town Plaza, S138602")
        elif data == "FlavoursDES":
            bot.send_message(query.message.chat.id, "Flavours@Utown is one of the many food outlets located in NUS "
                                                    "UTown. Popular food choices include the Yong Tau Foo. There are "
                                                    "around 10 stalls and it has a seating capacity of 700!"
                                                    "\n \nLocation: Flavours@UTown, Level 2 Stephen Riady Centre, "
                                                    "2 College Avenue West, S138607")

        bot.send_message(query.message.chat.id, "Use /locations to find out more dining locations near NUS"
                                                "\n \nUse /start to use Chatthias to find a lunch date now!"
                                                "\n \nUse /help for more commands")

bot.polling(none_stop=True)
