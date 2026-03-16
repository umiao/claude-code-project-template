---
title: Introduction to Git - Branching and Advanced
date: 2024-08-13 22:42:55
categories:
- [Job Search, Software Engineering]
tags:
- Git
- Data System
- Version Control
description: "Part 2 of Git learning notes covering branching, rebasing, server protocols, reflog, stashing, searching, reset, and merge tips."
key_concepts:
  - Git Branching
  - Git Rebasing
  - Git Reset
series: Git Guide
series_index: 2
takeaways:
  - Rebase creates linear history while merge preserves branch topology; choose based on collaboration needs
  - Reflog tracks all HEAD movements and enables recovery of seemingly lost commits
  - Never rebase commits that exist outside your repository and that people may have based work on
  - git reset --soft/--mixed/--hard offer different levels of undo by moving HEAD, index, and working directory
---
Continued Git learning notes covering branching, rebasing, and advanced topics.
{% asset_img cover.jpg Introduction to Git cover: branching and advanced topics %}
<!-- more -->

# Branch

Git stores **snapshots** (as **BLOB** objects) for files, rather than patches or diffs.

When making a commit, Git stores a commit object that contains a **pointer** to the snapshot of the content you staged. Also contains the author’s name and email address, the message that you typed, and pointers to the commit or commits that directly came before this commit (its **parent** or **parents**): 
\* **0** parents for the initial commit, **1** parent for a normal commit, and **multiple** parents for a commit that results from a merge of two or more branches.
\*\* Aside from the commit information and blob obj, a **tree object** is used to record the directory structure and blob object reference.

A branch in Git is a **movable pointer** to one commit. The default branch name in Git is `master`.

---
**Commands**:
- Run `git branch` without parameters, you will see a list of branches, with the current branch marked with `*`.
- `git branch --merged` / `git branch --no-merged` can show the branches which are already merged (can be safely deleted) / not yet merged by the current branch (cannot be deleted by `git branch -d`, need to use `git branch -D`).

### Create a new branch
1. `git branch <name>`: creates a new pointer to the same commit you are currently on.
2. A speical pointer `HEAD` marks the current branch.
\* Note that with `git branch`, you just created a new branch, do not checkout to that branch by default.
3. You can use `git log --decorate` to check which commit objects the branch pointers are pointing to.

---

### Checkout to branch
1. Use `git checkout <name>` to have `HEAD` pointing to another branch (for checking out).
2. You can create a new branch, and checkout to that branch with: `git checkout -b <name>`

A branch in Git is actually a simple file that contains the 40 character **SHA-1** checksum of the commit it points to. This makes the branch creating & checkout extremely efficient.

\* You do not need to provide the entire 40-character SHA-1. You just need to provide **at least 4 beginning characters** (by default 7) (have to be **unambiguous**).
\*\* **Branch reference**:  If a commit is at the tip of a branch, you can refer to it with `git show <commit_id>` or `git show <branch_name>`

### Merge of branch
1. In case you want to switch to the master branch to add some fix while shelving the changes in your current dev branch, you can first **commit** and the changes and then **checkout** to master.
2. When the fix is finished, and the dev is finished after that, you can checkout to master and use `git merge <dev_branch>` to merge the changes.

### Rename of branch
1. Locally: `git branch --move bad-branch-name corrected-branch-name`
2. Globally: `git push --set-upstream origin corrected-branch-name`
We can use `git branch --all` to check if the **renaming** is successful.

---

## Remote branches
1. Remote-tracking branches are **references** to the **state** of remote branches. Git moves such local references (pointers) for you whenever you do network communications to make them up-to-date.

2. Remote-tracking branch names take the form `<remote>/<branch>`
3. 	Remote-tracking branches (pointers) will not move if you do **NOT** connect to remote server and pull.
4. Use `git remote add <remote_alia> <remote_url>` to **add** a new remote repository for your project.
5. `git checkout -b <branch> <remote>/<branch>` or `git checkout --track <remote>/<branch>`, to create a local branch which tracks the remote branch. 
	\* To set the local branch to use a **different** name, use `git checkout -b local_name remote/branch`
	\*\* Use `-u` or `--set-upstream-to` to set / update the upstream branch for an existing local branch.
6. Use `git branch -vv` for **ALL** tracked branches.
	\* This may not be updated. Run `git fetch --all` ahead.
7. Use `git push origin --delete remote_branch` to **remove** a branch from server. This can usually be recovered before garbage collection.

---

