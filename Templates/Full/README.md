# Full Template
This template has more code, and is made more for public discord bots. This template has some JSON files that store custom prefixes for servers, and a command list for the custom "help" command
## Setup:
Go to the [Discord Develeper Portal]("https://discord.com/developers/applications") and create an application, open it and create a bot, paste the bot token into the "TOKEN" value in the first lines of the template, make sure that you have the [discord.py](https://github.com/Rapptz/discord.py) module installed, and run the script.
Get the bot invite link by opening the OAuth2 panel in the [Discord Develeper Portal]("https://discord.com/developers/applications"), only select scope "bot", and the "Send Messages" permission. Open it to invite the bot to a server that you manage. Test it by pinging the bot.
## Template functions and commands
This template includes a few custom functions and discord commands.
### ``await embed_send()``
```python
async def embed_send(ctx, title, description, color=oxfffffe)
```
This sends an embed message to the discord server that is specified in the context, and has the ctx, title, description, and color paramaters. Should be used to respond to user commands.

Example:
```python
await embed_send(ctx, "Hello There!", "This is an embed!", color=0xefefef)
```
### "setprefix" command ("prefix" alias)
This command will set a custom prefix that will be used for the server, the default prefix is "$"
To check the set prefix, ping  the bot.
**NOTE: This command can only be triggered by users with the "Manage Server" permission in discord, and can't be used in DMs**

### "help" command ("h" alias)
This command will display all commands that are in json/commands.json


### "info" command ("ping" alias)
This command displays information about the bot, it displays bot uptime and ping.

### Error handling
General discord errors that may happen:
* Command Not Found: Tells the user that the command doesn't exist.
* Missing Arguments: Tells the user that the command is missing certain arguments
* Missing Permissions: Tells the user which permissions they are missing
* Bad Token: Prints that the token is missing or incorrect, and terminates script after a minute (**This will also trigger if token is correct but there are connection issues to Discord**)
* Other discord errors: Will only print to the terminal
* General python errors: No handling

These errors will also print to the terminal
