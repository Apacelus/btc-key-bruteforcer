import logging
import threading

from math import floor
from bitcoin import privtopub, pubtoaddr, compress
from sys import exit
from time import sleep, time
from random import randint

logging.basicConfig(filename="bruteforce.log", level=logging.DEBUG,
                    format='%(asctime)s |%(levelname)s|\t%(message)s')
btc_chars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
             "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i",
             "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
exit_main_thread = False


def from_top():
    global completed_calculations
    penis = 1
    while True:
        # increase counter
        if list_counter_from_top[0] == 57:
            list_counter_from_top[0] = 0
            list_counter_from_top[1] += 1
        else:
            list_counter_from_top[0] += 1
        for i in range(len(list_counter_from_top)):
            if list_counter_from_top[i] == 57:
                list_counter_from_top[i] = 0
                list_counter_from_top[i + 1] += 1
        temp_key = []
        for i in range(len(list_counter_from_top)):
            temp_key.append(split_key[i])
            temp_key.append(btc_chars[int(list_counter_from_top[i])])
        temp_key.append(split_key[-1])
        temp_key_joined = "".join(temp_key)
        try:
            if pubtoaddr(compress(privtopub(temp_key_joined))) == public_key:
                save_key(temp_key_joined)
            else:
                logging.warning("Wrong key: " + temp_key_joined)
        except AssertionError:
            logging.debug("Key invalid: " + temp_key_joined)
        completed_calculations += 1


def from_bottom():
    global completed_calculations
    while True:
        # increase counter
        if list_counter_from_bottom[0] == 0:
            list_counter_from_bottom[0] = 57
            list_counter_from_bottom[1] -= 1
        else:
            list_counter_from_bottom[0] -= 1
        for i in range(len(list_counter_from_bottom)):
            if list_counter_from_bottom[i] == 0:
                list_counter_from_bottom[i] = 57
                list_counter_from_bottom[i + 1] -= 1
        temp_key = []
        for i in range(len(list_counter_from_bottom)):
            temp_key.append(split_key[i])
            temp_key.append(btc_chars[int(list_counter_from_bottom[i])])
        temp_key.append(split_key[-1])
        temp_key_joined = "".join(temp_key)
        try:
            if pubtoaddr(compress(privtopub(temp_key_joined))) == public_key:
                save_key(temp_key_joined)
            else:
                logging.warning("Wrong key: " + temp_key_joined)
        except AssertionError:
            logging.debug("Key invalid: " + temp_key_joined)
        completed_calculations += 1


def random_search():
    while True:
        temp_key = []
        for i in range(len(list_counter_from_bottom)):
            temp_key.append(btc_chars[randint(0, 57)])
        temp_key.append(split_key[-1])
        temp_key_joined = "".join(temp_key)
        try:
            if pubtoaddr(compress(privtopub(temp_key_joined))) == public_key:
                save_key(temp_key_joined)
            else:
                logging.warning("Wrong key: " + temp_key_joined)
        except AssertionError:
            logging.debug("Key invalid: " + temp_key_joined)


def save_key(priv_key):
    total_time = time() - starting_time
    print("KEY FOUND!!!!!!: " + priv_key)
    logging.info("Key found: " + priv_key)
    with open("key.txt", "w") as f:
        f.write(priv_key)
    print("Bruteforce completed in " + str("%.2f" % total_time))
    global exit_main_thread
    exit_main_thread = True
    exit()


if __name__ == "__main__":
    public_key = input("Enter public key \n")
    partial_key = input('Enter partial private key. Replace missing characters with "_".\n')
    partial_key = partial_key.replace(" ", "")
    logging.info("User input key: " + partial_key)
    if not len(partial_key) == 52:
        logging.info("Private key length invalid")
        print("Private key length invalid, please verify your private key")
        exit()
    # Calculating amount of missing chars
    missing_chars = [i for i in range(len(partial_key)) if partial_key.startswith("_", i)]
    missing_chars_amount = len(missing_chars)
    logging.info("Missing chars: " + str(missing_chars_amount))
    logging.debug("Missing chars positions: " + str(missing_chars))
    logging.info("Splitting private key")
    split_key = partial_key.split("_")
    logging.debug("Split key:" + str(split_key))
    # creating the top "number"
    list_counter_from_top = []
    for i in range(missing_chars_amount):
        list_counter_from_top.append(0)
    list_counter_from_top[0] = -1
    # creating the bottom "number"
    list_counter_from_bottom = []
    for i in range(missing_chars_amount):
        list_counter_from_bottom.append(57)
    list_counter_from_bottom[0] = 58
    logging.debug("Counter created " + str(list_counter_from_top))
    # Estimating time for user:
    possible_combinations = pow(58, missing_chars_amount)
    est_sec = str("%.2f" % (0.0003 * possible_combinations / 2))
    est_hour = str("%.2f" % (0.0003 * possible_combinations / 720))
    est_years = str("%.2f" % (0.0003 * possible_combinations / 360 / 24 / 365 / 2))
    print("Missing " + str(missing_chars_amount) + " characters. Possible combinations: " + str(
        possible_combinations) + ". Estimated bruteforce time: " + est_sec + " seconds or " + est_hour + "hours or " +
          est_years + " years.")
    logging.info(
        "Estimated bruteforce time: " + est_sec + " seconds or " + est_hour + "hours or " + est_years + " years.")
    input("Press Enter to start bruteforce")
    print("Starting bruteforce...")
    completed_calculations = 0
    starting_time = time()
    threading.Thread(target=from_top, daemon=True).start()
    threading.Thread(target=from_bottom, daemon=True).start()
    threading.Thread(target=random_search, daemon=True).start()
    # Progress bar calculations
    amount_per_percent = floor(possible_combinations / 100)
    logging.debug("amount per percent: " + str(amount_per_percent))
    old_percent = 0
    percent_bar_as_list = [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
                           ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
                           ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
                           ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
                           ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".",
                           ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
    while True:
        percentage_of_done = floor(completed_calculations / amount_per_percent)
        if exit_main_thread:
            print("Exiting")
            exit()
        if percentage_of_done > old_percent:
            old_percent = percentage_of_done
            for i in range(percentage_of_done):
                percent_bar_as_list[i] = "#"
            print("[" + "".join(percent_bar_as_list) + "]" + str(percentage_of_done) + "%")
        sleep(0.2)