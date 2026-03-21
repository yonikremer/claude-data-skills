---
name: windows-cli
description: Executes file and system operations using Windows cmd and PowerShell. Use when listing files or managing directories on Windows. Do NOT use for file operations within Python (use pathlib) or for version control (use git).
---
# Windows Command Line Usage

This skill focuses on using the Windows Command Prompt (cmd.exe) and PowerShell for basic file and directory operations.

## Key Commands

### Command Prompt (cmd.exe)

*   `dir`: List directory contents.
*   `cd`: Change directory.
*   `mkdir`: Create a new directory.
*   `rmdir`: Remove a directory.
*   `del`: Delete a file.
*   `copy`: Copy a file.
*   `move`: Move a file.
*   `echo`: Display messages.
*   `type`: Display content of a file.

### PowerShell

*   `Get-ChildItem` (or `ls`, `gci`): List directory contents.
*   `Set-Location` (or `cd`, `sl`): Change directory.
*   `New-Item -ItemType Directory`: Create a new directory.
*   `Remove-Item`: Remove a directory or file.
*   `Copy-Item`: Copy a file.
*   `Move-Item`: Move a file.
*   `Write-Output` (or `echo`): Display messages.
*   `Get-Content` (or `cat`, `gc`): Display content of a file.
