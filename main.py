import telebot
from telebot import types
import requests
import random
import flask

appname="hp--quiz"
server = flask.Flask(_name_)
apikey="c3b72fba-ccc3-4d99-a3d3-e8576f62152c"

token="992524029:AAEfRoU11Gipy9_bspGQfGGLqHc-oRDpvV0"
bot=telebot.TeleBot(token)

link="http://hp-api.herokuapp.com/api/characters"
dataa=requests.get(link)
data=dataa.json()
    
a=0
ans=0
x="Guess"

@bot.message_handler(commands=["start"])
def Start(msg):
    name=msg.from_user.first_name
    bot.send_message(msg.chat.id, "Hello, "+name+"!")
    bot.send_message(msg.chat.id, "Let's play!")
    GetApi(msg)

def GetApi(msg):
    global a
    global data
    a=random.randint(1,25)
    character=data[a]
    print(character)
    Ask(msg)
    
def Ask(msg):
    global x
    keyboard=types.ReplyKeyboardMarkup()
    btn1=types.KeyboardButton("What is his/her gender?")
    btn2=types.KeyboardButton("Character's ancestry is...")
    btn3=types.KeyboardButton("What house does character belong to?")
    btn4=types.KeyboardButton("What colour hair is?")
    btn5=types.KeyboardButton("Does the character studies at Hogwards?")
    btn6=types.KeyboardButton("I know the name")
    btn7=types.KeyboardButton("I don't know, I don't knoooow")

    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    keyboard.add(btn5)
    keyboard.add(btn6)
    keyboard.add(btn7)
    answer=bot.send_message(msg.chat.id, x, reply_markup=keyboard)
    bot.register_next_step_handler(answer, Answer)
    
def Answer(msg):
    global x
    global a
    global data
    if msg.text=="What is his/her gender?":
        gender=data[a]["gender"]
        x="Character is "+gender
        Ask(msg)
    if msg.text=="Character's ancestry is...":
        ancestry=data[a]["ancestry"]
        if ancestry=="":
            x="Character's ancestors unknown"
            Ask(msg)
        else:
            x="Character is "+ancestry
            Ask(msg)
    if msg.text=="What house does character belong to?":
        house=data[a]["house"]
        if house=="":
            x="Character's house unknown"
            Ask(msg)
        else:
            x="Character studied at "+house
            Ask(msg)
    if msg.text=="What colour hair is?":
        hair=data[a]["hairColour"]
        x="Character hair is "+hair
        Ask(msg)
    if msg.text=="Does the character studies at Hogwards?":
        Hogwards=data[a]["hogwartsStudent"]
        if str(Hogwards)=="True":
            x="Hmmm...Yes"
            Ask(msg)
        else:
            x="Nope"
            Ask(msg)
    if msg.text=="I know the name":
        keyboard=types.ReplyKeyboardRemove(selective=False)
        bot.send_message(msg.chat.id, "You have only 3 chances", reply_markup=keyboard)
        answer=bot.send_message(msg.chat.id, "And who?")
        bot.register_next_step_handler(answer, Name)
    if msg.text=="I don't know, I don't knoooow":
        keyboard=types.ReplyKeyboardRemove(selective=False)
        bot.send_message(msg.chat.id, ":(", reply_markup=keyboard)
        Name3(msg)
##    else:
##        bot.send_message(msg.chat.id, "You know the rules")
def Name(msg):
    global a
    global data
    if msg.text==data[a]["name"]:
        bot.send_message(msg.chat.id, """Awesome!
You are right!""")
        answer=bot.send_message(msg.chat.id, """Would you like to know about character more?
Yes/No""")
        bot.register_next_step_handler(answer, Info)
    else:
        answer=bot.send_message(msg.chat.id, "no :)")
        bot.register_next_step_handler(answer, Name2)
def Name2(msg):
    global a
    global data
    if msg.text==data[a]["name"]:
        bot.send_message(msg.chat.id, """Awesome!
You are right!""")
        answer=bot.send_message(msg.chat.id, """Would you like to know about character more?
Yes/No""")
        bot.register_next_step_handler(answer, Info)
    else:
        answer=bot.send_message(msg.chat.id, "no :)")
        bot.register_next_step_handler(answer, Name3)
def Name3(msg):
    global a
    global data
    if msg.text==data[a]["name"]:
        bot.send_message(msg.chat.id, """Awesome!
You are right!""")
    else:
        bot.send_message(msg.chat.id, """Regretfully, you fail.
My character was: """+data[a]["name"])
    answer=bot.send_message(msg.chat.id, """Would you like to know about character more?
Yes/No""")
    bot.register_next_step_handler(answer, Info)
def Info(msg):
    global a
    global data
    d=data[a]
    if msg.text=="Yes":
        for key in d.keys():
            bot.send_message(msg.chat.id, str(key)+" : "+str(d[key]))
    else:
        bot.send_message(msg.chat.id, "OK")

#bot.polling()
#If you wanna hack this code, know that code is made by 15 year old girl who loves IT and lives in KZ... You may broke her heart. Because she is very pround with it!

@server.route('/' + token, methods=['POST'])
def get_message():
     bot.process_new_updates([types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
     return "!", 200

@server.route('/', methods=["GET"])
def index():
     bot.remove_webhook()
     bot.set_webhook(url=f"https://{appname}.herokuapp.com/{token}")
     return "Hello from Heroku!", 200
     

if _name_ == "_main_":
     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
