





FAQ No 1
:regional_indicator_q: Where can I find dem juicy missions on the Steam Workshop?
:regional_indicator_a: Go here, boy:
<https://steamcommunity.com/id/OfficialAntiStasiCommunity/myworkshopfiles/>





FAQ No 2
:regional_indicator_q: Where do I find the PBO files for the missions?
:regional_indicator_a: The most current versions of the PBOs can be found here:
<https://github.com/official-antistasi-community/A3-Antistasi/releases/latest>
GitHub
official-antistasi-community/A3-Antistasi
AntiStasi Community Version - work in progress - Discord <https://discord.gg/t7JD7eT> - official-antistasi-community/A3-Antistasi






FAQ No 3
:regional_indicator_q: How to play Antistasi in Singleplayer?
:regional_indicator_a: Also for Singleplayer it’s recommended to host it locally in Multiplayer as you have more options like for example all the parameters and singleplayer will be deactivated shortly.





FAQ No 4
:regional_indicator_q: How do I save parameters?
:regional_indicator_a: HOW TO SAVE PARAMETERS:
To have the same parameters all the time you start the mission you need to do following things:
for locally hosted MP game
\--> Either take the PBO from the download folder or from the release page on GitHub.
\--> Save the PBO in your C:\\Users\\USERNAME\\Documents\\Arma 3 - Other Profiles\\USERNAME\\mpmissions folder.
\--> Use the PBO manager to unpack it.
\--> Go to params.hpp and change the values you want to change.
\--> DO NOT pack it back into a PBO but leave it as a folder - Arma only reads out other folders in there, not PBOs.
\--> Start the game, launch the mission.

for hosted MP on a dedicated server
\-->go to your server.cfg and set up your mission cycle as shown in the example above.
\-->The class names as well as the values which can be set can be found in the missionDescription/params.hpp file
<https://github.com/official-antistasi-community/A3-Antistasi/blob/master/A3-Antistasi/MissionDescription/params.hpp>

PLEASE NOTE THAT THE SHOWN CODE IS AN EXAMPLE AND YOU AT LEAST NEED TO ADAPT THE NAME OF THE MISSION
If you come to me with a problem and you have not even adapted the mission name to the exact filename (excluding the .pbo at the end) I'm gonna shoot myself.
// MISSIONS CYCLE (see below)
class Missions {
class Mission1    {
    template ="Antistasi-Malden-2-2-1.Malden";
        difficulty = "Custom";
            class Params {
            switchComm = 0;
            pMarkers = 0;
            AISkill = 2;
            unlockItem = 40;
            memberOnlyMagLimit = 60;
            teamSwitchDelay = 1800;
        };
};
};                // An empty Missions class means there will be no mission rotation

missionWhitelist\[] = {

}; //an empty whitelist means there is no restriction on what missions' available

If you have never setup a server, please use Google to get at least a basic knowledge before you attempt setting one up.







FAQ No 5
:regional_indicator_q: Which is the most current version?
:regional_indicator_a: The following link automatically redirects to the most current published version - there you cans ee the version number <https://github.com/official-antistasi-community/A3-Antistasi/releases/latest>





FAQ No 6
:regional_indicator_q: What is the story of the Antistasi version history?
:regional_indicator_a: Look at dis! It’s showing the history bottom to top.






FAQ No 7
:regional_indicator_q: I have a signature mismatch / my mod is corrupted (and so on). What do I do?
:regional_indicator_a: Step #1:
Go to ArmA 3 launcher, then mods, after that find the mod, now click on it, see the 3 dots in bottom right of the mod display? Click it, open via Windows file explorer, delete @ModName close that window and go back to the launcher, delete the mod/unsub.

Step #2:
Go to the steam directory, then SteamApps, then Workshop, now Content, then find ArmA3 number (107410) now open that, finally find the mod number and delete the file that has the number.
You can find the mod number in the link of it.
Example: RHSUSAF is (843577117)

Step #3:
Close the launcher, then subscribe to the mod, go to steam download manager and top the download of ArmA 3 workshop, DO NOT open the game/launcher before the download is %100 completed.





