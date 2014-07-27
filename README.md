# Jeff's Configuration Module

## Overview

JSON(ish) based configuration system that supports inline comments, easy
switching between profiles, and nested files.

Comments are started with // as the first non-whitespace characters on each
line. Profile specific lines are indicated with @profile as the first
non-whitespace characters on each line. Nested files are included with
include(filename).

## Use

JConf can take two arguments: the "root" configuration file and an optional
profile name.

### Example (default profile)

    from pyJConf import JConf

    settings = JConf("settings.jconf")

    print settings.username

### Example (specified profile)

    from pyJConf import JConf

    settings = JConf("settings.jconf", "user")

    print settings.username
    print settings.useronlysetting

## Future work

A significant issue with this version is that extra or missing commas can
result from optionally including profile lines. For instance the easily
readable example below fails when the default profile is loaded.

    {"A": 1,
    @test "testsetting": "True"}

Instead the file must be formatted with the comma moved to the second line.

    {"A": 1
    @test, "testsetting": "True"}

I hope to make parsing such files more lenient by either checking for and
removing such terminal commas or ditching JSON entirely and using another
format. 

Since some configuration files can get really complex, I'd also like to add
more specific error messages to help debug faulty config files as well as add
debugging methods to list which settings were overwritten by profile specific
settings.