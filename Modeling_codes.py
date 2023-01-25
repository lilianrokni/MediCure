#!/usr/bin/env python
# coding: utf-8

# In[39]:


from collections import namedtuple as nt
from docplex.mp.model import Model as md
import pandas as pd


# In[62]:


df =pd.read_excel("sampledata.xlsx",sheet_name = "Data_Table")
df


# In[63]:


data = df.loc[df['Category'].isin([0, 2])]


# In[64]:


FOODS = data.loc[:,['FoodName↓',"Energy (kcal)","MIN","MAX"]].values

print(FOODS)


# In[75]:


NUTRIENTS = [  
    ("Protein", 50, 100),
    ("Fat", 30, 100),
    ("Vitamin D", 100, 2000),
    ("Vitamin E", 100, 2000),
    ("Sum sugars", 30, 100),
    
]


# In[76]:


FOOD_NUTRIENTS = df.loc[:,['FoodName↓', '→ParameterName','Protein','Fat','Vitamin A','Sum sugars']].values
print(FOOD_NUTRIENTS)


# In[77]:


Food = nt("Food", ["name", "energy", "qmin", "qmax"])
Nutrient = nt("Nutrient", ["name", "qmin", "qmax"])


# In[78]:


def build_diet_model(name='diet', **kwargs):

    foods = [Food(*f) for f in FOODS]
    nutrients = [Nutrient(*row) for row in NUTRIENTS]

    food_nutrients = {(fn[0], nutrients[n].name):
                      fn[1 + n] for fn in FOOD_NUTRIENTS for n in range(len(NUTRIENTS))}                   
    # load model
    mdl = md(name=name, **kwargs)
 
    qty = mdl.var_dict(foods, mdl.integer_vartype, lb=lambda f: f.qmin, ub=lambda f: f.qmax, name=lambda f: "q_%s" % f.name)
    print('food quantity：',qty)
    for n in nutrients:
  
        amount = mdl.sum(qty[f] * food_nutrients[f.name, n.name] for f in foods)

        mdl.add_range(n.qmin, amount, n.qmax)
        print('nutrient name：={}  nutrient amount：={}'.format(n.name,amount))
    # compute the total cost of energy
    total_cost = mdl.sum(qty[f] * f.energy for f in foods)
    # define the objective function
    mdl.minimize(total_cost)

    return mdl


# In[95]:


if __name__ == '__main__':
    # Call model function Decision, variable is integer, output log file, floating point display precision 6 digits
    mdl = build_diet_model(ints=True, log_output=True, float_precision=6)

    # mdl.print_information()

    s = mdl.solve()
    if s:

        qty_vars = mdl.find_matching_vars(pattern="q_")
        print('qty_vars:',qty_vars)

        for fv in qty_vars:
  
            food_name = fv.name[2:]

            print("The diet should include {0:<25} = {1:9.6g}".format(food_name, fv.solution_value))

    else:
        print("* model has no solution")


# In[96]:


all_vars = s.iter_var_values()
print(all_vars)


# In[98]:


non_zero_vars = [fv for fv in qty_vars if fv.solution_value != 0]
non_zero_vars


# In[81]:


import matplotlib.pyplot as plt


# In[99]:


x = [fv.name for fv in non_zero_vars]
y = [fv.solution_value for fv in non_zero_vars]

plt.bar(x,y)
plt.show()


# In[106]:


menu=[x,y]
menu = dict(zip(menu[0],menu[1]))
print(menu)


# In[ ]:




