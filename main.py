- encoding: utf-8 -*-
import discord,asyncio, time, string, random, datetime, os, re, threading, chardet, sys, emoji, json, urllib.request, pytesseract
from PIL import Image
from discord.ext.commands import Bot
from discord.ext import commands
from threading import Timer
from threading import Thread
global total
total = 0

Client = discord.Client()
client = commands.Bot(command_prefix = "?")

def char_is_emoji(character):
    return character in emoji.UNICODE_EMOJI


def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False



@client.event
async def on_ready():
    print("Bot online.")
    client.loop.create_task(background_loop())

@client.event
async def on_member_join(member):
    for server in client.servers:
        member=member.id
    with open("tracker.txt", "r") as track:
        for ids in track:
            if str(member) in ids:
                member = server.get_member(member)
                role = discord.utils.get(server.roles, name="subscriber")
                await client.add_roles(member, role)

@client.event
async def background_loop():
    channelID = ["441203448323768320", "440951129052938240", "440951822639824907", "440951766616375306"]
    for channel in channelID:
        channelName = client.get_channel(channel)
        await client.purge_from(channelName, limit=1000000)     
    await asyncio.sleep(7200)


@client.event
async def on_message_edit(before, after):
    message = after
    test = "<@"+message.author.id+">"
    blacklistArray = []
    postedMessage = message.content.lower().replace(" ", "")
    if any(c.isdigit() for c in postedMessage):
        try:
            postedMessage = postedMessage.replace("4", "a")
            postedMessage = postedMessage.replace("1", "i")
            postedMessage = postedMessage.replace("3", "e")
        except:
            pass

    pmArray = ['.', '-', '/', ',', ';', "'", '"', '\\','{','}','|','[',']','=', '_']

    for symbol in pmArray:
        try:
            postedMessage = postedMessage.replace(symbol, "")
        except:
            pass
        
    postedMessage = postedMessage.replace('@', "a")
    postedMessage = postedMessage.replace("l", "i")
    postedMessage = postedMessage.replace("L", "i")
    emojiIn = text_has_emoji(postedMessage)
    if emojiIn == True:
        for symbol in postedMessage:
            if symbol in emoji.UNICODE_EMOJI:
                postedMessage = postedMessage.replace(symbol, "")
        
    
    non = isEnglish(postedMessage)
    if non == False:
        if not message.author.server_permissions.administrator:
            await client.delete_message(message)
            await client.send_message(message.channel, test+": Please only speak english in the chat. Non-Ascii Characters are not allowed.")


    if str(message.author.id) not in open("muted.txt", "r").read():
        with open("blacklist.txt", mode='r') as blacklist:
            for word in blacklist:
                word= word.rstrip()
                if not message.author.server_permissions.administrator:
                    if word in postedMessage:
                        await client.delete_message(message)
                        await client.send_message(message.channel, test+": Please do not speak of this in the chat, take some time to review discords terms of service. https://discordapp.com/terms")

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

        
@client.event
async def on_message(message):

    
    test = "<@"+message.author.id+">"
    blacklistArray = []
    postedMessage = message.content.lower().replace(" ", "")
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    if any(c.isdigit() for c in postedMessage):
        try:
            postedMessage = postedMessage.replace("4", "a")
            postedMessage = postedMessage.replace("1", "i")
            postedMessage = postedMessage.replace("3", "e")
        except:
            pass
            
    pmArray = ['.', '-', '/', ',', ';', "'", '"', '\\','{','}','|','[',']','=', '_']
    pmOkArray= ['yes', 'respect']

    
        
    for symbol in pmArray:
        try:
            postedMessage = postedMessage.replace(symbol, "")
        except:
            pass

    for word in pmOkArray:
        postedMessage = postedMessage.replace(word, "")
        
    postedMessage = postedMessage.replace('@', "a")
    postedMessage = postedMessage.replace("l", "i")
    postedMessage = postedMessage.replace("L", "i")

    
    emojiIn = text_has_emoji(postedMessage)
    if emojiIn == True:
        for symbol in postedMessage:
            if symbol != "'" or symbol != ',' or symbol != '‘':
                if symbol in emoji.UNICODE_EMOJI:
                    postedMessage = postedMessage.replace(symbol, "")
        
    
    non = isEnglish(postedMessage)
    if non == False:
        if not message.author.server_permissions.administrator:
            await client.delete_message(message)
            await client.send_message(message.channel, test+": Please only speak english in the chat. Non-Ascii Characters are not allowed.")
            print(str(message.content).translate(non_bmp_map))

    if str(message.author.id) not in open("muted.txt", "r").read():
        with open("blacklist.txt", mode='r') as blacklist:
            for word in blacklist:
                word= word.rstrip()
                if not message.author.server_permissions.administrator:
                    if word in postedMessage:
                        await client.delete_message(message)
                        await client.send_message(message.channel, test+": Please do not speak of this in the chat, take some time to review discords terms of service. https://discordapp.com/terms")
                        print(str(message.content).translate(non_bmp_map))
                        print(str(word).translate(non_bmp_map))

    if str(message.author.id) in open("muted.txt", "r").read():
        await client.delete_message(message)

    if message.content.upper().startswith("?PING"):
        time_then = time.monotonic()
        pinger = await client.send_message(message.channel, '__*`Pinging...`*__')
        ping = '%.2f' % (1000*(time.monotonic()-time_then))
        await client.edit_message(pinger, '**Pong!** __**`' + ping + 'ms`**__') 

    
    if message.content.upper().startswith('?PURGE'):
        args = message.content.split(" ") 
        command1 = (" ".join(args[1:2]))
        if message.author.server_permissions.administrator:
            try:
                await client.purge_from(message.channel, limit=int(command1))
            except:
                await client.send_message(message.channel, "You must enter a digit, not a string.")
                pass

        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")

            
            
    if message.content.upper().startswith('?BLACKLIST'):
        args = message.content.split(" ") 
        command1 = (" ".join(args[1:2]))
        command2 = (" ".join(args[2:3]))
        if message.author.server_permissions.administrator:
            if command1.lower() == "add":
                with open("blacklist.txt", mode='a+') as blacklist:
                    blacklist.write(command2+"\n")
                    await client.send_message(message.channel, command2 +" has been blacklisted.")
            elif command1.lower() == "del" or command1.lower() == "delete" or command1.lower() == "remove":
                with open("blacklist.txt", mode='r') as blacklistRead:
                    with open("blacklistTemp.txt", mode='a+') as blacklistTemp:
                        for word in blacklistRead:
                            if word !=command2+"\n":
                                blacklistTemp.write(word)
                        open('blacklist.txt', 'w').close()
                        await client.send_message(message.channel, command2 +" has been deleted.")
                os.replace("blacklistTemp.txt", "blacklist.txt")
                                    
                                
                            
            elif command1.lower() == "list":
                blacklistArray = []
                with open("blacklist.txt", mode='r') as blacklist:
                    for line in blacklist:
                        line = line.rstrip()
                        blacklistArray.append(line)
                    await client.send_message(message.channel, blacklistArray)
            elif command1.lower() == "help":
                await client.send_message(message.channel, "```diff\n-Blacklist Help-\n```\n\n")
                await client.send_message(message.channel, """```fix\n?blacklist add [word] | Blacklists the the word.
                                            \n?blacklist del|delete|remove [word] | Removes a word from the blacklist.
                                            \n?blacklist list | Displays the current blacklist.\n```""")
                    
                    
        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")
            
        
    if message.content.upper().startswith('?FA'):
        for server in client.servers:

            roles = server.roles
            members = server.members
            member = None

            for role in roles:
                role = role.id
                break

            for mem in members:
                if mem.id == message.author.id:
                    member = message.author.id
                    break
        if message.author.server_permissions.administrator:
             with open("tracker.txt", mode='r') as tracker:
                 await client.send_message(message.channel, "Fixing all subscribers.")
                 for current_line in tracker:
                     try:
                         split = current_line.split(" ")
                         userID = split[0]
                         role = discord.utils.get(server.roles, name="subscriber")
                         member = server.get_member(userID)
                         await client.add_roles(member, role)
                     except:
                         pass
        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")

            

    if message.content.upper().startswith('?SUDO'):
        for server in client.servers:

            roles = server.roles
            members = server.members
            member = None

            for role in roles:
                role = role.id
                break

            for mem in members:
                if mem.id == message.author.id:
                    member = message.author.id
                    break
        args = message.content.split(" ") 
        command1 = (" ".join(args[1:]))
        length = len(command1)
        if message.author.server_permissions.administrator:
            await client.delete_message(message)
            await client.send_message(message.channel, command1)
        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")



    if message.content.upper().startswith('?UNMUTE'):
        if message.author.server_permissions.administrator:
            args = message.content.split(" ")
            command1 = (" ".join(args[1:]))
            name = command1[2:]
            name = name[:-1]
            for server in client.servers:

                roles = server.roles
                members = server.members
                member = None
                for role in roles:
                    role = role.id
                    break

                for mem in members:
                    if mem.id == message.author.id:
                        member = message.author.id
                        break
            f = open("muted.txt","r")
            lines = f.readlines()
            f.close()
            f = open("muted.txt","w")
            for line in lines:
                if line!=name +"\n":
                    f.write(line)
            f.close()
        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")
            

    if message.content.upper().startswith('?HELP'):
        if str(message.author.id) not in open("muted.txt", "r").read():
            if message.author.server_permissions.administrator:
                await client.send_message(message.channel, "```diff\n-Staff Help List-\n```\n\n")
                await client.send_message(message.channel, "```?fix @16digitcode | Adds you to the premium rank.```")
                await client.send_message(message.channel, """\n```css\n?reset loaderName | Resets the user's WW HWID.
                                          \n?password loaderName | Resets the user's loader password.```""")
                await client.send_message(message.channel, """```fix\n?mute @user#0001 | Mutes the user and blocks user from running commands.
                                          \n?unmute @user#0001 | Unmutes a muted user.
                                          \n?upgrade @user#0001 | Upgrades specified user to premium rank in discord and adds user to the auto-db.\n```""")
                
            else:
                await client.send_message(message.channel, "```tex\n$ Help List $\n```\n\n")
                await client.send_message(message.channel, "```\n?fix @16digitcode | Adds you to the premium rank.\n```")
                

    if message.content.upper().startswith('?UPGRADE'):
        if message.author.server_permissions.administrator or "440949898695933962" in message.author.roles:
            try:
                args = message.content.split(" ")
                command1 = (" ".join(args[1:]))
                name = command1[2:]
                name = name[:-1]
                if "@" not in command1:
                    await client.send_message(message.channel, "Incorrect usage.\n \n Usage: ?upgrade @user#0001")  
                elif "@" in command1:
                    
                    for server in client.servers:
                        hi = server.get_member(name)
                    with open("tracker.txt", "a") as text_file:
                        text_file.write(name + " 1234567890123456" +"\n")
                    role = discord.utils.get(server.roles, name="subscriber")
                    await client.add_roles(hi, role)
                    test = "<@"+name+">"
                    await client.send_message(message.channel, "Successfully set %s's rank to premium." % test)
            except:
                await client.send_message(message.channel, "Not a valid user.")
                pass

        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")




    if message.content.upper().startswith('?MUTE'):
        if message.author.server_permissions.administrator:
            args = message.content.split(" ")
            command1 = (" ".join(args[1:]))
            name = command1[2:]
            name = name[:-1]
            for server in client.servers:
                hi = server.get_member(name)
            try:
                if hi.server_permissions.administrator:
                    await client.send_message(message.channel, "You cannot use this against another staff member.")
                else:
                    for server in client.servers:

                        roles = server.roles
                        members = server.members
                        member = None
                        for role in roles:
                            role = role.id
                            break

                        for mem in members:
                            if mem.id == message.author.id:
                                member = message.author.id
                                break
                    with open("muted.txt", "a") as text_file:
                        text_file.write(name + "\n")
            except:
                 pass
                
                
        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")


        
    #Depreciated as of 5/01/2018
    ''' 
    if message.content.upper().startswith('?FIX'):
        if str(message.author.id) not in open("muted.txt", "r").read():
            args = message.content.split(" ")
            command1 = (" ".join(args[1:]))
            length = len(command1)
            for server in client.servers:

                roles = server.roles
                members = server.members
                member = None
                for role in roles:
                    role = role.id
                    break

                for mem in members:
                    if mem.id == message.author.id:
                        member = message.author.id
                        break

            if str(command1).upper() == "HELP":
                test = "<@"+message.author.id+">"
                await client.delete_message(message)
                await client.send_message(message.channel, test +":\n"
                                          "```css\n"
                                          "This command can only be used once per code.\n"
                                          "To activate your premium role you must find the selly.gg email and use the registration key at the bottom of your email.\n"
                                          "Once you have located this code send the following message;\n"
                                          "?fix ENTERCODEHERE\n"
                                          "After usage of code your Discord account will have premium access.```")

            if len(command1)< 16 or len(command1) > 16:
                test = "<@"+message.author.id+">"
                await client.delete_message(message)
                await client.send_message(message.channel, test +":\n"
                                          "```css\n"
                                          "This command can only be used once per code.\n"
                                          "To activate your premium role you must find the selly.gg email and use the registration key at the bottom of your email.\n"
                                          "Once you have located this code send the following message;\n"
                                          "?fix ENTERCODEHERE\n"
                                          "After usage of code your Discord account will have premium access.```")
                
            else:
                if length == 16:
                    if command1 in open("RegKeysFix.txt","r").read():
                        f = open("RegKeysFix.txt","r")
                        lines = f.readlines()
                        f.close()
                        f = open("RegKeysFix.txt","w")
                        for line in lines:
                          if line!=command1 +"\n":
                            f.write(line)
                        f.close()
                        
                        with open("tracker.txt", "a") as myfile:
                            myfile.write(str(message.author.id) + " " + str(command1) + "\n")
                        await client.delete_message(message)
                        role = discord.utils.get(server.roles, name="subscriber")
                        member = server.get_member(member)
                        await client.add_roles(member, role)
                        test = "<@"+message.author.id+">"
                        await client.send_message(message.channel, "Successfully set %s's rank to premium." % test)

                    else:
                        await client.delete_message(message)
                        await client.send_message(message.channel, "This is not a valid premium code.")
                else:
                    await client.delete_message(message)
                    await client.send_message(message.chfannel, "This is not a valid premium code.")

            '''

client.run("[Token]")
