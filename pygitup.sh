#!/bin/sh

cwd=$(pwd)
shopt -s expand_aliases
source ~/.bash_profile
cdpy

# folders
git add -u Python\ Files/CoursePlan/*.py Python\ Files/CoursePlan/*.png
git add Python\ Files/Lyrics/*.py
git add Python\ Files/Simplifier/*.py Python\ Files/Simplifier/*.png
git add Python\ Files/MatrixGenerator/*.py
git add Python\ Files/PathConverter/*.py
git add Python\ Files/PyExport/*.py
git add Python\ Files/FileConverter/*.py
git add Python\ Files/FileDuplicator/*.py
git add Python\ Files/WxChatbox/*.py
git add Python\ Files/Sudoku/*.py Python\ Files/Sudoku/sudoku.*
git add Python\ Files/学习强国/*.py

# Scripts
git add ez.py ezs.py eztk.py
git add Python\ Files/FIR.py Python\ Files/FlappyBird.py Python\ Files/stats.py Python\ Files/GroupRename.py Python\ Files/贪吃蛇.py Python\ Files/整钱换零钱.py Python\ Files/diary.py Python\ Files/BackupHelper.py Python\ Files/LifeGame.py

# README.md
git add README.md

# gitignore
git add .gitignore

if [ $# -eq 0 ]; then
    git commit -m "Code update"; git push origin head
elif [ $# -eq 1 ]; then
    if [ "$1" = "-f" ]; then
        git commit -m "Code update"; git push -f origin head
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
        git push origin master
    fi
elif [ $# -eq 2 ]; then
    if [ "$1" = "-f" ]; then
        git commit -m "$2"; git push -f origin head
    else
        echo "Usage: pygitup -f \"message\""
        exit 1
    fi
else
    echo "Usage: pygitup or pygitup \"message\" "
    exit 1
fi

cd "$cwd"