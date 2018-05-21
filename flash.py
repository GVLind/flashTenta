#!/usr/bin/python3

import pandas as pd
import os
import sys


def correct_ans(row):

    print("\ncorrect\n")
    print("comment:")
    print(row["expl"])


def incorrect_ans():

    print("\nincorrect answer\n")


def generate_question(row):

    print(row["query"])
    print("\n")
    print(row["a"])
    print(row["b"])
    print(row["c"])
    print(row["d"])

    if pd.notna(row["e"]):
        print(row["e"])

    print("")


def get_answer():

    ans = input("answer: ")
    return ans


def get_correct(row):

    corr = row["correct"]
    return corr


def wait():

    print("")
    wait = input("next..")


def query_loop(df, version):

    points = 0
    counter = 0
    col = list(df.columns.values)
    dfredo = pd.DataFrame(columns = col)

    for ind, row in df.iterrows():

        if row["incl"] == "$" and row["version"] == version:

            clear(version, points, counter)

            generate_question(row)

            corrans = get_correct(row)

            ans = get_answer()

            if ans == "s":
                continue

            if ans == "q":
                break

            if ans == "kill":
                sys.exit()

            if ans == corrans:
                correct_ans(row)
                points += 1
                counter += 1

            else:
                incorrect_ans()
                dfredo = dfredo.append(row)
                counter += 1

            wait()
        else:
            continue

    return dfredo, points, counter


def redo_loop():

    redo = input("redo missed? y/n ")
    userredo = False

    while 1 < 2:
        if redo == "n":
            print("breaking")
            break

        elif redo == "y":
            userredo = True
            break

        else:
            redo = input("redo missed? y/n ")

    return userredo


def set_version(df):

    versionlist = df["version"].dropna().unique().tolist()

    for ind, version in enumerate(versionlist):
        print (ind, version)

    userin = input("version: ")

    verindex = int(userin)

    ver = versionlist[verindex]

    return ver


def clear(version, points, counter):

    os.system("clear")
    print("%s\tpassed:%s/%s\n" % (version, points, counter))


df = pd.read_excel("../data/long.xlsx")

ver = set_version(df)

while 1 < 2:

    missedAns, points, counter = query_loop(df, ver)

    clear(ver, points, counter)

    if len(missedAns.index) == 0:
        print("all done.. \nterminating..")
        sys.exit()

    userRedo = redo_loop()

    if userRedo:
        df = missedAns

    elif userRedo:
        sys.exit()


