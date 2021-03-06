# -*- coding: utf-8 -*-
"""
This module is distributed as part of the Laminaria Core (Python Version).
Get the Source Code in GitHub:
https://github.com/MrKelpy/LaminariaCore

The LaminariaCore is Open Source and distributed under the
MIT License
"""

# Built-in Imports
import datetime
import random
import asyncio
import os

# Third Party Imports
import screeninfo
from discord.ext import commands
import discord
from fpdf import FPDF

# Local Application Imports

###############################################################################
###                             DATE & TIME                                 ###
###############################################################################


def twochars(arg):
    """
    Formats a string of two characters into the format of (0X), useful for date formatting.
    :param arg: The string
    :return: String
    """

    if len(arg) == 1:
        return f"0{arg}"
    return arg


def get_formatted_date(date: datetime, include_seconds: bool = False):
    """
    Returns a given date in the handy DD/MM/YY - HH:MM:SS format.
    :param date: The date to be formatted -> datetime.datetime
    :param include_seconds: If set to True, include seconds in the format.
    :return: String
    """

    date_string = f"{twochars(str(date.day))}/{twochars(str(date.month))}/{twochars(str(date.year))} - " \
                  f"{twochars(str(date.hour))}:{twochars(str(date.minute))}"

    if include_seconds:
        date_string += f":{twochars(str(date.second))}"

    return date_string


def get_formatted_date_now(include_seconds: bool = False, formatting: int = 1):
    """
    Returns the current date in the handy DD/MM/YY - HH:MM:SS format (default) or in the specified one.
    :param formatting: Format type -> int
    :param include_seconds: If set to True, include seconds in the format.
    :return: String
    """

    now = datetime.datetime.now()
    if formatting == 1:
        date_string = f"{twochars(str(now.day))}/{twochars(str(now.month))}/{twochars(str(now.year))} - " \
                      f"{twochars(str(now.hour))}:{twochars(str(now.minute))}"

    elif formatting == 2:
        date_string = f"{twochars(str(now.day))}.{twochars(str(now.month))}.{twochars(str(now.year))}_" \
                      f"{twochars(str(now.hour))}.{twochars(str(now.minute))}"

    else:
        date_string = f"{twochars(str(now.day))}/{twochars(str(now.month))}/{twochars(str(now.year))} - " \
                      f"{twochars(str(now.hour))}:{twochars(str(now.minute))}"

    if include_seconds:
        date_string += f":{twochars(str(now.second))}"

    return date_string


def time_until_midnight():
    """
    Get seconds left until midnight
    """
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    timedelta_until_midnight = datetime.datetime.combine(tomorrow, datetime.time.min) - datetime.datetime.now()
    return timedelta_until_midnight.seconds


###############################################################################
###                               GENERAL                                   ###
###############################################################################


def get_absolute_screen_coords(relx, rely):
    """
    Returns absolute screen coordinates based off the given relative
    coordinates. For instance, in a 1920x720 screen, the x50, y50 input would be
    x960, y360.
    :param relx: Relative X Coordinate
    :param rely: Relative Y Coordinate
    :return: Absolute Coordinates
    """

    monitor = screeninfo.get_monitors()[0]
    x = (relx*monitor.width)/100
    y = (rely*monitor.height)/100
    return x, y


def get_relative_screen_coords(x, y):
    """
    Returns relative screen coordinates based off the given absolute
    coordinates. The relative coordinates are percentage-based values calculates
    relatively to the monitor specs and the given coords.
    :param x: Absolute X
    :param y: Absolute Y
    :return:
    """

    monitor = screeninfo.get_monitors()[0]
    relx = (x*100)/monitor.width
    rely = (y*100)/monitor.height
    return relx, rely


###############################################################################
###                            PLACEHOLDERS                                 ###
###############################################################################


async def small_ipsum():
    """
    Returns the small version of the lorem impsum placeholder
    :return:
    """
    return "Lorem ipsum dolor sit amet."


