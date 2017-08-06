from telegram.ext import Updater, CommandHandler
import sched, time, random, logging, pickle, datetime, calendar

configFile = "./session.pk"

watb = "-1001049406492"
newseeds = "-1001138132564"
retardStickerId = "CAADBAAD2wADeyqRC60Pvd---1a5Ag";
tagMsg = "#musictheatre @jntn7 @poisonparty @ruderubikscube @zhmaky @Xanes @Tova96 @danitkoy @greinchrt @jokullmusic @GalaxyDrache @ysoftware @sexy_nutella_69 @Tom_veldhuis @Doomgoat @ilya_mordvinkin @amobishoproden @tbshfmn";

admins = [
          "ysoftware",
          "tbshfmn",
          "sexy_nutella_69",
          "amobishoproden",
          "Doomgoat",
          "ruderubikscube",
          "Tom_veldhuis"
          ]

# - utilities

# time

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt): # datetime.datetime.now()
    return (dt - epoch).total_seconds() * 1000.0

def checkAccess(update):
    return update.message.from_user.username in admins

def isNewCommand(update):
    timenow = unix_time_millis(datetime.datetime.now())
    messageTime = unix_time_millis(update.message.date)
    dt = timenow - messageTime
    print(update.message.text + " from " + update.message.from_user.username + " delayed by {}".format(dt))
    return dt < 23456

# quotes

def randomCunt():
    return random.choice(["Ready Lets Go", "Here we go...", "Come to Daddy"])

# session persistence

def saveConfig(config):
    with open(configFile, "wb") as fi:
        pickle.dump(config, fi)
        print("- {}".format(config))

def loadConfig():
    try:
        with open(configFile, "rb") as fi:
            config = pickle.load(fi)
            return config
    except:
        print("config file is not found")
        config = [False, "", "", ""]
        saveConfig(config)
        return config

# - commands

# session

def over(bot, update):
    if not checkAccess(update):
        return
    config = loadConfig()
    if config[0] == True:
        if isNewCommand(update):
            bot.sendMessage(newseeds, "#musictheatre it's OVER.")
        endSession()
    else:
        update.message.reply_text("You betcha it is.")

def abort(bot, update):
    if not checkAccess(update):
        return
    config = loadConfig()
    if config[0] == True:
        if isNewCommand(update):
            bot.sendMessage(newseeds, "#musictheatre it's ABORTED.")
        endSession()
    else:
        update.message.reply_text("I'll abort you, you fucking bitch.")

