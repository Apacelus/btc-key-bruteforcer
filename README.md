# partial-priv-btc-key-recovery

This script can bruteforce a private key with missing characters. This is rather a proof of concept, as anything above 5
characters will take a while to bruteforce. This script has only one thread, which makes it quite slow at its task.

## How to use:

1. Download the [repo](https://github.com/apacelus/partial-priv-btc-key-recovery/archive/refs/heads/main.zip) and unpack
   it.
2. Install dependencies with ```python3 -m pip install -r requirements.txt```
   or ```python -m pip install -r requirements.txt```
3. Start the scipt with ```python3 main.py``` or ```python main.py```

Ignore any "app not responding" popups from your os.

## To-do:

- [ ] GPU hashing