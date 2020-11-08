

def config_channels_convert(channels: list):
    _out = {}
    for item in channels:
        item = item.strip()

        channel_name, channel_id = item.split(' ')
        _out[channel_name] = int(channel_id)
    return _out
