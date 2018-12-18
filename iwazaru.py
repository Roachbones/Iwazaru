#version 0.1

import discord

client = discord.Client()

with open("token.txt", "r", encoding="utf-8") as opened:
    TOKEN = opened.read()
with open("emojisurrogates.txt", "r", encoding="utf-8") as opened:
    EMOJISURROGATES = [i.strip() for i in opened.readlines()]
    #note: this might be harsh to regional pairs who lack ZWJs
    #they are supposed to be ZWJed but i think sometimes they aren't
with open("emojinames.txt", "r", encoding="utf-8") as opened:
    EMOJINAMES = [":"+i.strip()+":" for i in opened.readlines()]
BONUSCHARS = [" ", "\n"]

MORPHEMES = EMOJISURROGATES + EMOJINAMES + BONUSCHARS

SERVERID = "523999837968924693"
GENERALCHANNELID = "524040381323542528"

def isvalid(text): #it's a tree! it's recursion! it's beautiful!
    """Check is text is a valid emoji message (can be composed of substrings in MORPHEMES)."""
    if text == "":
        return True
    for m in MORPHEMES:
        if text.startswith(m):
            if isvalid(text[len(m):]):
                return True
    return False
def purgecheck(message):
    """Checks if a message should be purged for the cleanse command."""
    return not isvalid(message.content)

@client.event
async def on_message(message):
    if message.channel.is_private:
        # ignore DMs
        return
    
    if message.content == "cleanse":
        # purge non-emoji messages
        print("cleansing...")
        await client.purge_from(message.channel, limit=5000, check=purgecheck)
        print("done cleansing! :3")
        return
    if message.content == "shutdown" and message.author.id == "174636314019364864":
        # silence everyone, so that they can't say non-emoji while iwazaru is offline
        client.delete_message(message)
        server = client.get_server(SERVERID)
        default_role = server.default_role
        permissions = default_role.permissions
        permissions.send_messages = False
        await client.edit_role(server, default_role, permissions=permissions)
        await client.send_message(client.get_channel(GENERALCHANNELID), "😴") #sleeping face emoji
        print("shutting down UwU")
        await client.logout()
    
    if not isvalid(message.content):
        # delete non-emoji messages
        await client.delete_message(message)

@client.event
async def on_message_edit(_, message):
    if not isvalid(message.content):
        await client.delete_message(message)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    server = client.get_server(SERVERID)
    default_role = server.default_role
    permissions = default_role.permissions
    permissions.send_messages = True
    await client.edit_role(server, default_role, permissions=permissions)

client.run(TOKEN)
