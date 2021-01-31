import time

import lib.sds011

def main():
    sds = lib.sds011.SDS011("/dev/ttyUSB0")
    while True:
        print("measure:")
        print(sds.queryPM())
        time.sleep(120)


if __name__ == "__main__":
    main()
