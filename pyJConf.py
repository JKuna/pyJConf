# pyJConf

# Jeff's Configuration Module
#
# JSON(ish) based configuration system that supports inline comments, easy
# switching between profiles, and nested files.
#
# Comments are started with // as the first non-whitespace characters on each
# line. Profile specific lines are indicated with @profile as the first
# non-whitespace characters on each line. Nested files are included with
# include(filename).

import json

class JConf:
    _settings_dict = {}

    def __init__(self, filename, profile='default'):
        jsondata = self._parser(filename, profile)
        try:
            self._settings_dict = json.loads(jsondata)
        except ValueError:
            raise JConfSyntaxError


    def _parser(self, filename, profile, filelist = None):
        temp_data = []
        if filelist:
            if filename in filelist: raise JConfRecursiveFileError
            filelist.append(filename)
        else:
            filelist = [filename]
        with open(filename) as f:
            for line in f:
                linestripped = line.strip()
                if linestripped.startswith('//'): continue
                if linestripped.startswith('@'):
                    if linestripped.startswith('@' + profile):
                        linestripped = linestripped[len(profile) + 1:].strip()
                    else:
                        continue
                if linestripped.startswith('include('):
                    linestripped = linestripped[len('include('):]
                    subfilename = linestripped.split(')', 1)[0]
                    linestripped = self._parser(subfilename, profile, filelist)
                temp_data.append(linestripped)
        return ''.join(temp_data)
        

    def __getattr__(self, name):
        if name in self._settings_dict:
            return self._settings_dict[name]
        else:
            raise SettingUnspecifiedError


class SettingUnspecifiedError(LookupError):
    pass


class JConfSyntaxError(ValueError):
    pass


class JConfRecursiveFileError(Exception):
    pass