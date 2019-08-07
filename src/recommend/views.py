from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
from .forms import CuisineForm
from .models import Cuisine
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import math
import json
import pickle
import random
from gensim import models
from gensim import matutils
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
from nltk.tokenize import sent_tokenize
import glob
import argparse
import os
from operator import itemgetter

dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path2business = os.path.join(dirname, 'recommend/yelp_academic_dataset_business.json')
path2review= os.path.join(dirname, 'recommend/yelp_academic_dataset_review.json')
best_indian = ['Paneer Butter Masala',  'Dum Biryani', 'Masala Dosa', 'Vada Pao', 'Garlic Naan', 'Vegetable Kurma', 'Vegetable Samosa', 'Spinach Pakoda', 'Bhindi Masala', 'Tomato Rice', 'Vegetable Thali']
best_chinese = ['Noodle Soup', 'Chow Mein', 'Kung Pao Chicken', 'Ma Po Tofu', 'Dim Sum', 'Mongolian Beef', 'Dumplings', 'Wontons', 'Hot and Sour soup', 'Roast Duck', 'Peking Duck', 'Shao Mai', 'Radish Cakes', 'Egg Tart']


# Create your views here.

#Sadhana's changes
def cuisine_input_view(request):
	form = CuisineForm(request.POST or None)

	if form.is_valid():
		#form.save()
		#After saving it, remove the previous values
		#form = ProductForm()
		cuisine = form.cleaned_data['cuisine']
		print("Sadhana, The cuisine you have entered is ",cuisine)

		cuisine_view(request, cuisine)
		#if cuisine == 'Indian':
			#return HttpResponse("<H1> The top five dishes in Indian cuisine are: </H1> ")
			#return redirect(request, "cuisines/cuisine_dishes.html", context)
		#elif cuisine == 'Chinese':
			#return HttpResponse("<H1> The top five dishes in Chinese cuisine are: </H1> ")

	context = {
		'form': form
	}
	return render(request, "cuisines/cuisine_create.html", context)

def cuisine_dishes_view(request):
	#template = loader.get_template("cuisines/cusine_dishes.html")
	#return HttpRespones("The top five dishes in %s are " %cuisineName)
	form = CuisineForm(request.GET or None)
	cuisineName=None
	if request.GET.get('cuisine'):
		cuisineName = request.GET.get('cuisine')
	return render(request, 'cuisines/cuisine_dishes.html', {'cuisineName': cuisineName})

def cuisine_view(request):
	#form = CuisineForm(request.GET or None)
	return render(request, 'cuisines/cuisine_create.html')

#TODO : Change this to the actual URL once you have hosted it.
def cuisine_absolute_view(request):
    return redirect('http//127.0.0.1:8000/cuisine/')

def displayRestaurantsForCuisine(request):
	c = request.GET["cuisineNameInput"]
	zipcode = request.GET["zipcode"]
	#d will be the list of restaurants.
	d = []
	#d = top3Dishes(c)
	d = top3Restaurants(c, zipcode)

	if ( d != None and len(d) >= 6):
		d1 = d[0]
		d2 = d[1]
		d3 = d[2]
		d4 = d[3]
		d5 = d[4]
		d6 = d[5]
	elif ( d != None and len(d) >= 4 and len(d) < 6):
		d1 = d[0]
		d2 = d[1]
		d3 = d[2]
		d4 = d[3]
		d5 = ''
		d6 = ''
	elif (d != None and len(d) >= 2 and len(d) < 4):
		d1 = d[0]
		d2 = d[1]
		d3 = ''
		d4 = ''
		d5 = ''
		d6 = ''
	else:
		#d1 = 'Unfortunately, we do not have a recommended list for this zipcode based on our yelp reviews dataset'
		#d2 = ''
		#d3 = ''
		#d4 = ''
		#d5 = ''
		#d6 = ''
		return render(request, 'cuisines/zipcodeError.html')
	return render(request, 'cuisines/cuisine_restaurant.html', {'cuisineName': c, 'zipcode':zipcode, 'd1' : d1, 'd2' : d2, 'd3' :d3, 'd4' : d4, 'd5' : d5, 'd6' :d6})