def newAlbum(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    config = loadConfig()
    if config[0] == False:
        message = update.message.text.split(" ", 1)[1].strip()
        artistName = message.split(" - ", 1)[0].strip()
        albumName = message.split(" - ", 1)[1].strip()

        if len(albumName) > 0 and len(artistName) > 0:
            config[0] = True
            config[1] = artistName
            config[2] = albumName
            config[3] = ""
            text = "#musictheatre New Album: {0} - {1}".format(config[1].encode('utf-8'), config[2].encode('utf-8'))
            bot.sendMessage(newseeds, text)
            saveConfig(config)
    else:
        bot.sendMessage(newseeds, "Fuck no, not this shitty album.")

def nextSong(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    config = loadConfig()
    if config[0] == True:
        trackName = update.message.text.split(" ", 1)[1].strip()
        if len(trackName) > 0 and len(config[1]) > 0 and trackName != config[3]:
            config[3] = trackName
            text = "#musictheatre {0} - {1}".format(config[1].encode('utf-8'), config[3].encode('utf-8'))
            bot.sendMessage(newseeds, text)
            saveConfig(config)
    else:
        bot.sendMessage(newseeds, "What album was that again?")

def endSession():
    saveConfig([False, "", "", ""])

# current

def currentAlbum(bot, update):
    if not isNewCommand(update):
        return
    config = loadConfig()
    if config[0] == True:
        if len(config[1]) > 0 and len(config[2]) > 0:
            text = "{0} by {1}".format(config[2].encode('utf-8'), config[1].encode('utf-8'))
            update.message.reply_text(text)
    else:
        update.message.reply_text("Nothing is playing.")


def currentTrack(bot, update):
    if not isNewCommand(update):
        return
    config = loadConfig()
    if config[0] == True:
        if len(config[1]) > 0 and len(config[2]) > 0 and len(config[3]) > 0:
            text = "Now playing: {0} - {1} (from {2})".format(config[1].encode('utf-8'), config[3].encode('utf-8'), config[2].encode('utf-8'))
            update.message.reply_text(text)
    else:
        update.message.reply_text("Nothing is playing.")

# countdown

def cunt(bot, update):
    if not isNewCommand(update):
        return
    if checkAccess(update):
        bot.sendMessage(newseeds, randomCunt().encode('utf-8'))
        count = 5
        while count:
            bot.sendMessage(newseeds, "{}".format(count))
            time.sleep(1)
            count -= 1
        bot.sendMessage(newseeds, "PLAY!")

# roll

def roll(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    config = loadConfig()
    print(config)
    if config[0] == False:
        limit = int(update.message.text.split(" ")[1])
        if limit and limit >= 4:
            result = random.randint(4, limit)
            bot.sendMessage(newseeds, "Rolled <b>{}</b>.".format(result), parse_mode="HTML")
    else:
    	update.message.reply_text("I'm sorry. I'm afraid I can't do that.")

# suggest

def suggest(bot, update):
    if not isNewCommand(update):
        return
    config = loadConfig()
    if config[0] == False:
        bot.sendMessage(newseeds, "<b>Anyone in for a </b>#musictheatre<b> session?</b>", parse_mode="HTML")
    else:
        bot.sendMessage(newseeds, "The session is still on, isn't it? ISN'T IT?")


# help

def help(bot, update):
    if not isNewCommand(update):
        return
    update.message.reply_text("Here's the list of available commands:\n<b>/spreadsheet</b> gives you the link to our spreadsheet\n<b>/suggest</b> will ask if anyone wants to start a session\n<b>/admins</b> for the list of people who have admin access\n\nUse these while in session:\n<b>/song</b> or <b>/album</b> to find out what's playing".encode('utf-8'), parse_mode="HTML")

# say something

def say(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    if update.message.chat_id == newseeds:
        return
    message = update.message.text.split(" ", 1)[1].strip()
    bot.sendMessage(newseeds, message.encode('utf-8'), parse_mode="HTML")

def sticker(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    if update.message.chat_id == newseeds:
        return
    message = update.message.text.split(" ", 1)[1].strip()
    bot.sendSticker(newseeds, message)

# admins

def adminList(bot, update):
    if not isNewCommand(update):
        return
    text = "These <i>(%username%)</i>s have access to the bot's #musictheatre session commands:\n"
    for name in admins:
        text += "- " + name + "\n"
    text += "If they are not around, God help you."
    update.message.reply_text(text.encode('utf-8'), parse_mode="HTML")

# spreadshit link

def shit(bot, update):
    if not isNewCommand(update):
        bot.sendMessage(newseeds, "Hey folks, our spreadshit is here: http://bit.ly/mtheatre", parse_mode="HTML")
    else:
        update.message.reply_text("Here's the link to our spreadshit: http://bit.ly/mtheatre")

# tag

def tagPeople(bot, update):
    if not isNewCommand(update):
        return
    if not checkAccess(update):
        return
    if not isNewCommand(update):
        return
    bot.sendMessage(newseeds, tagMsg, parse_mode="HTML")

# retarded

def slow(bot, update):
    if not isNewCommand(update):
        return
	bot.sendSticker(newseeds, retardStickerId)

# work

def test(bot, update):
    if not isNewCommand(update):
        return
    if update.message.from_user.username == "ysoftware":
        update.message.reply_text("9")

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater('337143431:AAH1TZLyqBTuHEKIIZ7OvEnmNL03I-EcHRM')

# general commands

updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('admins', adminList))

updater.dispatcher.add_handler(CommandHandler('shit', shit))
updater.dispatcher.add_handler(CommandHandler('sheet', shit))
updater.dispatcher.add_handler(CommandHandler('spreadshit', shit))
updater.dispatcher.add_handler(CommandHandler('spreadsheet', shit))

updater.dispatcher.add_handler(CommandHandler('suggest', suggest))
updater.dispatcher.add_handler(CommandHandler('song', currentTrack))
updater.dispatcher.add_handler(CommandHandler('album', currentAlbum))
updater.dispatcher.add_handler(CommandHandler('tag', tagPeople))

# admin commands

updater.dispatcher.add_handler(CommandHandler('roll', roll))
updater.dispatcher.add_handler(CommandHandler('cunt', cunt))
updater.dispatcher.add_handler(CommandHandler('new', newAlbum))
updater.dispatcher.add_handler(CommandHandler('n', nextSong))
updater.dispatcher.add_handler(CommandHandler('abort', abort))
updater.dispatcher.add_handler(CommandHandler('over', over))

updater.dispatcher.add_handler(CommandHandler('b', say))
updater.dispatcher.add_handler(CommandHandler('s', sticker))
updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(CommandHandler('slow', slow))

updater.start_polling()
updater.idle()
