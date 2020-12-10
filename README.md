# <p align="center">Anti-Petros Discord Bot</p> #


<p align="center"><img src="misc/images/AntiPetros_for_readme.png" alt="Anti-Petros Avatar"/></p>


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

- > channel_name

- > guild

- > is_a_channel

- > last_message

- > members_list

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

- > auto_accept_suggestions

- > clear_all_suggestions

- > get_all_suggestions

- > remove_all_my_data

- > request_my_data

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

- aiohttp<=`3.6.3`
- pdfkit<=`0.6.1`
- dpytest<=`0.0.22`
- watchgod<=`0.6`
- WeasyPrint<=`52.2`
- fuzzywuzzy<=`0.18.0`
- async_property<=`0.2.1`
- Jinja2<=`2.11.2`
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

#### todo [admin_cog.py](/antipetros_discordbot/cogs/admin_cog.py): ####


- [ ] [admin_cog.py line 186:](/antipetros_discordbot/cogs/admin_cog.py#L186) `make as embed`


- [ ] [admin_cog.py line 209:](/antipetros_discordbot/cogs/admin_cog.py#L209) `make as embed`


- [ ] [admin_cog.py line 228:](/antipetros_discordbot/cogs/admin_cog.py#L228) `make as embed`


- [ ] [admin_cog.py line 234:](/antipetros_discordbot/cogs/admin_cog.py#L234) `make as embed`


- [ ] [admin_cog.py line 244:](/antipetros_discordbot/cogs/admin_cog.py#L244) `make as embed`


- [ ] [admin_cog.py line 250:](/antipetros_discordbot/cogs/admin_cog.py#L250) `make as embed`


- [ ] [admin_cog.py line 256:](/antipetros_discordbot/cogs/admin_cog.py#L256) `make as embed`


- [ ] [admin_cog.py line 266:](/antipetros_discordbot/cogs/admin_cog.py#L266) `make as embed`


- [ ] [admin_cog.py line 270:](/antipetros_discordbot/cogs/admin_cog.py#L270) `make as embed`


- [ ] [admin_cog.py line 278:](/antipetros_discordbot/cogs/admin_cog.py#L278) `make as embed`


- [ ] [admin_cog.py line 281:](/antipetros_discordbot/cogs/admin_cog.py#L281) `make as embed`


- [ ] [admin_cog.py line 283:](/antipetros_discordbot/cogs/admin_cog.py#L283) `make as embed`


- [ ] [admin_cog.py line 293:](/antipetros_discordbot/cogs/admin_cog.py#L293) `make as embed`


- [ ] [admin_cog.py line 298:](/antipetros_discordbot/cogs/admin_cog.py#L298) `make as embed`


- [ ] [admin_cog.py line 310:](/antipetros_discordbot/cogs/admin_cog.py#L310) `make as embed`


- [ ] [admin_cog.py line 313:](/antipetros_discordbot/cogs/admin_cog.py#L313) `make as embed`


- [ ] [admin_cog.py line 315:](/antipetros_discordbot/cogs/admin_cog.py#L315) `make as embed`


- [ ] [admin_cog.py line 326:](/antipetros_discordbot/cogs/admin_cog.py#L326) `make as embed`


---


#### todo [general_debug_cog.py](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py): ####


- [ ] [general_debug_cog.py line 46:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L46) `create regions for this file`


- [ ] [general_debug_cog.py line 47:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L47) `Document and Docstrings`


---


#### todo [image_manipulation_cog.py](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py): ####


- [ ] [image_manipulation_cog.py line 49:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L49) `create regions for this file`


- [ ] [image_manipulation_cog.py line 50:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L50) `Document and Docstrings`


- [ ] [image_manipulation_cog.py line 246:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L246) `make as embed`


- [ ] [image_manipulation_cog.py line 250:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L250) `make as embed`


- [ ] [image_manipulation_cog.py line 257:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L257) `make as embed`


- [ ] [image_manipulation_cog.py line 261:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L261) `maybe make extra attribute for input format, check what is possible and working. else make a generic format list`


- [ ] [image_manipulation_cog.py line 275:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L275) `make as embed`


---


#### todo [save_link_cog.py](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py): ####


- [ ] [save_link_cog.py line 58:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L58) `refractor 'get_forbidden_list' to not use temp directory but send as filestream or so`


- [ ] [save_link_cog.py line 60:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L60) `need help figuring out how to best check bad link or how to format/normalize it`


- [ ] [save_link_cog.py line 62:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L62) `Add Method to add forbidden url words and forbidden links`


- [ ] [save_link_cog.py line 64:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L64) `check if everything is documented`


- [ ] [save_link_cog.py line 220:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L220) `make as embed`


- [ ] [save_link_cog.py line 231:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L231) `make as embed`


- [ ] [save_link_cog.py line 281:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L281) `make as embed`


- [ ] [save_link_cog.py line 291:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L291) `make as embed`


- [ ] [save_link_cog.py line 314:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L314) `refractor that monster of an function`


- [ ] [save_link_cog.py line 336:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L336) `make as embed`


- [ ] [save_link_cog.py line 361:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L361) `make as embed`


- [ ] [save_link_cog.py line 538:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L538) `Add logging`


---


#### todo [save_suggestion_cog.py](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py): ####


- [ ] [save_suggestion_cog.py line 51:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L51) `create report generator in different formats, at least json and Html, probably also as embeds and Markdown`


- [ ] [save_suggestion_cog.py line 53:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L53) `Document and Docstrings`


- [ ] [save_suggestion_cog.py line 196:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L196) `make as embed`


- [ ] [save_suggestion_cog.py line 202:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L202) `make as embed`


- [ ] [save_suggestion_cog.py line 217:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L217) `make as embed`


- [ ] [save_suggestion_cog.py line 229:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L229) `make as embed`


- [ ] [save_suggestion_cog.py line 233:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L233) `make as embed`


- [ ] [save_suggestion_cog.py line 237:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L237) `make as embed`


- [ ] [save_suggestion_cog.py line 242:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L242) `make as embed`


- [ ] [save_suggestion_cog.py line 288:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L288) `make as embed`


- [ ] [save_suggestion_cog.py line 291:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L291) `make as embed`


- [ ] [save_suggestion_cog.py line 302:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L302) `make as embed`


- [ ] [save_suggestion_cog.py line 306:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L306) `make as embed`


- [ ] [save_suggestion_cog.py line 310:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L310) `make as embed`


- [ ] [save_suggestion_cog.py line 315:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L315) `make as embed`


- [ ] [save_suggestion_cog.py line 325:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L325) `make as embed`


- [ ] [save_suggestion_cog.py line 360:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L360) `make as embed`


- [ ] [save_suggestion_cog.py line 363:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L363) `make as embed`


- [ ] [save_suggestion_cog.py line 367:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L367) `make as embed`


---


#### idea [render_new_cog_file.py](/antipetros_discordbot/dev_tools/render_new_cog_file.py): ####


- [ ] [render_new_cog_file.py line 114:](/antipetros_discordbot/dev_tools/render_new_cog_file.py#L114) `create gui for this`


---


#### idea [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 47:](/antipetros_discordbot/engine/antipetros_bot.py#L47) `Use an assistant class to hold some of the properties and then use the __getattr__ to make it look as one object, just for structuring`


#### todo [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 45:](/antipetros_discordbot/engine/antipetros_bot.py#L45) `create regions for this file`


- [ ] [antipetros_bot.py line 46:](/antipetros_discordbot/engine/antipetros_bot.py#L46) `Document and Docstrings`


---


#### todo [sqldata_storager.py](/antipetros_discordbot/utility/sqldata_storager.py): ####


- [ ] [sqldata_storager.py line 31:](/antipetros_discordbot/utility/sqldata_storager.py#L31) `create regions for this file`


- [ ] [sqldata_storager.py line 32:](/antipetros_discordbot/utility/sqldata_storager.py#L32) `update save link Storage to newer syntax (composite access)`


- [ ] [sqldata_storager.py line 33:](/antipetros_discordbot/utility/sqldata_storager.py#L33) `Document and Docstrings`


- [ ] [sqldata_storager.py line 34:](/antipetros_discordbot/utility/sqldata_storager.py#L34) `refractor to subfolder`


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

