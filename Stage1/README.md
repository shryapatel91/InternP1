
# Stage 1

### Task: 
Create a Calculator Application completely which allows Infinite operations along with Decimals (2+ 4.56+89*9/3.........) 




### Run the program
```bash
  python calculator.py
```

- In terminal after the program starts, you can enter the expression in this format: 2+3*5+2**4-9
```bash
Enter the expression: 2+3*5+2**4-9
```

- It will give the list of operands and operators in order, after checking the validity of the expression
```bash
['2', '+', '3', '*', '5', '+', '2', '**', '4', '-', '9']
```

- It then gives the result of the expression which is 24.0

- If the expression given is not valid, then it will print the error and ask for the next expression

- It will keep asking for the expression till you enter 'quit'
    

### Features

- Checks the validity of the expression and syntactically and mathematically
- Operators used are +,-,*,/,**(power),%
- Handles digits as well as decimals operations
- Keeps taking expressions from input till the word 'quit' is entered
- It takes '+-' as '-' and '-+' as '+' from the expression
- Operator precedence order: ** ,  / ,  * ,  + ,  - ,  %


### Some things you may want to know:
- parentheses are not handled in this program
- ++, -- are not handled
- // is not handled
- Use % carefully, it only works for integers, and it is calculated after division and multiplication
