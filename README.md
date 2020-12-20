# <p align="center">Antipetros Discordbot</p> #


<p align="center"><img src="misc/images/AntiPetros_for_readme.png" alt="Anti-Petros Avatar"/></p>


None


## Installation

still WiP





## Features ##

<details><summary><b>Currently usable Cogs</b></summary><blockquote>


### <p align="center">[AbsoluteTime](/antipetros_discordbot/cogs/general_cogs/absolute_time_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > register_timezone_city

- > tell_all_registered_timezones

- > to_absolute_times

</blockquote></details>

---


### <p align="center">[AdministrationCog](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > add_to_blacklist

- > delete_msg

- > die

- > list_configs

- > overwrite_config

- > reload_all

- > remove_from_blacklist

- > send_config

- > show_command_names

- > tell_uptime

- > write_data

</blockquote></details>

---


### <p align="center">[GeneralDebugCog](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > all_info_from_command_trigger

- > last_message

- > message_by_id

- > tell_member_amount

- > tell_member_amount_from_id

</blockquote></details>

---


### <p align="center">[ImageManipulatorCog](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > antistasify

- > available_stamps

- > member_avatar

</blockquote></details>

---


### <p align="center">[SaveLinkCog](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>An extension Cog to let users temporary save links.

Saved links get posted to a certain channel and deleted after the specified time period from that channel (default in config).
Deleted links are kept in the bots database and can always be retrieved by fuzzy matched name.

Checks against a blacklist of urls and a blacklist of words, to not store malicious links.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > add_forbidden_word

- > clear_all_links

- > delete_link

- > get_all_links

- > get_forbidden_list

- > get_link

- > remove_forbidden_word

- > save_link

</blockquote></details>

---


### <p align="center">[SaveSuggestionCog](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > auto_accept_suggestions

- > clear_all_suggestions

- > get_all_suggestions

- > mark_discussed

- > remove_all_my_data

- > request_my_data

- > unsave_suggestion

</blockquote></details>

---


### <p align="center">[TestPlaygroundCog](/antipetros_discordbot/cogs/dev_cogs/test_playground_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > add_special_name

- > big_message

- > changesettings

- > check_md_helper

- > check_md_helper_specific

- > combquote

- > embed_experiment

- > furthermore_do_you_want_to_say_something

- > get_cfg_name

- > map_changed

- > new_google_calender_event

- > request_server_restart

- > roll

- > translate

</blockquote></details>

---

</blockquote></details>

## Dependencies ##

***Currently only tested on Windows***

**Developed with Python Version `3.8.6`**

- WeasyPrint<=`52.2`
- pdfkit<=`0.6.1`
- googletrans<=`4.0.0rc1`
- pytz<=`2020.4`
- watchgod<=`0.6`
- aiohttp<=`3.6.3`
- google_auth_oauthlib<=`0.4.2`
- async_property<=`0.2.1`
- fuzzywuzzy<=`0.18.0`
- dpytest<=`0.0.22`
- Jinja2<=`2.11.2`
- discord<=`1.0.1`
- gidappdata<=`0.1.1`
- gidlogger<=`0.1.3`
- google_api_python_client<=`1.12.8`
- Pillow<=`8.0.1`
- protobuf<=`3.14.0`
- PyQt5<=`5.15.2`
- python-dotenv<=`0.15.0`





## License

MIT

## Development


### Todo ###

<details><summary><b>TODOS FROM CODE</b></summary>

#### todo [admin_cog.py](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py): ####


- [ ] [admin_cog.py line 57:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L57) `get_logs command`


- [ ] [admin_cog.py line 58:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L58) `get_appdata_location command`


- [ ] [admin_cog.py line 186:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L186) `make as embed`


- [ ] [admin_cog.py line 205:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L205) `make as embed`


- [ ] [admin_cog.py line 211:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L211) `make as embed`


- [ ] [admin_cog.py line 220:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L220) `make as embed`


- [ ] [admin_cog.py line 226:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L226) `make as embed`


- [ ] [admin_cog.py line 232:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L232) `make as embed`


- [ ] [admin_cog.py line 242:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L242) `make as embed`


- [ ] [admin_cog.py line 246:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L246) `make as embed`


- [ ] [admin_cog.py line 254:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L254) `make as embed`


- [ ] [admin_cog.py line 257:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L257) `make as embed`


- [ ] [admin_cog.py line 259:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L259) `make as embed`


- [ ] [admin_cog.py line 269:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L269) `make as embed`


- [ ] [admin_cog.py line 274:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L274) `make as embed`


- [ ] [admin_cog.py line 286:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L286) `make as embed`


