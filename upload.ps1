cd _includes
./upload.bat
cd ../

cd _layouts
./upload.bat
cd ../

cd assets
./upload.bat
cd ../

git config --local user.name "HomunMage"
git config --local user.email "homun@posetmage.com"
git remote set-url origin git@HO:homunmage/GPTs.git

git submodule update --recursive --remote

git pull
git add .
git commit -m "upload"
git push
