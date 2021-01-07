# <p align="center">Antipetros Discordbot</p> #


<p align="center"><img src="misc/images/AntiPetros_for_readme.png" alt="Anti-Petros Avatar"/></p>


None


## Installation

still WiP





## Features ##

<details><summary><b>Currently usable Cogs</b></summary><blockquote>


### <p align="center">[AbsoluteTimeCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/general_cogs/absolute_time_cog.py)</p> ###

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


### <p align="center">[AdministrationCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/admin_cogs/admin_cog.py)</p> ###

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

- > config_request

- > delete_msg

- > list_configs

- > make_feature_suggestion

- > overwrite_config_from_file

- > purge_channel

- > reload_all_ext

- > remove_from_blacklist

- > show_command_names

- > shutdown

- > tell_uptime

- > write_data

</blockquote></details>

---


### <p align="center">[GeneralDebugCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > quote

- > roll

</blockquote></details>

---


### <p align="center">[ImageManipulatorCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > available_stamps

- > member_avatar

- > stamp_image

</blockquote></details>

---


### <p align="center">[PerformanceCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/admin_cogs/performance_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > get_command_stats

- > report

- > report_latency

- > report_memory

</blockquote></details>

---


### <p align="center">[PurgeMessagesCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/admin_cogs/purge_messages_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- > purge_antipetros

</blockquote></details>

---


### <p align="center">[SaveLinkCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/general_cogs/save_link_cog.py)</p> ###

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


### <p align="center">[SaveSuggestionCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py)</p> ###

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

- > remove_all_userdata

- > request_my_data

- > user_delete_suggestion

</blockquote></details>

---

</blockquote></details>

## Dependencies ##

***Currently only tested on Windows***

**Developed with Python Version `3.9.1`**

- fuzzywuzzy<=`0.18.0`
- pyfiglet<=`0.8.post1`
- graphviz<=`0.16`
- aiohttp<=`3.6.3`
- google_auth_oauthlib<=`0.4.2`
- pytz<=`2020.5`
- Jinja2<=`2.11.2`
- click<=`7.1.2`
- networkx<=`2.5`
- pdfkit<=`0.6.1`
- python_benedict<=`0.22.4`
- psutil<=`5.8.0`
- dpytest<=`0.0.22`
- googletrans<=`4.0.0rc1`
- async_property<=`0.2.1`
- matplotlib<=`3.3.3`
- WeasyPrint<=`52.2`
- pyowm<=`3.1.1`
- watchgod<=`0.6`
- benedict<=`0.3.2`
- discord<=`1.0.1`
- gidappdata<=`0.1.1`
- gidlogger<=`0.1.3`
- google_api_python_client<=`1.12.8`
- Pillow<=`8.1.0`
- protobuf<=`3.14.0`
- PyQt5<=`5.15.2`
- python-dotenv<=`0.15.0`
- udpy<=`2.0.0`





## License

MIT

## Development


### Todo ###

<details><summary><b>TODOS FROM CODE</b></summary>

#### todo [admin_cog.py](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py): ####


- [ ] [admin_cog.py line 60:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L60) `get_logs command`


- [ ] [admin_cog.py line 61:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L61) `get_appdata_location command`


- [ ] [admin_cog.py line 249:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L249) `make as embed`


- [ ] [admin_cog.py line 255:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L255) `make as embed`


- [ ] [admin_cog.py line 264:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L264) `make as embed`


- [ ] [admin_cog.py line 270:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L270) `make as embed`


- [ ] [admin_cog.py line 276:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L276) `make as embed`


- [ ] [admin_cog.py line 283:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L283) `CRITICAL ! CHANGE TO SAVE TO JSON AND MAKE BOT METHOD FOR SAVING BLACKLIST JSON FILE`


- [ ] [admin_cog.py line 286:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L286) `make as embed`


- [ ] [admin_cog.py line 290:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L290) `make as embed`


- [ ] [admin_cog.py line 298:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L298) `make as embed`


- [ ] [admin_cog.py line 301:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L301) `make as embed`


- [ ] [admin_cog.py line 303:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L303) `make as embed`


- [ ] [admin_cog.py line 313:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L313) `make as embed`


- [ ] [admin_cog.py line 318:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L318) `make as embed`


- [ ] [admin_cog.py line 330:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L330) `make as embed`


- [ ] [admin_cog.py line 333:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L333) `make as embed`


- [ ] [admin_cog.py line 335:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L335) `make as embed`


- [ ] [admin_cog.py line 346:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L346) `make as embed`


---


#### todo [performance_cog.py](/antipetros_discordbot/cogs/admin_cogs/performance_cog.py): ####


