import logging
import threading
import time

from time import sleep

from bitcoin import privtopub, pubtoaddr, compress
from sys import exit

logging.basicConfig(filename="bruteforce.log", level=logging.DEBUG,
                    format='%(asctime)s |%(levelname)s|\t%(message)s')
btc_chars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
             "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i",
             "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


def initialize():
    public_key = input("Enter public key \n")
    partial_key = input('Enter partial private key. Replace missing characters with "_".\n')
    partial_key = partial_key.replace(" ", "")
    logging.info("User input key: " + partial_key)
    if not len(partial_key) == 52:
        logging.info("Private key length invalid")
        print("Private key length invalid, please verify your private key")
        return
    # Calculating amount of missing chars
    missing_chars = [i for i in range(len(partial_key)) if partial_key.startswith("_", i)]
    missing_chars_amount = len(missing_chars)
    logging.info("Missing chars: " + str(missing_chars_amount))
    logging.debug("Missing chars positions: " + str(missing_chars))
    logging.info("Splitting private key")
    split_key = partial_key.split("_")
    logging.debug("Split key:" + str(split_key))
    # creating the "number"
    list_counter = []
    for i in range(missing_chars_amount):
        list_counter.append(0)
    list_counter[0] = -1
    logging.debug("Counter created " + str(list_counter))
    # Estimating time for user:
    possible_combinations = pow(58, missing_chars_amount)
    est_sec = str("%.2f" % (0.0003 * possible_combinations))
    est_hour = str("%.2f" % (0.0003 * possible_combinations / 360))
    est_years = str("%.2f" % (0.0003 * possible_combinations / 360 / 24 / 365))
    print("Missing " + str(missing_chars_amount) + " characters. Possible combinations: " + str(
        possible_combinations) + ". Estimated bruteforce time: " + est_sec + " seconds or " + est_hour + "hours or " +
          est_years + " years.")
    logging.info(
        "Estimated bruteforce time: " + est_sec + " seconds or " + est_hour + "hours or " + est_years + " years.")
    input("Press Enter to start bruteforce")
    #  threading.Thread(target=show_signs_of_life()).start()
    # Entering main loop
    while True:
        # increase counter
        if list_counter[0] == 57:
            list_counter[0] = 0
            list_counter[1] += 1
        else:
            list_counter[0] += 1
        for i in range(len(list_counter)):
            if list_counter[i] == 57:
                list_counter[i] = 0
                list_counter[i + 1] += 1
        temp_key = []
        for i in range(len(list_counter)):
            test = int(list_counter[i])
            temp_key.append(split_key[i])
            temp_key.append(btc_chars[test])
        temp_key.append(split_key[-1])
        temp_key_joined = "".join(temp_key)
        try:
            if pubtoaddr(compress(privtopub(temp_key_joined))) == public_key:
                print("KEY FOUND!!!!!!: " + temp_key_joined)
                logging.info("Key found: " + temp_key_joined)
                with open("key.txt", "w") as f:
                    f.write(temp_key_joined)
                exit()
            else:
                logging.warning("Wrong key: " + temp_key_joined)
        except AssertionError:
            logging.debug("Key invalid: " + temp_key_joined)


def show_signs_of_life():
    print("Starting bruteforce")
    while True:
        print("Still bruteforcing...")
        sleep(10)


initialize()
