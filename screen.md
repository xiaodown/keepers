## Screen primer

### Starting and managing screens

To start a screen, simply type `screen`.

You can name a screen with the `-S <name>` argument, i.e. you can spawn multiple screens, and detach / reattach to a specific one.  You can get a list of them with `screen -ls`:
```
# screen -S development
# screen -S testing
# screen -ls
There are screens on:
        1188.testing    (01/27/2016 01:11:13 PM)        (Detached)
        1165.development        (01/27/2016 01:10:55 PM)        (Detached)
2 Sockets in /var/run/screen/S-root.
``` 
And you can reattach with `screen -r <name>`.  
If you are logged in on a different terminal, you can add the `-d` flag to the reattach, which will detach existing connections and reattach your current session: `screen -dr <name>`.

### Screenrc

I recommend using [my `.screenrc`](https://github.com/xiaodown/dotfiles/blob/master/.screenrc) - it will make screen all nice and pretty.

This screenrc will set up visible tabs along the bottom (like this: http://i.imgur.com/sahGhp0.png), as well as some unix-y stuff to manage the delete key, the terminal bell, etc.

### Screen commands

All of the screen commands use `ctl-a`, as in control-a, as a prefix.  For the purposes of this document, this will be written as `^a`.  To send a literal control-a into the program that's running in screen, you can use `^a a`.

To exit a screen, you must simply exit all of the bash sessions that are inside the screen, which can be done by typing `exit`, or by using the unix-y shortcut for end-of-file, `^d` (control-d).  You must do this on each tab in the screen session to exit.

To detach from a screen, use `^a d`.  This leaves the screen running (and everything in it running), and you can reattach to it later to check up on it.  Be ware: this does weird things with SSH agent forwarding if you're authenticating with ssh keys via an ssh agent and using these keys to forward your auth to other servers.  This seems to not work when you resume a screen after logging out of the box and back in.

Here is a quick reference:

#### Screen management
Command | effect
----|----
`^a d` | detach from current screen

#### Window Management

Command | effect
--- | ---
`^a c` | create a new tab
`^a <number>` | switch to tab # (works for tabs 0-9)
`^a ' <number>` | switch to tab #
`^a n` | switch to next tab 
`^a p` | switch to previous tab
`^a ^a` | switch back to the last tab you were on (flip flop between two tabs)
`^a "` | presents a curses menu of tabs for switching
`^a A` | rename current window (useful for running many applications, tailing multiple logs, etc)
`^a ESC` | allows you to scroll up (up key / pgup) 

The scrolling up takes a bit of getting used to, but basically, `^a ESC`, then you go into a mode where you can use the arrow keys or pgup to scroll up and see output that's gone off of the screen / out of view.  To exit this mode, just hit enter a couple of times, and it returns you to your prompt.

#### Advanced window management

Command | effect
--- | ---
`^a S` | split screen horizontally
`^a \|` | split screen vertically
`^a TAB` | jump to the next split region
`^a X` | remove current region
`^a Q` | remove all other regions except current

#### Sharing screens

Useful for pair programming, you may want to share a screen with a co-worker.  
To get a list of screens running under a different user, you can use `screen -ls xiaodown/`.  Note the trailing slash, and of course, replace `xiaodown` with the unix username of the user's screen that you are attempting to attach to.  To share a screen, first, the "host" of the session will also need to enable multiuser mode, covered below.  To attach to a screen, use `screen -x xiaodown/foobar` where `xiaodown` is the user and `foobar` is the name of the screen.  

Command (note colons) | effect
---|---
`^a :multiuser on` | turn multi-user on
`^a :acladd <username>` | allow `<username>` to join screen session
`^a :fit` | resize the window to the size of your terminal window / xterm / putty (kinda rude, ask first)

And the commands used to invoke screen:

#### Screen command-line commands
Command | effect
--- | ---
`screen` | invoke screen
`screen -S <name>`| invoke a screen named `<name>`
`screen -ls` | see a list of screens (for the current user)
`screen -r <name>` | reattach to the screen named `<name>`
`screen -dr <name>` | detach other sessions and reattach to the screen named `<name>`
`screen -ls xiaodown/` | get a list of `xiaodown`'s screens
`screen -x xiaodown/foobar` | multiuser attach to the `foobar` screen that `xiaodown` is running




