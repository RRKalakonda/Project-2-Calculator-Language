import sys
from collections import deque

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




# def tokenize(input_str):
#     tokens = []
#     i = 0
#     while i < len(input_str):
#         if input_str[i].isspace() and input_str[i] != '\n':
#             i += 1
#             continue
#         elif input_str[i] in '+-*/%^()=':
#             token_type = TokenType.OPERATOR
#             if input_str[i] == '(' or input_str[i] == ')':
#                 token_type = TokenType.PARENTHESIS
#             elif input_str[i] == '=':
#                 token_type = TokenType.ASSIGN
#             tokens.append(Token(token_type, input_str[i]))
#             i += 1
#         elif input_str[i].isdigit() or input_str[i] == '.':
#             j = i + 1
#             while j < len(input_str) and (input_str[j].isdigit() or input_str[j] == '.'):
#                 j += 1
#             tokens.append(Token(TokenType.NUMBER, float(input_str[i:j])))
#             i = j
#         elif input_str[i].isalpha() or input_str[i] == '_':
#             j = i + 1
#             while j < len(input_str) and (input_str[j].isalnum() or input_str[j] == '_'):
#                 j += 1
#             value = input_str[i:j]
#             if value == "print":
#                 tokens.append(Token(TokenType.PRINT, value))
#             else:
#                 tokens.append(Token(TokenType.VARIABLE, value))
#             i = j
#         elif input_str[i] == ',':
#             tokens.append(Token(TokenType.COMMA, ','))
#             i += 1
#         elif input_str[i] == '\n':
#             tokens.append(Token(TokenType.NEWLINE, 'NONE'))
#             i += 1
#         else:
#             raise ValueError(f"Invalid character: '{input_str[i]}'")
#     return tokens

def tokenize(input_str):
    tokens = []
    i = 0
    while i < len(input_str):
        if input_str[i].isspace() and input_str[i] != '\n':
            i += 1
            continue
        elif input_str[i] in '+-*/%^()=':
            token_type = TokenType.OPERATOR
            if input_str[i] == '(' or input_str[i] == ')':
                token_type = TokenType.PARENTHESIS
            elif input_str[i] == '=':
                token_type = TokenType.ASSIGN
            if input_str[i] == '-' and i + 1 < len(input_str) and input_str[i + 1].isdigit() and (
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
        elif input_str[i].isalpha() or input_str[i] == '_':
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
        '+': 1, '-': 1,
        '*': 2, '/': 2, '%': 2,
        '^': 3,
        'u-': 4,
    }

    left_associative = {'+', '-', '*', '/', '%'}

    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()

        if operator == 'u-':
            values.append(Node(Token(TokenType.OPERATOR, '-'), right=right))
        else:
            left = values.pop()
            values.append(Node(Token(TokenType.OPERATOR, operator), left, right))



    # def apply_operator(operators, values):
    #     operator = operators.pop()
    #     right = values.pop()

    #     if operator == 'u-':
    #         values.append(Node(Token(TokenType.OPERATOR, '-'), right=right))
    #     else:
    #         left = values.pop()
    #         while operators and operators[-1] == '^':
    #             operator = operators.pop()
    #             left = Node(Token(TokenType.OPERATOR, operator), left, right)
    #             right = values.pop()
    #         values.append(Node(Token(TokenType.OPERATOR, operator), left, right))




    # def greater_precedence(op1, op2):
    #     # if op1 == op2 and op1 == '^':
    #     #     return False
    #     return precedence[op1] > precedence[op2]

    def greater_precedence(op1, op2):
        if op1 in left_associative and op2 in left_associative:
            return precedence[op1] >= precedence[op2]
        return precedence[op1] > precedence[op2]

    operators = []
    values = []

    # print(tokens)

    while tokens and tokens[0].token_type != TokenType.NEWLINE and tokens[0].token_type != TokenType.COMMA:
        token = tokens.pop(0)

        # print("Token:", token) 

        if token.token_type == TokenType.NUMBER or token.token_type == TokenType.VARIABLE:
            values.append(Node(token))
        elif token.token_type == TokenType.OPERATOR:
            if token.value == '-':
                if not values or (
                        values[-1].token.token_type == TokenType.OPERATOR and values[-1].token.value != 'u-'):
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
        statements.append(parse_statement(tokens))
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
        if node.token.value is variables:
            return variables[node.token.value]
        else:
            return float(0)
    elif node.token.token_type == TokenType.OPERATOR:
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
    elif node.token.token_type == TokenType.ASSIGN:
        value = evaluate(node.right, variables)
        variables[node.left.token.value] = value
        return value
    elif node.token.token_type == TokenType.PRINT:
        values = [evaluate(child, variables) for child in node.left]
        print(*values)
        return values[0] if values else None


def main(program):
    tokens = tokenize(program)
    #print(tokens)
    statements = parse_program(tokens)
    # print(statements)

    # ast_nodes = [
    #     None,
    #     Node(Token(TokenType.ASSIGN, '='), Node(Token(TokenType.VARIABLE, 'pi'), None, None), Node(Token(TokenType.NUMBER, 3.14159), None, None)),
    #     Node(Token(TokenType.ASSIGN, '='), Node(Token(TokenType.VARIABLE, 'r'), None, None), Node(Token(TokenType.NUMBER, 2.0), None, None)),
    #     Node(Token(TokenType.ASSIGN, '='), Node(Token(TokenType.VARIABLE, 'area'), None, None), Node(Token(TokenType.OPERATOR, '*'), Node(Token(TokenType.VARIABLE, 'pi'), None, None), Node(Token(TokenType.OPERATOR, '^'), Node(Token(TokenType.VARIABLE, 'r'), None, None), Node(Token(TokenType.NUMBER, 2.0), None, None)))),
    #     Node(Token(TokenType.PRINT, 'print'), left=[Node(Token(TokenType.VARIABLE, 'area'), None, None)])
    # ]

    variables = {}
    for node in statements:
        if node:
            evaluate(node, variables)




    # statements = parse_program(tokens)
    # evaluate_program(statements)

if __name__ == '__main__':
    input_string = sys.argv[1]
    test1 = """
print -2^4
"""
    program = """
print 2^3^2
print 5-1-1-1
print 2^-3+1
print (2 + 3) * (4 - 2) / (1 + 1) + 2 ^ 3
print ((3 + 4) * 2 - 5) ^ 2
print 2 ^ 3 * (1 + 1) + 4 / 2
a = 2
b = 3
c = (a + b) * (a - b) + x
print c
x = 5
y = 2 * x + 3
z = y ^ 2 - 4 * y + 4
print z
base = 2
exponent = 3
result = base ^ exponent
print result * (1 - base) + (base * 2)
print -2 ^ 3
print -(3 ^ 2) + 4 * 3 - 5
print 2 ^ 3 * -2 + 4, -2 ^ 3 + 1
"""
    # print(input_string)
    main(input_string)



## print 2^-1 print -(3 ^ 2) + 4 * 3 - 5





    # def greater_precedence(op1, op2):
    #     return precedence[op1] > precedence[op2]

    # def greater_precedence(op1, op2):
    #     if op1 == op2 and op1 == '^':
    #         return False
    #     return precedence[op1] > precedence[op2]


    # def greater_precedence(op1, op2):
    #     if op1 in left_associative and op2 in left_associative:
    #         return precedence[op1] >= precedence[op2]
    #     return precedence[op1] > precedence[op2]


    # def greater_precedence(op1, op2):
    #     if op1 == op2 and op1 == '^':
    #         return False
    #     elif precedence[op1] == precedence[op2]:
    #         return True
    #     return precedence[op1] > precedence[op2]