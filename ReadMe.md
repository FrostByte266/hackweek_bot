# Discord hackweek bot
![alttext](https://github.com/FrostByte266/hackweek_bot/blob/master/assets/Japanese%20Animals.png)

**Hackweek Team:**
Nerd#4271 ,caladanbrood#5363, bAnanaS#6056, MidLoki#6680

Discord Moderation Bot first developed for discord's HackWeek 2019 contest.
Includes auto incident reporting feature, a verification feature with three variations, and a roles graph feature.


 **Terms:**
Discord, Bot, Python, Moderation

**Prerequisites**
* [discord.py](https://github.com/Rapptz/discord.py)
* [pandas](https://github.com/pandas-dev/pandas)
* [matplotlib](https://github.com/matplotlib/matplotlib)
* [aiohttp](https://github.com/aio-libs/aiohttp)
* [networkx](https://github.com/networkx)
* [Docker (optional but highly recommended)](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community-1)

**Running the bot (with docker)**

  We recommend running this bot using docker. To setup and run the bot with docker:
  * Grant execution permissions to the setup and start-bot-container scripts
  ```bash
  chmod +x ./setup
  chmod +x ./start-bot-container
  ```
  * Build the docker image by running the setup script
  ```bash
  ./setup
  ```
  * Run the start script and provide your bot token (you only need to provide your token on the first run, any subsequent run it is not required)
  ```bash
  ./start-bot-container <your bot token here>
  ```

  **Running the bot (without docker)**
  
  We strongly encourage you to run this bot using docker, however if you are unable to use docker for any reason you may run the bot without docker
  * Install all dependencies with pip
  ```bash
  pip install discord.py aiohttp networkx pandas matplotlib
  ```
  * Run the bot and follow setup prompts
  ```bash
  python main.py
  ```

**Features**

* Role statistics -
    - b!plot - Generate a plot of how many people are assigned to each role in the server     
        example from Coding Community Server:
        ![alttext](https://github.com/FrostByte266/hackweek_bot/blob/master/assets/Coding_Community_role_chart.png)

    - b!networkplot - Generate a network graph of role co-occurrence.     
        example from Coding Community Server:
        ![alttext](https://github.com/FrostByte266/hackweek_bot/blob/master/assets/Coding_Community_role_co-occurrence_graph.png)
* Verification - Users will join as 'unverified', to verify users will be given one of three different types of challenge prompts that they must successfully answer to become a verified member

    - b!verification <true/false> - Enable or disable the system, if enabled, creates a channel and role, auto deletes when the feature is disabled

    - b!verify - Verify yourself as a user. The bot will DM you and you will have to complete one of three challenges. The first possible challenges is to repeat back a three word phrase,
    copy/pasting will not work, you must type the phrase back. Second possible challenge is to solve a simple 3 operand math problem. Third challenge is to type back the color of an object.

* Incident Reports - When a user is kicked, banned, or unbanned it will auto generate an incident report and a 'receipt' will be sent via DM to both the recipient and the staff member that issued it.
Optionally it can post these receipts into a channel. There is also an option to create a custom incident report. These incidents will be preserved through restarts and can be searched with
commands. Individual reports can also be deleted if required.

    - b!reporting <true/false> - Enable or disable reporting feature, if enabled a channel is created and a report 'receipt' will be sent in that channel.
    Channel will be deleted if feature is disabled.

    - b!kick <user mention or ID> <reason> - Kick the specified user, reason is required.

    - b!ban <user mention or ID> <reason> - Bans the specified user,reason is required.

    - b!hackban <user ID> <reason> - This is used to ban a user that is not in the server, reason is required.

    - b!unban <user ID> <reason> - Unban the user with the ID provided, reason is required.

    - b!report <user mention or ID> <action> <reason> - Create a custom report, action and reason are both required.

    - b!lookup <user mention, user ID, or case number> --receipt(optional parameter) - Lookup reports, if user ID or mention is provided, it will show all reports attached to that user.
    If a case number is specified, it will show that specific report. If only fetching one report, appending '--receipt' to the end of the command will cause the bot to send you a copy of the
    report via DM.

    - b!recall <case number> - Delete a single report from the system.

* General message management features

    - b!purge <amount> <user mention or ID>(optional) - Bulk delete messages from a channel, if you mention a user it will only delete messages from said user.

    - b!move <amount> <target channel> <copy (defaults to false, unless otherwise specified)> - Move the specified number of messages to the target channel, if copy is set to true,
    it will copy instead of move.

* Join/Leave responses - The bot greets people as they come, and wishes them well as they leave. Will be automatically sent to the server's system message channel
