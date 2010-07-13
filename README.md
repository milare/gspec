GSpec
=============

GSpec is a Gedit Plugin to run rspec tests in Rails Application


Install
-------
command(cd ~/.gnome2/gedit/plugins)
command(git clone git@github.com:milare/gspec.git)
command(mv gspec/gspec.gedit-plugin ./)

Go to: Edit->Preferences->Plug-ins and active plugin


WARNING
-------
Check requires to our spec_helper

command(require File.expand_path(File.dirname(__FILE__) + '/../spec_helper'))