FAQ No 8
:regional_indicator_q: How do I set up a dedicated server?
:regional_indicator_a: We have this fancy thingy which is called a forum. Take a look at it!
<https://a3antistasi.enjin.com/forum/m/38173738/viewforum/7925231>





FAQ No 9
:regional_indicator_q: What are the differences between the current community version and [insert random version number here]?
:regional_indicator_a: Way too many to list them here. Have a look at the releases page of out GitHub and enjoy reading through the changelogs of the different versions.
<https://github.com/official-antistasi-community/A3-Antistasi/releases>
NO, we won’t give you a rundown of them!





FAQ No 10
:regional_indicator_q: Which mods are compatible?
:regional_indicator_a: Vanilla, RHS, 3CB. But take a look at our recommended and tested modsets!
<https://steamcommunity.com/id/OfficialAntiStasiCommunity/myworkshopfiles/?section=collections>





FAQ No 11
:regional_indicator_q: Will mod [insert random mod name here] be compatible at the future?
:regional_indicator_a: You will see it when it comes out and the list above gets updated.





FAQ No 12
:regional_indicator_q: When will Antistasi be updated?
:regional_indicator_a: We NEVER give out any ETA as the whole Dev Team is working unpaid and only in their free time in the code. Don’t bother us with “when this, when that”. It’s done when it’s done.





FAQ No 13
:regional_indicator_q: Can we have [insert random item] unlocked from the start?
:regional_indicator_a: No, but you can add them on your own using Zeus. Zeus can be entered ingame by the host (if hosted locally) and the logged in admin (if on a dedicated server).





FAQ No 14
:regional_indicator_q: How do I play Antistasi?
:regional_indicator_a: There is no correct way to play Antistasi. Simply jump into the game and start dying exploring!





FAQ No 15
:regional_indicator_q: Can we have mod [modname]?
:regional_indicator_a: If the mod has a sufficient amount of units and assts for all three factions, please contact Meerkat with your suggestion.
In case the mod you would like to add is non-conform with this requirement, most likely it is not possible to set up a proper compatibility due to technical restrictions.





FAQ No 16
:regional_indicator_q: I can’t join the server, it kicks me because of wrong mods. What do?
:regional_indicator_a: Sort out your modlist and don’t randomly load everything!





FAQ No 17
:regional_indicator_q: How to become a server member?
:regional_indicator_a: Read the channel description on teamspeak or below;

Becoming a member:

Joining our ranks is simple: play with us and participate in this community! If the members like you you may be granted trial membership by an admin upon recommendation.

Your contribution and participation to this community will determine how long the trial period will be, and whether or not it results in full membership. As a trial member, you will receive in-game membership and a [trial] tag on these forums which assures you an invite to all events including official member meetings. Do note that only full members are entitled to vote on issues at meetings.





FAQ No 18
:regional_indicator_q: Why do I have to have TS/TFAR?
:regional_indicator_a: Because we decided on that, it’s the main thing for communications and it’s an obstacle to keep fucking trolls of the server.





FAQ No 19
:regional_indicator_q: When will the mission be changed?
:regional_indicator_a: If completed during the weekend it will be changed after the completion. If it’s not completed, it’ll be changed after the admin meeting on Sunday.





FAQ No 20
:regional_indicator_q: We are playing Vanilla/RHS/[insert random modest here] on the server. Can we change it?
:regional_indicator_a: The modest gets changed once the mission is completed/changed.





FAQ No 21
:regional_indicator_q: How many people are currently online?
:regional_indicator_a: Join the server and find out.





FAQ No 22
:regional_indicator_q: Which mission is currently being played?
:regional_indicator_a: Join the server and find out.





FAQ No 23
:regional_indicator_q: Which modest is currently on the server?
:regional_indicator_a: Join the server and find out.





FAQ No 24
:regional_indicator_q: I am stuck on the loading screen for a very long time, why?
:regional_indicator_a: Most likely you have waaayyyy to many mods loaded (which most likely also unsupported). We suggest using the tested and recommended modsets available here:
<https://steamcommunity.com/id/OfficialAntiStasiCommunity/myworkshopfiles/?section=collections>
If it’s still not working, feel free to write in #help





