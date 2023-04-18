
import sys

variables = {}

class TokenType:
    NUMBER = 'NUMBER'
    VARIABLE = 'VARIABLE'
    OPERATOR = 'OPERATOR'
    PARENTHESIS = 'PARENTHESIS'
    NEWLINE = 'NEWLINE'
    ASSIGN = 'ASSIGN'
    PRINT = 'PRINT'
    COMMA = 'COMMA'

class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f'Token({self.token_type}, {self.value})'

class Node:
    def __init__(self, token, left=None, right=None):
        self.token = token
        self.left = left
        self.right = right

    def __repr__(self):
        return f'Node({self.token}, {self.left}, {self.right})'


def tokenize(input_str):
    tokens = []
    i = 0
    while i < len(input_str):
        if input_str[i].isspace() and input_str[i] != '\n':
            i += 1
            continue
        elif input_str[i] in '+-*/%^()=<>!':
            token_type = TokenType.OPERATOR
            if input_str[i] == '(' or input_str[i] == ')':
                token_type = TokenType.PARENTHESIS
            elif input_str[i] == '=':
                token_type = TokenType.ASSIGN
                if tokens and (tokens[-1].token_type == TokenType.OPERATOR or tokens[-1].token_type == TokenType.ASSIGN):
                    op= tokens[-1].value
                    if op in ['+', '-', '*', '/', '%', '^', '=', '<', '>', '!']:
                        tokens.pop()
                        tokens.append(Token(TokenType.OPERATOR, op+'='))
                        i+=1
                        continue


            if input_str[i] == '&':
                if (i+1 < len(input_str) and input_str[i+1] == '&'):
                    tokens.append(Token(TokenType.OPERATOR, '&&'))
                    i=i+2
                else:
                    raise Exception("parse error")
    
            if input_str[i] == '|':
                if (i+1 < len(input_str) and input_str[i+1] == '|'):
                    tokens.append(Token(TokenType.OPERATOR, '||'))
                    i=i+2
                else:
                    raise Exception("parse error")

            if input_str[i] == '+' and  (i+1 < len(input_str) and input_str[i+1] == '+'):
                if i>0 and tokens[-1].token_type == TokenType.VARIABLE:
                    tokens.append(Token(TokenType.OPERATOR, '_++'))
                    i=i+2
                elif i+2 < len(input_str) and input_str[i+2].isalpha():
                    tokens.append(Token(TokenType.OPERATOR, '++_'))
                    i=i+2
                else:
                    raise Exception("parse error")
            elif input_str[i] == '-' and (i+1 < len(input_str) and input_str[i+1] == '-'):
                if i>0 and tokens[-1].token_type == TokenType.VARIABLE:
                    tokens.append(Token(TokenType.OPERATOR, '_--'))
                    i=i+2
                elif i+2 < len(input_str) and input_str[i+2].isalpha():
                    tokens.append(Token(TokenType.OPERATOR, '--_'))
                    i=i+2
                else:
                    raise Exception("parse error")
                
            elif input_str[i] == '-' and i + 1 < len(input_str) and input_str[i + 1].isdigit() and (
                    i == 0 or tokens[-1].token_type in (TokenType.OPERATOR, TokenType.PARENTHESIS, TokenType.COMMA, TokenType.NEWLINE, TokenType.ASSIGN, TokenType.PRINT)):
                j = i + 1
                while j < len(input_str) and (input_str[j].isdigit() or input_str[j] == '.'):
                    j += 1
                tokens.append(Token(TokenType.NUMBER, float(input_str[i:j])))
                i = j
            else:
                tokens.append(Token(token_type, input_str[i]))
                i += 1
        elif input_str[i].isdigit() or input_str[i] == '.':
            j = i + 1
            while j < len(input_str) and (input_str[j].isdigit() or input_str[j] == '.'):
                j += 1
            tokens.append(Token(TokenType.NUMBER, float(input_str[i:j])))
            i = j
        elif input_str[i].isalpha():
            j = i + 1
            while j < len(input_str) and (input_str[j].isalnum() or input_str[j] == '_'):
                j += 1
            value = input_str[i:j]
            if value == "print":
                tokens.append(Token(TokenType.PRINT, value))
            else:
                tokens.append(Token(TokenType.VARIABLE, value))
            i = j
        elif input_str[i] == ',':
            tokens.append(Token(TokenType.COMMA, ','))
            i += 1
        elif input_str[i] == '\n':
            tokens.append(Token(TokenType.NEWLINE, 'NONE'))
            i += 1
        else:
            raise ValueError(f"Invalid character: '{input_str[i]}'")
    return tokens




