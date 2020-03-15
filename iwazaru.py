import discord
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()

with open("token.txt", "r", encoding="utf-8") as file:
    TOKEN = file.read().strip()
with open("emoji_surrogates.txt", "r", encoding="utf-8") as file:
    EMOJI_SURROGATES = file.read().split("\n")
BONUS_CHARS = [" ", "\n"]

MORPHEMES = EMOJI_SURROGATES + BONUS_CHARS

def made_of_emoji(text): #it's recursion! it's beautiful!
    """Check if text is valid emoji message content (can be composed of substrings in MORPHEMES)."""
    if text == "":
        return True
    for m in MORPHEMES:
        if text.startswith(m):
            if made_of_emoji(text[len(m):]):
                return True
    return False
def message_is_valid(message):
    """Valid messages have emoji-only content and no embeds."""
    return made_of_emoji(message.content) and not message.embeds

@client.event
async def on_message(message):
    if not (message.guild and message.channel.permissions_for(message.guild.me).manage_messages):
        logging.info("Ignoring message in restricted channel. u_u")
        return
    
    if message.content == "cleanse":
        # purge non-emoji messages
        logging.info("Cleansing... >-<")

        await message.delete()
        
        messagescleansed = 0
        reactionscleansed = 0

        async for message in message.channel.history():
            if not message_is_valid(message):
                await message.delete()
                messagescleansed += 1
                continue
            for reaction in message.reactions:
                #is this really the way to mass-remove specific reactions? it seems kind of bad
                if reaction.custom_emoji or not made_of_emoji(reaction.emoji):
                    for user in await reaction.users().flatten():
                        await reaction.remove(user)
                    reactionscleansed += 1

        logging.info("Done cleansing! :3\n  Messages deleted: {}\n  Reactions deleted: {}".format(messagescleansed, reactionscleansed))
        return
    
    if not message_is_valid(message):
        # delete non-emoji messages
        logging.info("Invalid message! Deleting! >.<")
        logging.info(message.content)
        await message.delete()

@client.event
async def on_message_edit(_, message): #we don't care about the before-message
    if not (message.guild and message.channel.permissions_for(message.guild.me).manage_messages):
        logging.info("Ignoring message edit in restricted channel. u_u")
        # ignore DMs
        return
    if message_is_valid(message):
        logging.info("Invalid message edit! Deleting! >.<")
        logging.debug(message.content)
        await message.delete()

@client.event
async def on_reaction_add(reaction, user):
    #basically, no nitro reactions and no regional indicator reactions.
    logging.debug("Reaction added!")
    if not (reaction.message.guild and reaction.message.channel.permissions_for(reaction.message.guild.me).manage_messages):
        logging.info("Ignoring reaction in restricted channel. u_u")
        # ignore DMs
        return
    if reaction.custom_emoji or not made_of_emoji(reaction.emoji):
        logging.info("That was a bad reaction! Removing...! >.<")
        logging.info(reaction.emoji)
        await reaction.remove(user)

@client.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)
    logging.info('--------')

client.run(TOKEN)
