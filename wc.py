# _*_ coding: utf-8 _*_
import argparse
import sys

total_lines_num = 0
total_words_num = 0
total_bytes_num = 0
total_chars_num = 0
max_line_length = 0


# print the help message
def print_help():
    expected = """Usage: wc [OPTION]... [FILE]...
  or:  wc [OPTION]... --files0-from=F
Print newline, word, and byte counts for each FILE, and a total line if
more than one FILE is specified.  A word is a non-zero-length sequence of
characters delimited by white space.

With no FILE, or when FILE is -, read standard input.

The options below may be used to select which counts are printed, always in
the following order: newline, word, character, byte, maximum line length.
  -c, --bytes            print the byte counts
  -m, --chars            print the character counts
  -l, --lines            print the newline counts
      --files0-from=F    read input from the files specified by
                           NUL-terminated names in file F;
                           If F is - then read names from standard input
  -L, --max-line-length  print the maximum display width
  -w, --words            print the word counts
      --help     display this help and exit
      --version  output version information and exit

GNU coreutils online help: <http://www.gnu.org/software/coreutils/>
Full documentation at: <http://www.gnu.org/software/coreutils/wc>
or available locally via: info '(coreutils) wc invocation'"""
    return expected


# print the version message
def print_version():
    expected = """wc (GNU coreutils) 8.26
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Paul Rubin and David MacKenzie."""
    return expected


# bubble all the flags
def rearrange_args(arguments):
    result_args = []  # store all args and pass them to the function
    flag_args = []  # store flags in the args
    file_args = []  # store files in the args
    # args = sys.argv
    for a in arguments:
        if a == '-l' or a == '-w' or a == '-c' or a == '-m' or a == '-L':
            flag_args.append(a)
        else:
            file_args.append(a)
    flag_args = list(set(flag_args))
    for flag in flag_args:
        result_args.append(flag)
    for file in file_args:
        result_args.append(file)
    return result_args


# define how to print wc
def print_wc(is_l, is_w, is_c, is_m, is_L, line, word, byte, char, max_length, file_name):
    line_str = " {:>6}".format(line) if is_l else ""
    word_str = " {:>6}".format(word) if is_w else ""
    byte_str = " {:>6}".format(byte) if is_c else ""
    char_str = " {:>6}".format(char) if is_m else ""
    max_length_str = " {}".format(max_length) if is_L else ""
    file = " {}".format(file_name)
    if is_l is False and is_w is False and is_c is False and is_m is False and is_L is False:
        return " {:>6} {:>6} {:>6} {}".format(line, word, byte, file_name)
    else:
        return line_str + word_str + char_str + byte_str + max_length_str + file


# main wc program
def mini_wc(is_l, is_w, is_c, is_m, is_L, files):
    global total_lines_num, total_words_num, total_bytes_num, total_chars_num, max_line_length
    try:
        f = open(files)
        lines_num = 0
        words_num = 0
        bytes_num = 0
        chars_num = 0
        store_length = 0
        for line in f.readlines():
            lines_num += 1
            words_num += len(line.split())
            if len(line) > store_length:
                if line[-1:] == '\n':
                    store_length = len(line) - 1
                else:
                    store_length = len(line)
            for letter in line:
                bytes_num += len(letter.encode("utf8"))
                chars_num += len(letter)
        f.close()
        lines_num -= 1
        total_lines_num += lines_num
        total_words_num += words_num
        total_bytes_num += bytes_num
        total_chars_num += chars_num
        max_line_length += store_length
        return print_wc(is_l, is_w, is_c, is_m, is_L, lines_num, words_num, bytes_num, chars_num, store_length, files)
    except FileNotFoundError:
        return "No such file or directory"
    except IsADirectoryError:
        return "A directory is not allowed"


def wc(is_l, is_w, is_c, is_m, is_L, file_list):
    for file in file_list:
        if file is "-":
            while True:
                try:
                    f = open("temp.txt", "w+")
                    message = input()
                    f.write(message)
                    f.close()
                    a = list()
                    a.append("temp.txt")
                    b = wc(flag_l, flag_w, flag_c, flag_m, flag_L, a)
                    if b:
                        print(b)
                except KeyboardInterrupt:
                    sys.exit()
        else:
            print(mini_wc(is_l, is_w, is_c, is_m, is_L, file))
    is_print = True
    if len(file_list) == 1:
        is_print = False
    elif len(file_list) == 0:
        is_print = False
    if is_print:
        return print_wc(is_l, is_w, is_c, is_m, is_L, total_lines_num, total_words_num, total_bytes_num,
                        total_chars_num, max_line_length, "total")
    return None


if __name__ == '__main__':
    # bubble all the flags
    args = sys.argv
    result_list = []
    for arg in args[1:]:
        result_list.append(arg)

    p = argparse.ArgumentParser(add_help=False)
    p.add_argument('-l', action="store_true", help="print the new line counts")
    p.add_argument('-w', action="store_true", help="print the word counts")
    p.add_argument('-c', action="store_true", help="print the byte counts")
    p.add_argument('-m', action="store_true", help="print the character counts")
    p.add_argument('-L', action="store_true", help="print the maximum display width")
    p.add_argument('--files0-from', action="append",
                   help="read input from the files specified by NUL-terminated names in file F;If F is - then read names from standard input")
    p.add_argument('--help', action="store_true", help="display this help and exit")
    p.add_argument('--version', action="store_true", help="output version information and exit")
    p.add_argument('file', nargs="*")
    result = p.parse_args(rearrange_args(result_list))

    # get the output of result
    flag_l = result.l
    flag_w = result.w
    flag_c = result.c
    flag_m = result.m
    flag_L = result.L
    flag_fileFrom = result.files0_from
    flag_help = result.help
    flag_version = result.version
    file_arg = result.file

    # if --help --version exitst
    if flag_help is True or flag_version is True:
        if flag_help is True and flag_version is False:
            print(print_help())
        elif flag_help is False and flag_version is True:
            print(print_version())
        else:
            indexOfHelp = result_list.index("--help")
            indexOfVersion = result_list.index("--version")
            if indexOfHelp < indexOfVersion:
                print(print_help())
            else:
                print(print_version())
    elif flag_help is False and flag_version is False and flag_fileFrom is not None:
        if flag_fileFrom[0] == '':
            print("python3 wc.py: cannot open '' for reading: No such file or directory")
        elif flag_fileFrom[0] == '-':
            while True:
                try:
                    file_input_from_command = input()
                    a = file_input_from_command.split("\x00")
                    b = a[:len(a) - 1]
                    wc_result = wc(flag_l, flag_w, flag_c, flag_m, flag_L, b)
                    if wc_result:
                        print(wc_result)
                except KeyboardInterrupt:
                    sys.exit()
        else:
            with open(flag_fileFrom[0]) as data:
                a = data.read()
                b = a.split("\x00")
                c = b[:len(b) - 1]
                wc_result = wc(flag_l, flag_w, flag_c, flag_m, flag_L, c)
                if wc_result:
                    print(wc_result)
    else:
        if len(file_arg) == 0:
            print("No such file or directory")
        else:
            wc_result = wc(flag_l, flag_w, flag_c, flag_m, flag_L, file_arg)
            if wc_result:
                print(wc_result)
