---
title: Introduction to Git - Basics
permalink: introduction-to-git/
date: 2024-08-06 22:42:55
categories:
- [Job Search, Software Engineering]
tags:
- Git
- Data System
- Version Control
description: "Part 1 of Git learning notes covering fundamentals: config, status, staging, committing, history, remotes, tagging, and aliases."
key_concepts:
  - Git Version Control
  - Git Three-Area Model
series: Git Guide
series_index: 1
takeaways:
  - Git stores snapshots of the entire project state, not diffs between file versions
  - The three-area model (working directory, staging area, repository) gives precise control over commits
  - git add stages a snapshot at command time; later changes need a new add
  - Lightweight tags are simple pointers while annotated tags are full objects with metadata
---
Thorough analysis and learning note based on git documentation (https://git-scm.com/book/en/v2).
{% asset_img cover.jpg Introduction to Git cover: version control concepts %}
<!-- more -->

- **Patches set**: the differences between files / versions; can be used to recreate files
- **Centralized Version Control Systems**: single server contains all versioned files. Clients checkout file from central place. Prone to *single point failure*.
- **Distributed Version Control Systems**: clients fully mirror the repository and history.

---

Git is **snapshot** based (store and index changed files), rather than difference based (storing the delta / change of files).
Near all operation is local.
Integrity is enforced by **checksum** (empowered by **SHA-1** hash). Git will be able to detect change / corruption.
Git generally only adds data. committed changes are hard to lost.

### Three status
1. **Modified**: file changed, not committed
2. **Staged**: marked a modified file in its current version to go into your next commit snapshot
3. **Committed**: data is safely stored in your local database

These states lead us to main sections of git project: **working tree**, **staging area**, **git directory**.

{% asset_img 1.jpg Git three-area model: working tree, staging area, and git directory %}

---
Installation: refer to this [link](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

---

### Git Config
1. **Configuration Overwrite**: `.git/config` (local project) will overwrite (`~/.gitconfig ` / ` ~/.config/git/config`, current user) and will overwrite `/etc/gitconfig` (system level).
2. Show where setting comes from: `git config --list --show-origin`
3. Setting up user email: 
`git config --global user.name "John Doe"`
`git config --global user.email johndoe@example.com`
(remove `--global` to make local setting only)
4. Check all configuration: `git config --list`

---

Use `git help` for help page. 
You can use `git COMMAND -h` for brief help message, like `git add -h`.  `git help add` will be more comprehensive.


---

### Git Repository Initialize

- Create repository from scratch:

`cd /Users/user/my_project`
`cd /Users/user/my_project`
`git add *.c`
`git add LICENSE`
`git commit -m 'initial project version'`

---

- Clone existing repo:
`git clone https://github.com/libgit2/libgit2 (optional_alias)`

---
### Git Status
Use `git status` to check the status of your files.
You can check if any file is `untracked` (can be tracked via `git add`) or change `uncommitted`.

You can use `git status -s` to get more **compacted** output.

---

### Git Add
**Example**: `git add <files>`, the input can be either directory or file name.
This command can **track** new files, **stage** files and mark merge-conflict files as **resolved**.
\*Note that `git add` will only stage the snapshot of a file by the time "add" command is executed. If changes happended later, we need to add again.

**Ignoring files**: for log or temp files which we do not want Git to automatically add or even show as "untracked", we can configure in **.gitignore** file.

Rules of writing `.gitignore` file:
1. Blank lines or lines starting with # are ignored.
2. Standard glob (shell simplified regular expression) patterns work, and will be applied recursively throughout the entire working tree.
3. You can start patterns with a forward slash (/) to avoid recursivity.
4. You can end patterns with a forward slash (/) to specify a directory.
5. You can negate a pattern by starting it with an exclamation point (!).

For more examples of `.gitignore`, please check [here](https://github.com/github/gitignore).

---
### Git Diff
1. `git diff`:
Inspect what have **changed** but not yet **staged**.
2. `git diff --staged` or `git diff --cached`:
Inspect what you’ve **staged** that will go into your next **commit**.

---
### Git Commit
1. `git commit`: will run the default text editor for creating a message for the commit, and the changes to be committed will be shown.
2. Use: `git commit -m "YOUR MESSAGE"` can create the commit with message in one line.
3. `git commit -a -m 'YOUR MESSAGE'` can skip the stage area without manually adding all the changed files. However, we should be careful before doing this (should check `git status`).

---

### Removing Files
1. `git rm` will remove a file from your tracked files (more accurately, remove it from your staging area) and then commit. The file will also be removed from your working directory.
	**Example**: `git rm YOUR_FILE_NAME`
2. To remove a **edited / staged** file, we need to add `-f` (force removal) to prevent accidental removal of data that hasn't been recorded in a snapshot.
3. `git rm --cached YOUR_FILE_NAME` can remove (accidentally staged) files from **staging area** but keep the file in the working tree. 
	**Example**: If you forget to add log files or compiled files to the `.gitignore` file and accidentally staged.
4. You can pass files, directories, and file-glob patterns to the git rm command.
	**Example**: `git rm log/\*.log` and `git rm \*~`. Note that the `\` is needed because Git does its own filename expansion in addition to shell's filename expansion.
5. We can rename file with: `git mv file_from file_to`
	This is actually equivalent to running 3 commands of: `mv README.md README`, `git rm README.md` and `git add README`

---

### Check commit history
1. `git log`: by default,  this command lists each commit with its SHA-1 checksum, the author’s name and email, the date written, and the commit message.
2. Use the `-p` or `--patch` mode to show the difference of each commit in the format of **patches** : `git log -p -NUM`. Here `NUM` restricts to show only `NUM` entries.
3. Use the `git log --stat` to show some **abbreviated stats**.
4. Use `git log --pretty=oneline` to show the commit history in different **formats**. (also have other options like `short`, `full` and `fuller`). 
5. We can use `git log --pretty=format:"%h - %an, %ar : %s"` to format the commit history and extract the information you need. E.g. `%h` shows the **abbreviated hash**, `%an` shows the **author name** and `%ar` is **Author date, relative** and `%s` is the subject.
6. Use `--graph` option to **visualize** the branch and merge history. 
	**Example**: `git log --pretty=format:"%h %s" --graph`
7. **Time limiting** options such as `--since` and `--until`. E.g., `git log --since=2.weeks`.
8. `-S` / **pickaxe** option. By using `git log -S function_name`, we will show only those commits that changed the number of occurrences of that string.

---

### Undo things

1. Use `git commit --amend` takes your staging area and use it for the commit. This will **overwrite** your previous commit.
2. Use `git reset HEAD <file>…` to **unstage**. In this case, it will be removed from the staging area but changes kept in working tree.
	\* It should be noted that `reset` is a dangerous command. In git, almost all **commited** data can be recovered. However, **uncommited** changes may lost forever. 

---

### Working with Remotes
1. `git remove -v`: shows you the URLs that Git has stored for the shortname to be used when reading and writing to that remote.
2. `git remote add <shortname> <url>` will add a new remote explicitly.
3. `git fetch <remote>`: goes out to that remote project and pulls down all the data from that remote project that you don’t have yet. (If you used `clone` to copy a remote, it will be automatically added as remote "origin"). Also, `git fetch` will do the data downloading only without changing your work.
4. `git pull`: automatically **fetch** and then **merge** that remote branch into your current branch.
5. `git push <remote> <branch>` will push your changes to the upstream. (This command works only if you cloned from a server to which you have **write access** and if nobody has pushed in the meantime)
6. `git remote show <remote>` to check more information a remote.
7. `git remote rename <old_name> <new_name>` to **rename** a remote. `git remote remove <remote>` to **remove** a remote.

---

### Tagging

Git has the ability to tag specific points in a repository’s history as being **important**.

- **Lightweight tag**: a pointer to a specific commit
- **Annotated tag**: full objects, checksummed, with the tagger name, email and date and message.

**Example**: 
1. Annotated: `git tag -a v1.4 -m "my version 1.4"`
2. Light-weighted: `git tag v1.4-lw`

Use `git show` to check the tagger information, data the commit was tagged and theannotation message. 

Use `git tag -d <tagname>` to **remove** a tag.

\* By default, `git push` will not transfer tags to remote. We need to do that explicityly: `git push origin <tagname>`
Or we can use `git push origin --tags` to push **ALL** tags. 
\*\* if you `checkout` to a tag, your repo will be at **detached HEAD** status. In such case, if you make changes and then created a commit, the tag will stay the same, but your new commit will not belong to any branch and become **unreachable**.

---

### Alias
We can create **alias** for git commands for convenience, examples:
`git config --global alias.co checkout`
`git config --global alias.br branch`
`git config --global alias.unstage 'reset HEAD --'`
`git config --global alias.last 'log -1 HEAD'`

To run an external command, rather than a Git subcommand, start the command with a `!` character.

`git config --global alias.visual '!gitk'`
