#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install py_edamam


# In[ ]:


pip install flask


# In[ ]:


from IPython.display import display
from IPython.display import HTML
from IPython.display import IFrame
from IPython.display import FileLinks
from IPython.core.display import Javascript


# In[ ]:


import requests
import pandas as pd
import pandas.io.json as json_normalize
from ipywidgets import widgets
from py_edamam import PyEdamam


# In[ ]:


HTML("<script src='main.js'></script> <link rel='stylesheet' type='text/css' href='index.html'>")


# In[ ]:


get_ipython().run_cell_magic('javascript', '', 'require(["main.js"])')


# In[ ]:


dietLabels = ["balanced","high-fiber","high-protein","low-carb","low-fat","low-sodium"]

healthLabels = ["dairy-free","egg-free","fish-free","gluten-free","immuno-supportive",
"keto-friendly","kidney-friendly","kosher","low-potassium","low-sugar","no-oil-added",
"paleo","peanut-free","pescatarian","pork-free","red-meat-free","shellfish-free",
"soy-free","tree-nut-free","vegan","vegetarian","wheat-free"]

cuisineType = ["American", "Asian", "Caribbean", "Central Europe", "Chinese", 
"Eastern Europe", "French", "Indian", "Italian", "Japanese", "Kosher", "Mediterranean", 
"Mexican", "Middle Eastern", "Nordic", "South American", "South East Asian"]


# In[ ]:


dietSelection = widgets.SelectMultiple(
    options=dietLabels,
    value=['balanced'],
    #rows=10,
    description='Diet Labels - *Select multiple labels by holding shift and left-clicking all the labels needed',
    disabled=False
)

healthSelection = widgets.SelectMultiple(
    options=healthLabels,
    value=['dairy-free'],
    #rows=10,
    description='Health Label',
    disabled=False
)

cuisineSelection = widgets.SelectMultiple(
    options=cuisineType,
    value=['American'],
    #rows=10,
    description='Cuisine Type',
    disabled=False
) 

display(dietSelection)
display(healthSelection)
display(cuisineSelection)


# In[ ]:


dietSelection1 = dietSelection.value
dietSelectionValue = ' '.join(dietSelection1)
dietSelectionValue = dietSelectionValue.replace("'", "")

healthSelection1 = healthSelection.value 
healthSelectionValue = ' '.join(healthSelection1)
healthSelectionValue = healthSelectionValue.replace("'", "")
    
cuisineSelection1 = cuisineSelection.value 
cuisineSelectionValue = ' '.join(cuisineSelection1)
cuisineSelectionValue = cuisineSelectionValue.replace("'", "")

#print(dietSelectionValue)
#print(healthSelectionValue)
#print(cuisineSelectionValue)


# In[ ]:


# Create a text field for specific ingredient restriction
ingredient_restriction_text = widgets.Text(
    value='',
    placeholder='Enter specific ingredient restriction',
    description='Ingredient Restriction:',
    disabled=False
)

display(ingredient_restriction_text)


# In[ ]:


excluded = ingredient_restriction_text.value
    #print(excluded)
excluded_list = excluded.split(",")
    #print(excluded_list)
      
if len(excluded_list) >= 1:
    excluded = excluded_list[0]
    excluded = excluded.strip()
else: 
    excluded = ''
if len(excluded_list) >= 2:
    excluded1 = excluded_list[1]
    excluded1 = excluded1.strip()
else: 
    excluded1 = ''
if len(excluded_list) >= 3:
    excluded2 = excluded_list[2]
    excluded2 = excluded2.strip()
else: 
    excluded2 = ''
    


# In[ ]:


#API Request Parameters

edamam_id = "5f36f0d2"
edamam_key = "36183fb32a466e53e994a472a4934d20"

base_url = "https://api.edamam.com"
recipes_path = "/api/recipes/v2"
qType = "public"
query = "chicken"


# In[ ]:


def myFunction(dietSelectionValue, healthSelectionValue, cuisineSelectionValue):
    base_url = "https://api.edamam.com"
    recipes_path = "/api/recipes/v2"
    edamam_id = "5f36f0d2"
    edamam_key = "36183fb32a466e53e994a472a4934d20"
    qType = "public"
    url = f"{base_url}{recipes_path}?type={qType}&app_id={edamam_id}&app_key={edamam_key}&diet={dietSelectionValue}&health={healthSelectionValue}&cuisineType={cuisineSelectionValue}"
    response = requests.get(url)
    data = response.json()
    hits = data['hits']
    filtered_hits = [{'label': hit['recipe']['label'],
                  'dietLabels': hit['recipe']['dietLabels'],
                  'healthLabels': hit['recipe']['healthLabels'],
                  'ingredients': [{'food': ingredient['food'], 'quantity': ingredient['quantity']} for ingredient in hit['recipe']['ingredients']],
                  'calories': hit['recipe']['calories'],
                  'cuisineType': hit['recipe']['cuisineType']
                  } for hit in hits]
    recipeDisplay = filtered_hits[1:5]
    display(recipeDisplay)


# In[ ]:


myFunction(dietSelectionValue, healthSelectionValue, cuisineSelectionValue)


# In[ ]:


get_ipython().run_cell_magic('javascript', '', 'data = display(data)\nmyFunction(data);\n\n%%javascript\ndocument.getElementById("output").innerHTML = JSON.stringify(data);')


# In[ ]:


url = f"{base_url}{recipes_path}?type={qType}&app_id={edamam_id}&app_key={edamam_key}&diet={dietSelectionValue}&health={healthSelectionValue}&cuisineType={cuisineSelectionValue}"
response = requests.get(url)
data = response.json()


# In[ ]:


hits = data['hits']


# In[ ]:


#NUTRITION CONSTRAINTS 

# Create a dropdown menu for gender
gender_dropdown = widgets.Dropdown(
    options=['M', 'F'],
    value='M',
    description='Gender:',
    disabled=False,
)

# Create a dropdown menu for activity level
activity_level_dropdown = widgets.Dropdown(
    options=['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'],
    value='Sedentary',
    description='Activity Level:',
    disabled=False,
)

# Create a dropdown menu for body type
body_type_dropdown = widgets.Dropdown(
    options=['Ectomorph', 'Mesomorph', 'Endomorph'],
    value='Ectomorph',
    description='Body Type:',
    disabled=False,
)

# Create a dropdown menu for goal
goal_dropdown = widgets.Dropdown(
    options=['Lose', 'Maintain', 'Gain'],
    value='Maintain',
    description='Goal:',
    disabled=False,
)

height = float(input("Enter your height in inches: "))
weight = float(input("Enter your weight in pounds: "))
age = float(input("Enter your age in years: "))


# Display the dropdown menu and text fields
display(gender_dropdown)
display(activity_level_dropdown)
display(body_type_dropdown)
display(goal_dropdown)


# In[ ]:


gender = gender_dropdown.value
age = int(age)
activity_level = activity_level_dropdown.value
body_type = body_type_dropdown.value
goal = goal_dropdown.value

if gender.upper() == "M":
    # Harris-Benedict equation for men
    bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
elif gender.upper() == "F":
    # Harris-Benedict equation for women
    bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
else:
    print("Invalid input for gender")

# Use the BMR to calculate macro needs

if activity_level == "Sedentary":
    bmr *= 1.2
elif activity_level == "Light":
    bmr *= 1.375
elif activity_level == "Moderate":
    bmr *= 1.55
elif activity_level == "Active":
    bmr *= 1.725
else:
    print("Invalid input for activity level")

# Adjust the calories based on the user's goal
if goal == "Lose":
    bmr -= 250
elif goal == "Gain":
    bmr += 250
else:
    pass

# Calculate macro needs based on the adjusted calories
carbohydrates = bmr * 0.45 / 4
fats = bmr * 0.25 / 9
proteins = bmr * 0.3 / 4

# Print the macro and calorie needs
print("Calories: ",bmr)
print("Carbohydrates: ",carbohydrates)
print("Fats: ",fats)
print("Proteins: ",proteins)