# Rebasing
1. If `merge` is used in branch merging, a **three-way merge** will be performed on the 2 latest branch snapshots, and the most recent common ancestor of them 2. 
	\* This will result in a **new** snapshot and commit.
2. **Rebasing**: take the **patch** of the change that are introduced in dev branch, and **reapply** it on top of the master branch.
3. Rebasing works by:
	a. Going to the common ancestor of the two branches
	b. Getting the **diff** introduced by each commit of the branch you’re on
	c. Saving those diffs to temporary files
	d. Resetting the current branch to the same commit as the branch you are rebasing onto
	e. Finally applying each change in turn.
4. Rebasing makes the commits apply **cleanly** and appears as the work happened in **series** though they are originally in parallel.
5. Rebasing enables a **fast-forward** and a clean apply.

---

It is possible to apply the generated replays / patches to a **different** branch than the target branch.

`git rebase --onto master server client` will:
1. Take the client branch, figure out the patches since it **diverged** from the server branch
2. Replay these patches in the client branch as if it was based directly off the master branch instead.

---
### The Perils of Rebasing

Do **NOT** rebase commits that exist outside your repository and that people may have based work on.

In that case, you’re **abandoning** existing commits and creating new ones that are similar but different. 
If you changed the submission history in a public repo, you and cowork may face confusing results (**duplicates** of commit, and the deprecated commits can be found back).

**Solution**: Ask your coworkers to `git pull --rebase`. You should not remove commits where others may be doing development on.
**\* !** Rebase **local** changes before pushing to clean up your work, but **never** rebase anything that you’ve **pushed** somewhere.

---

# Git protocols on Server

1. **Local**: shared file system based, remote drive may be slow and inconvenient. Each user will gain complete shell acess of the remote directory.
2. **HTTP**: "Smart HTTP" works similar to SSH and Git, just on HTTP/S port with autentication mechanisms. Fast and easy, can provide encrption and pass firewalls. Setting up the server end can be less convenient. We also have "Dumb HTTP" which expects the bare Git repo to be served like normal files.
3. **SSH (Secure Shell)**: More common, safe and efficient. However, it does not support anonymous access to your Git repository. 
4. **Git**: Based on a special port 9418, **NO** authentication or cryptography. It is difficult to set up and requires firewall access to port 9418.

---

### Reflog

**reflog**: a log of your `HEAD` and branch references, kept for a few months. It should be noted that it is stored only **locally**. When a new repo is cloned, it is going to be emppty.
- Every time your branch tip is updated for any reason, Git stores that information for you in this temporary history. 
- Refer to older commits: `git show HEAD@{5}` to show the **fifth** prior value of the `HEAD` for your repo.
- Use `git show master@{yesterday}` to check the commits which are pointed by your master branch yesterday.
- Use `git log -g` to check the content of **reflog**, but using the format of `git log` output. 

---

### Ancestry References

- If you place a **^** (caret) at the end of a reference, Git resolves it to mean the **parent** of that commit.
- git show `HEAD^` will show the parent of `HEAD`.
- You can specify a number to identify which parent you want. `d921970^2` means the **second parent** of d921970.
- `~` refer to the first parent. Thus, `HEAD~` is equivalent to `HEAD^`.


---

### Commit Ranges
1. **Double Dot**: Show all commits reachable from experiment that aren’t reachable from master: `git log master..experiment`. Similarly, `git log experiment..master` shows everything in master not reachable from experiment.
		\* `git log origin/master..HEAD` Shows what is about to push to remote.
2. **Multiple Points**: See what commits are in any of several branches that aren’t in the branch you’re currently on: use `^` or `--not` before any reference from which you **don’t** want to see reachable commits.
		**Equivalent** expressions:
		1. `git log refA..refB`
		2. `git log ^refA refB`
		3. `git log refB --not refA`
		Use `git log refA refB ^refC` to see commits reachable from refA and refB, but not from refC.
3. **Triple Dot**: specifies all the commits that are reachable by **either** of two references but not by both of them.
		`git log --left-right master...experiment` shows which commit is unique and belongs to which branch.

---

### Stashing and Cleaning
- `git stash` can preserve the half-done work so you can work on other things and come back later.
		\* `git stash save` is to be migrated to: `git stash push`
- Use `git status` to see if the stash command takes effect (working tree clean)
- `git stash list` to **check** the stored stashes.
- `git stash apply` to **apply** the recently stashed work (by default the **most recent** one)
		\* To apply an older change, you can specify the name like `git stash apply stash@{2}`
		Also the working tree should be **clean**; Stashed changes can be apply to another branch, if not, merge conflicts.
		\*\* The staged files will **NOT** be **restaged**. To do that, run `git stash apply --index`
