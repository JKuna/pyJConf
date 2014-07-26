# pyJConf

# Jeff's Configuration Module
#
# JSON(ish) based configuration system that supports inline comments and easy
# switching between profiles.
#
# Comments are started with // as the first non-whitespace characters on each
# line. Profile specific lines are indicated with @profile as the first
# non-whitespace characters on each line.

import json

class JConf:
    _settings_dict = {}

    def __init__(self, filename, profile='default'):
        jsondata = self._parser(filename, profile)
        self._settings_dict = json.loads(jsondata)


    def _parser(self, filename, profile):
        temp_data = []
        with open(filename) as f:
            for line in f:
                linestripped = line.strip()
                if linestripped.startswith('//'): continue
                if linestripped.startswith('@'):
                    if linestripped.startswith('@' + profile):
                        temp_data.append(linestripped[len(profile) + 1:])
                else:
                    temp_data.append(linestripped)
        
        return ''.join(temp_data)


    def __getattr__(self, name):
        if name in self._settings_dict:
            return self._settings_dict[name]
        else:
            raise SettingUnspecifiedError


class SettingUnspecifiedError(LookupError):
    pass
