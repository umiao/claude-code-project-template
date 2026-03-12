---
title: Basics About Linux & Vim Usage
date: 2023-09-17 22:16:13
categories:
- [Job Search, Software Engineering]
tags:

- Linux
- Vim
- CLI
description: "For a Software Engineer / Researcher, Linux and Vim should be the basic of basics (as important parts of CLI, Command Line Interface). In this post, we have ..."
key_concepts:
  - Linux Command Line
  - Vim Editor
takeaways:
  - Linux file system follows a hierarchical tree structure rooted at / with standard directories
  - Vim operates in distinct modes (Normal, Insert, Command) each optimized for different editing tasks
  - Master essential CLI commands (ls, cd, grep, find, chmod) for efficient file and process management
  - Shell variables and environment configuration customize the command-line experience
---
For a Software Engineer / Researcher, Linux and Vim should be the basic of basics (as important parts of CLI, Command Line Interface). In this post, we have discussed some basic knowledge as well as useful tips.
{% asset_img cover.jpg Linux and Vim usage guide cover: command line interface basics %}
<!-- more -->


# Notes about Linux Usage:
## File System Structure of Linux
A tree like directory, the root would be **“/”**.
Some of the root folders: 
- ***“bin”*** storing binary executives
- ***“etc”*** for system configurations
- ***“home”*** for user files
- ***“lib”*** for libraries and modules
- ***“opt”*** for optionalpackages
- ***“root”*** for super user folder
- ***“tmp”*** for temporary files, etc.

## Format of commands:
`cmd [options] [arguments]`
The options and arguments all serve as part of input, use whitespace to separate.
For single character option, use `-option`. For a word, use `–-option` (two -s).

## Wildcard Matching Operator
- ***“*”*** for any character of any length
- ***“?”*** for single character
- ***\[ab..\]*** for any character among a, b, …, 
- ***\[!ab\]*** for any single character except a, b.

## File Type
- Normal file ***“-”***
- Directory ***“d”***
- Symbolic link ***“l”*** (hard link: point to a drive’s block of the file, just like a file; soft link: save an absolute path of a file)
- Character device file ***“c”***
- Block device file ***“b”***
- Socket ***“s”***
- Named pipe file ***“p”***

## Frequently Used Commands:
- ***“pwd”***: show the current directory of current user
- ***“cd”***: change dir
- ***“.”***: current directory
- ***“..”***: parent directory
- ***“-”***: the directory before “cd” command got executed
- ***“~”***: Absolute path name of the user’s main directory
- **Absolute directory**: start with “/”, describe the complete path to the location of file.
- **Relative directory**: not start with “/”, appoint a location in relative to your current
working dir.
- **Auto-Complete**: can press “Tab” to auto fill the command name / file name / etc. If
there are too many possibilities, need multiple press.
- ***“ls”***: show the information of file / dir
- ***“mkdir”***: create an empty dir in current dir
- ***“rmdir”***: remove empty dir only
- ***“touch”***: generate an empty file, or update the time of a file (-a, -m, -d)
- ***“cp”***: copy file or directory
- ***“mv”***: move / rename file or dir
- ***“rm”***: remove file or dir
- ***“ln”***: create a symbolic link
- ***“find”***: look up for a file
- ***“stat”***: look for file’s type / property
- ***“cat”***: create file / check the content of text file
- ***“more”***: used to view the text files, displaying one screen at a time.
- ***“less”***: similar to more, support search / roll back
- ***“tail”***: check the last n lines of file, with tail -n filename
- ***“head”***: check the first n lines instead
- ***“echo”***: redirect content into given files
- ***“|”***: pipe command. Pass the result of prior command to latter command, like: `ls -la | wc`. This is for listing info and word count.
- ***“&gt;, &gt;&gt;”***: &gt; would override content, &gt;&gt; would append content.
- ***“zip / unzip / gzip / gunzip /rar / tar”***: used to zip / unzip / pack.

