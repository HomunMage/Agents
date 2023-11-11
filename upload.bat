git config --local user.name "AIMageGuild"
git config --local user.email "AIMageGuild@users.noreply.github.com"
git remote set-url origin git@AI:aimageguild/GPTs.git

git pull
git add .
git commit -m "upload"
git push