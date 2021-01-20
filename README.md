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

- <ins>**REGISTER_TIMEZONE_CITY**</ins>
    - **aliases:** *registertimezonecity*, *register.timezone.city*, *register-timezone-city*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        <in_data>
        ```
    <br>

- <ins>**TELL_ALL_REGISTERED_TIMEZONES**</ins>
    - **aliases:** *tellallregisteredtimezones*, *tell.all.registered.timezones*, *tell-all-registered-timezones*
    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**TO_ABSOLUTE_TIMES**</ins>
    - **aliases:** *toabsolutetimes*, *to.absolute.times*, *to-absolute-times*
    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>


</blockquote>

</details>

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

- <ins>**ADD_TO_BLACKLIST**</ins>
    - **aliases:** *add.to.blacklist*, *addtoblacklist*, *add-to-blacklist*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        <user>
        ```
    <br>

- <ins>**CONFIG_REQUEST**</ins>
    - **aliases:** *config.request*, *send-config*, *send.config*, *sendconfig*, *configrequest*, *config-request*
    - **checks:** *dm_only*
    - **signature:**
        ```diff
        [config_name=all]
        ```
    <br>

- <ins>**DELETE_MSG**</ins>
    - **aliases:** *delete.msg*, *deletemsg*, *delete-msg*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        <msg_id>
        ```
    <br>

- <ins>**LIST_CONFIGS**</ins>
    - **aliases:** *list.configs*, *listconfigs*, *list-configs*
    - **checks:** *dm_only*
    <br>

- <ins>**MAKE_FEATURE_SUGGESTION**</ins>
    - **aliases:** *makefeaturesuggestion*, *make.feature.suggestion*, *make-feature-suggestion*

    - **signature:**
        ```diff
        <suggestion_content>
        ```
    <br>

- <ins>**OVERWRITE_CONFIG_FROM_FILE**</ins>
    - **aliases:** *overwrite-config-from-file*, *overwriteconfigfromfile*, *overwrite.config*, *overwriteconfig*, *overwrite.config.from.file*, *overwrite-config*
    - **checks:** *dm_only*
    - **signature:**
        ```diff
        <config_name>
        ```
    <br>

- <ins>**RELOAD_ALL_EXT**</ins>
    - **aliases:** *reload*, *reload.all*, *reload.all.ext*, *reload-all-ext*, *reload-all*, *reloadallext*, *reloadall*
    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**REMOVE_FROM_BLACKLIST**</ins>
    - **aliases:** *remove-from-blacklist*, *remove.from.blacklist*, *removefromblacklist*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        <user>
        ```
    <br>

- <ins>**SHOW_COMMAND_NAMES**</ins>
    - **aliases:** *show-command-names*, *showcommandnames*, *show.command.names*
    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**SHUTDOWN**</ins>
    - **aliases:** *turnof*, *goaway*, *die*, *turn.of*, *close*, *go.away*, *exit*, *turn-of*, *go-away*
    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**TELL_UPTIME**</ins>
    - **aliases:** *telluptime*, *tell-uptime*, *tell.uptime*
    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**WRITE_DATA**</ins>
    - **aliases:** *write.data*, *write-data*, *writedata*
    - **checks:** *in_allowed_channels*, *is_owner*
    <br>


</blockquote>

</details>

---


### <p align="center">[FaqCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/special_channels_cogs/faq_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>[summary]

[extended_summary]</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- <ins>**CREATE_FAQS_AS_EMBED**</ins>
    - **aliases:** *create-faqs-as-embed*, *create.faqs.as.embed*, *createfaqsasembed*
    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role*
    <br>

- <ins>**POST_FAQ_BY_NUMBER**</ins>
    - **aliases:** *post-faq-by-number*, *post.faq.by.number*, *postfaqbynumber*, *faq*
    - **checks:** *allowed_channel_and_allowed_role*
    - **signature:**
        ```diff
        [faq_numbers]...
        ```
    <br>


