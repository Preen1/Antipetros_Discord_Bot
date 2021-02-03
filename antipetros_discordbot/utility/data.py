COMMAND_CONFIG_SUFFIXES = {'enabled': ('_enabled', True), 'channels': ('_allowed_channels', ''), 'roles': ('_allowed_roles', ''), 'dm_ids': ('_allowed_dm_ids', '')}


DEFAULT_CONFIG_OPTION_NAMES = {'dm_ids': 'default_allowed_dm_ids', 'channels': 'default_allowed_channels', 'roles': 'default_allowed_roles'}


COG_CHECKER_ATTRIBUTE_NAMES = {'dm_ids': "allowed_dm_ids", 'channels': 'allowed_channels', 'roles': 'allowed_roles'}


COG_NEEDED_ATTRIBUTES = ['on_ready_setup', 'update', 'config_name', 'docattrs', 'required_config_options', 'support', 'allowed_channels', 'allowed_dm_ids', 'allowed_roles']
