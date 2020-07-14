#coding:utf-8
import re
if __name__ == '__main__':
    with open("source/Stream-2020-07-14-all_in_one.har", "r") as fuck_file :
        with open("stream/Stream-2020-07-14-all_in_one.har", "w") as test:
            test.write(fuck_file.read().replace('\/', '/'))