</blockquote>

</details>

---


### <p align="center">[GeneralDebugCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>[summary]

[extended_summary]</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- <ins>**GET_MESSAGES**</ins>

    - **checks:** *allowed_channel_and_allowed_role*
    - **signature:**
        ```diff
        <channel>
        ```
    <br>

- <ins>**MULTIPLE_QUOTES**</ins>
    - **aliases:** *multiple-quotes*, *multiple.quotes*, *multiplequotes*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        [amount=10]
        ```
    <br>

- <ins>**QUOTE**</ins>

    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**ROLL**</ins>

    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        [target_time=1]
        ```
    <br>


</blockquote>

</details>

---


### <p align="center">[GiveAwayCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/community_events_cogs/give_away_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>[summary]

[extended_summary]</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- <ins>**ABORT_GIVE_AWAY**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role*
    <br>

- <ins>**CHECK_DATETIME_STUFF**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role*
    - **signature:**
        ```diff
        <date_string>
        ```
    <br>

- <ins>**CREATE_GIVEAWAY**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role*
    <br>

- <ins>**FINISH_GIVE_AWAY**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role*
    <br>

- <ins>**START_GIVEAWAY**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role*
    <br>


</blockquote>

</details>

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

- <ins>**AVAILABLE_STAMPS**</ins>
    - **aliases:** *available.stamps*, *availablestamps*, *available-stamps*
    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**MAP_CHANGED**</ins>
    - **aliases:** *map-changed*, *map.changed*, *mapchanged*
    - **checks:** *allowed_channel_and_allowed_role*
    - **signature:**
        ```diff
        <marker> <color>
        ```
    <br>

- <ins>**MEMBER_AVATAR**</ins>
    - **aliases:** *memberavatar*, *member-avatar*, *member.avatar*
    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**STAMP_IMAGE**</ins>
    - **aliases:** *stamp.image*, *stamp-image*, *stampimage*, *antistasify*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        [stamp=ASLOGO1] [first_pos=bottom] [second_pos=right] [factor]
        ```
    <br>


</blockquote>

</details>

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

- <ins>**GET_COMMAND_STATS**</ins>
    - **aliases:** *getcommandstats*, *get-command-stats*, *get.command.stats*
    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**REPORT**</ins>

    - **checks:** *in_allowed_channels*, *has_any_role*
    <br>

- <ins>**REPORT_LATENCY**</ins>
    - **aliases:** *report-latency*, *report.latency*, *reportlatency*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        [with_graph=True] [since_last_hours=24]
        ```
    <br>

- <ins>**REPORT_MEMORY**</ins>
    - **aliases:** *reportmemory*, *report-memory*, *report.memory*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        [with_graph=True] [since_last_hours=24]
        ```
    <br>


</blockquote>

</details>

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

- <ins>**PURGE_ANTIPETROS**</ins>
    - **aliases:** *purge-antipetros*, *purge.antipetros*, *purgeantipetros*
    - **checks:** *in_allowed_channels*, *is_owner*
    - **signature:**
        ```diff
        [and_giddi] [number_of_messages=1000]
        ```
    <br>

- <ins>**PURGE_MSG_FROM_USER**</ins>
    - **aliases:** *purge-msg-from-user*, *purgemsgfromuser*, *purge.msg.from.user*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        <user> [number_of_messages=1000] [since]
        ```
    <br>


</blockquote>

</details>

---


### <p align="center">[SaveLinkCog](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>An extension Cog to let users temporary save links.

Saved links get posted to a certain channel and deleted after the specified time period from that channel (default in config).
Deleted links are kept in the bots database and can always be retrieved by fuzzy matched name.

Checks against a blacklist of urls and a blacklist of words, to not store malicious links.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- <ins>**ADD_FORBIDDEN_WORD**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role_no_dm*
    - **signature:**
        ```diff
        <word>
        ```
    <br>

- <ins>**CLEAR_ALL_LINKS**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role_no_dm*
    - **signature:**
        ```diff
        [sure=False]
        ```
    <br>

