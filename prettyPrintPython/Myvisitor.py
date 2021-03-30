from tinycVisitor import tinycVisitor
from tinycParser import tinycParser

class Myvisitor(tinycVisitor):

    def __init__(self):
        self

    # Visit a parse tree produced by tinycParser#program.
    def visitProgram(self, ctx:tinycParser.ProgramContext):
        print(self.visitChildren(ctx))
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tinycParser#statement.
    def visitStatement(self, ctx:tinycParser.StatementContext):
        if ctx.getChild(0).getText() =="{":
            result="" #statement 정보 저장
            sp = "" #depth마다 들여쓰기 개수 차이를 두기 위함
            if ctx.parentCtx.invokingState != 18 :
                sp+="    "
            for i in range(0, ctx.getChildCount()-2):
                result += "    "+sp+ self.visitStatement(ctx.statement(i))
            #출력문 저장
            str = sp+ctx.getChild(0).getText()+"\n"+result+sp+"\n"+sp+ctx.getChild(ctx.getChildCount()-1).getText()
            return str
        else:
            if ctx.getChildCount()>4:
                #'if' paren_expr statement 'else' statement
                if ctx.getChild(0).getText() == "if":
                    str = ctx.getChild(0).getText()+self.visitParen_expr(ctx.paren_expr())+"\n"+self.visitStatement(ctx.statement(0))+"\n"+ctx.getChild(3).getText()+"\n"+self.visitStatement(ctx.statement(1))
                    return str
                #'do' statement 'while' paren_expr ';'
                elif ctx.getChild(0).getText() == "while":
                    str = ctx.getChild(0).getText()+self.visitStatement(ctx.statement(0))+"\n"+ctx.getChild(2).getText()+self.visitParen_expr(ctx.paren_expr())+ctx.getChild(4).getText()
                    return str
            elif ctx.getChildCount()>2:
                #'while' paren_expr statement
                if ctx.getChild(0).getText() =="while":
                    str = ctx.getChild(0).getText()+self.visitParen_expr(ctx.paren_expr())+"\n"+self.visitStatement(ctx.statement(0))
                    return str
                #'if' paren_expr statement
                elif ctx.getChild(0).getText() =="if":
                    str = ctx.getChild(0).getText()+self.visitParen_expr(ctx.paren_expr())+"\n"+self.visitStatement(ctx.statement(0))
                    return str
            elif ctx.getChildCount()>1:
                #expr ';'
                str = self.visitExpr(ctx.expr())+ctx.getChild(1).getText()
                return str
            else:
                return ctx.getChild(0).getText()

        return self.visitChildren()



    # Visit a parse tree produced by tinycParser#paren_expr.
    def visitParen_expr(self, ctx:tinycParser.Paren_exprContext):
        # ( 시작할때 띄어쓰기 처리
        str = " "+ctx.getChild(0).getText() + self.visitExpr(ctx.expr()) + ctx.getChild(2).getText()
        return str


    # Visit a parse tree produced by tinycParser#expr.
    def visitExpr(self, ctx:tinycParser.ExprContext):
        if ctx.getChildCount()>1:
            # '=' 연산자와 피연산자 사이 띄어쓰기 처리
            str = self.visitId(ctx.id())+" "+ctx.getChild(1).getText()+" "+self.visitExpr(ctx.expr())
            return str
        else:
            return self.visitTest(ctx.test())

    # Visit a parse tree produced by tinycParser#test.
    def visitTest(self, ctx:tinycParser.TestContext):
        if ctx.getChildCount()>1:
            #연산자와 피연산자 사이 띄어쓰기 처리
            str = self.visitSum(ctx.sum(0))+" "+ctx.getChild(1).getText()+" "+self.visitSum(ctx.sum(1))
            return str
        else:
            return self.visitChildren(ctx)

    # Visit a parse tree produced by tinycParser#sum.
    def visitSum(self, ctx:tinycParser.SumContext):
        if ctx.getChildCount()>1:
            #연산자와 피연산자 사이 띄어쓰기 처리
            str = self.visitSum(ctx.sum())+" "+ctx.getChild(1).getText()+" "+self.visitTerm(ctx.term())
            return str
        else:
            str =self.visitTerm(ctx.term())
            return str

    # Visit a parse tree produced by tinycParser#term.
    def visitTerm(self, ctx:tinycParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by tinycParser#id.
    def visitId(self, ctx:tinycParser.IdContext):
        str = ctx.getText()
        return str


    # Visit a parse tree produced by tinycParser#integer.
    def visitInteger(self, ctx:tinycParser.IntegerContext):
        t = ctx.getText()
        return t