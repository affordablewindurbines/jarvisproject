jarvis Installation Script
==========================

Introduction
------------

This repository contains an installation script for all the libraries and
dependencies of [jarvis](http://jarvisproject.github.io/ "jarvis").

While the jarvis project provides an image for the model 1 of the
Raspberry Pi, there is no image for the model 2. Instead of mastering a
big image, I just provide a ready to run installation script.

The installation script will work on a model 1 or a model 2 Raspberry Pi
(Bananapi to be verified). Everything was tested with Raspian-Wheezy,
it might or might not work with Raspbian-Jessie (feedback on this
issue is appriciated).


Configure Installation
----------------------

After download of the package (or after cloning the repository) you will
find the installation script `jarvis-install` together with some
support files in the root-directory of the project. Configuration is
done using the file `jarvis-install.cfg`.

The file contains constants used by the installation program. Usually you
don't have to change any contstants except the value of `DEFAULT_USER` and
those named `INSTALL_xxx`. These constants select which modules the install
script actually installs. You can set the value of these constants to `0`
(don't install) or `1` (install).

For a Pi model 1, you must set `INSTALL_phonetisaurus_src=1`. For a
model 2, you are free to install from the Jessie package repository
(`INSTALL_phonetisaurus=1`) or from source.

Some of the modules do just basic tasks, so you should not change the
value - these constants are labelled *required*. Besides these modules, you
are free to select the STT and TTS engines you wan't (but observe the
dependencies). To understand the background, you should definitely read
the documentation on the project site of jarvis.


Install jarvis
--------------

The installation script `jarvis-install` assumes that you start of with
a *clean* installation of Raspbian-Wheezy (after initial configuration
with `raspi-config`). You need at least 4 GB free disk-space on the
root-partition, i.e. a 8GB (micro-) SDHC with expanded root-partition
should do fine.

A simple

    sudo ./jarvis-install all

should do the job. The script will create a (large) logfile named
`jarvis-install.log`, please check that file for errors.

Besides `all` you can pass the names of one or more individual modules to 
`jarvis-install`. This is more of a development feature to verify the
correct operation of the given install-task. To see all available
options of `jarvis-install`, just run `jarvis-install -h`.

If you connect with ssh and don't want to keep the connection open all
the time, you can also start the installation with

    nohup sudo ./jarvis-install all > /dev/null &

To monitor the progress in this case, you can use the command

    tail -f jarvis-install.log

or

    ./jarvis-install -S

The last command extracts a summary of the logfile.

The install script installs a number of packages using the normal package
management system of Debian (*apt*). Others are downloaded and compiled
from source. All files are installed below `$PREFIX`, which defaults to
`/usr/local`, i.e. you can copy this directory to another computer to
save some time during installation of a second machine(see the section
below labeled *Cloning the Installation* for details).


Some Timings
------------

Note that `jarvis-install` takes a lot of time to finish. This
depends on the speed of your internet connection, the speed of your
SD-card, overclocking and the number of configured modules. Also,
installation time is much faster on a model 2, since the compilations
of the source modules use all four available processors.

Running Raspbian off of an HDD/SDD speeds things up by about 5% for the
model1 and by 50% for model2. Search the web for instructions on how to move
your root-partition to an USB-attached HDD/SDD drive.

A complete installation will take

  - 7-8h on a Raspberry Pi Model 1
  - 3-5h on a Raspberry Pi Model 2
  - 2h on a Raspberry Pi Model 2 with a root-filesystem on HDD/SDD

OpenFST is the module taking longest, compile and linking of it alone
takes more than 5h on a model 1 (about 2h on a model 2).


Changes to the original install instructions
--------------------------------------------

There are some changes compared to the original install instructions from
jarvis's project site:

  - this script installs all programs globally
  - you can tailor the installation to your needs, e.g. if you don't plan
    to use phonetisaurus, you don't have to install all the programs
    needed by this STT-engine
  - you can run the jarvis-program with the simple command `jarvis`, or
    you can install jarvis as a system service`
  - jarvis is not added to a user's crontab (use the system service if you want
    to start jarvis automatically at boot time)
  - OpenFST is downloaded from the OpenFST-site in a slightly newer version
  - added configure-option to OpenFST to speed-up compilation
  - required package `python-pocketsphinx` was missing from the instruction
  - New download-address for phonetisaurus
  - only compile necessary binary for phonetisaurus
  - New download-address for phonetisaurus FST model
  - Download acoustic model and lexicon for Julius
  - create default profile.yml with all configuration-options
    (non-active STT/TTS-engines are added as comments)


Cloning the installation
------------------------

Since download and compile of all the prerequisite packages takes
so long, you can take a shortcut to clone jarvis to other computers.

The following steps are necessary:

  1. Copy everything below $PREFIX (i.e. `/usr/local`) to the new
     computer. You can use rsync for the task if you enabled
     root-login on the target computer (*clone*):

         sudo rsync -avz /usr/local/ root@clone:/usr/local

  2. Copy all `jarvis-install`-files to the target computer.
  3. Edit `jarvis-install.cfg.clone` to reflect your `jarvis-install.cfg`
     (read the comments in `jarvis-install.cfg.clone`).
  4. Run

         sudo ./jarvis-install -f -C jarvis-install.cfg.clone all


Running jarvis
--------------

To run jarvis as a foreground process from your normal user account
just run the command `jarvis` (your user account must be a member of 
the `audio` group and you should have configured this user as the
*DEFAULT_USER* in `jarvis-install.cfg`). If you like to see how jarvis
processes your commands, run

    jarvis --debug

Note that the install-script will create a default jarvis configuration 
profile for the default user (as defined in `jarvis-install.cfg`).
If you are not happy with the profile, you can delete it and run

    $PREFIX/lib/jarvis/client/populate.py

This will run you through the default configuration provided by jaser
itself. You can find details about the initial configuration on the
[jarvis project website](http://jarvisproject.github.io/
"jarvis project website").

As an alternative, you can install jarvis as a system-service. 
If not already done during installation, run

    sudo ./jarvis-install -f service
    sudo update-rc.d jarvis start

The last command is only necessary if you want to start the service at once.
Otherwise, it is automatically started at boot-time.

The configuration file for the service is in `$PREFIX/lib/jarvis/profile.yml`.

Sometimes, the service has problems to start right after installation and
reboot. In this case, delete the directory `$PREFIX/lib/jarvis/vocabularies`
and restart the service.


Renaming jarvis
---------------

If you have trouble pronouncing "jarvis", then you can change the
signal word from "jarvis" to "Thomas". You just have to define
`INSTALL_thomas=1` in `jarvis-install.cfg`. Note that this changes
the file `$PREFIX/lib/jarvis/jarvis.py` and some files in
`"$PREFIX/lib/jarvis/static`. If you want to return to the original
state, you should fetch the files from jarvis's Github-project.

To change the name after installation, you can run

    sudo ./jarvis-install -f thomas

to install this feature (regardless of the value of `INSTALL_thomas`).

If you prefer a different name, you should follow the instructions on
the project website of jarvis.
