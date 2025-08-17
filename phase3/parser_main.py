import sys, os
from lexer import initLexer
from parser import Parser

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parser_main.py <source_file.rsc>")
        sys.exit(1)

    src = sys.argv[1]
    if not initLexer(src):
        print(f"Failed to open file: {src}")
        sys.exit(1)

    base, _ = os.path.splitext(src)
    outname = base + '.rsp'

    parser = Parser()

    old_stdout = sys.stdout
    outf = open(outname, 'w')
    try:
        sys.stdout = outf
        parser.parse_Program()
    finally:
        sys.stdout = old_stdout
        outf.close()

    print(f"Output file: {outname}")

if __name__ == "__main__":
    main()
