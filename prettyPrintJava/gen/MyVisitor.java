//여는 중괄호 시작할때 \n 처리와 스페이스파 4개 처리


public class MyVisitor extends tinycBaseVisitor<Object> {

    public MyVisitor() {

    }

    @Override public Object visitProgram(tinycParser.ProgramContext ctx) {
        Object result = visitChildren(ctx);
        System.out.println(result);
        return result;
    }
    /**
     * {@inheritDoc}
     *
     * <p>The default implementation returns the result of calling
     * {@link #visitChildren} on {@code ctx}.</p>
     */
    @Override public Object visitStatement(tinycParser.StatementContext ctx) {

        if(ctx.getChild(0).getText().equals("{")){
            //'{' statement* '}'
            ////여는 중괄호 시작할때 \n 처리와 스페이스파 4개 처리
            System.out.println(ctx.parent.parent.getRuleIndex());

            if(ctx.parent.parent.getRuleIndex() ==0){
                Object temp ="\n";
                for(int i=0;i<ctx.getChildCount()-2;i++){
                    Object result = visitStatement(ctx.statement(i));
                    temp +=ctx.getChild(0).getText()+"\n    "+result +"\n"+ctx.getChild(2).getText();
                }
                return temp;
            }else{
                Object temp ="\n";
                int cnt = ctx.parent.parent.getRuleIndex();
                Object sp ="";
                for(int i=0;i<cnt;i++){
                   sp+="    ";
                }
                for(int i=0;i<ctx.getChildCount()-2;i++){
                    Object result = visitStatement(ctx.statement(i));
                    temp +=sp+ctx.getChild(0).getText()+"\n    "+sp+result +"\n"+sp+ctx.getChild(2).getText();

                }
                return temp;
            }

        }else{
            if(ctx.getChildCount()>4){
                //'if' paren_expr statement 'else' statement
                if(ctx.getChild(0).getText().equals("if")){
                    Object str = ctx.getChild(0).getText()+visitParen_expr(ctx.paren_expr())+visitStatement(ctx.statement(0))+
                           "\n"+ ctx.getChild(3).getText()+visitStatement(ctx.statement(1));
                    return str;
                }//'do' statement 'while' paren_expr ';'
                else if(ctx.getChild(0).getText().equals("do")){
                    Object str = ctx.getChild(0).getText()+visitStatement(ctx.statement(0))+ctx.getChild(2).getText()+ visitParen_expr(ctx.paren_expr())+ctx.getChild(4).getText();
                    return str;
                }
            }else if(ctx.getChildCount()>2){
                //'while' paren_expr statement
                if(ctx.getChild(0).getText().equals("while")){
                    Object str = ctx.getChild(0).getText()+visitParen_expr(ctx.paren_expr())+visitStatement(ctx.statement(0));
                    return str;
                }//'if' paren_expr statement
                else if(ctx.getChild(0).getText().equals("if")){
                    Object str = ctx.getChild(0).getText()+visitParen_expr(ctx.paren_expr())+visitStatement(ctx.statement(0));
                    return str;
                }
            }else if(ctx.getChildCount()>1){
                //expr ';'
                Object str = visitExpr(ctx.expr())+ctx.getChild(1).getText();
                return str;
            }else{
                return ctx.getChild(0).getText();
            }
        }


        return visitChildren(ctx);
    }
    /**
     * {@inheritDoc}
     *
     * <p>The default implementation returns the result of calling
     * {@link #visitChildren} on {@code ctx}.</p>
     */
    @Override public Object visitParen_expr(tinycParser.Paren_exprContext ctx) {
        //( 시작할 때 공백 두기
        Object str =" "+ ctx.getChild(0).getText()+visitExpr(ctx.expr())+ctx.getChild(2).getText();
        return str;
    }
    /**
     * {@inheritDoc}
     *
     * <p>The default implementation returns the result of calling
     * {@link #visitChildren} on {@code ctx}.</p>
     */
    @Override public Object visitExpr(tinycParser.ExprContext ctx) {
        //lvalue 출력 ex) g, h
        if(ctx.getChildCount() >1){
            String temp = ctx.id().getText();
            System.out.println("lvalue : "+ temp);

            Object str = visitId(ctx.id())+" "+ctx.getChild(1).getText()+" "+visitExpr(ctx.expr());
            return str;
        }else{
            return visitTest(ctx.test());
        }

    }
    /**
     * {@inheritDoc}
     *
     * <p>The default implementation returns the result of calling
     * {@link #visitChildren} on {@code ctx}.</p>
     */
    @Override public Object visitTest(tinycParser.TestContext ctx) {
        //연산자와 피연산자 띄어쓰기 처리
        if(ctx.getChildCount()>1) {
            Object res = visitSum(ctx.sum(0))+" "+ctx.getChild(1).getText()+" "+visitSum(ctx.sum(1));
            return res;
        }else{
            return visitChildren(ctx);
        }
    }
    /**
     * {@inheritDoc}
     *
     * <p>The default implementation returns the result of calling
     * {@link #visitChildren} on {@code ctx}.</p>
     */
    @Override public Object visitSum(tinycParser.SumContext ctx) {
        //연산자와 피연산자 띄어쓰기 처리

        if(ctx.getChildCount()>1){
            Object str = visitSum(ctx.sum()) +" "+ ctx.getChild(1).getText()+" "+ visitTerm(ctx.term());
            return str;
        }else{
           Object str = visitTerm(ctx.term());
           return str;
        }

    }
    /**
     * {@inheritDoc}
     *
     * <p>The default implementation returns the result of calling
     * {@link #visitChildren} on {@code ctx}.</p>
     */
    @Override public Object visitTerm(tinycParser.TermContext ctx) {
       return visitChildren(ctx);
    }
    /**
     * {@inheritDoc}
     *
     * <p>The default implementation returns the result of calling
     * {@link #visitChildren} on {@code ctx}.</p>
     */
    @Override public Object visitId(tinycParser.IdContext ctx) {
        Object str = ctx.getChild(0).getText();
        return str;
    }
    /**
     * {@inheritDoc}
     *
     * <p>The default implementation returns the result of calling
     * {@link #visitChildren} on {@code ctx}.</p>
     */
    @Override public Object visitInteger(tinycParser.IntegerContext ctx) {
        Object temp = ctx.getChild(0).getText();
        return temp;
    }

}
