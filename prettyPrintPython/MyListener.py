from antlr4.tree.ParseTreeMatch import ParseTreeMatch
from antlr4.tree.ParseTreePattern import ParseTreePattern
from antlr4.tree.ParseTreePatternMatcher import ParseTreePatternMatcher
from tinycListener import tinycListener
from tinycParser import tinycParser

class MyListener(tinycListener):

    def __init__(self):
        self.ppm = ParseTreePatternMatcher
        self.pp = ParseTreePattern
        self.pm = ParseTreeMatch
        self.labels = []



    # Enter a parse tree produced by tinycParser#program.
    def enterProgram(self, ctx:tinycParser.ProgramContext):
        pass

    # Exit a parse tree produced by tinycParser#program.
    def exitProgram(self, ctx:tinycParser.ProgramContext):
        pass


    # Enter a parse tree produced by tinycParser#statement.
    def enterStatement(self, ctx:tinycParser.StatementContext):
        pass

    # Exit a parse tree produced by tinycParser#statement.
    def exitStatement(self, ctx:tinycParser.StatementContext):
        pass


    # Enter a parse tree produced by tinycParser#paren_expr.
    def enterParen_expr(self, ctx:tinycParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by tinycParser#paren_expr.
    def exitParen_expr(self, ctx:tinycParser.Paren_exprContext):
        pass


    # Enter a parse tree produced by tinycParser#expr.
    def enterExpr(self, ctx:tinycParser.ExprContext):
        pass

    # Exit a parse tree produced by tinycParser#expr.
    def exitExpr(self, ctx:tinycParser.ExprContext):
        pass


    # Enter a parse tree produced by tinycParser#test.
    def enterTest(self, ctx:tinycParser.TestContext):
        pass

    # Exit a parse tree produced by tinycParser#test.
    def exitTest(self, ctx:tinycParser.TestContext):
        pass


    # Enter a parse tree produced by tinycParser#sum.
    def enterSum(self, ctx:tinycParser.SumContext):
        pass

    # Exit a parse tree produced by tinycParser#sum.
    def exitSum(self, ctx:tinycParser.SumContext):
        pass


    # Enter a parse tree produced by tinycParser#term.
    def enterTerm(self, ctx:tinycParser.TermContext):
        pass

    # Exit a parse tree produced by tinycParser#term.
    def exitTerm(self, ctx:tinycParser.TermContext):
        pass


    # Enter a parse tree produced by tinycParser#id.
    def enterId(self, ctx:tinycParser.IdContext):
        pass

    # Exit a parse tree produced by tinycParser#id.
    def exitId(self, ctx:tinycParser.IdContext):
        pass


    # Enter a parse tree produced by tinycParser#integer.
    def enterInteger(self, ctx:tinycParser.IntegerContext):
        pass

    # Exit a parse tree produced by tinycParser#integer.
    def exitInteger(self, ctx:tinycParser.IntegerContext):
        self.ppm.map(self.labels, ctx.INT().__str__(), ctx)
        print(ctx.INT())

