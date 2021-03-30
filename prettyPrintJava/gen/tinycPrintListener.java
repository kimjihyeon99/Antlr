import org.antlr.v4.runtime.ParserRuleContext;
import org.antlr.v4.runtime.tree.ErrorNode;
import org.antlr.v4.runtime.tree.ParseTreeProperty;
import org.antlr.v4.runtime.tree.TerminalNode;

public class tinycPrintListener extends tinycBaseListener{

    ParseTreeProperty<String> newTexts;

    public tinycPrintListener() {
        super();
        newTexts = new ParseTreeProperty<String>();
    }

    @Override
    public void enterProgram(tinycParser.ProgramContext ctx){
        System.out.println("\n hello, world!");
    }

    @Override
    public void exitProgram(tinycParser.ProgramContext ctx) {
        System.out.println("\n end, world!");
        System.out.println(newTexts.get(ctx.getChild(0)));
//        try (FileWriter fw = new FileWriter("Test.j");) {
//            fw.write(newTexts.get(ctx.getChild(0).getChild(0)));
//            fw.close();
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
    }

    @Override
    public void enterStatement(tinycParser.StatementContext ctx) {

    }

    @Override
    public void exitStatement(tinycParser.StatementContext ctx) {
        //여는 중괄호 시작할때 \n 처리와 스페이스파 4개 처리
        if(ctx.getChild(0).getText().equals("{")){
            // '{' statement* '}'
            String temp ="\n    "+newTexts.get(ctx.getChild(0));
            for(int i=1;i<ctx.getChildCount()-1;i++){
                temp +=newTexts.get(ctx.getChild(i));
            }
            temp+= "\n    "+ctx.getChild(ctx.getChildCount()-1).getText();
            newTexts.put(ctx, temp);
        }else{
            if(ctx.getChildCount()>4){
                if(ctx.getChild(0).getText().equals("if")){
                    //'if' paren_expr statement 'else' statement
                    String temp = ctx.getChild(0).getText()+newTexts.get(ctx.getChild(1))+
                            newTexts.get(ctx.getChild(2))+newTexts.get(ctx.getChild(3))+newTexts.get(ctx.getChild(4));
                    newTexts.put(ctx, temp);
                }else if(ctx.getChild(0).getText().equals("do")){
                    //'do' statement 'while' paren_expr ';'
                    String temp = ctx.getChild(0).getText()+" "+newTexts.get(ctx.getChild(1))+
                          "\n    "+  ctx.getChild(2).getText()+newTexts.get(ctx.getChild(3))+ctx.getChild(4).getText();
                    newTexts.put(ctx, temp);
                }
            }else if(ctx.getChildCount()>2){
                if(ctx.getChild(0).getText().equals("while")){  //'while' paren_expr statement
                    String temp = ctx.getChild(0).getText()+newTexts.get(ctx.getChild(1))+newTexts.get(ctx.getChild(2));
                    newTexts.put(ctx,temp);
                }else if(ctx.getChild(0).getText().equals("if")){//'if' paren_expr statement
                    String temp = ctx.getChild(0).getText()+newTexts.get(ctx.getChild(1))+
                            newTexts.get(ctx.getChild(2));
                    newTexts.put(ctx, temp);
                }
            }else if(ctx.getChildCount()>1){
                //expr ';'
                String str = newTexts.get(ctx.getChild(0))+newTexts.get(ctx.getChild(1));
                newTexts.put(ctx,str);
            }else{
                // ;
                String str = ctx.getChild(0).getText();
                newTexts.put(ctx,str);
            }
        }



    }

    @Override
    public void enterParen_expr(tinycParser.Paren_exprContext ctx) {

    }

    @Override
    public void exitParen_expr(tinycParser.Paren_exprContext ctx) {
        //( 시작할 때 공백 두기
        String temp =newTexts.get(ctx.getChild(0))+newTexts.get(ctx.getChild(1))+newTexts.get(ctx.getChild(2));
        newTexts.put(ctx ,temp);
    }

    @Override
    public void enterExpr(tinycParser.ExprContext ctx) {
    }

    @Override
    public void exitExpr(tinycParser.ExprContext ctx) {
        //lvalue 출력 ex) g, h
        String temp = ctx.getChild(0).getText();
        if(ctx.invokingState==51 &&ctx.getChildCount()>1){
            System.out.println("lvalue! : "+temp);
        }
        //연산자와 피연산자 띄어쓰기 처리
        if(ctx.getChildCount()>1){
            String temp2 = newTexts.get(ctx.getChild(0))+newTexts.get(ctx.getChild(1))+newTexts.get(ctx.getChild(2));
            newTexts.put(ctx,temp2);
        }else{
            String temp3 = newTexts.get(ctx.getChild(0));
            newTexts.put(ctx,temp3);
        }

    }

    @Override
    public void enterTest(tinycParser.TestContext ctx) {
    }

    @Override
    public void exitTest(tinycParser.TestContext ctx) {
        if(ctx.getChildCount()>1){
            String temp = newTexts.get(ctx.getChild(0))+newTexts.get(ctx.getChild(1))+newTexts.get(ctx.getChild(2));
            newTexts.put(ctx,temp);
        }else{
            String temp = newTexts.get(ctx.getChild(0));
            newTexts.put(ctx,temp);
        }
    }

    @Override
    public void enterSum(tinycParser.SumContext ctx) {

    }

    @Override
    public void exitSum(tinycParser.SumContext ctx) {
        if(ctx.getChildCount()>1){
            String temp = newTexts.get(ctx.getChild(0))+newTexts.get(ctx.getChild(1))+newTexts.get(ctx.getChild(2));
            newTexts.put(ctx,temp);
        }else{
            String temp = newTexts.get(ctx.getChild(0));
            newTexts.put(ctx, temp);
        }
    }

    @Override
    public void enterTerm(tinycParser.TermContext ctx) {
    }

    @Override
    public void exitTerm(tinycParser.TermContext ctx) {
        String temp = newTexts.get(ctx.getChild(0));
        newTexts.put(ctx, temp);
    }

    @Override
    public void enterId(tinycParser.IdContext ctx) {

    }

    @Override
    public void exitId(tinycParser.IdContext ctx) {
        newTexts.put(ctx, ctx.getText());
    }

    @Override
    public void enterInteger(tinycParser.IntegerContext ctx) {
    }

    @Override
    public void exitInteger(tinycParser.IntegerContext ctx) {
        newTexts.put(ctx, ctx.getText());
    }

    @Override
    public void visitTerminal(TerminalNode terminalNode) {
        if(terminalNode.getText().equals("=") || terminalNode.getText().equals("+") || terminalNode.getText().equals("-") ||
                terminalNode.getText().equals("<")){
            //연산자와 피연산자 띄어쓰기 처리
            newTexts.put(terminalNode, " "+terminalNode.getText()+" ");
        }else if(terminalNode.getText().equals("(")){
            newTexts.put(terminalNode, " "+terminalNode.getText());
        }else if(terminalNode.getText().equals("else")){
            newTexts.put(terminalNode, "\n"+terminalNode.getText());
        }else if(terminalNode.getText().equals("{")){
            newTexts.put(terminalNode, terminalNode.getText()+"\n    ");
        }else{
            newTexts.put(terminalNode, terminalNode.getText());

        }

    }

    @Override
    public void visitErrorNode(ErrorNode errorNode) {

    }

    @Override
    public void enterEveryRule(ParserRuleContext parserRuleContext) {

    }

    @Override
    public void exitEveryRule(ParserRuleContext parserRuleContext) {

    }
}