def thankyou_view(request):
	return render(request, 'cuisines/thankyou.html')

def YesDishes(request):
	#cuisine = request.GET["cuisineNameInput"]
	#cuisine = "Indian"
	#cuisine = request.GET["cuisineNameYesDishes"]
	#print("**** Hey SAdhana, I am inside YesDishes and i am getting the cuisine value for cuisineNameYesDishes as ", cuisine)
	c2 = request.GET["cid"]
	z2 = request.GET["zid"]

	#d2 = getDishList(c2, z2)
	return render(request, 'cuisines/cuisine_dishes.html', { 'dish1' : 'Dum Biryani', 'dish2' : 'Paneer Butter Masala', 'dish3' : 'Garlic Naan', 'dish4' : 'Bhindi Masala', 'dish5' : 'Vegetable Samosa' ,'dish6' : 'Chicken 65'})
	"""
	if ( d2 != None and len(d2) >= 6):
		dish1 = d2[0]
		dish2 = d2[1]
		dish3 = d2[2]
		dish4 = d2[3]
		dish5 = d2[4]
		dish6 = d2[5]
	elif ( d2 != None and len(d2) >= 4 and len(d2) < 6):
		dish1 = d2[0]
		dish2 = d2[1]
		dish3 = d2[2]
		dish4 = d2[3]
		dish5 = ''
		dish6 = ''
	elif (d2 != None and len(d2) >= 2 and len(d2) < 4):
		dish1 = d2[0]
		dish2 = d2[1]
		dish3 = ''
		dish4 = ''
		dish5 = ''
		dish6 = ''
	else:
		return render(request, 'cuisines/cuisine_dishes.html', { 'dish1' : 'Dum Biryani', 'dish2' : 'Paneer Butter Masala', 'dish3' : 'Garlic Naan', 'dish4' : 'Bhindi Masala', 'dish5' : 'Vegetable Samosa' ,'dish6' : 'Chicken 65'})
		#d1 = 'Unfortunately, we do not have a recommended list for this zipcode based on our yelp reviews dataset'
		#d2 = ''
		#d3 = ''
		#d4 = ''
		#d5 = ''
		#d6 = ''
		#return render(request, 'cuisines/zipcodeError.html')


	return render(request, 'cuisines/cuisine_dishes.html', { 'dish1' : dish1, 'dish2' : dish2, 'dish3' : dish3, 'dish4' : dish4, 'dish5' : dish5 ,'dish6' : dish6})
	#return render(request, 'cuisines/thankyou.html')"""


def NoDishes(request):
	return render(request, 'cuisines/thankyou.html')

def top3Dishes(cuisineName):
	print("Inside top3Dishes function... the cuisine passed is ", cuisineName)
	dishList = ['chicken', 'rice', 'mango lassi']
	if cuisineName == 'Indian':
		#TODO : Plugin the processing logic to get top dishes for a given cuisine (Kapils code)
		#for now hardcoding the list of dishes
		dishList = ['Saag', 'Paneer', 'Dosa']
	elif cuisineName == 'Chinese':
		dishList = ['Noodlesoup', 'bokchoi', 'dim sum']
	elif cuisineName == 'Thai':
		dishList = ['Pad Thai', 'Spring roll', 'thai wrap']	

	return dishList

def getKeysByValue(dictOfElements, valueToFind):
	listOfKeys = list()
	listOfItems = dictOfElements.items()
	zip_code = valueToFind
	for item  in listOfItems:
		if item[1][2] == zip_code:
			listOfKeys.append(item[0])
	return  listOfKeys


