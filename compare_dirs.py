#!/usr/bin/env python
#

import argparse
import os

from souvenir_utils import *

parser = argparse.ArgumentParser()
parser.add_argument('source_dir', help='source root directory')
parser.add_argument('target_dir', help='backup root directory')
parser.add_argument('-p', '--path', help='display full path', action='store_true')
parser.add_argument('-c', '--cmd', help='display processing command', action='store_true')
parser.add_argument('-m', '--mode', help=\
  'CHECK_SOURCE - list files which are in the source directory but not in the target, ' +
  'CHECK_TARGET - list files which are in the target directory but not in the source, ' +
  'CHECK (default) = CHECK_SOURCE + CHECK_TARGET', default='CHECK')
ARGS = parser.parse_args()

SOURCE_ROOT = ''
TARGET_ROOT = ''
TO_BE_PROCESSED = []
CMD_TYPE_CP = 1
CMD_TYPE_RM = 2
CMD_TYPE = ''


class ItemInfo:
  def __init__(self, dir_path, name):
    self.name = name
    self.dir_path = dir_path
    self.source_path = os.path.abspath(os.path.join(SOURCE_ROOT, dir_path, name))
    self.target_path = os.path.abspath(os.path.join(TARGET_ROOT, dir_path, name))
    self.is_dir = os.path.isdir(self.source_path)
    
  def has_target(self):
    if self.is_dir:
      return os.path.isdir(self.target_path)
    return os.path.isfile(self.target_path)
    
  def get_report(self):
    sub_path = os.path.join(self.dir_path, self.name)
    if self.is_dir:
      res = textc('[{}]'.format(sub_path), Colors.BOLD)
    else:
      res = textc(sub_path, Colors.BOLD)
    if ARGS.path:
      res += textc(" ('{}')".format(self.source_path), Colors.MODEST)
    # TODO: disable or correct commands on Windows
    if ARGS.cmd:
      if CMD_TYPE == CMD_TYPE_CP:
        (path, name) = os.path.split(self.target_path)
        if self.is_dir:
          cmd = "cp -r '{}' '{}'".format(self.source_path, path)
        else:
          cmd = "cp '{}' '{}'".format(self.source_path, path)
      elif CMD_TYPE == CMD_TYPE_RM:
        if self.is_dir:
          cmd = "rm -rf '{}'".format(self.source_path)
        else:
          cmd = "rm '{}'".format(self.source_path)
      if cmd:
        res += '\n    ' + textc(cmd, Colors.CMD)
    return res


def process_dir(dir_name):
  dirs_count, files_count = (0, 0)
  for name in os.listdir(os.path.join(SOURCE_ROOT, dir_name)):
    item = ItemInfo(dir_name, name)
    if item.is_dir:
      dirs_count += 1
    else:
      files_count += 1
    if item.has_target():
      if item.is_dir:
        d_count, f_count = process_dir(os.path.join(dir_name, item.name))
        dirs_count += d_count
        files_count += f_count
    else:
      TO_BE_PROCESSED.append(item)
  return dirs_count, files_count


def process_root_dir(source_root, target_root, cmd_type):
  global SOURCE_ROOT
  global TARGET_ROOT
  global CMD_TYPE
  SOURCE_ROOT = source_root
  TARGET_ROOT = target_root
  CMD_TYPE = cmd_type

  dirs_count, files_count = process_dir('')
  dirs_count += 1 # include root dir
  print('Directories checked: {}, files checked: {}'.format(dirs_count, files_count))


def run_check_source():
  printc('\nChecking source directory...', Colors.HEADER) 

  process_root_dir(ARGS.source_dir, ARGS.target_dir, CMD_TYPE_CP)

  if TO_BE_PROCESSED:
    print('These items should be backuped ({}):'.format(len(TO_BE_PROCESSED)))
    for item in TO_BE_PROCESSED:
      print('  ' + item.get_report())
  else:
    printc('All files already backuped', Colors.OKGREEN)


def run_check_target():
  printc('\nChecking target directory...', Colors.HEADER)

  process_root_dir(ARGS.target_dir, ARGS.source_dir, CMD_TYPE_RM)

  if TO_BE_PROCESSED:
    print('These items are backuped but not found in the source directory ({}):'.format(len(TO_BE_PROCESSED)))
    for item in TO_BE_PROCESSED:
      print('  ' + item.get_report())
  else:
    printc('All backuped items have corresponding sources', Colors.OKGREEN)


#-----------------------------------------------------------------------
if __name__ == '__main__':
  print_welcome()

  print('Source directory: ' + textc(ARGS.source_dir, Colors.BOLD))
  if not os.path.isdir(ARGS.source_dir):
    print_error_and_exit('Source directory does not exist')

  print('Target directory: ' + textc(ARGS.target_dir, Colors.BOLD))
  if not os.path.isdir(ARGS.target_dir):
    print_error_and_exit('Target directory does not exist')

  if ARGS.mode == 'CHECK':
    run_check_source()
    TO_BE_PROCESSED = []
    run_check_target()
  elif ARGS.mode == 'CHECK_SOURCE':
    run_check_source()
  elif ARGS.mode == 'CHECK_TARGET':
    run_check_target()
  else:
    print_error_and_exit('Unknown run mode ' + ARGS.mode)

  print('')