- <ins>**DELETE_LINK**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role_no_dm*
    - **signature:**
        ```diff
        <name> [scope=channel]
        ```
    <br>

- <ins>**GET_ALL_LINKS**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role_no_dm*
    - **signature:**
        ```diff
        [in_format=txt]
        ```
    <br>

- <ins>**GET_FORBIDDEN_LIST**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role_no_dm*
    - **signature:**
        ```diff
        [file_format=json]
        ```
    <br>

- <ins>**GET_LINK**</ins>

    - **checks:** *allowed_channel_and_allowed_role_no_dm*
    - **signature:**
        ```diff
        <name>
        ```
    <br>

- <ins>**REMOVE_FORBIDDEN_WORD**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role_no_dm*
    - **signature:**
        ```diff
        <word>
        ```
    <br>

- <ins>**SAVE_LINK**</ins>

    - **checks:** *allowed_channel_and_allowed_role_no_dm*
    - **signature:**
        ```diff
        <link> [link_name] [days_to_hold]
        ```
    <br>


</blockquote>

</details>

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

- <ins>**AUTO_ACCEPT_SUGGESTIONS**</ins>
    - **aliases:** *auto-accept-suggestions*, *auto.accept.suggestions*, *autoacceptsuggestions*
    - **checks:** *dm_only*
    <br>

- <ins>**CLEAR_ALL_SUGGESTIONS**</ins>
    - **aliases:** *clearallsuggestions*, *clear.all.suggestions*, *clear-all-suggestions*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        [sure=False]
        ```
    <br>

- <ins>**GET_ALL_SUGGESTIONS**</ins>
    - **aliases:** *get.all.suggestions*, *getallsuggestions*, *get-all-suggestions*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        [report_template=basic_report.html.jinja]
        ```
    <br>

- <ins>**MARK_DISCUSSED**</ins>
    - **aliases:** *mark-discussed*, *markdiscussed*, *mark.discussed*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        [suggestion_ids...]
        ```
    <br>

- <ins>**REMOVE_ALL_USERDATA**</ins>
    - **aliases:** *remove.all.my.data*, *remove.all.userdata*, *removeallmydata*, *removealluserdata*, *remove-all-userdata*, *remove-all-my-data*
    - **checks:** *dm_only*
    <br>

- <ins>**REQUEST_MY_DATA**</ins>
    - **aliases:** *request.my.data*, *requestmydata*, *request-my-data*
    - **checks:** *dm_only*
    <br>

- <ins>**USER_DELETE_SUGGESTION**</ins>
    - **aliases:** *unsave-suggestion*, *unsavesuggestion*, *unsave.suggestion*, *user.delete.suggestion*, *userdeletesuggestion*, *user-delete-suggestion*
    - **checks:** *dm_only*
    - **signature:**
        ```diff
        <suggestion_id>
        ```
    <br>


</blockquote>

</details>

---


### <p align="center">[TestPlaygroundCog](d:/dropbox/hobby/modding/programs/github/my_repos/antipetros_discord_bot_new/.venv/lib/site-packages/antipetros_discordbot/cogs/dev_cogs/test_playground_cog.py)</p> ###

<details><summary><b>Description</b></summary>

<blockquote>The base class that all cogs must inherit from.

A cog is a collection of commands, listeners, and optional state to
help group commands together. More information on them can be found on
the :ref:`ext_commands_cogs` page.

When inheriting from this class, the options shown in :class:`CogMeta`
are equally valid here.</blockquote>

</details>

<details><summary><b>Commands</b></summary><blockquote>

- <ins>**CHECK_DATE_CONVERTER**</ins>
    - **aliases:** *check.date.converter*, *checkdateconverter*, *check-date-converter*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        <in_date>
        ```
    <br>

