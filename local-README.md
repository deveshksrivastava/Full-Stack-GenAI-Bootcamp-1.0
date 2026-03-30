# Commands to update your fork from the main repo.

GIT LINK 

- sunnysavita10/Full-Stack-GenAI-Bootcamp-1.0
- https://drive.google.com/file/d/1NGjG3wVadDw12Dk-WOQNkGSj2FUG2rUK/view

## One-time setup (if upstream is not added yet)
- git remote -v
- git remote add upstream https://github.com/sunnysavita10/Full-Stack-GenAI-Bootcamp-1.0.git
- git remote -v

### Update your fork’s main from main repo
- git checkout main
- git fetch upstream --prune
- git merge --ff-only upstream/main
- git push origin main

### Optional: single-line version
git checkout main && git fetch upstream --prune && git merge --ff-only upstream/main && git push origin main

### Optional checks
git status -sb
git log --oneline --decorate --graph -n 10
git branch -vv