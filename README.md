# <p align="center">AntiPetrosDiscordBot</p> #


<p align="center"><img src="../misc/images/AntiPetros_for_readme.png" alt="Anti-Petros Avatar"/></p>


None


## Installation

still WiP





## Features ##

<details><summary><b>Currently usable Cogs</b></summary><blockquote>


### <p align="center">[Administration](/antipetros_discordbot/cogs/admin_cog.py)</p> ###

<details><summary><b>Description</b></summary><blockquote>

    None

</blockquote></details>

<details><summary><b>Commands</b></summary><blockquote>

- > add_to_blacklist

- > delete_msg

- > die

- > list_configs

- > overwrite_config

- > reload_all

- > remove_from_blacklist

- > send_config

- > tell_uptime

</blockquote></details>

---


### <p align="center">[GeneralDebug](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py)</p> ###

<details><summary><b>Description</b></summary><blockquote>

    None

</blockquote></details>

<details><summary><b>Commands</b></summary><blockquote>

- > all_info_from_command_trigger

- > last_message

- > message_by_id

</blockquote></details>

---


### <p align="center">[ImageManipulator](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py)</p> ###

<details><summary><b>Description</b></summary><blockquote>

    None

</blockquote></details>

<details><summary><b>Commands</b></summary><blockquote>

- > antistasify

- > available_stamps

- > flag_test

- > member_avatar

</blockquote></details>

---


### <p align="center">[SaveLink](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py)</p> ###

<details><summary><b>Description</b></summary><blockquote>

    
An extension Cog to let users temporary save links.

Saved links get posted to a certain channel and deleted after the specified time period from that channel (default in config).
Deleted links are kept in the bots database and can always be retrieved by fuzzy matched name.

Checks against a blacklist of urls and a blacklist of words, to not store malicious links.

cogs_config.ini section: self.config_name

currently implemented config options:

- 'allowed_roles' --> comma-seperated-list of role names
(eg: Dev_helper, Admin) !names have to match completely and are case-sensitive!

- 'allowed_channels' --> comma-seperated-list of channel names
(eg: bot-development-and-testing, general-dev-stuff) !names have to match completely and are case-sensitive!

- 'link_channel' --> channel id for the channel that is used as 'storage', where the bot posts the saved links for the time period
(eg: 645930607683174401)

- 'delete_all_allowed_roles' --> comma-seperated-list of role names that are allowed to clear the link Database, all links will be lost.
will propably be turned into user id list

- bad_link_image_path/bad_link_image_name --> file_path or appdata file name to an image to use when answering to an forbidden link (None means no image)


- default_storage_days --> integer of days to default to if user does not specifiy amount of time to keep link
(eg: 7)

- member_to_notifiy_bad_link --> comma-seperated-list of user_ids of users that should be notified per DM when an bad link is posted.

- notify_with_link --> boolean if the notification DM should include the bad link


</blockquote></details>

<details><summary><b>Commands</b></summary><blockquote>

- > clear_all_links

- > delete_link

- > get_all_links

- > get_forbidden_list

- > get_link

- > save_link

</blockquote></details>

---


### <p align="center">[SaveSuggestion](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py)</p> ###

<details><summary><b>Description</b></summary><blockquote>

    None

</blockquote></details>

<details><summary><b>Commands</b></summary><blockquote>

- > clear_all_suggestions

- > remove_all_my_data

- > request_my_data

- > retrieve_all

- > unsave_suggestion

</blockquote></details>

---


### <p align="center">[TestPlayground](/antipetros_discordbot/cogs/general_cogs/test_playground_cog.py)</p> ###

<details><summary><b>Description</b></summary><blockquote>

    None

</blockquote></details>

<details><summary><b>Commands</b></summary><blockquote>

- > FAQ_you

- > big_message

- > changesettings

- > check_md_helper

- > check_md_helper_specific

- > embed_experiment

- > furthermore_do_you_want_to_say_something

- > map_changed

- > request_server_restart

- > roll

</blockquote></details>

---

</blockquote></details>

## Dependencies ##

***Currently only tested on Windows***

**Developed with Python Version `3.8.6`**

- async_property<=`0.2.1`
- fuzzywuzzy<=`0.18.0`
- Jinja2<=`2.11.2`
- discord_flags<=`2.1.1`
- watchgod<=`0.6`
- aiohttp<=`3.7.3`
- discord<=`1.0.1`
- gidconfig<=`0.1.2`
- gidlogger<=`0.1.2`
- Pillow<=`8.0.1`
- python-dotenv<=`0.15.0`





## License

MIT

## Development


### Todo ###

<details><summary><b>TODOS FROM CODE</b></summary>

