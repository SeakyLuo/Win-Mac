#!/bin/sh

git add .
if [ $# -eq 0 ]; then
    git commit -m "Code update"; git push origin master
elif [ $# -eq 1 ]; then
    if [ "$1" = "-f" ]; then
        git commit -m "Code update"; git push -f origin master
    else
        if [ "$1" = "-b" ]; then
            git commit -m "Bug fixes";
        elif [ "$1" = "-i" ]; then
            git commit -m "Various improvements";
        elif [ "$1" = "-n" ]; then
            git commit -m "New features";
        elif [ "$1" = "-d" ]; then
            git commit -m "Debugging test";
        elif [ "$1" = "-s" ]; then
            git commit -m "Save work"
        elif [ "$1" = "-bi" ]; then
            git commit -m "Bug fixes and various improvements"
        else
            git commit -m "$1";
        fi
        git push origin head
    fi
elif [ $# -eq 2 ]; then
    if [ "$1" = "-f" ]; then
        git commit -m "$2"; git push -f origin master
    else
        echo "Usage: gitup -f \"message\""
        exit 1
    fi
else
    echo "Usage: gitup or gitup \"message\" "
    exit 1
fi
exit 0