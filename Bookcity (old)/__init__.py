#-*- coding: UTF-8 -*-
# from sys import argv
from BookcityParser import Parser as BookcityParser
# Script, SectionName, StoppedIndex = argv

if __name__ == '__main__':
    print("Welcome to Bookcity parser by foxychmoxy")
    print("Did you ever parse bookcity before?")
    answer = input("yes or no: ")
    if(answer == "yes" or answer == "y"):
        print("Where did you stop?")
        SectionName = input("Section name: ")
        StoppedIndex = input("Stopped index: ")
        try:
            bp = BookcityParser()
            bp.AppGetBooksRun(SectionName, int(StoppedIndex))
        except:
            print("Something went wrong")
    elif (answer == "no" or answer == "n"):
        bp = BookcityParser()
        bp.AppGeneralRun()
    else:
        print("I do not understand you")