- [ ] [performance_cog.py line 65:](/antipetros_discordbot/cogs/admin_cogs/performance_cog.py#L65) `get_logs command`


- [ ] [performance_cog.py line 66:](/antipetros_discordbot/cogs/admin_cogs/performance_cog.py#L66) `get_appdata_location command`


- [ ] [performance_cog.py line 155:](/antipetros_discordbot/cogs/admin_cogs/performance_cog.py#L155) `limit amount of saved data, maybe archive it`


---


#### todo [purge_messages_cog.py](/antipetros_discordbot/cogs/admin_cogs/purge_messages_cog.py): ####


- [ ] [purge_messages_cog.py line 65:](/antipetros_discordbot/cogs/admin_cogs/purge_messages_cog.py#L65) `get_logs command`


- [ ] [purge_messages_cog.py line 66:](/antipetros_discordbot/cogs/admin_cogs/purge_messages_cog.py#L66) `get_appdata_location command`


---


#### todo [general_debug_cog.py](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py): ####


- [ ] [general_debug_cog.py line 55:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L55) `create regions for this file`


- [ ] [general_debug_cog.py line 56:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L56) `Document and Docstrings`


---


#### todo [image_manipulation_cog.py](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py): ####


- [ ] [image_manipulation_cog.py line 55:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L55) `create regions for this file`


- [ ] [image_manipulation_cog.py line 56:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L56) `Document and Docstrings`


- [ ] [image_manipulation_cog.py line 240:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L240) `make as embed`


- [ ] [image_manipulation_cog.py line 244:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L244) `make as embed`


- [ ] [image_manipulation_cog.py line 251:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L251) `make as embed`


- [ ] [image_manipulation_cog.py line 255:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L255) `maybe make extra attribute for input format, check what is possible and working. else make a generic format list`


- [ ] [image_manipulation_cog.py line 270:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L270) `make as embed`


---


#### todo [save_link_cog.py](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py): ####


- [ ] [save_link_cog.py line 52:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L52) `refractor 'get_forbidden_list' to not use temp directory but send as filestream or so`


- [ ] [save_link_cog.py line 54:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L54) `need help figuring out how to best check bad link or how to format/normalize it`


- [ ] [save_link_cog.py line 364:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L364) `refractor that monster of an function`


---


#### todo [save_suggestion_cog.py](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py): ####


- [ ] [save_suggestion_cog.py line 57:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L57) `create report generator in different formats, at least json and Html, probably also as embeds and Markdown`


- [ ] [save_suggestion_cog.py line 59:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L59) `Document and Docstrings`


- [ ] [save_suggestion_cog.py line 212:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L212) `make as embed`


- [ ] [save_suggestion_cog.py line 218:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L218) `make as embed`


- [ ] [save_suggestion_cog.py line 234:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L234) `make as embed`


- [ ] [save_suggestion_cog.py line 246:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L246) `make as embed`


- [ ] [save_suggestion_cog.py line 250:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L250) `make as embed`


- [ ] [save_suggestion_cog.py line 254:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L254) `make as embed`


- [ ] [save_suggestion_cog.py line 259:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L259) `make as embed`


- [ ] [save_suggestion_cog.py line 298:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L298) `make as embed`


- [ ] [save_suggestion_cog.py line 301:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L301) `make as embed`


- [ ] [save_suggestion_cog.py line 312:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L312) `make as embed`


- [ ] [save_suggestion_cog.py line 316:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L316) `make as embed`


- [ ] [save_suggestion_cog.py line 320:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L320) `make as embed`


- [ ] [save_suggestion_cog.py line 325:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L325) `make as embed`


- [ ] [save_suggestion_cog.py line 336:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L336) `make as embed`


- [ ] [save_suggestion_cog.py line 371:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L371) `make as embed`


- [ ] [save_suggestion_cog.py line 374:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L374) `make as embed`


- [ ] [save_suggestion_cog.py line 378:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L378) `make as embed`


---


#### idea [render_new_cog_file.py](/antipetros_discordbot/dev_tools/render_new_cog_file.py): ####


- [ ] [render_new_cog_file.py line 119:](/antipetros_discordbot/dev_tools/render_new_cog_file.py#L119) `create gui for this`


---


#### idea [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 65:](/antipetros_discordbot/engine/antipetros_bot.py#L65) `Use an assistant class to hold some of the properties and then use the __getattr__ to make it look as one object, just for structuring`


#### todo [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 63:](/antipetros_discordbot/engine/antipetros_bot.py#L63) `create regions for this file`


- [ ] [antipetros_bot.py line 64:](/antipetros_discordbot/engine/antipetros_bot.py#L64) `Document and Docstrings`


---


#### todo [sqldata_storager.py](/antipetros_discordbot/utility/sqldata_storager.py): ####


- [ ] [sqldata_storager.py line 35:](/antipetros_discordbot/utility/sqldata_storager.py#L35) `create regions for this file`


- [ ] [sqldata_storager.py line 36:](/antipetros_discordbot/utility/sqldata_storager.py#L36) `update save link Storage to newer syntax (composite access)`


- [ ] [sqldata_storager.py line 37:](/antipetros_discordbot/utility/sqldata_storager.py#L37) `Document and Docstrings`


- [ ] [sqldata_storager.py line 38:](/antipetros_discordbot/utility/sqldata_storager.py#L38) `refractor to subfolder`


---

### General Todos ###
</details>

