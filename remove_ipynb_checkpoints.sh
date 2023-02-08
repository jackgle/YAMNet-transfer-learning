# to remove the file on git without deleting from local
#  use -> git rm --cached 
find . -name .ipynb_checkpoints -print0 | xargs -0 git rm -r --ignore-unmatch
echo .ipynb_checkpoints >> .gitignore