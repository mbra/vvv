"""

Tab policy
====================

Validator name:: ``tabs``

Do not allow hard tabs in committed files.
Instead, use soft tabs and spaces.


To allow hard tabs in any file add the following in your ``validator-options.yaml``::

    tabs:
        enable: false

To allow hard tabs in specific files use ``validator-files.yaml``::

    tabs:
      Makefile
      *.mk 

Converting tabs to spaces 
--------------------------------

VVV provides a Python script to expand tabs to spaces in-place.

With ``find`` and ``xargs`` you can easily convert the whole project 
tree away from hard tabs::

    
    # Find all ascii files and convert them to use tabs
    find . -name "*" -type f -print | xargs file | grep ASCII | cut -d: -f1 | xargs scripts/expand_tabs.py --inplace --tabsize=4 

        
Supported files
----------------

* All text files, Makefiles are excluded by default

Options
-----------

No options.

More info
------------

* http://dougneiner.com/post/641596410/tabs-vs-spaces

"""

import logging

from vvv.plugin import Plugin

class TabsPlugin(Plugin):
    """
    Hard tab banisher plug-in.
    """

    def setup_local_options(self):
        if not self.hint:
            self.hint = "Adjust your text editor settings to indent using spaces instead of hard tabs.\nUse a converter to convert existing tabs to spaces.\nhttp://dougneiner.com/post/641596410/tabs-vs-spaces"

    def get_default_matchlist(self):
        """
        These files require hard tabs
        """
        return [
            "*",
            "!Makefile",
            "!*.mk"
        ]

    def validate(self, fname):
        """
        Tabs validator code runs in-line.
        """

        errors = False

        i = 0
        f = open(fname, "rt")
        for line in f:
            i += 1
            if "\t" in line:
                errors = True
                self.reporter.report_detailed(self.id, logging.ERROR, fname, i, None, None, "Line contains hard tabs", excerpt=line)
        f.close()

        return not errors