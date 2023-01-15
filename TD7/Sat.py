# -*- coding: utf-8 -*-
import random

class Sat:
      
  def __init__(self,n,L):
    self.nr_var=n   # variables are x1,...,xn
    self.clauses=L
    self.values=[True for i in range(n+1)] # position 0 in this list is not used
    self.fixed={}

  # Question 1
  
  def is_clause_satisfied(self,c):
        for x in c:
            if (x>0 and self.values[x]) or (x<0 and not self.values[-x]):
                return True
        return False
        
  def satisfied(self):
    for c in self.clauses:
        if not self.is_clause_satisfied(c):
            return False
    return True

  # Questions 2 & 8
  
  def initialize(self):
    '''
    only initialise non fixed variables
    :return:
    '''
    for i in range(1,self.nr_var+1):
        if not i in self.fixed:
            self.values[i]=random.choice([True,False])
      
  def walk_sat(self,N):
        self.clauses.sort(key=len)
        self.initialize()
        for i in range(N):
            for k in range(len(self.clauses)):
                if not self.is_clause_satisfied(self.clauses[k]):
                      choice_k = abs(random.choice(self.clauses[k]))
                      self.values[choice_k] = 1 - self.values[choice_k]
                      break
                if k==len(self.clauses)-1:
                    return True
        return False




   
  ##################################################
  # PROPAGATION METHODS
  ##################################################  

  # Question 6
  
  def fix_values_from_1clauses(self):
    '''
    pdates the dictionary self.fixed from the clauses of size 1 in the current CNF formula (stored in self.clauses),
    for instance if the current CNF formula contains the clause (x ̄4), then one has to add 4 to self.fixed assigning
    it to False (self.fixed[4]=False) and assign self.values[4]=False. The method also has to return a Boolean that indicates
    if at least one clause of size 1 has been found.
    :return:
    '''
    res=False
    for c in self.clauses:
        if len(c)==1:
            res=True
            self.fixed[abs(c[0])]=c[0]>0
            self.values[abs(c[0])]=c[0]>0
    return res
  # Helper functions for Question 7
  
  def simplify_clause(self,c):
    res=[]
    for x in c:
        if not abs(x) in self.fixed:
            res.append(x)
        else:
            if (x>0 and self.values[x]) or (x<0 and not self.values[-x]):
                return -1
    return res   

  def simplify_clauses(self):
    res=[]    
    for c in self.clauses:  
       cp=self.simplify_clause(c)
       if not cp==-1:
           res.append(cp)
    return res        

  # Question 7
  
  def simplify_formula_by_propagation(self):
    '''
    This method is used to simplify the current CNF formula (stored in self.clauses) by using the fixed values
    (stored in self.fixed). The method has to return a Boolean that indicates if the current CNF formula is still satisfiable.
    :return:
    '''
    while self.fix_values_from_1clauses():
        self.clauses=self.simplify_clauses()
    return self.satisfied()

  ##################################################
  # DISPLAY METHODS
  ##################################################                      
                                  
  def clause_to_string(self,c):
     res="" 
     for i in range(0,len(c)):
         if i==0: res="("
         else: res=res+" ∨ "
         if(c[i]>0): res=res+"x"+str(c[i])
         else: res=res+"¬x"+str(-c[i])
     return res+")"
     
  def display_statistics(self):
      print("Number of clauses: "+str(len(self.clauses)))
      print("Number of non-fixed variables: "+str(self.nr_var-len(self.fixed)))
      print("")

  def display_formula(self):
     L=self.clauses
     res=self.clause_to_string(L[0])
     for i in range(1,len(L)):     
         res=res+" ∧ "+self.clause_to_string(L[i])   
     print(res)    
              
  def display_values(self):
     res="" 
     for i in range(1,self.nr_var+1):
         res=res+"x"+str(i)+"="+str(self.values[i])+" "
     print(res)    

            
