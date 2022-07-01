import logging
import hashlib
import base58
import codecs
import ecdsa
import ripemd160

logging.basicConfig(filename="priv-key.log", level=logging.DEBUG,
                    format='%(asctime)s |%(levelname)s|\t%(message)s')

btc_chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
             "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" "A", "B", "C", "D",
             "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
             "Y", "Z"]


def initialize():
    partial_key = input('Enter partial private key. Replace missing characters with "_" ')
    logging.info("Using private key: " + partial_key)
    generate_keys(partial_key)


def generate_keys(partial_key):
    logging.info("Generating private keys")
    print("Generating keys: Dont close the app!")

    with open("priv_keys.txt", "w") as f:
        f.write("test")


# Credit: Michael K @medium.com
# Original file:
# https://medium.com/@kootsZhin/step-by-step-guide-to-getting-bitcoin-address-from-private-key-in-python-7ec15072b71b
# Below is a shortened and modified version(to use python implementation of ripemd) of the original file. Not intended
# to be human-readable, see original file for explanation.
def calculate_public_key(private_key):
    public_key_bytes = ecdsa.SigningKey.from_string(codecs.decode(private_key, 'hex'),
                                                    curve=ecdsa.SECP256k1).verifying_key.to_string()
    public_key = (b'04' + codecs.encode(public_key_bytes, 'hex')).decode("utf-8")
    if ord(bytearray.fromhex(public_key[-2:])) % 2 == 0:
        public_key_compressed = '02'
    else:
        public_key_compressed = '03'
    public_key_compressed += public_key[2:66]
    hex_str = bytearray.fromhex(public_key_compressed)
    sha = hashlib.sha256()
    sha.update(hex_str)
    ripemd160.ripemd160(sha.digest())
    modified_key_hash = "00" + ripemd160.ripemd160(sha.digest()).hex()
    sha = hashlib.sha256()
    hex_str = bytearray.fromhex(modified_key_hash)
    sha.update(hex_str)
    sha_2 = hashlib.sha256()
    sha_2.update(sha.digest())
    byte_25_address = modified_key_hash + sha_2.hexdigest()[:8]
    return base58.b58encode(bytes(bytearray.fromhex(byte_25_address))).decode('utf-8')
