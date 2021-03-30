from antlr4 import *

from MyListener import MyListener
from Myvisitor import Myvisitor
from tinycLexer import tinycLexer
from tinycParser import tinycParser

def main():
    lexer = tinycLexer(FileStream("input.c"))
    token_stream = CommonTokenStream(lexer)

    parser = tinycParser(token_stream)
    tree = parser.program()

    visitor = Myvisitor()
    visitor.visit(tree)

    # walker = ParseTreeWalker()
    # walker.walk(MyListener(),tree)

if __name__ == '__main__':
    main()