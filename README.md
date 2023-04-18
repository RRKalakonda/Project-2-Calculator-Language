# Project-2-Calculator-Language


##  Rishika Reva Kalakonda - rkalakon@stevens.edu

##  URL of this Git repo https://github.com/RRKalakonda/Project-2-Calculator-Language

I spent a considerable amount of time working on this project, particularly on implementing order precedence, parsing and evaluation of complex expressions. I ran into issues with some test cases, which I eventually realized was due to extra space characters being printed. This caused some frustration, but once corrected, the test cases began to pass. More test cases were passed after the professor corrected the wrong outputs in gradescope. Handling of op-equals operations, pre-increment and decrement (like ++x or --z ), post-increment and decrement (like x++ or z-- ) also took decent amount of time.

Overall, it took me around 50 hours to complete the project. 

## Description of code

This program is an implementation of a basic interpreter for a programming language. The code reads a program as a string input, tokenizes it into a list of tokens, parses the tokens to generate an abstract syntax tree (AST), and then evaluates the AST to execute the program.

The program consists of two main parts. The first part includes functions for tokenizing, parsing, and evaluating the AST, and the second part includes the main function that reads the input string, calls the tokenizing, parsing, and evaluating functions in sequence, and handles any exceptions or errors that occur during execution.

The tokenize function takes the input string and generates a list of tokens based on a set of rules that define how the language's keywords, operators, and values should be identified and represented. The function uses traverses in loop & uses logic to match patterns in the input string and generate tokens for each matched pattern.

The parse_program function is responsible for taking the list of tokens produced by the tokenize function and transforming it into an Abstract Syntax Tree (AST) that represents the structure and logic of the program. During the process, the function also handles the precedence of operators to ensure that the resulting AST is correct and follows the order of operations.

The evaluate function is responsible for computing the value of an AST node, given its type and the variable values provided in a dictionary. This function performs a recursive traversal of the AST, evaluating each node in the correct order, until the entire tree has been evaluated. The function supports a variety of expressions and operators, including arithmetic, comparison, logical, assignment, and increment/decrement operators. Additionally, the function accounts for left and right associativity by recursively calling itself on sub-nodes as needed.

The comment_parser function takes the input string and removes any comments that are enclosed in '/*' and '*/' or followed by '#'. This function helps to simplify the input string and remove any irrelevant information that could cause errors during tokenization or parsing.

Finally, the main function takes the input string, applies the comment_parser function to it, then tokenizes and parses the resulting string to generate an AST, and finally evaluates the AST using the evaluate function. The function handles any exceptions or errors that occur during execution, such as parse errors or division by zero errors, and prints an appropriate error message to the console.

## Description of testing

To test the program thoroughly, we used a variety of inputs that covered all aspects of the language.

First, we tested basic arithmetic expressions, such as addition, subtraction, multiplication, and division, to ensure that the program can handle simple calculations. For example, we tested expressions like 2+3, 5-1, 2*4, and 10/2.

Next, we tested assignment statements, where a variable is assigned a value. We tested cases where the value is a number and where it is the result of an arithmetic expression. For example, we tested statements like x=5, y=2*3+1, and z=7-2.

We also tested complex statements that involve all the operators, such as expressions with multiple levels of parentheses and expressions with different operator precedences. For example, we tested expressions like (2+3)*4, 3*(5-2)+1, and (10-2)/(3+1)*5.

To ensure that the program takes operator precedence into account, we tested expressions with different levels of precedence, such as multiplication before addition and subtraction. For example, we tested expressions like 2+3*4, 5*3-1, and (10-2)/(3+1).

Additionally, we also tested the program with various test cases for the modulo operator, which involves dividing two numbers and returning the remainder, and checked if the output was as expected. We also tested the program with the use of variables, where we assigned values to variables and used them in various expressions to check if they were being evaluated correctly.

We tested the program for post and pre-increment and decrement operations, which involved increasing or decreasing the value of a variable by 1, and checked if the values were being updated correctly.

To test the binary operators, we provided expressions with multiple binary operators and checked if the program was evaluating them correctly, taking into consideration the precedence of the operators.

To test the relation operators, we provided expressions that involved comparison of two values using operators such as '==', '<=', '>=', '!=', '<', '>', and checked if the output was correct.

We also tested the program for the op equal to extension, which involved implementing the operation of '+=' , '-=' , '*=' , '/=' , '%=' and '^=' , and checked if the program was evaluating them correctly.

Finally, we tested statements with a combination of different operators and variable assignments, to ensure that the program can handle complex expressions and store the correct variable values. For example, we tested statements like x=2+3*4; y=5*(x-1); print y/2, x += 2 * ++x.

##  Any bugs or issues you could not resolve

As far as I remember I have resolved all the bugs which cropped up during testing, and I think there are no bugs which are yet to be resolved 

## An example of a difficult issue or bug

The process of implementing this program came with some difficulties that I had to overcome. 

Initially, I wrote the basic code and tested it locally with multiple test cases, which all worked fine. However, after submitting the code, I only got a few correct answers. I tried to correct the code as many times as possible, but it still didn't work. Finally, after carefully examining the output, I realized that I was printing an extra space character at the end of each answer. Once I removed the extra space character, many cases passed in Gradescope.

Another difficulty I faced was with the test cases in Gradescope. As mentioned earlier, my code was working for many inputs, but Gradescope was showing fewer test case passes. After receiving your message that the test case output was wrong (0 instead of 0.0) and correcting it, I finally saw that most of the cases passed.

In some of my submissions, I faced an infinite loop problem and received a runtime error on Gradescope. After examining the issue, I discovered that there was a problem in the tokenize function, where I had forgotten to handle the case for incorrect input. I resolved this issue by adding an else block that raises a parse error, which terminates the infinite loop.

During the implementation of the "op equal to" extension, I initially did not take into account the right-associative property of this extension. This led to incorrect outputs in some cases. After further analysis, I realized that these operators should be treated similarly to the power operator in the evaluate function, which helped me to resolve this issue.

Another bug I encountered was when there was a '-' operator after a closed parenthesis in the input, causing the program to behave incorrectly. In this case, the '-' operator was mistakenly considered as a unary minus operator instead of a binary operator, resulting in the failure of some test cases. To resolve this, I added a flag to an if block where the '-' operator was analyzed for conversion to a unary minus operator, and used it to distinguish between binary and unary minus operators.


## A list of the four extensions I've chosen to implement
1. Op-equals
2. Relational operations
3. Boolean operations
4. Comments