FAQ No 25
:regional_indicator_q: Where are the save files of Antistasi stored?
:regional_indicator_a: The information are stored in the vars-file.
When playing locally it's located in your user/documents/arma 3 - otherprofiles/username folder.
For hosted on dedicated or such it's depending on your folder structure. We can't tell.







FAQ No 26
:regional_indicator_q: Do you have twitter?
:regional_indicator_a: Hell yeah!
<https://twitter.com/AntistasiO>








FAQ No 27
:regional_indicator_q: Why are PvP players killing me with [Jet, Heli, APC, Tank, Submarine, Drone, Artillery, Mortar]?
:regional_indicator_a: Congratulation! You have been annihilated by the AI.
 PvP players are not even physically able to enter this vehicles so please don’t blame it on them.







FAQ No 28
:regional_indicator_q: Where/how can we buy [Jet, Heli, APC, Tank, Submarine, Drone, Artillery ]?
:regional_indicator_a: You can’t. You only get what you are able to steal from the enemies.







FAQ No 29
:regional_indicator_q: [Insert random question regarding Antistasi 1.8/1.9]
:regional_indicator_a: These older versions are no longer supported, therefore we can’t and won’t answer questions regarding them.








FAQ No 30
:regional_indicator_q: REEEEEEEEEEEEEEEEEEEEEE, I NEED CONSOLE COMMANDS!
:regional_indicator_a: Stop yelling!
We have a wiki page of all our commands here:
<https://github.com/official-antistasi-community/A3-Antistasi/wiki/Debug-Console-Commands>
GitHub
official-antistasi-community/A3-Antistasi
AntiStasi Community Version - work in progress - Discord <https://discord.gg/t7JD7eT> - official-antistasi-community/A3-Antistasi







FAQ No 31
:regional_indicator_q: How can I port a map for Antistasi?
:regional_indicator_a: Read below. Please note, that's not an easy task.

First and foremost please note that we don't take any responsibility and will not give any support if anything goes wrong as it is not an official ported map but done by yourself and we can't even say based on which version you have done your map port.

One of the largest parts is the creation of the mission sqm. For Antistasi to run properly you need a lof of placed markers, units and modules of which some require specific names. These names are crucial so that the code can read out what a marker/module/unit is suppossed to be/do. Best thing here would be to look at already ported maps.

On the general topic of PROPER  map-porting, make sure you have adapted fn_initGarrisons.sqf, fn_initVarCommon.sqf, you have added the map relevant information in the stringtable.xml and replaced all the stringtable references within the mission.sqm as well as the description.ext.
If you want to go proper-proper, export the hightmap of the map of your choice, convert the ~30-50mb .emf file into a reasonable sized .jpg and put in on the whiteboard which you then can have on the ingame map, showing the correct map of your choice instead of the one used in the template you copy.

Also, you would need to create the roadsDB file as well as the navGrid file.
The tool for creating the navGrid file can be found in the NavGridTools folder and it also contains a proper readme which contains exact instructions on how to do it.
To create the roadsDB you would need to use following code and then safe the information in a properly named sqf file:
copyToClipboard ("{roadsX setVariable [_x select 0,_x select 1]} forEach " + str (call A3A_fnc_generateRoadsDB))







FAQ No 32
:regional_indicator_q: I HATE 3CB AND WANT CUP!!!!!
:regional_indicator_a: We currently can not implement CUP as a modset due to possible code issues and time constraints.
It IS on the list but there is certainly NO ETA.
So please stop molesting Meerkat, for fucks sake!!








FAQ No 33
:regional_indicator_q: Me have an aircraftcarrier spawned like in the picture
:regional_indicator_a: Me should not load unsupported mods like CUP Units and CUP vehicles as they break stuff
To answer your question "Which mods are compatible", please read FAQ No 10 in this channel.








FAQ No 34
:regional_indicator_q: Is [Insert name or date] event for members only?
:regional_indicator_a: Unless it is said somewhere in the event on the sign-up page then the event is always public, we rarely have restricted events but when we do it is written in the sign-up.
