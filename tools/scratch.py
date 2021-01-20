a = """googletrans==4.0.0-rc1
Jinja2
checksumdir
click
regex
parce
fuzzywuzzy
python-Levenshtein
Pillow
PyGithub
WeasyPrint
discord.py
url-normalize
async-property
watchgod
pdfkit
pytz
google-auth
google_api_python_client
google_auth_oauthlib
psutil
--force-reinstall cchardet
python-benedict
udpy
commonmark
pyfiglet
graphviz
pydot
lxml
networkx
pyowm
colormap
aiosqlite
discord-flags
paramiko[all]
antistasi_template_checker
cryptography
humanize
marshmallow
parse
invoke
arrow
pendulum
python-dateutil
dateparser
"""

_out = []
for i in a.splitlines():
    if i != '':
        p = i.split('=')[0].split("[")[0].split()[-1]
        _out.append(p)
print(','.join(_out))