- <ins>**CHECK_FLAGS**</ins>
    - **aliases:** *checkflags*, *check-flags*, *check.flags*
    - **checks:** *allowed_channel_and_allowed_role*
    - **signature:**
        ```diff
        [flags]... <ending>
        ```
    <br>

- <ins>**CHECK_TEMPLATE**</ins>
    - **aliases:** *check.template*, *check-template*, *checktemplate*
    - **checks:** *has_attachments*, *allowed_channel_and_allowed_role*
    - **signature:**
        ```diff
        [all_items_file=True] [case_insensitive=False]
        ```
    <br>

- <ins>**EMBED_EXPERIMENT**</ins>

    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role*
    <br>

- <ins>**GET_ALL_TEMPLATE_MESSAGES**</ins>
    - **aliases:** *getalltemplatemessages*, *get-all-template-messages*, *get.all.template.messages*
    - **checks:** *allowed_channel_and_allowed_role*
    <br>

- <ins>**MAKE_FIGLET**</ins>
    - **aliases:** *make-figlet*, *make.figlet*, *makefiglet*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        <text>
        ```
    <br>

- <ins>**RANDOM_EMBED_COLOR**</ins>
    - **aliases:** *random-embed-color*, *random.embed.color*, *randomembedcolor*
    - **checks:** *allowed_channel_and_allowed_role*
    <br>

- <ins>**SEARCH_USERNAMES**</ins>
    - **aliases:** *search-usernames*, *searchusernames*, *search.usernames*
    - **checks:** *log_invoker*, *allowed_channel_and_allowed_role*
    - **signature:**
        ```diff
        <names>
        ```
    <br>

- <ins>**SEND_ALL_COLORS_FILE**</ins>
    - **aliases:** *sendallcolorsfile*, *send-all-colors-file*, *send.all.colors.file*
    - **checks:** *allowed_channel_and_allowed_role*
    <br>

- <ins>**TEST_DYN_TIME**</ins>
    - **aliases:** *testdyntime*, *test-dyn-time*, *test.dyn.time*
    - **checks:** *allowed_channel_and_allowed_role*
    <br>

- <ins>**TEXT_TO_IMAGE**</ins>
    - **aliases:** *texttoimage*, *text-to-image*, *text.to.image*
    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        <text>
        ```
    <br>

- <ins>**THE_DRAGON**</ins>
    - **aliases:** *thedragon*, *the-dragon*, *the-wyvern*, *thewyvern*, *the.dragon*, *the.wyvern*
    - **checks:** *allowed_channel_and_allowed_role*
    <br>

- <ins>**TRANSLATE**</ins>

    - **checks:** *in_allowed_channels*, *has_any_role*
    - **signature:**
        ```diff
        <out_lang> <text>
        ```
    <br>


</blockquote>

</details>

---

</blockquote></details>

## Dependencies ##

***Currently only tested on Windows***

**Developed with Python Version `3.9.1`**

- humanize<=`3.2.0`
- cryptography<=`3.3.1`
- marshmallow<=`3.10.0`
- psutil<=`5.8.0`
- arrow<=`0.17.0`
- dpytest<=`0.0.22`
- pyfiglet<=`0.8.post1`
- paramiko<=`2.7.2`
- pytz<=`2020.5`
- async_property<=`0.2.1`
- aiohttp<=`3.7.3`
- python_benedict<=`0.23.2`
- googletrans<=`4.0.0rc1`
- Jinja2<=`2.11.2`
- autopep8<=`1.5.4`
- WeasyPrint<=`52.2`
- matplotlib<=`3.3.3`
- click<=`7.1.2`
- fuzzywuzzy<=`0.18.0`
- watchgod<=`0.6`
- dateparser<=`1.0.0`
- antistasi_template_checker<=`0.1.1`
- benedict<=`0.3.2`
- discord<=`1.0.1`
- gidappdata<=`0.1.7`
- gidlogger<=`0.1.7`
- Pillow<=`8.1.0`
- PyQt5<=`5.15.2`
- python-dotenv<=`0.15.0`
- udpy<=`2.0.0`