### Regular Expression related:
- ***“grep”***: stands for “global search regular expression”.
**Format**: `grep [options] PATTERN [FILE…]`
**Examples**: 
1. grep &#39;^[a-zA-Z]&#39; myfile
2. grep -v &#39;^#&#39; myfile (reverse, only keep not matched result)
3. grep -lr root /etc/* (recursively list all filenames under /etc/ with
“root”)

## Shell Variables:
It can be classified as:
1. **Internal Variable**: provided by the system, use only to the user (cannot be modified)
2. **Environment Variable**: define the work env, can be used in shell; user can modify some of them
3. **User Variable**: defined by user (often used in script). (Definition: varName=Value, Reference: $varName).
4. **“export”** can switch variables between “Global” and “Local”
5. Some common shell env variables: **HOME, LOGNAME, USER, PWD, MAIL, HOSTNAME,
INPUTRC, SHELL, LANG, HISTSIZE, PATH, PS1, PS2**.

# VI / VIM (Visual Interface iMproved)
**Entering**: 
- `vim +n filename` (open file, place cursor to the beginning of nth line)
- `vim + filename` (open file, place cursor to the beginning of last line)
- `vim +/pattern` filename (open file, place cursor to first matched position)

**Modes**: 
- **Normal**: default mode when run vim
- **Insert**: press i, o, a to enter insert mode
- **Cmdline**: type commands starting with :, /, ?, !

## Under Normal Mode:

- ***G*** : jump to the end of file
- ***ZZ*** : save and exit
- ***ZQ*** : exit without save
- ***/*** or ***?*** : for string look up. (can be used with “n” for next match)
- ***n*** : Next. Search for next match.
- ***yy*** : copy one line
- ***p*** : paste to next line; P: paste to previous line
- ***dd*** : delete one line
- ***dw*** : delete a word; can use “dnw” to delete n words.
- ***d$*** : delete to the end of current line. “dG” will delete to end of document.

- ***y*** : similarly, we can use “y” just as d to duplicate words.
- ***p*** : use p for pasting. Can use “10p” to paste for 10 times.
- ***x*** : delete the character at the cursor.
- ***u*** : Undo. Undo the last operation.
- ***“Ctrl + r”*** : to revoke the undo.
- ***“h,j,k,l”*** : move the cursor to left/down/up/right
- ***“0”*** : move to head of line
- ***“^”*** : move to the first non-blank character
- ***“$”*** : move to end of line
- ***“g_”*** : move to the last non-blank character of current line
- ***“w”*** : move to the beginning of next word
- ***“e”*** : move to the end of next word
- ***“fa”*** : move to the position of next “a”. If use “Fa”, would move to previous a. 
- ***“nfa”*** : would move to the nth “a”’s position in current line. 
	Can use “;” to jump to next appointed character, “,” can jump to previous appointed character.

- ***“nG”*** : move cursor to the beginning of line n.
- ***“gg”*** : move cursor to beginning of line 1.
- ***“G”*** : move to the beginning of last line.
- ***“H / M / L”***: move cursor to the beginning / middle / end of current screen
- ***“% / * / #”*** : match parenthesis / match next word where cursor locates / match previous word where cursor locates

## Under Insertion Mode:

After entering this mode, any typed character would be recognized as content of file and then added.

***“Esc”***: press to exit insertion mode (back to normal mode)

## Under Command Mode:
Under Normal Mode, press ***“:”*** to enter Command mode. 
Vim would get into “Pending command” state.

- ***“:w”*** : save file
- ***“:w newfile”*** : save as a new file named “newfile”
- ***“:wq”*** : save and exit
- ***“:q!”*** : exit without save
- ***“:q”*** : save without changes made

- ***“:!command”*** : execute linux command, e.g., “date”, “ls”, …
- ***“:r !command”*** : e.g., “:r !date”: add the result to the position of cursor 

### Environment Setup:

- ***“:set autoindent / noautoindent”*** 
- ***“:set number / nonumber”*** : row number setting
- ***“:set ic / noic”*** : require being insensitive / sensitive to capitalized characters
- ***“:set tabstop=value”*** : map tab into “value” spaces
- ***“:set all”*** : show all the configurable options
- ***“:n”*** : locate at line n

- ***“2, 5d”*** : delete lines with row numbers of 2 – 5.
- ***“:s/aa/bb/g”*** : replace all “aa” with “bb” at current line.
	Replace “s” with “%s” would do the replacement across the entire document. 
	Replace “s” with “n1, n2” would do the replacements for lines (with line number n1~n2). 
	If omit “/g”, would only replace the first appearance. 
	If replace “/g” with “/gc”, confirmation would be required.