- The `git stash apply` will not remove your stash.
		To **remove**, use `git stash drop stash@{0}` to drop stash by name (0 is the most recent one)
		`git stash pop` will apply & delete the most recent stash.
- By default, only **tracked** files will be stashed.
		To stash untracked files: `git stash -u / --include-untracked`
		To stash **ignored** files, `git stash -a \ --all`
- Use `git stash --patch` to **interactively** determine what to stash.
- `git stash branch <new branchname>` to create a **NEW** branch based on the stash.

---

### Git Clean
1. Use `git clean` to remove redundant files / clean up working directory which are **NOT ignored** 
		(remove **untracked** files / **empty** dir by ` git clean -f -d`) 
		(remvoe **ignored** files using `-x`)
		Better `git stash --all` first, because such files may not be able to be retrieved.
2. Use `git clean -d -n / --dry-run` to see what it **will** do.

---

## Search
1. Use `git grep keyword` to search **files** in your working directory.
2. `git grep -n keyword` to search the **line number**.
3. Use `-c / --count` to **summarize** the output.
4. Use `-p /  --show-function` to display the enclosing **method or function** for each matching string.

---

## Log Searching
- To see **when** a term existed or was introduced, we can use `-S`:
`git log -S keyword --oneline`.
- We can use `-G` to search with **regular expression**.
- Use `-L` to trigger **Line Log Search**.
		 `git log -L :FunctionName:FileName`
		 Git will try to figure out what the bounds of that function are and then look through the history and show us every change that was made to the function as a series of patches back to when the function was first created.

---

### Rewrite History
1. `git commit --amend` to rewrite the **last** commit changes and message.
2. Use `git rebase -i HEAD~3` to rewrite the **last three** commits. You can also specify a **branch** to rewrite all the diverging commits.
		When entering the text editor, you can change "pick" into "edit" to edit a commit, or use "squash" to merge a commit.
		After making the changes, run `git commit --amend` and `git rebase --continue`
		You can use this method to **reorder** commits, or **eliminate** some entirely.
3. To rewrite huge swaths of history, you can use **filter-branch**, or just use the more recommended [git-filter-repo](https://github.com/newren/git-filter-repo).

---

### Reset

**Mental frame** of Git: Managing 3 **trees** (collections of files).
1. **HEAD**: Last commit snapshot, next parent
2. **Index**: Proposed next commit snapshot
3. **Working Directory**: Sand box.

After `git add`, content in working tree will be added to index. With `git commit`, content in index will be further saved as a permanent **snapshot**, create a commit object pointing to that snapshot and update the current **branch**. 

1. `git reset --soft`: Move `HEAD` only to **revert** the last commit. This can be used to **compact** the commits.
2. `git reset --mixed`: Move `HEAD` and update index to be aligned with the current `HEAD`. Aside from reverting the commit, we **unstaged** everything.
3. `git reset --hard`: the working directory is eventually overwritten with the commit we reset to. 
	It is **dangerous** because it destroys data.
4. If a path is set, `git reset` will skip the moving of `HEAD` but update the index and working directory partially.

---

- `git checkout <branch>` can be very similar with `git reset --hard <branch>`. However, for checkout, the working directory is safe, and will try to do a trivial merge in the working directory.
	Also, `reset` will change a commit a branch pointing to, but `checkout` will change the branch itself.
- If a path is attached, checkout works like `git reset --hard [branch] file`. It will not move `HEAD` and is not safe for working directory.

---

### Tips About Merge
1. If you **revert**ed a merged change, but later want to merge again, it will not work because the original merge is still reachable. 
	In that case, you will also need to revert the revert.
2. `git config --global rerere.enabled true` can trigger the rerere function. 
	After merging, how conflicts are resolved will be recorded and can be check using `git rerere status`.
	`git rerere diff` will raise the text editor so that conflicts will be resolved. After resolving that, the solution will be kept and remembered.
	In the future, we can see something like `Resolved 'hello.rb' using previous resolution.`
	\* if you have the solution, just use `git rerere` to reuse solution for resolving.
3. `git blame -L Line_range_beg,Line_range_end <FileName>` can check who introduced certain change.
4. `git bisect` can be used to detect when failure is introduced.
	a. `git bisect start`: start searching
	b. `git bisect bad`: current commit is **bad**
	c. `git bisect good <good_commit>`: certain commit is good
		We can keep giving "good" and "bad" feedbacks to figure out the first bad one.
		After all, use `git bisect reset` to reset the `HEAD`pointer.








