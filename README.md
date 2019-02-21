# Iwazaru

Discord bot to enforce emoji-only chat.

Allowed morphemes (characters for composing messages) are all standard discord emoji, without regional selectors or custom emoji. Regular spaces and newlines are also allowed.

Immediately deletes any sent or edited message that isn't solely composed of the allowed morphemes. Also removes any reaction whose emoji isn't a valid morpheme.

There is one command: if you say "cleanse", then Iwazaru will delete all recent messages, and reactions on those messages, that are not allowed. This can be useful if the bot goes offline temporarily.
