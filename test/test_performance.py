import sys
sys.path.insert(0, "../code")
from keyCount import start

if __name__ == '__main__':
    for i in range(10000):
        start(filepath='../data/key.c', level_type=4)

