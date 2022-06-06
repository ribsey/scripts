git init
git remote add -f origin https://github.com/ribsey/scripts
git config core.sparseCheckout true

echo fun_stuff/AdSi/ >> .git/info/sparse-checkout

git pull origin master