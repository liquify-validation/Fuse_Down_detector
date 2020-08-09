def first_of(attr, match, it):
    """ Return the first item in a set with an attribute that matches match """
    if it is not None:
        for i in it:
            try:
                if getattr(i, attr) == match:
                    return i
            except: pass

    return None

def command_from_message(message, default=None):
    """ Extracts the first command from a Telegram Message """
    if not message or not message.text:
        return default

    command = None
    text = message.text
    entities = message.entities
    command_def = first_of('type', 'bot_command', entities)

    if command_def:
        command = text[command_def.offset:command_def.length]

    return command or default

def message_from_message(message, default=None):
    """ Extracts the first command from a Telegram Message """
    if not message or not message.text:
        return default

    command = None
    text = message.text
    entities = message.entities
    command_def = first_of('type', 'bot_command', entities)

    if command_def:
        command = text[command_def.offset + command_def.length:]

    return command or default

def convert_list_to_string(org_list, seperator=', '):
    """ Convert list to string, by joining all item in list with given separator.
        Returns the concatenated string """
    return seperator.join(org_list)