def parse_expression(tokens):
    precedence = {
        '+=': 0, '-=': 0, '*=': 0, '/=': 0, '%=': 0, '^=': 0, '==': 0, '<=': 0, '>=': 0, '!=': 0, '<': 0, '>': 0, '&&': 0, '||': 0,
        '+': 1, '-': 1,
        '*': 2, '/': 2, '%': 2,
        '^': 3,
        'u-': 4, '!': 4,
        '_++': 5, '_--': 5, '++_': 5, '--_': 5
    }

    left_associative = {'+', '-', '*', '/', '%'}

    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()

        if operator == 'u-':
            values.append(Node(Token(TokenType.OPERATOR, '-'), right=right))
        elif operator in { '_++', '_--', '++_', '--_'}:
            values.append(Node(Token(TokenType.OPERATOR, operator), right=right))
        elif operator == '!':
            values.append(Node(Token(TokenType.OPERATOR, '!'), right=right))
        else:
            left = values.pop()
            values.append(Node(Token(TokenType.OPERATOR, operator), left, right))


    def greater_precedence(op1, op2):
        if op1 in left_associative and op2 in left_associative:
            return precedence[op1] >= precedence[op2]
        return precedence[op1] > precedence[op2]

    operators = []
    values = []
    p_u_flag = False

    # print(tokens)

    while tokens and tokens[0].token_type != TokenType.NEWLINE and tokens[0].token_type != TokenType.COMMA:
        token = tokens.pop(0)

        # print("Token:", token) 

        if token.token_type == TokenType.NUMBER or token.token_type == TokenType.VARIABLE:
            values.append(Node(token))
        elif token.token_type == TokenType.OPERATOR:
            if token.value == '-':
                if not values or (
                        values[-1].token.token_type == TokenType.OPERATOR and values[-1].token.value != 'u-' and p_u_flag==False):
                    token = Token(TokenType.OPERATOR, 'u-')

            while (operators and operators[-1] != '(' and
                   greater_precedence(operators[-1], token.value)):
                apply_operator(operators, values)

            operators.append(token.value)
        elif token.token_type == TokenType.PARENTHESIS:
            if token.value == '(':
                operators.append(token.value)
            else:
                while operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()
                if tokens[0].token_type == TokenType.OPERATOR and tokens[0].value == '-':
                    p_u_flag = True
        else:
            tokens.insert(0, token)
            break

    while operators:
        apply_operator(operators, values)

    # print("Values:", values, "Operators:", operators)

    return values[0]

def parse_statement(tokens):
    if not tokens:
        return None

    if tokens[0].token_type == TokenType.NEWLINE:
        tokens.pop(0)
        return None

    if tokens[0].token_type == TokenType.PRINT:
        tokens.pop(0)
        expressions = []
        while tokens and tokens[0].token_type != TokenType.NEWLINE:
            # tokens.insert(0,Token(TokenType.PARENTHESIS, "("))
            # tokens.append(Token(TokenType.PARENTHESIS, ")"))
            expressions.append(parse_expression(tokens))
            if tokens and tokens[0].token_type == TokenType.COMMA:
                tokens.pop(0)
        if tokens:
            tokens.pop(0)
        return Node(Token(TokenType.PRINT, "print"), left=expressions)

    elif tokens[0].token_type == TokenType.VARIABLE and len(tokens) ==1:
        variable = tokens.pop(0)
        if tokens and tokens[0].token_type == TokenType.NEWLINE:
            tokens.pop(0)
        return Node(Token(TokenType.ASSIGN, '='), left=Node(variable), right=Node(Token(TokenType.NUMBER, float(0))))
        
    elif tokens[0].token_type == TokenType.VARIABLE and tokens[1].token_type == TokenType.ASSIGN:
        variable = tokens.pop(0)
        tokens.pop(0)  # Remove the assignment operator
        expression = parse_expression(tokens)
        if tokens and tokens[0].token_type == TokenType.NEWLINE:
            tokens.pop(0)
        return Node(Token(TokenType.ASSIGN, '='), left=Node(variable), right=expression)

    else:
        expression = parse_expression(tokens)
        if tokens and tokens[0].token_type == TokenType.NEWLINE:
            tokens.pop(0)
        return expression


def parse_program(tokens):
    statements = []
    while tokens:
        try:
            statements.append(parse_statement(tokens))
        except Exception as e:
            print("parse error")
            sys.exit()
        # print(statements)
    return statements