def restaurant_details(cusine,pathtofile):
	cusine = cusine
	path2buisness = pathtofile
	cat2ridMain = {}
	categories = set([])
	restaurant_ids = set([])
	cat2rid = {}
	rest2rate={}
	rest2revID = {}
	r = 'Restaurants'
	with open (path2buisness, 'r') as f:
		for line in f.readlines():
			business_json = json.loads(line)
			bjc = business_json['categories']
			if r in bjc:
				if len(bjc) > 1:
					for cat in bjc:
						if cat.lower()  == cusine.lower():
							restaurant_ids.add(business_json['business_id'])
							categories = set(bjc).union(categories) - set([r])
							stars = business_json['stars']
							res_name = business_json['name']
							address = business_json['full_address']
							address_list = list(address.split(' '))
							zip_code = address_list[-1]
							rest2rate[ business_json['business_id'] ] = [res_name,stars,zip_code,address]
					
	return rest2rate

def top3Restaurants(cuisine, zipcode):
	output = restaurant_details(cuisine, path2business)
	resperzip = getKeysByValue(output,zipcode)
	res4cuisine = []
	for i in range(len(resperzip)):
		res4cuisine.append(output[resperzip[i]])
	
	res4cuisine_sorted = sorted(res4cuisine, key=itemgetter(1), reverse=True)
	#print(f"The top resturants serving {val1} in zipcode {val2} are:" )
	res_recommendation = res4cuisine_sorted[:3]
	
	recommendedRestaurants = []
	
	for i in range(len(res_recommendation)):
		recommendedRestaurants.append(res_recommendation[i][0])
		recommendedRestaurants.append(res_recommendation[i][3])
		#print('\n')
		#printmd(res_recommendation[i][0])
		#print(res_recommendation[i][3])
	 
	return recommendedRestaurants

"""def displayDishesForCuisine(request):
	yesOrNo = request.GET["yesOrNo"]
	#cuisine = request.GET["cuisineNameInput"]
	print("**** Hey SAdhana, I am inside displayDishesForCuisine and i am getting the cuisine value as ", cuisine)
	if yesOrNo == 'yes':
		print("Hello, the yesorno is ", yesOrNo)
		#dishList = getDishList(request)
		dish1 = "dish1diss"
		dish2 = "dish2diss"
		dish3 = "dish3diss"
		dish4 = "dish4diss"
		dish5 = "dish5diss"
		dish6 = "dish6diss"
		return render(request, 'cuisines/cuisine_dishes.html', { 'dish1' : dish1, 'dish2' : dish2, 'dish3' : dish3, 'dish4' : dish4, 'dish5' : dish5 ,'dish6' : dish6})
	else:
		return render(request, 'cuisines/thankyou.html')"""

def getDishList(cuisine, zipcode):
	dishlist=[]
	output={}
	resperzip = getKeysByValue(output,zipcode)
	review_dict={}
	with open (path2review, 'r') as f:
		for line in f.readlines():
			review_json = json.loads(line)
			if review_json['business_id'] in resperzip:
				if review_json['business_id'] in review_dict:
					review_dict[review_json['business_id']].append(review_json['text'])
				else:
					review_dict[review_json['business_id']] = [ review_json['text']]

	dish = {}
	for key, value in review_dict.items():
		count = 0
		if val1.lower() == 'indian':
			cuisine_list = best_indian
		elif val1.lower() == 'chinese':
			cuisine_list = best_chinese
		if key in resperzip:
			for i in range(len(cuisine_list)):
				if cuisine_list[i] in str(value).lower():
					if (('good' in str(value).lower()) or ('best' in str(value).lower()) or ('amazing' in str(value).lower())):
						if cuisine_list[i] in dish:
							dish_name = cuisine_list[i]
							count = dish[dish_name]
							count += 1
							temp_dish = {dish_name:count}
							dish.update(temp_dish)
						else:
							dish_name = cuisine_list[i]
							dish[dish_name] = 1
		#import operator
		#print(max(dish.items(), key=operator.itemgetter(1))[0])
		list1 = max(dish.values())
		for key1,value1 in dish.items():
			if value1 == list1:
				dishlist.append(key1)
	return dishlist
	


