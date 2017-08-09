if [ $# = 1 ]
then
    words=$1
else
    words='quick sub'
fi
git add *
git status
git commit -m '$words'
git push origin master
