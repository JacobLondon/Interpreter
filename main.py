import sys

from parse import Lexer, Parser

def main():
    """filename = ''
    try:
        filename = sys.argv[1]
    except Exception as e:
        print(e)"""

    while True:
        lexer = Lexer(text=input('>>> '))
        parser = Parser(lexer)
        print(parser.read())

if __name__ == '__main__':
    main()