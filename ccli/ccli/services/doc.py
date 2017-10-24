#------------------------------------------------------------------------------#
# Copyright (c) 2014 Los Alamos National Security, LLC
# All rights reserved.
#------------------------------------------------------------------------------#

import ast
from pickle import Unpickler
from collections import OrderedDict

from ccli.base import Service
from ccli.services.doc_drivers.walk import *

#------------------------------------------------------------------------------#
# Documentation handler.
#------------------------------------------------------------------------------#

class CINCHDoc(Service):

  #--------------------------------------------------------------------------#
  # Initialization.
  #--------------------------------------------------------------------------#

  def __init__(self, subparsers):

    """
    """

    # get a command-line parser
    self.parser = subparsers.add_parser('doc',
      help='Service to generate documentation using Pandoc.')

    # add command-line options
    self.parser.add_argument('-c', '--config', action="store",
      help='configuration module.' +
        '  Load the configuration information' +
        ' from python module CONFIG.')

    self.parser.add_argument('-o', '--output', action="store",
      help='output target.' +
        '  Write output to file OUTPUT.')

    self.parser.add_argument('-v', '--verbose', action="store_true",
      help='verbose output.')

    self.parser.add_argument('-d', '--development', action="store_true",
      help='development output (inline metadata).')

    self.parser.add_argument('directories', nargs='+',
      help='A colon-delimited list of directories to process.')

    # set the callback for this sub-command
    self.parser.set_defaults(func=self.main)

  # __init__

  #--------------------------------------------------------------------------#
  # Main.
  #--------------------------------------------------------------------------#

  def main(self, args=None):

    """
    """

    # Recognized file suffixes
    suffixes = (".md", ".tex")

    # Setup default options
    opts = {
      'document' : 'Default',
      'output' : 'cinchdoc.mdwn'
    }

    #----------------------------------------------------------------------#
    # Process command-line arguments
    #----------------------------------------------------------------------#

    # Check for user-defined configuration and import as module
    # if option is set
    if args.config:
      (path, configfile) = os.path.split(args.config)

      # Add configfile path to module search path
      if not path:
        sys.path.append(os.getcwd())
      else:
        sys.path.append(path)

      # import the options from the specified module
      opts = __import__(os.path.splitext(configfile)[0]).opts
    # if

    # Check for command-line output specification
    # NOTE: this option will over-write the value specified in
    # the configuration file
    if args.output:
      opts['output'] = args.output

    #----------------------------------------------------------------------#

    # Create the document object
    document = Document(opts['document'])

    # Process sections-prepend option
    if 'sections-prepend' in opts:
      for section in opts['sections-prepend']:
        document.add_section(section)

    # Process sections option
    if 'sections' in opts:
      for section in opts['sections']:
        document.add_section(section)

    # Recurse directories passed by user
    for directory in args.directories:

      # Search sub-directories for documentation files
      walk_tree(directory, suffixes, document,
        args.verbose, args.development)

    # Remove the default section if sections were found
    # Because we add a 'header' section, there should be
    # two sections if none were added by the user.
    if (len(document.sections()) > 2) and 'Default' in document.sections():
      document.delete_section('Default')

    #----------------------------------------------------------------------#
    # Process sections-append
    # This removes section-append keys and then re-adds them, this
    # effectively sorts them to the end in-order because we are using
    # an ordered dict.
    #----------------------------------------------------------------------#

    if 'sections-append' in opts:
      saved = dict()
      for section in document.sections():
        for key in opts['sections-append']:
          if key == section:
            saved[key] = document.sections()[key]

      for key in saved:
        document.delete_section(key)

      for key in saved:
        document.add_section(key, saved[key])

    #----------------------------------------------------------------------#
    # End Process sections-append
    #----------------------------------------------------------------------#

    # For now, just write to the specified output
    document.write(opts['output'])

  # main

  #--------------------------------------------------------------------------#
  # Object factory for service creation.
  #--------------------------------------------------------------------------#

  class Factory:
    def create(self, subparsers): return CINCHDoc(subparsers)
  # class Factory

# class CINCHDoc

#------------------------------------------------------------------------------#
# Formatting options for emacs and vim.
# vim: set tabstop=2 shiftwidth=2 expandtab :
#------------------------------------------------------------------------------#
