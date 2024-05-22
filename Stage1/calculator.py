#making list of opeartors 
# running the for loop throughout the expression, finding operator and operands

''' Basic things to check
1. if all operands are numbers and decimals
2. if every operator is valid
3. if the expression is valid(like no zerodivision error)
4. also ignore whitespaces in between the expression
5. shouldnot start and end with operator(except starting with '-')
6. shouldnot have two operators together(excluding -+, +-)

all these things are done by eval() function in python
eval also includes bitwise operators also.
But eval() has some risks
'''

#------------------------------------------------------------------------------------
'''
def calculator(expression):
    #removing whitespaces
    expression = expression.replace(" ","")
    #checking if the expression is valid
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return str(e)
''' 
#------------------------------------------------------------------------------------

#lets have simple expression 2+3*4
#first converting string into list of characters
#['2','+','3','*','4']
#and finding some basic syntax like errors right away

#------------------------------------------------------------------------------------

ops = ['+', '-', '*', '/','**','%']

def pm_operator(expr: str):
    expr = expr.replace('+-','-').replace('-+','+')
    for t in range(len(expr)-1):
        if expr[t] in '+-' and expr[t+1] in '+-': #including operators like '+++..'
            raise ValueError('Invalid expression: Cannot have two operators together')
    return expr

def check_expr(expr):
        if (expr[0] in ops and expr[0] != '-') or expr[-1] in ops:
            raise ValueError('Invalid expression: Cannot start or end with an operator')
        for i in range(len(expr)-1):  
            if expr[i] in ops and expr[i+1] in ops: 
                if (expr[i:i+2] == '**' and expr[i+2] in ops): 
                    raise ValueError('Invalid expression: Cannot have two operators together')
                elif expr[i:i+2] in ['--','++']:
                    raise ValueError('Invalid expression: Cannot have two operators together')
def exprtolist(expr):
    #removing whitespaces
    expr = expr.replace(" ","")
    #checking if the expression is valid
    
    try:
        corrected_expr = pm_operator(expr)
        check_expr(corrected_expr)
        terms = []
        current_term = ''
        i=0
        while i < len(corrected_expr):
            #to handle operands
            if corrected_expr[i].isdigit() or corrected_expr[i] == '.':
                current_term += corrected_expr[i] #concatenate
                i+=1
            else:
                if '.' in current_term or current_term or '-' in current_term:
                    terms.append(current_term)
                    current_term = ''

                if corrected_expr[i:i+2] == '**':
                    terms.append('**')
                    i=i+2
                    continue
                if corrected_expr[i] in '*/%':
                    terms.append(corrected_expr[i])
                if corrected_expr[i] in '+-' :
                    if corrected_expr[i]=='-' and i==0:
                        current_term = '-'
                    elif corrected_expr[i]=='-' and i<len(corrected_expr)-1 and corrected_expr[i+1].isdigit() and corrected_expr[i-1] in ops:
                        current_term = '-'
                    elif corrected_expr[i]=='-' and corrected_expr[i-1] not in ops:
                        terms.append(corrected_expr[i])
                    else:
                        terms.append(corrected_expr[i])
                elif corrected_expr[i] not in ops:
                    raise ValueError('Invalid expression')
                i+=1

                
        #while loop ends here
        if current_term:
            terms.append(current_term)
        return terms        

    except Exception as e:
        return str(e)




# print(exprtolist('2+3**4-4.56/4*56%2'))


#Now evaluating from the list

def calculator(expr):
    lst = exprtolist(expr)
    print(lst)

    if len(lst) == 1:
        return float(lst[0])

    while('**' in lst):
            i = lst.index('**')
            lst[i-1] = float(lst[i-1])**float(lst[i+1])
            lst.pop(i)
            lst.pop(i)

    div_count = lst.count('/')
    while div_count>0:
        i = lst.index('/')
        try:
            lst[i-1] = float(lst[i-1])/float(lst[i+1])
        except ZeroDivisionError as e:
            print(str(e))

        lst.pop(i)
        lst.pop(i)
        div_count-=1

    mul_count = lst.count('*')
    while mul_count>0:
        i = lst.index('*')
        lst[i-1] = float(lst[i-1])*float(lst[i+1])
        lst.pop(i)
        lst.pop(i)
        mul_count-=1

    mod_count = lst.count('%')
    while mod_count>0:
        i = lst.index('%')
        try:
            lst[i-1] = int(lst[i-1])%int(lst[i+1])
        except ValueError as ve:
            print(str(ve))
        except ZeroDivisionError as ze:
            print(str(ze))
        lst.pop(i)
        lst.pop(i)
        mod_count-=1

    add_count = lst.count('+')
    while add_count>0:
        i = lst.index('+')
        lst[i-1] = float(lst[i-1])+float(lst[i+1])
        lst.pop(i)
        lst.pop(i)
        add_count-=1
    
    sub_count = lst.count('-')
    while sub_count>0:
        i = lst.index('-')
        lst[i-1] = float(lst[i-1])-float(lst[i+1])
        lst.pop(i)
        lst.pop(i)
        sub_count-=1

    return lst[0] if type(lst[0]) in [int,float] else ''

a = ''
while a!='quit':
    a = input('Enter the expression: ').strip()
    if a!='quit': 
        print(calculator(a))
    else:
        print('quitting...')



#--------------------------------------------------------------------------------------------------
