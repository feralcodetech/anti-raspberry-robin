# Anti-Raspberry Robin

This is a relatively simple open-source Python script designed to make removing the Raspberry
Robin Trojan (also known as simply "the USB virus") easier for non-experienced users.

I got this idea when one of my teachers was having problems with the Trojan, and since I was one
of the victims of this malicious piece of software that spreads it self through flash drives, and
I pretty much figured out how it works and what it does, I decided to try to make an automated
script to remove it to help other people.

Key features:

- Automated removal of some of the most common traces of the malware
- Restoration of hidden files (which are actually just hidden, not deleted or encrypted, but guess
what, not everyone is a computer geek and not everyone knows how to use commands)

Currently, this script is for Windows only (sorry Linux users), but I plan to expand it to other
operating systems as well (maybe, if this makes it any further from my GitHub page).

Usage:

```cmd
anti-raspberry-robin [drive]
```

`[drive]` - the letter of the drive to operate on, followed by a colon (":")

I made this project open-source because I don't think anyone would pay a cent for 200-ish lines
of Python code, so any help (feature recommendations, bug reports, new malware pattern reports)
would be greatly appreciated.

**Disclaimer:** This script is made to remove the installation processes (or whatever it's called)
and restore files hidden by the malware.

If you get this Trojan, do NOT click the shortcut you see on your drive, as it will install the
Trojan on your machine.

If you already clicked it, it's too late, but you can still use this script to restore your
files.

Hopefully, we'll make it somewhere with this project...

## License

This project is distributed under the [Boost Software License 1.0](LICENSE.txt).