async def big_ipsum():
    """
    Returns a bigger version of the lorem ipsum text than the small_ipsum function does.
    :return:
    """
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt " \
           "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco " \
           "laboris nisi ut aliquip ex ea commodo consequat."


###############################################################################
###                             DISCORD.PY                                  ###
###############################################################################


async def hasrole(role: discord.Role, user: discord.Member, add: bool = False):
    """
    Checks if a user has a certain role.
    :param role: The role to be checked for. -> discord.Role
    :param user: The user. -> discord.Member
    :param add: If set to True, adds the role to the user, will always return True.
    :return: True, if user has the role. False otherwise.
    """

    for r in user.roles:

        if r == role:
            return True

    else:
        if add is True:
            await user.add_roles(role)
            return True

        return False


async def getrolenamed(role: str, guild: discord.Guild, create: bool = False, exact: bool = True):
    """
    Returns a role inside a Guild based on a given name.
    :param role: The role to be gathered. -> str
    :param guild: The guild to retrieve the role from. -> discord.Guild
    :param create: If set to True, creates the role. (If non existant!)
    :param exact: If set to True, matches the role exactly
    :return: discord.Role, None if not found.
    """

    for r in guild.roles:

        if exact and r.name == role:
            return r

        elif role in r.name:
            return r
    else:
        if create is True:
            colours = [discord.Colour.red(), discord.Colour.dark_teal(), discord.Colour.teal(), discord.Colour.gold(),
                       discord.Colour.blurple(), discord.Colour.purple(), discord.Colour.green(),
                       discord.Colour.greyple(),
                       discord.Colour.orange(), discord.Colour.light_grey()]

            return_role = await guild.create_role(name=role, colour=random.choice(colours))
            return return_role

        return None


async def get_textchannel_by_name(channel: str, guild: discord.Guild,
                                  delete: bool = False, create: bool = False, category: str = None, exact: bool = True):
    """
    Returns a text channel based on a given name.
    :param channel: The channel to be gathered. -> str
    :param guild: The guild to retrieve the channel from. -> discord.Guild
    :param delete: If set to True, deletes the role. (If found!)
    :param create: If set to True, creates the role. (If not found!)
    :param category: The category to create the channel into. (If create is True!)
    :param exact: If set to True, the channelname needs to match the channel at 100%. Else, no.
    :return: discord.TextChannel, None if not found.
    """

    for text_channel in guild.text_channels:

        if exact:
            if text_channel.name == channel.lower():

                if delete is True:
                    await text_channel.delete()
                    continue

                return text_channel

        else:
            if channel.lower() in text_channel.name:

                if delete is True:
                    await text_channel.delete()
                    continue

                return text_channel

    if create is True:
        text_channel = await guild.create_text_channel(channel, category=category)
        return text_channel

    return None


async def get_category_by_name(category_name: str, guild: discord.Guild, delete: bool = False, create: bool = False,
                               exact: bool = True):
    """
    Returns a category based on a given name.
    :param exact: If set to True, matches the name exactly as it is.*
    :param category_name: The category to be gathered. -> str
    :param guild: The guild to retrieve the category from. -> discord.Guild
    :param delete: If set to True, deletes the category. (If found!)
    :param create: If set to True, creates the category. (If not found!)
    :return: discord.Category, None if not found.
    """

    for category in guild.categories:
        if exact and category.name == category_name:

            if delete is True:
                await category.delete()
                continue

            return category

        elif not exact and category_name in category.name:

            if delete is True:
                await category.delete()
                continue

            return category

    if create is True:
        category = await guild.create_category(category_name)
        return category

    return None


async def twochars_async(arg):
    """
    Formats a string of two characters into the format of (0X), useful for date formatting.
    :param arg: The string
    :return: String
    """

    if len(arg) == 1:
        return f"0{arg}"
    return arg


