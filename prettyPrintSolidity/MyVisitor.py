from gen.SolidityVisitor import SolidityVisitor
from gen.SolidityParser import SolidityParser

class MyVisitor(SolidityVisitor):

    def __init__(self):
        self

    # Visit a parse tree produced by SolidityParser#sourceUnit.
    def visitSourceUnit(self, ctx:SolidityParser.SourceUnitContext):
        cd = ""
        if ctx.getChildCount()>2:
            for i in range (1,ctx.getChildCount()-1):
                cd += self.visitContractDefinition(ctx.getChild(i))
            str = self.visitPragmaDirective(ctx.getChild(0)) + cd
        else:
            str = self.visitPragmaDirective(ctx.getChild(0))

        print(str)
        return str


    # Visit a parse tree produced by SolidityParser#pragmaDirective.
    def visitPragmaDirective(self, ctx:SolidityParser.PragmaDirectiveContext):
        str = ctx.getChild(0).__str__()+" "+ self.visitVersionPragma(ctx.pragma())+ctx.getChild(2).__str__()+"\n"
        return str


    # Visit a parse tree produced by SolidityParser#VersionPragma.
    def visitVersionPragma(self, ctx:SolidityParser.VersionPragmaContext):
        str = ctx.getChild(0).__str__()+" "+self.visitVersion(ctx.version())
        return str


    # Visit a parse tree produced by SolidityParser#version.
    def visitVersion(self, ctx:SolidityParser.VersionContext):
        #versionConstraint versionConstraint?
        str= self.visitVersionConstraint(ctx.versionConstraint(0))
        if ctx.getChildCount()>1:
            str+= self.visitVersionConstraint(ctx.versionConstraint(1))
        return str

    # Visit a parse tree produced by SolidityParser#versionOperator.
    def visitVersionOperator(self, ctx:SolidityParser.VersionOperatorContext):
        #  '^' | '~' | '>=' | '>' | '<' | '<=' | '='
        str =ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#versionConstraint.
    def visitVersionConstraint(self, ctx:SolidityParser.VersionConstraintContext):
        # versionOperator VersionLiteral
        if ctx.getChildCount()>1:
            str = self.visitVersionOperator(ctx.versionOperator())+ ctx.getChild(1).__str__()
        #  VersionLiteral
        else:
            str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#contractDefinition.
    def visitContractDefinition(self, ctx:SolidityParser.ContractDefinitionContext):
        cp = ""
        str = ctx.getChild(0).__str__()+ " "+self.visitIdentifier(ctx.identifier())+" "+ctx.getChild(2).__str__()+"\n"
        for i in range (0, ctx.getChildCount()-4):
            cp += "    "+self.visitContractPart(ctx.contractPart(i))+"\n"
        str +=  cp+ctx.getChild(ctx.getChildCount()-1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#contractPart.
    def visitContractPart(self, ctx:SolidityParser.ContractPartContext):
        # 아래로 내려가기만 함
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#stateVariableDeclaration.
    def visitStateVariableDeclaration(self, ctx:SolidityParser.StateVariableDeclarationContext):
        # ( keywords+=FinalKeyword )* annotated_type=annotatedTypeName
        # ( keywords+=ConstantKeyword )*
        # idf=identifier ('=' expr=expression)? ';'
        str=""
        if ctx.getChildCount()>6:
            #고민중
            print("ddd")
        # annotated_type=annotatedTypeName ( keywords+=ConstantKeyword ) idf=identifier ('=' expr=expression) ';'
        # ( keywords+=FinalKeyword ) annotated_type=annotatedTypeName idf=identifier ('=' expr=expression) ';'
        elif ctx.getChildCount()>5:
            if ctx.annotatedTypeName().__eq__(ctx.getChild(0)):
                str += self.visitAnnotatedTypeName(ctx.annotatedTypeName())+ctx.getChild(1).__str__()
            else:
                str += ctx.getChild(0).__str__()+self.visitAnnotatedTypeName(ctx.annotatedTypeName())
            str+= self.visitIdentifier(ctx.identifier())+ctx.getChild(3).__str__()+self.visit(ctx.expression())
        #annotated_type=annotatedTypeName idf=identifier ('=' expr=expression) ';'
        elif ctx.getChildCount()>4:
            str += self.visitAnnotatedTypeName(ctx.annotatedTypeName())+self.visitIdentifier(ctx.identifier())+ctx.getChild(2).__str__()+self.visit(ctx.expression())+ctx.getChild(4).__str__()
        #annotated_type=annotatedTypeName idf=identifier ';'
        else:
            str+= self.visitAnnotatedTypeName(ctx.annotatedTypeName())+" "+self.visitIdentifier(ctx.identifier())+ctx.getChild(2).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#constructorDefinition.
    def visitConstructorDefinition(self, ctx:SolidityParser.ConstructorDefinitionContext):
        str = ctx.getChild(0).__str__() + self.visitParameterList(ctx.parameterList()) + self.visitModifierList(ctx.modifierList())+ self.visitBlock(ctx.block())
        return str


    # Visit a parse tree produced by SolidityParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:SolidityParser.FunctionDefinitionContext):
        #'function' idf=identifier parameters=parameterList modifiers=modifierList return_parameters=returnParameters? body=block
        str = ctx.getChild(0).__str__()+" "+ self.visitIdentifier(ctx.identifier())+ self.visitParameterList(ctx.parameterList())+self.visitModifierList(ctx.modifierList())
        if ctx.getChildCount()>5:
            str +=" "+self.visitReturnParameters(ctx.returnParameters())+ self.visitBlock(ctx.block())
        #'function' idf=identifier parameters=parameterList modifiers=modifierList body=block
        else:
            str +=self.visitBlock(ctx.block())
        return str


    # Visit a parse tree produced by SolidityParser#returnParameters.
    def visitReturnParameters(self, ctx:SolidityParser.ReturnParametersContext):
        str = ctx.getChild(0).__str__() +" " + self.visitParameterList(ctx.parameterList())
        return str


    # Visit a parse tree produced by SolidityParser#modifierList.
    def visitModifierList(self, ctx:SolidityParser.ModifierListContext):
        str = ""
        for i in range (0, ctx.getChildCount()):
            str += self.visitModifier()
        return str


    # Visit a parse tree produced by SolidityParser#modifier.
    def visitModifier(self, ctx:SolidityParser.ModifierContext):
        #바로 아래로 내려보내기
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#parameterList.
    def visitParameterList(self, ctx:SolidityParser.ParameterListContext):
        # '(' ( params+=parameter (',' params+=parameter)* )? ')'
        str = ctx.getChild(0).__str__()
        #'(' ( params+=parameter (',' params+=parameter)* ) ')'
        if ctx.getChildCount()>3:
            str += self.visitParameter(ctx.parameter(0))
            pr = ""
            for i in range (2, ctx.getChildCount()-1,2):
                pr+= ctx.getChild(i).__str__()+ self.visitParameter(ctx.getChild(i+1))
            str += pr +ctx.getChild(ctx.getChildCount()-1).__str__()
        #'(' ( params+=parameter ) ')'
        elif ctx.getChildCount()>2:
            str += self.visitParameter(ctx.parameter(0))+ctx.getChild(2).__str__()
        # '(' ')'
        else :
            str +=ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#parameter.
    def visitParameter(self, ctx:SolidityParser.ParameterContext):
        if ctx.annotatedTypeName().__eq__(ctx.getChild(0)):
            #annotated_type=annotatedTypeName idf=identifier?
            str = self.visitAnnotatedTypeName(ctx.annotatedTypeName())
            if ctx.getChildCount()>1:
                str += " "+self.visitIdentifier(ctx.identifier())
        else:
            #(keywords+=FinalKeyword) annotated_type=annotatedTypeName idf=identifier?
            str = ctx.FinalKeyword().__str__()+ self.visitAnnotatedTypeName(ctx.annotatedTypeName())
            if ctx.getChildCount()>2:
                str+=self.visitIdentifier(ctx.identifier())
        return str


    # Visit a parse tree produced by SolidityParser#enumValue.
    def visitEnumValue(self, ctx:SolidityParser.EnumValueContext):
        str = self.visitIdentifier(ctx.identifier())
        return str


    # Visit a parse tree produced by SolidityParser#enumDefinition.
    def visitEnumDefinition(self, ctx:SolidityParser.EnumDefinitionContext):
        #'enum' idf=identifier '{' values+=enumValue? (',' values+=enumValue)* '}'
        str = ctx.getChild(0).__str__()+" "+ self.visitIdentifier(ctx.identifier())+" "+ ctx.getChild(2).__str__()+" "
        if ctx.getChildCount()>4:
            ev = ""
            for i in range (3, ctx.getChildCount()-1):
                if(ctx.getChild(i).__str__().__eq__(",")):
                    ev += ctx.getChild(i).__str__()+" "
                else:
                    ev += self.visit(ctx.getChild(i))
            str+= ev+" "+ctx.getChild(ctx.getChildCount()-1).__str__();
        #'enum' idf=identifier '{' '}'
        else:
            str+= " "+ctx.getChild(3).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:SolidityParser.VariableDeclarationContext):
        # (keywords+=FinalKeyword) annotated_type=annotatedTypeName idf=identifier
        if ctx.getChildCount()>2:
            str = ctx.getChild(0).__str__()+" "+self.visitAnnotatedTypeName(ctx.annotatedTypeName())+" "+self.visitIdentifier(ctx.identifier())
        # annotated_type=annotatedTypeName idf=identifier
        else:
            str = self.visitAnnotatedTypeName(ctx.annotatedTypeName())+" "+self.visitIdentifier(ctx.identifier())
        return str


    # Visit a parse tree produced by SolidityParser#typeName.
    def visitTypeName(self, ctx:SolidityParser.TypeNameContext):
        #바로 아래로 보내기
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#userDefinedTypeName.
    def visitUserDefinedTypeName(self, ctx:SolidityParser.UserDefinedTypeNameContext):
        #names+=identifier ( '.' names+=identifier )*
        str = self.visitIdentifier(ctx.identifier(0))
        dt = ""
        for i in range(1,ctx.getChildCount(),2):
            dt+= ctx.getChild(i)+self.visitIdentifier(ctx.getChild(i+1))
        str+= dt
        return str


    # Visit a parse tree produced by SolidityParser#mapping.
    def visitMapping(self, ctx:SolidityParser.MappingContext):
        #'mapping' '(' key_type=elementaryTypeName ( '!' key_label=identifier )? '=>' value_type=annotatedTypeName ')'
        str = ctx.getChild(0).__str__()+ctx.getChild(1).__str__()+self.visitElementaryTypeName(ctx.elementaryTypeName())
        if ctx.getChildCount()>6:
            str+= ctx.getChild(3).__str__()+self.visitIdentifier(ctx.identifier())+ctx.getChild(5).__str__()+self.visitAnnotatedTypeName(ctx.annotatedTypeName())+ctx.getChild(7).__str__()
        #'mapping' '(' key_type=elementaryTypeName '=>' value_type=annotatedTypeName ')'
        else :
            str+= ctx.getChild(3).__str__()+self.visitAnnotatedTypeName(ctx.annotatedTypeName())+ctx.getChild(5).__str__()
        return str

    # Visit a parse tree produced by SolidityParser#stateMutability.
    def visitStateMutability(self, ctx:SolidityParser.StateMutabilityContext):
        #문자열 출력하기
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#block.
    def visitBlock(self, ctx:SolidityParser.BlockContext):
        # '{' statements+=statement* '}'
        st = ""
        sp = "" #들여쓰기를 의한것
        sp2 = "    " # statement 들여쓰기를 위한것
        i= int(len(ctx.parentCtx.__str__()) / 12)
        for i in range(0,i):
            sp+="    "

        str = " "+ctx.getChild(0).__str__() +"\n"
        for i in range (1, ctx.getChildCount()-1):
            st += sp+sp2+self.visitStatement(ctx.getChild(i))+"\n"
        str +=st+ sp+ctx.getChild(ctx.getChildCount()-1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#statement.
    def visitStatement(self, ctx:SolidityParser.StatementContext):
        #바로 아래로 내려보내기
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#expressionStatement.
    def visitExpressionStatement(self, ctx:SolidityParser.ExpressionStatementContext):
        #expr=expression ';'
        str = self.visit(ctx.expression()) + ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#ifStatement.
    def visitIfStatement(self, ctx:SolidityParser.IfStatementContext):
        #'if' '(' condition=expression ')' then_branch=statement
        str = ctx.getChild(0).__str__() +ctx.getChild(1).__str__()+ self.visit(ctx.expression())+ctx.getChild(3).__str__()+ self.visitStatement(ctx.statement(0))
        if ctx.getChildCount()>6:
            #'if' '(' condition=expression ')' then_branch=statement ( 'else' else_branch=statement )
            str += ctx.getChild(5).__str__()+self.visitStatement(ctx.statement(1))
        return str


    # Visit a parse tree produced by SolidityParser#whileStatement.
    def visitWhileStatement(self, ctx:SolidityParser.WhileStatementContext):
        #'while' '(' condition=expression ')' body=statement ;
        str = ctx.getChild(0).__str__()+" " +ctx.getChild(1).__str__() +self.visit(ctx.expression())+ctx.getChild(3).__str__()+ self.visitStatement(ctx.statement())
        return str


    # Visit a parse tree produced by SolidityParser#simpleStatement.
    def visitSimpleStatement(self, ctx:SolidityParser.SimpleStatementContext):
        #아래로 바로 보내기
        # ( variableDeclarationStatement | expressionStatement )
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#forStatement.
    def visitForStatement(self, ctx:SolidityParser.ForStatementContext):
        #  원본 'for' '(' ( init=simpleStatement | ';' ) condition=expression? ';' update=expression? ')' body=statement
        str = ctx.getChild(0).__str__()+" "+ctx.getChild(1).__str__()
        #'for' '(' ( ';' )
        if ctx.getChild(2).__str__().__eq__(";"):
            str+= ctx.getChild(2).__str__()
        #'for' '(' ( init=simpleStatement)
        else:
            str+= self.visitSimpleStatement(ctx.simpleStatement())

        # condition=expression ';' update=expression ')' body=statement
        if ctx.getChildCount()>7:
            str+= " "+self.visit(ctx.expression(0))+ctx.getChild(4).__str__()+" "+ self.visit(ctx.expression(1))+ctx.getChild(6).__str__()+self.visitStatement(ctx.statement())
        elif ctx.getChildCount()>6:
            #  ';' update=expression ')' body=statement
            if ctx.getChild(3).__eq__(";"):
                str+= ctx.getChild(3).__str__()+" "+ self.visit(ctx.expression())+ctx.getChild(5).__str__()+self.visitStatement(ctx.statement())
            # condition=expression ';'  ')' body=statement
            else:
                str+= " " +self.visit(ctx.expression())+ctx.getChild(4).__str__()+" "+ctx.getChild(5).__str__()+self.visitStatement(ctx.statement())
        # ';' ')' body=statement
        else:
            str += ctx.getChild(3).__str__()+ ctx.getChild(4).__str__()+ self.visitStatement(ctx.statement())
        return str


    # Visit a parse tree produced by SolidityParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:SolidityParser.DoWhileStatementContext):
        str = ctx.getChild(0).__str__()+self.visitStatement(ctx.statement())+ ctx.getChild(2).__str__() +ctx.getChild(3).__str__() + self.visit(ctx.expression())+ctx.getChild(4).__str__()+ctx.getChild(5).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#continueStatement.
    def visitContinueStatement(self, ctx:SolidityParser.ContinueStatementContext):
        str = ctx.getChild(0).__str__()+ctx.getChild(1).__str__()
        return str

    # Visit a parse tree produced by SolidityParser#breakStatement.
    def visitBreakStatement(self, ctx:SolidityParser.BreakStatementContext):
        str = ctx.getChild(0).__str__()+ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#returnStatement.
    def visitReturnStatement(self, ctx:SolidityParser.ReturnStatementContext):
        if ctx.getChildCount()>2:
            #return expression ;
            str = ctx.getChild(0).__str__() +" "+self.visit(ctx.expression())+ctx.getChild(2).__str__()
        else:
            #return ;
            str = ctx.getChild(0).__str__()+ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#variableDeclarationStatement.
    def visitVariableDeclarationStatement(self, ctx:SolidityParser.VariableDeclarationStatementContext):
        str = self.visitVariableDeclaration(ctx.variableDeclaration())
        if ctx.getChildCount()>2:
            # variable_declaration=variableDeclaration ( '=' expr=expression ) ';'
            str += " "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression())+ctx.getChild(3).__str__()
        else:
            # variable_declaration=variableDeclaration ';'
            str +=  ctx.getChild(1).__str__()

        return str


    # Visit a parse tree produced by SolidityParser#elementaryTypeName.
    def visitElementaryTypeName(self, ctx:SolidityParser.ElementaryTypeNameContext):
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#AndExpr.
    def visitAndExpr(self, ctx:SolidityParser.AndExprContext):
        # lhs=expression op='&&' rhs=expression
        str = self.visit(ctx.expression(0)) +" "+ ctx.getChild(1).__str__() +" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#ParenthesisExpr.
    def visitParenthesisExpr(self, ctx:SolidityParser.ParenthesisExprContext):
        #'(' expr=expression ')'
        str = ctx.getChild(0).__str__()+ self.visit(ctx.expression())+ ctx.getChild(2).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#BitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx:SolidityParser.BitwiseOrExprContext):
        #lhs=expression op='|' rhs=expression
        str =self.visit(ctx.expression(0)) + ctx.getChild(1).__str__() + self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#AllExpr.
    def visitAllExpr(self, ctx:SolidityParser.AllExprContext):
        #AllKeyword
        str= ctx.getChild(0).__str__()
        return str

    # Visit a parse tree produced by SolidityParser#IteExpr.
    def visitIteExpr(self, ctx:SolidityParser.IteExprContext):
        #cond=expression '?' then_expr=expression ':' else_expr=expression
        str = self.visit(ctx.expression(0))+" " +ctx.getChild(1).__str__()+" " +self.visit(ctx.expression(1))+" "+ ctx.getChild(3).__str__()+" "+self.visit(ctx.expression(2))
        return str


    # Visit a parse tree produced by SolidityParser#PowExpr.
    def visitPowExpr(self, ctx:SolidityParser.PowExprContext):
        #lhs=expression op='**' rhs=expression
        str = self.visit(ctx.expression(0))+ " "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#StringLiteralExpr.
    def visitStringLiteralExpr(self, ctx:SolidityParser.StringLiteralExprContext):
        #StringLiteral
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#PlusMinusExpr.
    def visitPlusMinusExpr(self, ctx:SolidityParser.PlusMinusExprContext):
        #연산자 띄어쓰기
        #lhs=expression op=('+' | '-') rhs=expression
        str = self.visit(ctx.expression(0))+" " +ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#CompExpr.
    def visitCompExpr(self, ctx:SolidityParser.CompExprContext):
        #연산자 띄어쓰기
        #lhs=expression op=('<' | '>' | '<=' | '>=') rhs=expression
        str = self.visit(ctx.expression(0))+" " +ctx.getChild(1).__str__()+" "+ self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#IndexExpr.
    def visitIndexExpr(self, ctx:SolidityParser.IndexExprContext):
        #arr=expression '[' index=expression ']'
        str = self.visit(ctx.expression(0))+ ctx.getChild(1).__str__()+ self.visit(ctx.expression(1))+ctx.getChild(3).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#SignExpr.
    def visitSignExpr(self, ctx:SolidityParser.SignExprContext):
        #op=('+' | '-') expr=expression
        str = ctx.getChild(0).__str__() + self.visit(ctx.expression())
        return str


    # Visit a parse tree produced by SolidityParser#NumberLiteralExpr.
    def visitNumberLiteralExpr(self, ctx:SolidityParser.NumberLiteralExprContext):
        # numberLiteral
        str = ctx.numberLiteral().getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#BitwiseNotExpr.
    def visitBitwiseNotExpr(self, ctx:SolidityParser.BitwiseNotExprContext):
        # '~' expr=expression
        str = ctx.getChild(0).__str__() + self.visit(ctx.expression())
        return str


    # Visit a parse tree produced by SolidityParser#IdentifierExpr.
    def visitIdentifierExpr(self, ctx:SolidityParser.IdentifierExprContext):
        # idf=identifier
        str = self.visitIdentifier(ctx.identifier())
        return str



    # Visit a parse tree produced by SolidityParser#BooleanLiteralExpr.
    def visitBooleanLiteralExpr(self, ctx:SolidityParser.BooleanLiteralExprContext):
        # BooleanLiteral
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#MeExpr.
    def visitMeExpr(self, ctx:SolidityParser.MeExprContext):
        # MeKeyword
        str = ctx.MeKeyword().__str__()
        return str


    # Visit a parse tree produced by SolidityParser#NotExpr.
    def visitNotExpr(self, ctx:SolidityParser.NotExprContext):
        # '!' expr=expression
        str = ctx.getChild(0).__str__() + self.visit(ctx.expression())
        return str


    # Visit a parse tree produced by SolidityParser#BitShiftExpr.
    def visitBitShiftExpr(self, ctx:SolidityParser.BitShiftExprContext):
        # lhs=expression op=('<<' | '>>') rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#BitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx:SolidityParser.BitwiseAndExprContext):
        #  lhs=expression op='&' rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#MultDivModExpr.
    def visitMultDivModExpr(self, ctx:SolidityParser.MultDivModExprContext):
        # lhs=expression op=('*' | '/' | '%') rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#AssignmentExpr.
    def visitAssignmentExpr(self, ctx:SolidityParser.AssignmentExprContext):
        # lhs=expression op=('=' | '|=' | '^=' | '&=' | '<<=' | '>>=' | '+=' | '-=' | '*=' | '/=' | '%=') rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#TupleExpr.
    def visitTupleExpr(self, ctx:SolidityParser.TupleExprContext):
        # expr=tupleExpression
        str = self.visitTupleExpression(ctx.tupleExpression())
        return str


    # Visit a parse tree produced by SolidityParser#OrExpr.
    def visitOrExpr(self, ctx:SolidityParser.OrExprContext):
        # lhs=expression op='||' rhs=expression
        str = self.visit(ctx.expression(0))+" "+ctx.getChild(1).__str__()+" "+self.visit(ctx.expression(1))
        return str

    # Visit a parse tree produced by SolidityParser#FunctionCallExpr.
    def visitFunctionCallExpr(self, ctx:SolidityParser.FunctionCallExprContext):
        # func=expression '(' args=functionCallArguments ')'
        str = self.visit(ctx.expression())+ ctx.getChild(1).__str__()+self.visitFunctionCallArguments(ctx.functionCallArguments())+ctx.getChild(3).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#EqExpr.
    def visitEqExpr(self, ctx:SolidityParser.EqExprContext):
        # lhs=expression op=('==' | '!=') rhs=expression
        str = self.visit(ctx.expression(0))+ctx.getChild(1).__str__()+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#PostCrementExpr.
    def visitPostCrementExpr(self, ctx:SolidityParser.PostCrementExprContext):
        # expr=expression op=('++' | '--')
        str = self.visit(ctx.expression())+ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#PrimitiveCastExpr.
    def visitPrimitiveCastExpr(self, ctx:SolidityParser.PrimitiveCastExprContext):
        # elem_type=elementaryTypeName '(' expr=expression ')'
        str = self.visitElementaryTypeName(ctx.elementaryTypeName())+ctx.getChild(1).__str__()+self.visit(ctx.expression())+ctx.getChild(3).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#BitwiseXorExpr.
    def visitBitwiseXorExpr(self, ctx:SolidityParser.BitwiseXorExprContext):
        # lhs=expression op='^' rhs=expression
        str = self.visit(ctx.expression(0))+ctx.getChild(1).__str__()+self.visit(ctx.expression(1))
        return str


    # Visit a parse tree produced by SolidityParser#MemberAccessExpr.
    def visitMemberAccessExpr(self, ctx:SolidityParser.MemberAccessExprContext):
        # expr=expression '.' member=identifier
        str = self.visit(ctx.expression())+ctx.getChild(1).__str__()+self.visitIdentifier(ctx.identifier())
        return str


    # Visit a parse tree produced by SolidityParser#PreCrementExpr.
    def visitPreCrementExpr(self, ctx:SolidityParser.PreCrementExprContext):
        # op=('++' | '--') expr=expression
        str = ctx.getChild(0).__str__()+self.visit(ctx.expression())
        return str


    # Visit a parse tree produced by SolidityParser#functionCallArguments.
    def visitFunctionCallArguments(self, ctx:SolidityParser.FunctionCallArgumentsContext):
        #원본 (exprs+=expression (',' exprs+=expression)*)?
        if ctx.getChildCount()>2:
            # (exprs+=expression (',' exprs+=expression)(',' exprs+=expression))
            str = self.visit(ctx.expression(0))
            for i in range(1, ctx.getChildCount(),2):
                str += ctx.getChild(i).__str__() + self.visit(ctx.getChild(i+1))
        elif ctx.getChildCount()>0:
            #(exprs+=expression)
            str = self.visit(ctx.expression())
        else:
            #
            str =""
        return str


    # Visit a parse tree produced by SolidityParser#tupleExpression.
    def visitTupleExpression(self, ctx:SolidityParser.TupleExpressionContext):
        #원본 '(' ( expression? ( ',' expression? )* ) ')'
        str = ctx.getChild(0).__str__()
        tp = ""
        if ctx.getChildCount()>2:
            for i in range(1, ctx.getChildCount()-1):
                if ctx.getChild(i).__str__().__eq__(","):
                    tp+= ctx.getChild(i).__str__()
                else :
                    tp+= self.visit(ctx.getChild(i))
            str += tp + ctx.getChild(ctx.getChildCount()-1).__str__()
        # '(' ')'
        else:
            str +=ctx.getChild(1).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#elementaryTypeNameExpression.
    def visitElementaryTypeNameExpression(self, ctx:SolidityParser.ElementaryTypeNameExpressionContext):
        str = ctx.elementaryTypeName().__str__()
        return str


    # Visit a parse tree produced by SolidityParser#numberLiteral.
    def visitNumberLiteral(self, ctx:SolidityParser.NumberLiteralContext):
        str = ctx.getChild(0).__str__()
        return str


    # Visit a parse tree produced by SolidityParser#annotatedTypeName.
    def visitAnnotatedTypeName(self, ctx:SolidityParser.AnnotatedTypeNameContext):
        # type_name=typeName ('@' privacy_annotation=expression)?
        str = self.visitTypeName(ctx.typeName())
        if ctx.getChildCount()>1:
            str += ctx.getChild(1).__str__()+ self.visit(ctx.expression())+" "
        return str

    # Visit a parse tree produced by SolidityParser#identifier.
    def visitIdentifier(self, ctx:SolidityParser.IdentifierContext):
        # IdentifierStart IdentifierPart*
        str =ctx.getChild(0).__str__()
        if ctx.getChildCount()>1:
            for i in range(1, ctx.getChildCount()-1):
                str +=ctx.getChild(i).__str__()
        return str
