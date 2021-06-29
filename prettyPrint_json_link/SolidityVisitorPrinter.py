from MyVisitor import MyVisitor
from gen.SolidityLexer import SolidityLexer
from gen.SolidityParser import SolidityParser

from antlr4 import *

def main():
    lexer = SolidityLexer(FileStream("input.sol"))
    token_stream = CommonTokenStream(lexer)

    parser = SolidityParser(token_stream)
    tree = parser.sourceUnit()

    visitor = MyVisitor()
    visitor.visit(tree)

if __name__ == '__main__':
    main()