async def as_get_formatted_date_now(include_seconds: bool = False, formatting: int = 1):
    """
    Returns the current date in the handy DD/MM/YY - HH:MM:SS format (default) or in the specified one.
    :param formatting: Format type -> int
    :param include_seconds: If set to True, include seconds in the format.
    :return: String
    """

    now = datetime.datetime.now()
    if formatting == 1:
        date_string = f"{await twochars(str(now.day))}/{await twochars(str(now.month))}/{await twochars(str(now.year))} - " \
                      f"{await twochars(str(now.hour))}:{await twochars(str(now.minute))}"

    elif formatting == 2:
        date_string = f"{await twochars(str(now.day))}.{await twochars(str(now.month))}.{await twochars(str(now.year))}_" \
                      f"{await twochars(str(now.hour))}.{await twochars(str(now.minute))}"

    else:
        date_string = f"{await twochars(str(now.day))}/{await twochars(str(now.month))}/{await twochars(str(now.year))} - " \
                      f"{await twochars(str(now.hour))}:{await twochars(str(now.minute))}"

    if include_seconds:
        date_string += f":{await twochars(str(now.second))}"

    return date_string


async def get_formatted_date_async(date: datetime, include_seconds: bool = False):
    """
    Returns a given date in the handy DD/MM/YY - HH:MM:SS format.
    :param date: The date to be formatted -> datetime.datetime
    :param include_seconds: If set to True, include seconds in the format.
    :return: String
    """

    date_string = f"{await twochars(str(date.day))}/{await twochars(str(date.month))}/{await twochars(str(date.year))} - " \
                  f"{await twochars(str(date.hour))}:{await twochars(str(date.minute))}"

    if include_seconds:
        date_string += f":{await twochars(str(date.second))}"

    return date_string


async def send_loading(channel: discord.TextChannel, colour=discord.Colour.red()):
    """
    Sends a loading embed to a specified channel.
    :param channel: The channel for the message to be sent to. -> discord.TextChannel
    :param colour: The embed colour. -> discord.Colour
    :return: discord.Embed
    """

    loading_embed = discord.Embed(
        title='Loading...',
        colour=colour
    )

    loading = await channel.send(embed=loading_embed)
    return loading


async def get_textchannel_chatlog(text_channel: discord.TextChannel, limit: int = None):
    """
    Returns a TextChannel chatlog
    :param text_channel: The text channel for the data to be gathered from
    :param limit: An integer to limit the amount of messages retrieved.
    :return: String
    """

    all_messages = await text_channel.history(limit=limit).flatten()
    all_messages.reverse()

    # Parses out and legibilises the messages into a chatlog
    chatlog = ""
    for message in all_messages:

        if message.embeds:
            content = message.embeds[0].title
        elif message.attachments:
            content = f"FILE(s) :{[file.filename for file in message.attachments]}"
        else:
            content = message.content
            content = content.split("```")
            content = '\n'.join(content)

        chatlog += f"[{await get_formatted_date_async(message.created_at, include_seconds=True)}] [- MSG ID: {message.id}]" \
                   f" [- AUTHOR ID: {message.author.id}] <{message.author}> {content}\n"

    return chatlog


async def get_textchannel_firstmessage(text_channel: discord.TextChannel):
    """
    Returns the first message on a TextChannel
    :param text_channel: The textchannel to retrieve the message from. -> discord.TextChannel
    :return: discord.Message
    """

    all_messages = await text_channel.history(limit=None).flatten()
    all_messages.reverse()

    return all_messages[0]


async def get_member_object(member_id: int, guild: discord.Guild):
    """
    Returns a discord.Member object of a member from a given ID
    :param member_id: The member ID. -> int
    :param guild: The guild to retrieve the member from. -> discord.Guild
    :return: discord.Member, None if not found.
    """

    for member in guild.members:

        if int(member.id) == int(member_id):
            return member

    return None


