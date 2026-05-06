# This project handles dependency in a "slim tree" kinda way, avoiding duplicate imports as much as possible.
# I think at the moment of writing, there isn't any duplicate imports, but any suggestion regarding architecture is very welcome.
# It is worth noting that ./skills.py uses objects defined higher in the tree, so the definitions therein are not input-strict.
# It's very likely that there's a better way to structure this, but I'm not a developer by trade so there's really no other way I know how to structure the codebase hahaha.
# Here's a diagram of the dependencies:
#
#                                                                       -- needs.py ---- states.py
#                                                                      /
#   Your BuddyAutomata script ---- imports.py ---- personalities.py --<
#       (like main.py)                                                 \
#                                                                       -- actors.py ---- worlds.py ---- fields.py ---- skills.py ---- locations.py ---- (numpy as np)
#

from personalities import *