## Changelog

All notable changes to this project will be documented here.

### 0.2.0 - 03/26/2025

#### Added

- Added an exception handling system: instead of Python errors printing directly into the
console, they are caught and the output is written in an "except.log" file generated in the
current working directory.

#### Changed

- Files are no longer restored into the root of the drive. Instead, the user now has to provide
a path to an empty directory in which all the files and/or folders will be stored.
- When aborted, the script now exits normally (in the previous version, when aborted, the program
would exit with code 1).

#### Fixed

- Fixed a bug where moving files that were marked as system files (usually by the malware)
would fail, due to the lack of appropriate actions in such cases.

#### Removed

- Removed trace deletion, meaning the user now has to manually remove trace files.
This was removed for security reasons.
- Removed the option to restart the script automatically after the user indicates the script
has failed.