async def show_help_menu(ctx, bot: commands.Bot, colour=discord.Colour.red(), reverse=False):
    """
    Standard help menu used between bots created by Alex, with loads of quirks to make the UI more appealing.
    The help menu is completely computer-generated.

    Description management:
        > Leaving the description of a command without text will it not be shown in the UI
        > Writing |String| at the beggining of a command description will have it sorted into a category
        (Replace "String" with the category name)
        > Categories are sorted alphabetically, aswell as bot_commands.
        > Not specifying a category will result in the command being thrown into a "General" category

    :param reverse:
    :param ctx: discord context.
    :param bot: discord BOT instance.
    :param colour: Help menu embed colour
    :return: discord.Embed
    """

    help_menu_base = discord.Embed(
        title=f"{bot.user.name}'s Help Menu - ",
        description=f"Prefix: `{ctx.prefix}`",
        colour=colour
    )

    dev = await bot.fetch_user(740969223681212507)
    commands_dictionary = dict()
    embed_list = list()

    for command in bot.commands:
        # Iterates through all the registered bot_commands

        if not command.description:
            # Skips over the command if no description is provided
            continue

        category_name = "General"
        if command.description.startswith("|") and command.description.count(
                "|") == 2 and not command.description.endswith("||"):
            # Parses out the category of a command if a match is detected

            category_name = command.description.split("|")[1].strip().title()
            command.description = command.description.split("|")[2].strip()

        params = ""
        alias_list = "No aliases found"
        for param in command.clean_params:
            # Parses out the command parameters for usage in the command info
            params += f" <{param}> "

        if command.aliases:
            # If any command aliases exist, parse them out for usage in the command info
            alias_list = ""

            for alias in command.aliases:
                alias_list += f"|{ctx.prefix}{alias}| "

        # Build the dict update
        try:
            _ = commands_dictionary[category_name]
            commands_dictionary[category_name].append([command.name, command.description, alias_list, params])

        except KeyError:
            command_registration = {category_name: [[command.name, command.description, alias_list, params]]}
            commands_dictionary.update(command_registration)

    for category in sorted(commands_dictionary):
        # Loads in the categories with their bot_commands to the help menu

        # Loads in the embed for the category
        category_embed = help_menu_base.copy()
        category_embed.title += f"{category} Commands"

        for command in sorted(commands_dictionary[category]):
            # Gets the command info
            name = command[0]
            description = command[1]
            aliases = command[2]
            params = command[3]

            category_embed.add_field(name=name.title(), value=f"{description}\n`USAGE: {ctx.prefix}{name}{params}`\n"
                                                              f"`ALIASES: {aliases}`", inline=False)
            category_embed.timestamp = datetime.datetime.now()
            category_embed.set_footer(text=f"Developed by {dev}")
            category_embed.set_thumbnail(url=bot.user.avatar_url)

        embed_list.append(category_embed)

    if reverse:
        embed_list = reversed(embed_list)

    for embed in embed_list:
        # Sends all the embeds in the list
        await ctx.send(embed=embed)


async def convert_txt_to_pdf(path: str):
    """
    Converts a .txt file to a .pdf file
    :param path: The path for the file. -> str
    :return:
    """

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    output_path = str(os.path.splitext(path)[0]) + ".pdf"

    with open(path, 'r') as txtfile:
        lines = txtfile.readlines()

    for line in lines:

        if line == '\n':
            pdf.cell(200, 10, txt='\n', ln=1, align="L")
            continue

        if line[0] == "|" and line[2] == "|":
            pdf.cell(200, 10, txt=line[3:].strip(), ln=1, align=line[1])
            continue

        pdf.cell(200, 10, txt=line.strip(), ln=1, align="L")

    pdf.output(output_path)


async def load_missing_perms_embed(colour=discord.Colour.red()):
    """
    Quickly loads a missing permissions embed
    :param colour: The embed colour
    :return: discord.Embed
    """

    embed = discord.Embed(
        title="Missing permissions!",
        description="Sorry, you can't use this command.",
        colour=colour
    )
    embed.timestamp = datetime.datetime.now()

    return embed