## License

MIT

## Development


### Todo ###

<details><summary><b>TODOS FROM CODE</b></summary>

#### todo [\_\_main\_\_.py](/antipetros_discordbot/__main__.py): ####


- [ ] [\_\_main\_\_.py line 40:](/antipetros_discordbot/__main__.py#L40) `create prompt for token, with save option`


---


#### todo [blacklist_warden.py](/antipetros_discordbot/bot_support/sub_support/blacklist_warden.py): ####


- [ ] [blacklist_warden.py line 139:](/antipetros_discordbot/bot_support/sub_support/blacklist_warden.py#L139) `make embed`


---


#### todo [error_handler.py](/antipetros_discordbot/bot_support/sub_support/error_handler.py): ####


- [ ] [error_handler.py line 35:](/antipetros_discordbot/bot_support/sub_support/error_handler.py#L35) `rebuild whole error handling system`


- [ ] [error_handler.py line 36:](/antipetros_discordbot/bot_support/sub_support/error_handler.py#L36) `make it so that creating the embed also sends it, with more optional args`


---


#### todo [admin_cog.py](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py): ####


- [ ] [admin_cog.py line 37:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L37) `get_logs command`


- [ ] [admin_cog.py line 38:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L38) `get_appdata_location command`


- [ ] [admin_cog.py line 231:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L231) `make as embed`


- [ ] [admin_cog.py line 237:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L237) `make as embed`


- [ ] [admin_cog.py line 246:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L246) `make as embed`


- [ ] [admin_cog.py line 252:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L252) `make as embed`


- [ ] [admin_cog.py line 258:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L258) `make as embed`


- [ ] [admin_cog.py line 267:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L267) `make as embed`


- [ ] [admin_cog.py line 292:](/antipetros_discordbot/cogs/admin_cogs/admin_cog.py#L292) `make as embed`


---


#### todo [performance_cog.py](/antipetros_discordbot/cogs/admin_cogs/performance_cog.py): ####


- [ ] [performance_cog.py line 41:](/antipetros_discordbot/cogs/admin_cogs/performance_cog.py#L41) `get_logs command`


- [ ] [performance_cog.py line 42:](/antipetros_discordbot/cogs/admin_cogs/performance_cog.py#L42) `get_appdata_location command`


- [ ] [performance_cog.py line 136:](/antipetros_discordbot/cogs/admin_cogs/performance_cog.py#L136) `limit amount of saved data, maybe archive it`


---


#### todo [purge_messages_cog.py](/antipetros_discordbot/cogs/admin_cogs/purge_messages_cog.py): ####


- [ ] [purge_messages_cog.py line 28:](/antipetros_discordbot/cogs/admin_cogs/purge_messages_cog.py#L28) `get_logs command`


- [ ] [purge_messages_cog.py line 29:](/antipetros_discordbot/cogs/admin_cogs/purge_messages_cog.py#L29) `get_appdata_location command`


---


#### todo [general_debug_cog.py](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py): ####


- [ ] [general_debug_cog.py line 48:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L48) `create regions for this file`


- [ ] [general_debug_cog.py line 49:](/antipetros_discordbot/cogs/dev_cogs/general_debug_cog.py#L49) `Document and Docstrings`


---


#### todo [image_manipulation_cog.py](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py): ####


- [ ] [image_manipulation_cog.py line 54:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L54) `create regions for this file`


- [ ] [image_manipulation_cog.py line 55:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L55) `Document and Docstrings`


- [ ] [image_manipulation_cog.py line 245:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L245) `make as embed`


- [ ] [image_manipulation_cog.py line 249:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L249) `make as embed`


- [ ] [image_manipulation_cog.py line 256:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L256) `make as embed`


- [ ] [image_manipulation_cog.py line 260:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L260) `maybe make extra attribute for input format, check what is possible and working. else make a generic format list`


- [ ] [image_manipulation_cog.py line 275:](/antipetros_discordbot/cogs/general_cogs/image_manipulation_cog.py#L275) `make as embed`


---


#### todo [save_link_cog.py](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py): ####


- [ ] [save_link_cog.py line 35:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L35) `refractor 'get_forbidden_list' to not use temp directory but send as filestream or so`


- [ ] [save_link_cog.py line 37:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L37) `need help figuring out how to best check bad link or how to format/normalize it`


- [ ] [save_link_cog.py line 372:](/antipetros_discordbot/cogs/general_cogs/save_link_cog.py#L372) `refractor that monster of an function`


---


#### todo [save_suggestion_cog.py](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py): ####


- [ ] [save_suggestion_cog.py line 57:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L57) `create report generator in different formats, at least json and Html, probably also as embeds and Markdown`


- [ ] [save_suggestion_cog.py line 59:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L59) `Document and Docstrings`


- [ ] [save_suggestion_cog.py line 198:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L198) `make as embed`


- [ ] [save_suggestion_cog.py line 204:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L204) `make as embed`


- [ ] [save_suggestion_cog.py line 219:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L219) `make as embed`


- [ ] [save_suggestion_cog.py line 231:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L231) `make as embed`


- [ ] [save_suggestion_cog.py line 235:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L235) `make as embed`


- [ ] [save_suggestion_cog.py line 239:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L239) `make as embed`


- [ ] [save_suggestion_cog.py line 244:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L244) `make as embed`


- [ ] [save_suggestion_cog.py line 280:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L280) `make as embed`


- [ ] [save_suggestion_cog.py line 283:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L283) `make as embed`


- [ ] [save_suggestion_cog.py line 294:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L294) `make as embed`


- [ ] [save_suggestion_cog.py line 298:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L298) `make as embed`


- [ ] [save_suggestion_cog.py line 302:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L302) `make as embed`


- [ ] [save_suggestion_cog.py line 307:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L307) `make as embed`


- [ ] [save_suggestion_cog.py line 317:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L317) `make as embed`


- [ ] [save_suggestion_cog.py line 352:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L352) `make as embed`


- [ ] [save_suggestion_cog.py line 355:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L355) `make as embed`


- [ ] [save_suggestion_cog.py line 359:](/antipetros_discordbot/cogs/general_cogs/save_suggestion_cog.py#L359) `make as embed`


---


#### idea [render_new_cog_file.py](/antipetros_discordbot/dev_tools_and_scripts/render_new_cog_file.py): ####


- [ ] [render_new_cog_file.py line 72:](/antipetros_discordbot/dev_tools_and_scripts/render_new_cog_file.py#L72) `create gui for this`


---


#### idea [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 55:](/antipetros_discordbot/engine/antipetros_bot.py#L55) `Use an assistant class to hold some of the properties and then use the __getattr__ to make it look as one object, just for structuring`


#### todo [antipetros_bot.py](/antipetros_discordbot/engine/antipetros_bot.py): ####


- [ ] [antipetros_bot.py line 53:](/antipetros_discordbot/engine/antipetros_bot.py#L53) `create regions for this file`


- [ ] [antipetros_bot.py line 54:](/antipetros_discordbot/engine/antipetros_bot.py#L54) `Document and Docstrings`


---


#### todo [sqldata_storager.py](/antipetros_discordbot/utility/sqldata_storager.py): ####


- [ ] [sqldata_storager.py line 36:](/antipetros_discordbot/utility/sqldata_storager.py#L36) `create regions for this file`


- [ ] [sqldata_storager.py line 37:](/antipetros_discordbot/utility/sqldata_storager.py#L37) `update save link Storage to newer syntax (composite access)`


- [ ] [sqldata_storager.py line 38:](/antipetros_discordbot/utility/sqldata_storager.py#L38) `Document and Docstrings`


- [ ] [sqldata_storager.py line 39:](/antipetros_discordbot/utility/sqldata_storager.py#L39) `refractor to subfolder`


---

### General Todos ###
</details>

