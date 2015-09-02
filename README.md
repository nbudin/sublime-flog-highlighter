# Flog Highlighting for Sublime Text 2 and 3

## Installation

First, install the `flog` and `json` gems to your *system* Ruby (and yes, you
really do have to use sudo for this, and call `/usr/bin/gem` directly):

```bash
sudo /usr/bin/gem install flog json
```

Then clone this plugin into your Sublime Text plugins directory.  For Sublime
Text 3, do:

```bash
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
git clone git@github.com:nbudin/sublime-flog-highlighter.git
```

If you're still on ST2, then do this:

```bash
cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
git clone git@github.com:nbudin/sublime-flog-highlighter.git
```

## Complexity analysis on save

When you save a file ending in .rb, Sublime will now automatically run Flog
against it and highlight the first line of methods that are complex.  The
default complexity thresholds are:

* 100 or higher: red background
* 50 or higher: red outline
* 25 or higher: string colored outline

## Detailed reporting

You can also use the "Flog Report" command (on Mac, Cmd-Shift-P and choose
"Flog Report").  This will open an output panel containing a detailed
complexity analysis of the file you're looking at.  This might be helpful in
figuring out why Flog thinks a particular method is complex.