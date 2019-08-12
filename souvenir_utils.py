#
# Helper functions commonly used in different scripts.
#

from __future__ import print_function

import platform

IS_WINDOWS = False
IS_LINUX = False
IS_MACOS = False
p = platform.system()
if p == 'Windows':
  IS_WINDOWS = True
elif p == 'Linux':
  IS_LINUX = True
elif p == 'Darwin':
  IS_MACOS = True
else:
  print('ERROR: Unknown platform {}'.format(p))
  exit()


# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
class Colors:
  HEADER = '\033[95;1m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  CMD = '\033[36m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  MODEST = '\033[30;1m'


def textc(txt, color):
  if IS_WINDOWS:
    # TODO
    return txt
  return color + txt + Colors.ENDC


def printc(txt, color):
  print(textc(txt, color))


def print_error_and_exit(txt):
  printc('\nERROR: {}\n'.format(txt), Colors.FAIL)
  exit()


def print_welcome():
  # http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Souvenir%20Tool
  printc('''
   _________                                .__         ___________           .__   
  /   _____/ ____  __ _____  __ ____   ____ |__|______  \__    ___/___   ____ |  |  
  \_____  \ /  _ \|  |  \  \/ // __ \ /    \|  \_  __ \   |    | /  _ \ /  _ \|  |  
  /        (  <_> )  |  /\   /\  ___/|   |  \  ||  | \/   |    |(  <_> |  <_> )  |__
 /_______  /\____/|____/  \_/  \___  >___|  /__||__|      |____| \____/ \____/|____/
         \/                        \/     \/                                        
''', Colors.OKBLUE)
