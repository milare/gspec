GSpec
=============

GSpec is a Gedit Plugin to run rspec tests in Rails Application


Install
-------
`git clone git@github.com:milare/gspec.git`

`cd gspec`

`./install.sh`

Go to: Edit->Preferences->Plug-ins and active plugin


WARNING
-------
Check if spec_helper is being required with its full path:

require File.expand_path(File.dirname(__FILE__) + '/../spec_helper')

