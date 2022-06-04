#!/usr/bin/env python
# coding: utf-8

# In[5]:





# In[ ]:


# -*- coding: utf-8 -*-
def menu():
  print("Welcome to the Nubalancer program that balances your nutrients!")
  print("----------------------------<Menu>-----------------------------")
  print("1. Searching for Nutrients in Food")
  print("2. Calculate the total nutrients of the food you ate today and tell me the nutrients you ate insufficiently or too much today")
  print("3. exit")
  num = input("Select the menu what you want (ex. If you want to use menu 1, input 1): ")

  return num


# In[52]:


import requests
import pprint
import json
import pandas as pd
from pandas.io.json import json_normalize 


# In[53]:


# -*- coding: utf-8 -*-
def menu_1():
  import requests
  import pprint
  import json
  import pandas as pd
  from pandas.io.json import json_normalize 
  while(True):
    food_name = input("\ninput food name which you are eat: ")

    url = "http://openapi.foodsafetykorea.go.kr/api/92ed443e8f9b422cb63f/I2790/json/1/422/DESC_KOR=" + food_name

    try:
      response = requests.get(url)
    except requests.exceptions.HTTPError as errh:
      print ("Http Error:",errh)
      break
    except requests.exceptions.ConnectionError as errc:
      print ("Error Connecting:",errc)
      break
    except requests.exceptions.Timeout as errt:
      print ("Timeout Error:",errt)
      break
    except requests.exceptions.RequestException as err:
      print ("OOps: Something Else",err)
      break

    contents = response.text
      
    pp = pprint.PrettyPrinter(indent = 4)
    #print(pp.pprint(contents))

    json_ob = json.loads(contents)
    # Encourage them to re-enter if there are no search results
    if(json_ob['I2790']['total_count'] == '0'):
      print("There is no food name \""+food_name+"\" in the database")
      print("\nPlease, enter the name of the food again\n")
      continue
    else: 
      body = json_ob['I2790']['row']  
      dataframe = json_normalize(body)
      #Data processing
      data = dataframe.rename(columns={'NUTR_CONT3':'단백질(g)','NUTR_CONT8':'포화지방산(g)','NUTR_CONT9':'트랜스지방(g)','NUTR_CONT4':'지방(g)','NUTR_CONT5':'당류(g)','NUTR_CONT6':'나트륨(mg)','NUTR_CONT7':'콜레스테롤(mg)','NUTR_CONT1':'열량(kcal)','NUTR_CONT2':'탄수화물(g)','DESC_KOR':'상품명'})
      data = data[['상품명', '탄수화물(g)', '단백질(g)', '지방(g)', '당류(g)', '나트륨(mg)','포화지방산(g)','트랜스지방(g)', '콜레스테롤(mg)', '열량(kcal)']]
      #show the list of the food
      print(data)
      break
  

  print("If you want to go to the menu, please press Enter!")
  input()
  
  


# In[54]:


def menu_2():
  import requests
  import pprint
  import json
  import pandas as pd
  from pandas.io.json import json_normalize 
  # To set data frames to show data in all rows
  pd.set_option('display.max_rows',None)

  columns = ['탄수화물(g)', '단백질(g)', '지방(g)', '당류(g)', '나트륨(mg)','포화지방산(g)','트랜스지방(g)', '콜레스테롤(mg)', '열량(kcal)']
  index = ['Sum']

  #Dataframe containing information on the user's nutritional content
  user_info = pd.DataFrame(columns = columns, index = index)
  user_info = user_info.fillna(0)
  #Gender and age of users to distinguish nutrient intake criteria by gender and age
  while(True):
    sex = input("당신의 성은 male인가요 female인지 알려주세요(ex. male)")
    if sex != 'male' and sex !='female' :
      print("male 또는 female을 다시 입력해주세요!")
      continue
    age = int(input("당신의 나이를 숫자로 적어주세요(age는 6 이상으로 입력해주세요)"))
    if age<6:
      print("age를 6이상으로 입력해주세요!")
      continue
    else:
      break

  while(True):
    #Get the name of the food you ate
    food_name = input("input food name which you are eat(After entering the name of the food, please enter 'done')")
  #If the user enters 'done', escape the loop.
    if(food_name == "done"):
      break
  #url to get Open API 
    url = "http://openapi.foodsafetykorea.go.kr/api/92ed443e8f9b422cb63f/I2790/json/1/422/DESC_KOR=" + food_name

    try:
      response = requests.get(url)
    except requests.exceptions.HTTPError as errh:
      print ("Http Error:",errh)
      break
    except requests.exceptions.ConnectionError as errc:
      print ("Error Connecting:",errc)
      break
    except requests.exceptions.Timeout as errt:
      print ("Timeout Error:",errt)
      break
    except requests.exceptions.RequestException as err:
      print ("OOps: Something Else",err)
      break

    contents = response.text
    
    pp = pprint.PrettyPrinter(indent = 4)
    #print(pp.pprint(contents))

    json_ob = json.loads(contents)
    # Encourage them to re-enter if there are no search results
    if(json_ob['I2790']['total_count'] == '0'):
      print("There is no food name \""+food_name+"\" in the database")
      print("\nPlease, enter the name of the food again\n")
      continue
    else:
      
      body = json_ob['I2790']['row']
      
      dataframe = json_normalize(body)
      #Data processing
      data = dataframe.rename(columns={'NUTR_CONT3':'단백질(g)','NUTR_CONT8':'포화지방산(g)','NUTR_CONT9':'트랜스지방(g)','NUTR_CONT4':'지방(g)','NUTR_CONT5':'당류(g)','NUTR_CONT6':'나트륨(mg)','NUTR_CONT7':'콜레스테롤(mg)','NUTR_CONT1':'열량(kcal)','NUTR_CONT2':'탄수화물(g)','DESC_KOR':'상품명'})
      data = data[['상품명', '탄수화물(g)', '단백질(g)', '지방(g)', '당류(g)', '나트륨(mg)','포화지방산(g)','트랜스지방(g)', '콜레스테롤(mg)', '열량(kcal)']]
    #Output search results
      print(data)
    #Enter the index to get accurate food information, and choose a specific food
      index_num = int(input("\nInput the food index number(ex. 0~n): "))
      food_info = list(data.iloc[index_num,1:])
      food_info = pd.DataFrame([food_info], columns = columns)
      food_info = food_info.replace('',0)
      user_info = user_info.append(food_info).astype(float)

  #Total for each nutrient, output the user's total daily nutrient intake
  nutrient_sum = pd.DataFrame([user_info.sum()], columns = columns, index = ['total'])
  user_info = user_info.append(nutrient_sum)
  print("\nThe total amount of nutrients you ate today\n")
  print(user_info.loc['total'])

  if sex == "male":
    #Classifying Calorie Intake Criteria by User's Age
    if age >=6 and age <=8:
    #Calories
      if user_info.at['total','열량(kcal)'] < 1650.0 :
        kcal = 1700 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >1750 :
        kcal = user_info.at['total','열량(kcal)']-1700.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
      #Protein
      if user_info.at['total','단백질(g)'] <30:
        protein = 35.0- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(round(protein,2))+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >40:
        protein = user_info.at['total','단백질(g)'] -35.0
        print("단백질 1일 권장 섭취량보다 " +str(round(protein,2))+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")
    
    elif age>=9 and age <=11:
      #Calories
      if user_info.at['total','열량(kcal)'] < 1950.0 :
        kcal = 2000.0 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2050 :
        kcal = user_info.at['total','열량(kcal)']-2000.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
    #Protein
      if user_info.at['total','단백질(g)'] <45:
        protein = 50- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(round(protein,2))+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >55:
        protein = user_info.at['total','단백질(g)'] -50
        print("단백질 1일 권장 섭취량보다 " +str(round(protein,2))+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")
      
    elif age>=12 and age <=14:
        #Calories
      if user_info.at['total','열량(kcal)'] < 2450.0 :
        kcal = 2500 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2550 :
        kcal = user_info.at['total','열량(kcal)']-2500.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <55:
        protein = 60- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >65:
        protein = user_info.at['total','단백질(g)'] -60
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")
    
    elif age>=15 and age <=18:
        #Calories
      if user_info.at['total','열량(kcal)'] < 2650.0 :
        kcal = 2700 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2750 :
        kcal = user_info.at['total','열량(kcal)']-2700.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")        
        #Protein
      if user_info.at['total','단백질(g)'] <60:
        protein = 65- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >70:
        protein = user_info.at['total','단백질(g)'] -65
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")

    elif age>=19 and age <=29:
        #Calories
      if user_info.at['total','열량(kcal)'] < 2550.0 :
        kcal = 2600 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2650 :
        kcal = user_info.at['total','열량(kcal)']-2600.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <60:
        protein = 65- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >70:
        protein = user_info.at['total','단백질(g)'] -65
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")      
      
    elif age>=30 and age <=49:
        #Calories
      if user_info.at['total','열량(kcal)'] < 2450.0 :
        kcal = 2500 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2550 :
        kcal = user_info.at['total','열량(kcal)']-2500.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <60:
        protein = 65- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >70:
        protein = user_info.at['total','단백질(g)'] -65
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")        
      
    elif age>=50 and age <=64:
        #Calories
      if user_info.at['total','열량(kcal)'] < 2150.0 :
        kcal = 2200 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2250 :
        kcal = user_info.at['total','열량(kcal)']-2200.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <55:
        protein = 60- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >65:
        protein = user_info.at['total','단백질(g)'] -60
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")

    elif age>=65 and age <=74:
        #Calories
      if user_info.at['total','열량(kcal)'] < 1950.0 :
        kcal = 2000 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2050 :
        kcal = user_info.at['total','열량(kcal)']-2000.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <55:
        protein = 60- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >65:
        protein = user_info.at['total','단백질(g)'] -60
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")

    elif age>=75:
        #Calories
      if user_info.at['total','열량(kcal)'] < 1850.0 :
        kcal = 1900 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >1950 :
        kcal = user_info.at['total','열량(kcal)']-1900.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <55:
        protein = 60- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >65:
        protein = user_info.at['total','단백질(g)'] -60
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")
        

  if sex == "female":
    #Classifying Calorie Intake Criteria by User's Age
    if age >=6 and age <=8:
      if user_info.at['total','열량(kcal)'] < 1450.0 :
        kcal = 1500.0 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >1550 :
        kcal = user_info.at['total','열량(kcal)']-1500.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <30:
        protein = 35.0- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >40:
        protein = user_info.at['total','단백질(g)'] -35
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")
    
    elif age>=9 and age <=11:
      if user_info.at['total','열량(kcal)'] < 1750.0 :
        kcal = 1800.0 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >1850 :
        kcal = user_info.at['total','열량(kcal)']-1800.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <40:
        protein = 45.0 - user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >50:
        protein = user_info.at['total','단백질(g)'] -45.0
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")

    elif age>=12 and age <=14:
      if user_info.at['total','열량(kcal)'] < 1950.0 :
        kcal = 2000.0 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2050 :
        kcal = user_info.at['total','열량(kcal)']-2000.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <50:
        protein = 55.0 - user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >60:
        protein = user_info.at['total','단백질(g)'] -55.0
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")

    elif age>=15 and age <=18:
      if user_info.at['total','열량(kcal)'] < 1950.0 :
        kcal = 2000.0 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2050 :
        kcal = user_info.at['total','열량(kcal)']-2000.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <50:
        protein = 55- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >60:
        protein = user_info.at['total','단백질(g)'] -55
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")

    elif age>=19 and age <=29:
      if user_info.at['total','열량(kcal)'] < 1950.0 :
        kcal = 2000 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >2050 :
        kcal = user_info.at['total','열량(kcal)']-2000.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
        #Protein
      if user_info.at['total','단백질(g)'] <50:
        protein = 55- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >60:
        protein = user_info.at['total','단백질(g)'] -55
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")

    elif age>=30 and age <=49:
      if user_info.at['total','열량(kcal)'] < 1850.0 :
        kcal = 1900 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >1950 :
        kcal = user_info.at['total','열량(kcal)']-1900.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
      #Protein
      if user_info.at['total','단백질(g)'] <45:
        protein = 50- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >55:
        protein = user_info.at['total','단백질(g)'] -50
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")
    
    elif age>=50 and age <=64:
      if user_info.at['total','열량(kcal)'] < 1650.0 :
        kcal = 1700 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >1750 :
        kcal = user_info.at['total','열량(kcal)']-1700.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
      #Protein
      if user_info.at['total','단백질(g)'] <45:
        protein = 50- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >55:
        protein = user_info.at['total','단백질(g)'] -50
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")

    elif age>=65 and age <=74:
      if user_info.at['total','열량(kcal)'] < 1550.0 :
        kcal = 1600 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >1650 :
        kcal = user_info.at['total','열량(kcal)']-1600.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
      #Protein
      if user_info.at['total','단백질(g)'] <45:
        protein = 50- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >55:
        protein = user_info.at['total','단백질(g)'] -50
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")
    elif age>=75:
      if user_info.at['total','열량(kcal)'] < 1450.0 :
        kcal = 1500 - user_info.at['total','열량(kcal)']
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 부족합니다.")
      elif user_info.at['total','열량(kcal)'] >1550 :
        kcal = user_info.at['total','열량(kcal)']-1500.0
        print("열량 1일 권장 섭취량보다" +str(round(kcal,2))+" kcal 만큼 초과합니다.")
      else :
        print("1일 영양소 권장 섭취량 기준 범위 이내로 열량(kcal)을 섭취하였습니다!")
      #Protein
      if user_info.at['total','단백질(g)'] <45:
        protein = 50- user_info.at['total','단백질(g)']
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 부족합니다.")
      elif user_info.at['total','단백질(g)'] >55:
        protein = user_info.at['total','단백질(g)'] -50
        print("단백질 1일 권장 섭취량보다 " +str(protein)+"g 만큼 초과합니다.")
      else: 
        print("1일 영양소 권장 섭취량 기준 범위 이내로 단백질(g)을 섭취하였습니다!")

  #Carbohydrate
  if user_info.at['total','탄수화물(g)']<125:
    carbohydrate = 130.0- user_info.at['total','탄수화물(g)']
    print("탄수화물 1일 권장 섭취량보다 "+ str(round(carbohydrate,2)) +"g 만큼 부족합니다.")
  elif user_info.at['total','탄수화물(g)'] >135:
    carbohydrate = user_info.at['total','탄수화물(g)'] -130.0
    print("탄수화물 1일 권장 섭취량보다 "+ str(round(carbohydrate,2)) +"g 만큼 초과합니다.")
  else :
    print("1일 영양소 권장 섭취량 기준 범위 이내로 탄수화물(g)을 섭취하였습니다!")

  #Fat
  if user_info.at['total','지방(g)']<45:
    fat = 50- user_info.at['total','지방(g)']
    print("지방 1일 권장 섭취량보다 "+ str(round(fat,2)) +"g 만큼 부족합니다.")
  elif user_info.at['total','지방(g)'] >65:
    fat = user_info.at['total','지방(g)'] -50.0
    print("지방 1일 권장 섭취량보다 "+ str(round(fat,2)) +"g 만큼 초과합니다.")
  else :
    print("1일 영양소 권장 섭취량 기준 범위 이내로 지방(g)을 섭취하였습니다!")

  #Sugars
  if user_info.at['total','당류(g)'] > 55.0:
    sugars = user_info.at['total', '당류(g)'] -50.0
    print("당류 1일 권장 섭취량보다 "+ str(round(sugars,2)) +"g 만큼 초과합니다.")
  else:
    print("1일 영양소 권장 섭취량 기준 범위 이내로 당류(g)을 섭취하였습니다!")  

  #Saturated fatty acid
  if user_info.at['total','포화지방산(g)'] > 15.0:
    saturated_FA = user_info.at['total', '포화지방산(g)'] -15.0
    print("포화지방산 1일 권장 섭취량보다 "+ str(round(saturated_FA,2)) +"g 만큼 초과합니다.")
  else:
    print("1일 영양소 권장 섭취량 기준 범위 이내로 포화지방산(g)을 섭취하였습니다!") 

  #Trans fatty acid
  if user_info.at['total','트랜스지방(g)'] > 2.2:
    trans_FA = user_info.at['total', '트랜스지방(g)'] -2.0
    print("트랜스지방 1일 권장 섭취량보다 "+ str(round(trans_FA,2)) +"g 만큼 초과합니다.")
  else:
    print("1일 영양소 권장 섭취량 기준 범위 이내로 트랜스지방(g)을 섭취하였습니다!")

  #Cholesterol
  if user_info.at['total','콜레스테롤(mg)'] > 250.0:
    Cholesterol = user_info.at['total', '콜레스테롤(mg)'] - 250.0
    print("콜레스테롤 1일 권장 섭취량보다 "+ str(round(Cholesterol,2)) +"mg 만큼 초과합니다.")
  else:
    print("1일 영양소 권장 섭취량 기준 범위 이내로 콜레스테롤(mg)을 섭취하였습니다!") 
  #Sodium
  if age >=6 and age <=8:
    if user_info.at['total','나트륨(mg)'] < 1150.0 :
      sodium = 1200 - user_info.at['total','나트륨(mg)']
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 부족합니다.")
    elif user_info.at['total','나트륨(mg)'] >1250 :
      sodium = user_info.at['total','나트륨(mg)']-1200.0
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 초과합니다.")
    else :
      print("1일 영양소 권장 섭취량 기준 범위 이내로 나트륨(mg)을 섭취하였습니다!")
    
  elif age>=9 and age <=11:
    if user_info.at['total','나트륨(mg)'] < 1450.0 :
      sodium = 1500 - user_info.at['total','나트륨(mg)']
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 부족합니다.")
    elif user_info.at['total','나트륨(mg)'] >1550 :
      sodium = user_info.at['total','나트륨(mg)']-1500.0
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 초과합니다.")
    else :
      print("1일 영양소 권장 섭취량 기준 범위 이내로 나트륨(mg)을 섭취하였습니다!")

  elif age>=12 and age <=14:
    if user_info.at['total','나트륨(mg)'] < 1450.0 :
      sodium = 1500 - user_info.at['total','나트륨(mg)']
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" kcal 만큼 부족합니다.")
    elif user_info.at['total','나트륨(mg)'] >1550 :
      sodium = user_info.at['total','나트륨(mg)']-1500.0
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" kcal 만큼 초과합니다.")
    else :
      print("1일 영양소 권장 섭취량 기준 범위 이내로 나트륨(mg)을 섭취하였습니다!")

  elif age>=15 and age <=18:
    if user_info.at['total','나트륨(mg)'] < 1450.0 :
      sodium = 1500 - user_info.at['total','나트륨(mg)']
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 부족합니다.")
    elif user_info.at['total','나트륨(mg)'] >1550 :
      sodium = user_info.at['total','나트륨(mg)']-1500.0
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 초과합니다.")
    else :
      print("1일 영양소 권장 섭취량 기준 범위 이내로 나트륨(mg)을 섭취하였습니다!")

  elif age>=19 and age <=29:
    if user_info.at['total','나트륨(mg)'] < 1450.0 :
      sodium = 1500 - user_info.at['total','나트륨(mg)']
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 부족합니다.")
    elif user_info.at['total','나트륨(mg)'] >1550 :
      sodium = user_info.at['total','나트륨(mg)']-1500.0
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 초과합니다.")
    else :
      print("1일 영양소 권장 섭취량 기준 범위 이내로 나트륨(mg)을 섭취하였습니다!")

  elif age>=30 and age <=49:
    if user_info.at['total','나트륨(mg)'] < 1450.0 :
      sodium = 1500 - user_info.at['total','나트륨(mg)']
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 부족합니다.")
    elif user_info.at['total','나트륨(mg)'] >1550 :
      sodium = user_info.at['total','나트륨(mg)']-1500.0
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 초과합니다.")
    else :
      print("1일 영양소 권장 섭취량 기준 범위 이내로 나트륨(mg)을 섭취하였습니다!")
    
  elif age>=50 and age <=64:
    if user_info.at['total','나트륨(mg)'] < 1450.0 :
      sodium = 1500 - user_info.at['total','나트륨(mg)']
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 부족합니다.")
    elif user_info.at['total','나트륨(mg)'] >1550 :
      sodium = user_info.at['total','나트륨(mg)']-1500.0
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" mg 만큼 초과합니다.")
    else :
      print("1일 영양소 권장 섭취량 기준 범위 이내로 나트륨(mg)을 섭취하였습니다!")

  elif age>=65 and age <=74:
    if user_info.at['total','나트륨(mg)'] < 1250.0 :
      sodium = 1300 - user_info.at['total','나트륨(mg)']
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" kcal 만큼 부족합니다.")
    elif user_info.at['total','나트륨(mg)'] >1350 :
      sodium = user_info.at['total','나트륨(mg)']-1300.0
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" kcal 만큼 초과합니다.")
    else :
      print("1일 영양소 권장 섭취량 기준 범위 이내로 나트륨(mg)을 섭취하였습니다!")

  elif age>=75:
    if user_info.at['total','나트륨(mg)'] < 1050.0 :
      sodium = 1100 - user_info.at['total','나트륨(mg)']
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" kcal 만큼 부족합니다.")
    elif user_info.at['total','나트륨(mg)'] >1150 :
      sodium = user_info.at['total','나트륨(mg)']-1100.0
      print("나트륨 1일 권장 섭취량보다" +str(round(sodium,2))+" kcal 만큼 초과합니다.")
    else :
      print("1일 영양소 권장 섭취량 기준 범위 이내로 나트륨(mg)을 섭취하였습니다!")
  
  print("If you want to go to the menu, please press Enter!")
  input()


# In[55]:


# -*- coding: utf-8 -*-
#Main body
while(True):
  option = menu()
 
  if option == "1" or option == "2" or option == "3" :
    if option =="1":
      menu_1()
 
    elif option =="2":
      menu_2()
 
    else :
      print("Bye!")
      break
  else:
    print("\nOptionError: Please check if you entered the option correctly!\n")
    continue;

