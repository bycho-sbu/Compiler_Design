import sys
from lexer import initLexer
from parser import Parser

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parser_main.py <source_file>")
        sys.exit(1)

    src = sys.argv[1]
    # Initialize lexer on the given file
    if not initLexer(src):
        print(f"Failed to open file: {src}")
        sys.exit(1)

    # Run parser and trace
    parser = Parser()
    parser.parse_Program()

    # after parsing -> emit segments and write output
    out_file = src.rsplit('.', 1)[0] + '.rso'
    parser.IR.write(out_file)
    print(f"Generated IR in {out_file}")

if __name__ == "__main__":
    main()
