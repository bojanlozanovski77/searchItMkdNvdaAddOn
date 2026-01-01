# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.


# Since some strings in `addon_info` are translatable,
# we need to include them in the .po files.
# Gettext recognizes only strings given as parameters to the `_` function.
# To avoid initializing translations in this module we simply roll our own "fake" `_` function
# which returns whatever is given to it as an argument.
def _(arg):
	return arg


# Add-on information variables
addon_info = {
	# add-on Name/identifier, internal for NVDA
	"addon_name": "searchItMKD",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on
	# to be shown on installation and add-on information found in Add-ons Manager.
	"addon_summary": _("searchItMKD"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description": _("""This tool gives an explanation for words in macedonian language. It has to be only one word that this script will give an explanation for. 
    NVDA + shit + z for activation.
    First layer of commands:
        q : for info about selected text. (proceed to second layer of commands)
        w : for clipboard text. (proceed to second layer of commands)
        e : for last saved text. (proceed to second layer of commands)
        o : show Settings Menu.
        c : copies last given result to clipboard.
    Second layer of commands:
        s : grammar + all the meanings (basically all the information you can get about a word from this addon) ('s' as 'se').
        g : only grammar information ('g' as 'gramatika').
        d : only all the meanings information ('d' as 'definicii').
        b : info about how many meanings there are in total ('b' za 'broj na definicii').
        1 : only first meaning information (if there is one).
        2 : only second meaning information (if there is one).
        ...
        0 : only 10-th meaning information (if there is one).
        shift + 1 : only first meaning's translations (if there are any).
        shift + 2 : only second meaning's translations (if therea are any).
        ...
        shift + 0 : only 10-th meaning's translations (if there are any).
    Meanings are taken from the Digital Dictionary of the Macedonian Language."""),
	# version
	"addon_version": "1.0",
	# Author(s)
	"addon_author": "Bojan Lozanovski <bojanlozanovski77@gmail.com>",
	# URL for the add-on documentation support
	"addon_url": None,
	# Documentation file name
	"addon_docFileName": "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3.0", minor version is optional)
	"addon_minimumNVDAVersion": 2020.2,
	# Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion": 2025.1,
	# Add-on update channel (default is None, denoting stable releases,
	# and for development releases, use "dev".)
	# Do not change unless you know what you are doing!
	"addon_updateChannel": None,
}

# Define the python files that are the sources of your add-on.
# You can either list every file (using ""/") as a path separator,
# or use glob expressions.
# For example to include all files with a ".py" extension from the "globalPlugins" dir of your add-on
# the list can be written as follows:
# pythonSources = ["addon/globalPlugins/*.py"]
# For more information on SCons Glob expressions please take a look at:
# https://scons.org/doc/production/HTML/scons-user/apd.html
pythonSources = []

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []

# Base language for the NVDA add-on
# If your add-on is written in a language other than english, modify this variable.
# For example, set baseLanguage to "es" if your add-on is primarily written in spanish.
baseLanguage = "en"

# Markdown extensions for add-on documentation
# Most add-ons do not require additional Markdown extensions.
# If you need to add support for markup such as tables, fill out the below list.
# Extensions string must be of the form "markdown.extensions.extensionName"
# e.g. "markdown.extensions.tables" to add tables.
markdownExtensions = []