- [ ] [admin_cog.py line 289:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L289) `make as embed`


- [ ] [admin_cog.py line 291:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L291) `make as embed`


- [ ] [admin_cog.py line 302:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L302) `make as embed`


---


#### todo [general_debug_cog.py](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py): ####


- [ ] [general_debug_cog.py line 49:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L49) `create regions for this file`


- [ ] [general_debug_cog.py line 50:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L50) `Document and Docstrings`


---


#### todo [image_manipulation_cog.py](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py): ####


- [ ] [image_manipulation_cog.py line 53:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L53) `create regions for this file`


- [ ] [image_manipulation_cog.py line 54:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L54) `Document and Docstrings`


- [ ] [image_manipulation_cog.py line 238:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L238) `make as embed`


- [ ] [image_manipulation_cog.py line 242:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L242) `make as embed`


- [ ] [image_manipulation_cog.py line 249:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L249) `make as embed`


- [ ] [image_manipulation_cog.py line 253:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L253) `maybe make extra attribute for input format, check what is possible and working. else make a generic format list`


- [ ] [image_manipulation_cog.py line 268:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L268) `make as embed`


---


#### todo [save_link_cog.py](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py): ####


- [ ] [save_link_cog.py line 51:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L51) `refractor 'get_forbidden_list' to not use temp directory but send as filestream or so`


- [ ] [save_link_cog.py line 53:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L53) `need help figuring out how to best check bad link or how to format/normalize it`


- [ ] [save_link_cog.py line 364:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L364) `refractor that monster of an function`


---


#### todo [save_suggestion_cog.py](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py): ####


- [ ] [save_suggestion_cog.py line 56:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L56) `create report generator in different formats, at least json and Html, probably also as embeds and Markdown`


- [ ] [save_suggestion_cog.py line 58:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L58) `Document and Docstrings`


- [ ] [save_suggestion_cog.py line 209:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L209) `make as embed`


- [ ] [save_suggestion_cog.py line 215:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L215) `make as embed`


- [ ] [save_suggestion_cog.py line 231:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L231) `make as embed`


- [ ] [save_suggestion_cog.py line 243:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L243) `make as embed`


- [ ] [save_suggestion_cog.py line 247:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L247) `make as embed`


- [ ] [save_suggestion_cog.py line 251:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L251) `make as embed`


- [ ] [save_suggestion_cog.py line 256:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L256) `make as embed`


- [ ] [save_suggestion_cog.py line 296:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L296) `make as embed`


- [ ] [save_suggestion_cog.py line 299:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L299) `make as embed`


- [ ] [save_suggestion_cog.py line 310:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L310) `make as embed`


- [ ] [save_suggestion_cog.py line 314:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L314) `make as embed`


- [ ] [save_suggestion_cog.py line 318:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L318) `make as embed`


- [ ] [save_suggestion_cog.py line 323:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L323) `make as embed`


- [ ] [save_suggestion_cog.py line 334:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L334) `make as embed`


- [ ] [save_suggestion_cog.py line 369:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L369) `make as embed`


- [ ] [save_suggestion_cog.py line 372:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L372) `make as embed`


- [ ] [save_suggestion_cog.py line 376:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L376) `make as embed`


---


#### idea [render_new_cog_file.py](/antipetros_discordbot/dev_tools/render_new_cog_file.py): ####


- [ ] [render_new_cog_file.py line 119:](/antipetros_discordbot/dev_tools/render_new_cog_file.py#L119) `create gui for this`


---


#### idea [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 54:](/antipetros_discordbot/engine/antipetros_bot.py#L54) `Use an assistant class to hold some of the properties and then use the __getattr__ to make it look as one object, just for structuring`


#### todo [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 52:](/antipetros_discordbot/engine/antipetros_bot.py#L52) `create regions for this file`


- [ ] [antipetros_bot.py line 53:](/antipetros_discordbot/engine/antipetros_bot.py#L53) `Document and Docstrings`


---


#### todo [sqldata_storager.py](/antipetros_discordbot/utility/sqldata_storager.py): ####


- [ ] [sqldata_storager.py line 35:](/antipetros_discordbot/utility/sqldata_storager.py#L35) `create regions for this file`


- [ ] [sqldata_storager.py line 36:](/antipetros_discordbot/utility/sqldata_storager.py#L36) `update save link Storage to newer syntax (composite access)`


- [ ] [sqldata_storager.py line 37:](/antipetros_discordbot/utility/sqldata_storager.py#L37) `Document and Docstrings`


- [ ] [sqldata_storager.py line 38:](/antipetros_discordbot/utility/sqldata_storager.py#L38) `refractor to subfolder`


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

