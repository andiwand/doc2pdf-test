import logging
import argparse
import os
import shutil
import time
import errno

POLLING_INERVAL = 0.1

RESULT_OK = 0
RESULT_WARNING = 1
RESULT_CRITICAL = 2
RESULT_UNKNOWN = 3

def replaceextension(path, new_extension):
    return path.rsplit(".", 1)[0] + "." + new_extension

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def touch(path, times=None):
    with open(path, "a"):
        os.utime(path, times)

def silentremove(filename):
    try:
        os.remove(filename)
        return True
    except:
        return False

def waitpoll():
    time.sleep(POLLING_INERVAL)

def main():
    parser = argparse.ArgumentParser(description="test script for doc2pdf")
    parser.add_argument("-t", "--timeout", default="10", help="seconds to wait for the pdf")
    parser.add_argument("-s", "--src", help="path to the file to copy")
    parser.add_argument("-d", "--debug", action="store_true", help="activate debug messages")
    parser.add_argument("dst", help="path to the file to create")
    args = parser.parse_args()
    
    level = logging.DEBUG if args.debug else logging.CRITICAL
    pdf_file = replaceextension(args.dst, "pdf")
    timeout = int(args.timeout)
    
    logging.basicConfig(level=level, format="%(asctime)s %(message)s")  # TODO: outsource
    
    logging.info("starting doc2pdf tester...")
    logging.debug("validate arguments")
    if args.src and not os.path.isfile(args.src):
        logging.error("src file does not exist")
        print("src file does not exist")
        return RESULT_UNKNOWN
    if not is_int(args.timeout):
        logging.error("timeout is not a number")
        print("timeout is not a number")
        return RESULT_UNKNOWN
    
    logging.info("remove pdf if exists %s" % pdf_file);
    silentremove(pdf_file)
    
    logging.info("create test file %s" % args.dst);
    if args.src:
        logging.info("copying from %s" % args.src)
        shutil.copyfile(args.src, args.dst)
    else:
        touch(args.dst)
    
    logging.info("checking for pdf file");
    
    start = time.time()
    while True:
        if os.path.isfile(pdf_file): break
        if (time.time() - start) > timeout: break
        waitpoll()
    
    result = os.path.isfile(pdf_file)
    if result:
        logging.info("pdf found")
        print("pdf found")
    else:
        logging.error("pdf not found")
        print("pdf not found")
    
    logging.info("clear files");
    # TODO: timeout and outsource
    if result:
        while not silentremove(pdf_file): waitpoll()
    while not silentremove(args.dst): waitpoll()
    
    logging.info("exit");
    if not result: return RESULT_CRITICAL
    return RESULT_OK

if __name__ == "__main__":
    main()
