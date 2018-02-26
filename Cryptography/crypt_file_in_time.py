from Crypto import Random
from Crypto.Cipher import AES

import glob
from time import *
import winsound


def pad(s):
    return s + b'\0' * (AES.block_size - len(s) % AES.block_size)


def encrypt(message, key):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)


def encrypt_file(file_name, key):
    with open(file_name, "rb") as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name, "wb") as fo:
        fo.write(enc)


def final_encrypt():
    file_list = glob.glob("H:\\CourseStudy\\*")
    key = 'totally died'
    for each_file in file_list:
        encrypt_file(each_file, key)
    print("Done!")


def clock_function():
    # *********************************************************************************
    # ********* comment part is used if you will never shut down your computer  *******
    # *********************************************************************************
    #difficulty = int(
    #    input("Difficulty?\nPress 1 for Easy(1 min), 2 for Hard(30 secs) and 3 for Nightmare(10 secs). >> "))
    #solve_time_list = [30, 15, 5]
    #hourprompt = input("What hour? >> ")
    #minuteprompt = input("What minute? >> ")
    #print("All right, you better be ready!")

    # *********************************************************************************
    # ******** This part is used for auto wake up setting *****************************
    # ******** So alarm is set firmly, So as difficulty   *****************************
    # *********************************************************************************
    difficulty = 1
    solve_time_list = [30, 15, 5]
    hourprompt = 7
    minuteprompt = 30

    not_executed = True
    while not_executed:
        dt = list(localtime())
        hour = dt[3]
        minute = dt[4]
        if int(hour) == int(hourprompt) and int(minute) == int(minuteprompt):
            if difficulty > 3 or difficulty < 1 or difficulty is None:
                pass
            solve_time = solve_time_list[difficulty - 1]
            computer = 0
            while computer < solve_time:
                winsound.Beep(440, 1000)
                sleep(1)
                computer += 1
            final_encrypt()
            not_executed = False


print(
    "Can not wake up? Check this out.\nEven though u cannot wake up with you alarm.\nShut the window down. Or your "
    "file will be encrypted.")
clock_function()