#### todo [\_\_main\_\_.py](/antipetros_discordbot/__main__.py): ####


- [ ] [\_\_main\_\_.py line 49:](/antipetros_discordbot/__main__.py#L49) `maybe put these functions into the Bot class or make an bot builder class`


- [ ] [\_\_main\_\_.py line 70:](/antipetros_discordbot/__main__.py#L70) `Deal wit the tripple or quadrouple redundancy in regards to the env file`


- [ ] [\_\_main\_\_.py line 121:](/antipetros_discordbot/__main__.py#L121) `make as embed`


---


#### todo [admin_cog.py](/antipetros_discordbot/cogs/admin_cog.py): ####


- [ ] [admin_cog.py line 185:](/antipetros_discordbot/cogs/admin_cog.py#L185) `make as embed`


- [ ] [admin_cog.py line 205:](/antipetros_discordbot/cogs/admin_cog.py#L205) `make as embed`


- [ ] [admin_cog.py line 224:](/antipetros_discordbot/cogs/admin_cog.py#L224) `make as embed`


- [ ] [admin_cog.py line 230:](/antipetros_discordbot/cogs/admin_cog.py#L230) `make as embed`


- [ ] [admin_cog.py line 240:](/antipetros_discordbot/cogs/admin_cog.py#L240) `make as embed`


- [ ] [admin_cog.py line 246:](/antipetros_discordbot/cogs/admin_cog.py#L246) `make as embed`


- [ ] [admin_cog.py line 252:](/antipetros_discordbot/cogs/admin_cog.py#L252) `make as embed`


- [ ] [admin_cog.py line 262:](/antipetros_discordbot/cogs/admin_cog.py#L262) `make as embed`


- [ ] [admin_cog.py line 266:](/antipetros_discordbot/cogs/admin_cog.py#L266) `make as embed`


- [ ] [admin_cog.py line 274:](/antipetros_discordbot/cogs/admin_cog.py#L274) `make as embed`


- [ ] [admin_cog.py line 277:](/antipetros_discordbot/cogs/admin_cog.py#L277) `make as embed`


- [ ] [admin_cog.py line 279:](/antipetros_discordbot/cogs/admin_cog.py#L279) `make as embed`


- [ ] [admin_cog.py line 289:](/antipetros_discordbot/cogs/admin_cog.py#L289) `make as embed`


- [ ] [admin_cog.py line 294:](/antipetros_discordbot/cogs/admin_cog.py#L294) `make as embed`


- [ ] [admin_cog.py line 306:](/antipetros_discordbot/cogs/admin_cog.py#L306) `make as embed`


- [ ] [admin_cog.py line 309:](/antipetros_discordbot/cogs/admin_cog.py#L309) `make as embed`


- [ ] [admin_cog.py line 311:](/antipetros_discordbot/cogs/admin_cog.py#L311) `make as embed`


- [ ] [admin_cog.py line 322:](/antipetros_discordbot/cogs/admin_cog.py#L322) `make as embed`


---


#### todo [general_debug_cog.py](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py): ####


- [ ] [general_debug_cog.py line 46:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L46) `create regions for this file`


- [ ] [general_debug_cog.py line 47:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L47) `Document and Docstrings`


---


#### todo [image_manipulation_cog.py](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py): ####


- [ ] [image_manipulation_cog.py line 48:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L48) `create regions for this file`


- [ ] [image_manipulation_cog.py line 49:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L49) `Document and Docstrings`


- [ ] [image_manipulation_cog.py line 233:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L233) `make as embed`


- [ ] [image_manipulation_cog.py line 243:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L243) `make as embed`


- [ ] [image_manipulation_cog.py line 247:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L247) `make as embed`


- [ ] [image_manipulation_cog.py line 254:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L254) `make as embed`


- [ ] [image_manipulation_cog.py line 258:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L258) `maybe make extra attribute for input format, check what is possible and working. else make a generic format list`


- [ ] [image_manipulation_cog.py line 272:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L272) `make as embed`


- [ ] [image_manipulation_cog.py line 279:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L279) `remove this, or move to debug`


- [ ] [image_manipulation_cog.py line 286:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L286) `make as embed`


- [ ] [image_manipulation_cog.py line 289:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L289) `make as embed`


- [ ] [image_manipulation_cog.py line 307:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L307) `make as embed`


---


#### todo [save_link_cog.py](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py): ####


- [ ] [save_link_cog.py line 81:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L81) `refractor 'get_forbidden_list' to not use temp directory but send as filestream or so`


- [ ] [save_link_cog.py line 83:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L83) `need help figuring out how to best check bad link or how to format/normalize it`


- [ ] [save_link_cog.py line 85:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L85) `Add Method to add forbidden url words and forbidden links`


- [ ] [save_link_cog.py line 87:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L87) `check if everything is documented`


- [ ] [save_link_cog.py line 251:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L251) `make as embed`


- [ ] [save_link_cog.py line 262:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L262) `make as embed`


- [ ] [save_link_cog.py line 284:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L284) `make as embed, also change to only get raw data from datastoragehandler`


- [ ] [save_link_cog.py line 309:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L309) `make as embed`


- [ ] [save_link_cog.py line 319:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L319) `make as embed`


- [ ] [save_link_cog.py line 342:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L342) `refractor that monster of an function`


- [ ] [save_link_cog.py line 364:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L364) `make as embed`


- [ ] [save_link_cog.py line 389:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L389) `make as embed`


- [ ] [save_link_cog.py line 450:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L450) `Docstring`


- [ ] [save_link_cog.py line 557:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L557) `Add logging`


---


#### todo [save_suggestion_cog.py](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py): ####


- [ ] [save_suggestion_cog.py line 48:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L48) `create report generator in different formats, at least json and Html, probably also as embeds and Markdown`


- [ ] [save_suggestion_cog.py line 50:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L50) `Document and Docstrings`


- [ ] [save_suggestion_cog.py line 144:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L144) `make as embed`


- [ ] [save_suggestion_cog.py line 175:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L175) `make as embed`


- [ ] [save_suggestion_cog.py line 184:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L184) `make as embed`


- [ ] [save_suggestion_cog.py line 189:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L189) `make as embed`


- [ ] [save_suggestion_cog.py line 201:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L201) `make as embed`


- [ ] [save_suggestion_cog.py line 205:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L205) `make as embed`


- [ ] [save_suggestion_cog.py line 209:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L209) `make as embed`


- [ ] [save_suggestion_cog.py line 214:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L214) `make as embed`


- [ ] [save_suggestion_cog.py line 221:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L221) `make completly new for sqlite or dynamic datahandler`


- [ ] [save_suggestion_cog.py line 240:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L240) `make as embed`


- [ ] [save_suggestion_cog.py line 243:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L243) `make as embed`


- [ ] [save_suggestion_cog.py line 254:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L254) `make as embed`


- [ ] [save_suggestion_cog.py line 258:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L258) `make as embed`


- [ ] [save_suggestion_cog.py line 262:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L262) `make as embed`


- [ ] [save_suggestion_cog.py line 267:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L267) `make as embed`


- [ ] [save_suggestion_cog.py line 277:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L277) `make as embed`


- [ ] [save_suggestion_cog.py line 312:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L312) `make as embed`


- [ ] [save_suggestion_cog.py line 315:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L315) `make as embed`


- [ ] [save_suggestion_cog.py line 319:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L319) `make as embed`


---


#### idea [render_new_cog_file.py](/antipetros_discordbot/dev_tools/render_new_cog_file.py): ####


- [ ] [render_new_cog_file.py line 114:](/antipetros_discordbot/dev_tools/render_new_cog_file.py#L114) `create gui for this`


---


#### idea [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 41:](/antipetros_discordbot/engine/antipetros_bot.py#L41) `Use an assistant class to hold some of the properties and then use the __getattr__ to make it look as one object, just for structuring`


#### todo [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 39:](/antipetros_discordbot/engine/antipetros_bot.py#L39) `create regions for this file`


- [ ] [antipetros_bot.py line 40:](/antipetros_discordbot/engine/antipetros_bot.py#L40) `Document and Docstrings`


---


#### todo [sqldata_storager.py](/antipetros_discordbot/utility/sqldata_storager.py): ####


- [ ] [sqldata_storager.py line 29:](/antipetros_discordbot/utility/sqldata_storager.py#L29) `create regions for this file`


- [ ] [sqldata_storager.py line 30:](/antipetros_discordbot/utility/sqldata_storager.py#L30) `update save link Storage to newer syntax (composite access)`


- [ ] [sqldata_storager.py line 31:](/antipetros_discordbot/utility/sqldata_storager.py#L31) `Document and Docstrings`


- [ ] [sqldata_storager.py line 32:](/antipetros_discordbot/utility/sqldata_storager.py#L32) `refractor to subfolder`


---

### General Todos ###
#### Bugs ####

- [ ] *important*: check everything for blocking functions and move big ones into threads (run in executor)


---

#### features ####

- [ ] *important*: create nice looking help command

- [ ] *important*: better docstrings and docstring all commands at least

- [ ] *important*: create all needed check methods

- [ ] *important*: move to gidappdata as storage

- [ ] *unimportant*: assign good names to the cogs as argument in the init

- [ ] *unimportant*: ask for symbols at art team


---

#### misc ####


---

#### tests ####


---

</details>

