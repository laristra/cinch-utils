#------------------------------------------------------------------------------#
# Copyright (c) 2014 Los Alamos National Security, LLC
# All rights reserved.
#------------------------------------------------------------------------------#

import re
import os
from os.path import join
from ccli.services.doc_drivers.utils import *
from ccli.services.doc_drivers.document import *

symbols = {
  'document' : 'DOCUMENT',
  'section' : 'SECTION',
}

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#

def walk_tree(directory, suffixes, document, verbose, development):

#def walk_tree(directory, suffixes, documents, \
#  initial_document, verbose, development):

  default_document = Document('Default')
  current_document = document
  current_section = current_document.section('Default')

  if(verbose):
    print 'ccli: search directory ' + directory
    print 'ccli: document ' + document.title()
    print 'ccli: initial section ' + current_section.title()
  # if

  # Walk directory looking for files in suffixes
  for root, dirs, files in os.walk(directory):
    for file in files:

      if file.endswith(suffixes):

        # Open file to search for symbols
        with open(join(root,file)) as fd:

          if verbose:
            print 'ccli: processing ---- ' + file + ' ----'
          # if

          # Grab all of the lines
          lines = fd.readlines()

          # Go through the lines
          for index, line in enumerate(lines):

            if "CHAPTER" in line:
              print 'WARNING: CHAPTER symbol is deprecated'
            # if

            # If this is a doc line, parse the symbols
            #if '<!-- CINCHDOC' in line or '% CINCHDOC' in line:
            if begin_identifier(line):
              parsed = {}

              # Check to see if this is all on one line
              # If this is a latex file, the symbols
              # must be on a single line
              #if '-->' in line or '% CINCHDOC' in line:
              if single_line_identifier(line):
                # If it is all on one line,
                # read all of the symbols off of the line
                for key in symbols:
                  if symbols[key] in line:
                    parsed[key] = \
                      read_token(symbols[key], line)
              else:
                # If not, read symbols until a close-comment
                # is encountered
                while True:
                  index += 1
                  line = lines[index]
                  
                  #if '-->' in line:
                  if end_identifier(line):
                    break

                  for key in symbols:
                    if symbols[key] in line:
                      parsed[key] = \
                        read_token(symbols[key], line)
                    # if
                  # for
                # while
              # if

              # See if the document needs to be reset
              if 'document' in parsed and \
                document.title() in parsed['document']:
                current_document = document
              else:
                current_document = default_document
              # if

              if(verbose):
                print 'ccli: -> document ' + \
                  current_document.title()
              # if

              # See if the section needs to be created or reset
              if 'section' in parsed:
                current_section = \
                  current_document.section(parsed['section'])

                if(verbose):
                  print 'ccli: -> section ' + \
                    current_section.title()
                # if
              # if

              # Append file information
              current_section.append('<!-- cinch metadata\n')
              current_section.append('FILE(' + join(root, file) +
                ')\n')
              current_section.append('-->\n')
              
              if(development):
                current_section.append('\n\color{green}')
                current_section.append('###############\n\n')
                current_section.append('\color{blue}CINCH METADATA ')
                current_section.append('\color{black}FILE:' +
                  join(root, file) + '\n')
              # if

              # Read the actual content until the end
              # of the file, or until another CINCHDOC block
              # is encountered
              while True and (index < len(lines) - 1):
                index += 1
                line = lines[index]

                #if '<!-- CINCHDOC' in line or \
                #    '% CINCHDOC' in line:
                if begin_identifier(line):
                  break
                # if

                # Strip comments (must be done after
                # cinch annotations directly above
                if begin_comment_identifier(line):
                  continue
                # if

                if(development):
                  if 'CINCHNOTE' in line:
                    note = '\color{red}{' + \
                      '\small{' + \
                      '\emph{' + \
                      'NOTE: ' + \
                      read_token('CINCHNOTE', line) + \
                      '}' + \
                      '}' + \
                      '}' + '\color{black}  ' # newline
                    line = re.sub(r'CINCHNOTE(.*)',
                      note, line)
                  # if
                # if

                current_section.append(line)
              # while
            # if
          # for
        # with
      # if
    # for
  # for
# walk_tree

#------------------------------------------------------------------------------#
# Formatting options for emacs and vim.
# vim: set tabstop=2 shiftwidth=2 expandtab :
#------------------------------------------------------------------------------#
