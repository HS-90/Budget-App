class Category:
    
    #setup initial budget category
    def __init__(self, budget_cat):
        self.budget_cat = budget_cat
        self.withdraws = 0
        #empty list for ledger
        self.ledger = []
    
    def deposit(self, amount, description=""):
        self.ledger.append({'amount': round(amount,2), 'description': description})
        
    def withdraw(self, amount, description=""):
        
        #calling get_balance function to obtain balance
        balance = self.check_funds(amount)
   
                
        #check if ledger has enough balance for withdrawal
        if balance == True:
            self.ledger.append({'amount': round(-amount,2), 'description': description})
            self.withdraws += amount
            return True
        else:
            return False
    
    
    #method to get balance
    def get_balance(self):
        balance = 0
        
        for x in self.ledger:
            balance += x['amount']
            
        return(round(balance,2))
    
    #transfer method
    def transfer(self, amount, other_cat):
        check = self.check_funds(amount)
    
        if check == True:
            self.withdraw(amount, description = f'Transfer to {str(other_cat.budget_cat)}')
            other_cat.deposit(amount, description =f'Transfer from {str(self.budget_cat)}')
            return True
        else:
            return False
    
    
    #method to check funds
    def check_funds(self, amount):
        
        if amount - self.get_balance() > 0:
            return False
        else:
            return True
    
    
    #print string representation
    def __str__(self):
        
        num_of_stars = 30 - len(str(self.budget_cat))    
        
        output = "*"*(int(num_of_stars//2)) + str(self.budget_cat).title()
        
        output += '*'*(30-len(output))
        
        for x in self.ledger:
            
            #if full description fits
            if len("{:.2f}".format(x['amount']) + ' '+ str(x["description"])) < 30:
                output += '\n'+ str(x['description']) + ' '*(30-len("{:.2f}".format(x['amount'])+str(x['description']))) + "{:.2f}".format(x['amount'])
            
            #if full description needs to be cut off to fit
            else:
                output += '\n'+str(x['description'])[0:((30-len("{:.2f}".format(x['amount'])))-1)] + ' ' + "{:.2f}".format(x['amount'])
        
        #Print total line
        output += '\nTotal: '+ "{:.2f}".format(self.get_balance())
        
        return(output)




def create_spend_chart(categories):
    percentages = {}
    total = 0
    
    #find longest string length for category name to be used later
    max_char = 0
    
    for x in categories:
        total += x.withdraws
        percentages[f'{x.budget_cat}'] = x.withdraws 
        if len(str(x.budget_cat)) > max_char:
            max_char = len(str(x.budget_cat))

    for key in percentages:
        percentages[key] = percentages[key]/total
        
    output = 'Percentage spent by category\n'
    
    line = 100
    
    while line >= 0:
        add_line = (str(line)+ str('|')).rjust(4)
        for key in percentages:
            if int(percentages[key]*100) >= line:
                add_line += ' o '
            else:
                add_line += '   '
                
        add_line += ' \n'
        
        if line == 0:
            add_line += '    ' + "-"*(len(add_line)-5) + "\n"
            
        output += add_line    
        line = line - 10
    
    
    
    for i in range(0,max_char):
        output += ' '*4
        for k in range(0,len(list(percentages.keys()))):
            try:
                #if i == 0:
                    #output += f' {str(list(percentages.keys())[k][i]).upper()} '
                
                #else:
                output += f' {list(percentages.keys())[k][i]} '
            
            except:
                output += '   '
        
        if i < max_char-1:
            output += ' \n'
            
        else:
            output += ' '

    return(output)