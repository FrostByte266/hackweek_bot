<b>hackweek_bot</b>

<b>Hackweek Team:</b>
    (@Nerd#0614 ,@caladanbrood#5363, @bAnanaS#6056, @MidLoki#6680 )

    Discord Moderation Bot first developed for discord's HackWeek 2019 contest
    Includes auto incidident reporting feature, a verification feature with three variations, and a roles graph feature

 
 <b>Terms:</b>
     Discord, Bot, Python, Moderation

<b>Prerequisites</b>
    discord
    pandas
    matplotlib
    aiohttp

<b>Commands and Features</b>

    b!plot - user of this command will be DM'ed a graph of all the roles and their respective counts
    
    Verification - Users will join as 'unverified', to verify users will be given one of three different types of challenge prompts that they must successfully answer to become a verified member
    
    Incident Reports - When a user is kicked, banned, or unbanned it will auto generate an incident report and a 'receipt' will be sent via DM to both the recipient and the staff member that issued it. 
    Optionally it can post these receipts into a channel. There is also an option to create a custom incident report. These incidents will be preserved through restarts and can be searched with 
    commands.