def evaluate(node, variables=None):

    if variables is None:
        variables = {}

    if not node:
        return float(0)
    if node.token.token_type == TokenType.NUMBER:
        return float(node.token.value)
    elif node.token.token_type == TokenType.VARIABLE:
        if node.token.value in variables:
            return variables[node.token.value]
        else:
            return float(0)
    elif node.token.token_type == TokenType.OPERATOR:
        if node.token.value in {'^', '+=', '-=', '*=', '/=', '%=', '^='}:
            right = evaluate(node.right, variables)
            left = evaluate(node.left, variables)
        else: 
            left = evaluate(node.left, variables)
            right = evaluate(node.right, variables)
        if node.token.value == '+':
            return left + right
        elif node.token.value == '-':
            return left - right
        elif node.token.value == '*':
            return left * right
        elif node.token.value == '/':
            return left / right
        elif node.token.value == '^':
            return left ** right
        elif node.token.value == '%':
            return left % right
        elif node.token.value in {'_++','_--','++_','--_'}:
            var_name = node.right.token.value
            if var_name not in variables:
                variables[var_name] = float(0)
            if node.token.value == '_++':
                old_value = variables[var_name]
                variables[var_name] += 1
                return old_value
            elif node.token.value == '_--':
                old_value = variables[var_name]
                variables[var_name] -= 1
                return old_value
            elif node.token.value == '++_':
                variables[var_name] += 1
                return variables[var_name]
            elif node.token.value == '--_':
                variables[var_name] -= 1
                return variables[var_name]
        elif node.token.value in {'+=', '-=', '*=', '/=', '%=', '^='}:
            var_name = node.left.token.value
            if var_name not in variables:
                variables[var_name] = float(0)
            if '+' in node.token.value:
                variables[var_name] = left + right
                return left + right
            elif '-' in node.token.value:
                variables[var_name] = left - right
                return left - right
            elif '*' in node.token.value:
                variables[var_name] = left * right
                return left * right
            elif '/' in node.token.value:
                variables[var_name] = left / right
                return left / right
            elif '^' in node.token.value:
                variables[var_name] = left ** right
                return left ** right
            elif '%' in node.token.value:
                variables[var_name] = left % right
                return left % right
        elif node.token.value in {'==' , '<=' , '>=' , '!=' , '<' , '>'}:
            if node.token.value == '==':
                return 1 if left == right else 0
            elif node.token.value == '<=':
                return 1 if left <= right else 0
            elif node.token.value == '>=' :
                return 1 if left >= right else 0
            elif node.token.value == '!=':
                return 1 if left != right else 0
            elif node.token.value == '<':
                return 1 if left < right else 0
            elif node.token.value == '>':
                return 1 if left > right else 0
        elif node.token.value in {'&&', '||', '!'}:
            if node.token.value == '&&':
                return 1 if abs(left) and abs(right) else 0
            if node.token.value == '||':
                return 1 if abs(left) or abs(right) else 0
            if node.token.value == '!':
                return 0 if abs(right) else 1

    elif node.token.token_type == TokenType.ASSIGN:
        value = evaluate(node.right, variables)
        variables[node.left.token.value] = value
        return value
    elif node.token.token_type == TokenType.PRINT:
        values = []
        try:
            if node.left == None or len(node.left)==0:
                raise Exception("parse error")
            for i, child in enumerate(node.left):
                ans = evaluate(child, variables)
                values.append(ans)
                if i == len(node.left) - 1:
                    print(ans)
                else:
                    print(ans, end=" ")
            # values = [evaluate(child, variables) for child in node.left]
        except ZeroDivisionError as e:
            # print(*values, end=" ")
            print("divide by zero")
            sys.exit()
        
        return values[0] if values else None

def comment_parser(program):
    lines=program.split("\n")
    res=""
    commandFlag=False
    for line in lines:
        if(line.strip()==''):
            continue
        if(not commandFlag):
            if('#' in line):
                l=line.split('#',2)
                if(l[0].strip()!=''):
                    res+=(l[0]+"\n")
            elif("/*" in line):
                commandFlag=True
                l=line.split('/*',2)
                if(l[0].strip()!=''):
                    res+=(l[0]+"\n")
            else:
                res+=(line+"\n")
        else:
            if("*/" in line):
                commandFlag=False
                l=line.split('*/',2)
                if(l[1].strip()!=''):
                    res+=(l[1]+"\n")
    # print(res)
    return res



def main(program):

    program = comment_parser(program)

    try:
        tokens = tokenize(program)
    except:
        print("parse error")
        sys.exit()
    #print(tokens)
    statements = parse_program(tokens)
    # print(statements)


    for node in statements:
        if node:
            try:
                evaluate(node, variables)
            except ZeroDivisionError as e:
                # print(*values, end=" ")
                print("divide by zero")
                sys.exit()
            except Exception as e:
                print("parse error")
                sys.exit()


if __name__ == '__main__':
    # input_string = sys.argv[1]
    
    final_string = ''
    # while True:
    input_string = sys.stdin.read()
    main(input_string)