async def interactive_dialog(**kwargs):
    """
    Creates an "interactive dialog" as i name it; An embed that uses the wait_for() function together to facilitate the
    creation of dialogs.

    :param kwargs: expects ctx, channel, check, title, body and optionally emojis, colour.
    > PILLAR ARGUMENTS are arguments that are mandatory; Vital for the function to be used.
    > OPTIONAL ARGUMENTS are... optional arguments. What did you expect?

    > "Ctx" is the command context. (PILLAR ARGUMENT)
    > "Check" is the type of event to happen, aswell as the wait_for check to perform on the response. (PILLAR ARGUMENT)
    > "Title" is the dialog embed title. (PILLAR ARGUMENT)
    > "Body" is the dialog embed description. (PILLAR ARGUMENT)
    > "Channel" is the place where to send the dialog to. (OPTIONAL ARGUMENT)
    > "Emojis" is a list with a list of reactions, (UTF-8 Symbols) to add into the dialog. (OPTIONAL ARGUMENT)
    > "Colour" is the dialog embed colour. Defaults to discord.Colours.red() (OPTIONAL ARGUMENT)
    > "Picture" is the dialog image, the big picture at the bottom of the embed. (OPTIONAL ARGUMENT)
    > "Thumbnail" is the dialog embed thumbnail, the small picture that gets placed on the top right side of the embed. (OPTIONAL ARGUMENT)
    > "Footer" is the dialog footer, the small text at the bottom of the embed. (OPTIONAL ARGUMENT)

    :return: The user's response.
    """

    # Performs a kwargs check to raise errors if any of the pillar arguments are missing
    if "ctx" not in kwargs: raise TypeError("Missing CTX argument in interactive dialog.")
    if "check" not in kwargs: raise TypeError("Missing CHECK argument in interactive dialog.")
    if "title" not in kwargs: raise TypeError("Missing TITLE argument in interactive dialog.")
    if "body" not in kwargs: raise TypeError("Missing BODY argument in interactive dialog.")

    # Performs a kwargs check to default the arguments if any of the optional arguments are missing
    if "channel" not in kwargs: kwargs["channel"] = kwargs["ctx"].author
    if "emojis" not in kwargs: kwargs["emojis"] = None
    if "colour" not in kwargs: kwargs["colour"] = discord.Colour.red()
    if "picture" not in kwargs: kwargs["picture"] = None
    if "thumbnail" not in kwargs: kwargs["thumbnail"] = None
    if "footer" not in kwargs: kwargs["footer"] = None

    # Loads the dialog embed
    dialog_embed = discord.Embed(
        title=kwargs["title"],
        description=kwargs["body"],
        colour=kwargs["colour"]
    )
    dialog_embed.timestamp = datetime.datetime.now()
    dialog_embed.set_thumbnail(url=kwargs["thumbnail"])
    dialog_embed.set_image(url=kwargs["picture"])
    dialog_embed.set_footer(text=kwargs["footer"])

    # Sends the embed to the desired channel
    dialog_message = await kwargs["channel"].send(embed=dialog_embed)

    # Starts the event type cheks, and their proper handles
    if kwargs["check"][0] == "message":
        try:
            msg = await kwargs["ctx"].bot.wait_for("message", kwargs["check"][1], timeout=120.0)
            return msg

        except asyncio.TimeoutError:
            # Returns an empty response if a timeout occurs.
            return

    if kwargs["check"][0] == "reaction":

        if kwargs["emojis"] is not None:
            # Adds the reactions to a message, if the emojis kwarg is not missing.

            for emoji in kwargs["emojis"]:
                await dialog_message.add_reaction(emoji)

        try:
            reaction, user = await kwargs["ctx"].bot.wait_for("message", kwargs["check"][1], timeout=120.0)
            return reaction, user

        except asyncio.TimeoutError:
            # Returns an empty response if a timeout occurs.
            return
