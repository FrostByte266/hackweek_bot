# Discord hackweek bot

**Hackweek Team:**
Nerd#0614 ,caladanbrood#5363, bAnanaS#6056, MidLoki#6680

Discord Moderation Bot first developed for discord's HackWeek 2019 contest.
Includes auto incident reporting feature, a verification feature with three variations, and a roles graph feature.

 
 **Terms:**
Discord, Bot, Python, Moderation

<b>Prerequisites</b>
* [discord.py](https://github.com/Rapptz/discord.py)
* [pandas](https://github.com/pandas-dev/pandas)
* [matplotlib](https://github.com/matplotlib/matplotlib)
* [aiohttp](https://github.com/aio-libs/aiohttp)
* [networkx](https://github.com/networkx)

<b>Features</b>

* Role statistics - 
    - b!plot - Generate a plot of how many people are assigned to each role in the server
    
    - b!networkplot - Generate a network graph of role co-occurrence.
* Verification - Users will join as 'unverified', to verify users will be given one of three different types of challenge prompts that they must successfully answer to become a verified member

* Incident Reports - When a user is kicked, banned, or unbanned it will auto generate an incident report and a 'receipt' will be sent via DM to both the recipient and the staff member that issued it. 
Optionally it can post these receipts into a channel. There is also an option to create a custom incident report. These incidents will be preserved through restarts and can be searched with 
commands. Individual reports can also be deleted if required.

* Join/Leave responses - The bot greets people as they come, and wishes them well as they leave.