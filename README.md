# Requirements

For full functionality, Cinch-Utils requires at least the tools
and versions listed here:

* CMake (Version 2.8)
* Python (Version 2.7)
* Pandoc (Version 1.12)

# Installation

To begin, configure Cinch-Utils with the path to the desired installation
directory:

    % mkdir build
    % cd build
    % cmake -DCMAKE_INSTALL_PREFIX=/path/to/install ..
    % make install

This will install the command-line tool and some helper scripts to
setup your environment.  After you have performed the above steps, you
should source the appropriate environment script, e.g.:

    % source /path/to/install/bin/cinchenv.sh (bash)

or

    % source /path/to/install/bin/cinchenv.csh (csh/tcsh)

The installation also includes an environment module that may be
used to configure your environment.  This may be installed in an
appropriate system location, or locally by adding the installation
bin directory to your MODULEPATH.

**If you prefer, you may also set the required environment variables
manually:**

***PATH*** add the bin directory of the install path to your PATH

***PYTHONPATH*** add the lib/pythonX.X/site-packages path to your PYTHONPATH
