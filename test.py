#!/usr/bin/env python3
#########################################################################
# > File Name: test.py
# > Author: Samuel
# > Mail: enminghuang21119@gmail.com
# > Created Time: Fri Jul  1 15:59:13 2022
#########################################################################

from listen import listen
def callback():
    print("abc")
x = listen("<cmd>+c", callback)
x.start()
a = input()
x.stop()
