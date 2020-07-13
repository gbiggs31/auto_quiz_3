# goal is to produce a random quiz question
# test if streamlit can help make this user interactive



# Import packages

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import wikipedia
import re
import random
import time
import streamlit as st


def main():


	def get_top_articles(article_link):
	    top_articles = requests.get(str(article_link))
	    data = top_articles.json()
	    return data


	def get_specific_article(article_number, top_articles):
	    specific_article = top_articles['items'][0]['articles'][article_number]['article']
	    return specific_article


	def get_wikipedia_article(specific_article):
	    page = wikipedia.summary(str(specific_article))
	    return page


	def create_question_from_article(page):
	    first_sentence = re.split('[. ] ',str(page))[0] + '.'
	    second_sentence = re.split('[. ] ',str(page))[1] + '.'
	    return first_sentence, second_sentence


	def hide_word_and_return_question(first_sentence):
	    blank = re.split('( is | was )',str(first_sentence),1)[0]
	    question = 'BLANK is/was ' + re.split('( is | was )',str(first_sentence), 1)[2]
	    return blank, question


	def turn_difficulty_to_range(difficulty):
	    # user provides difficulty and we must create a range to select from
	    # difficulty 10 should be bottom 10% of articles
	    # check integer is between 1-10
	    assert (difficulty < 11) & (difficulty > 0)
	    
	    #calculate bounds
	    lower_bound = difficulty * 100
	    upper_bound = difficulty * 100 - 100
	    return lower_bound, upper_bound

	# @st.cache(suppress_st_warning=True)
	def get_quiz_question(year,month,difficulty):
	    # range of choice is difficulty
	    # can also adjust date range
	    year = str(year)
	#     print(month)
	    month = '00' + str(month)
	    month = month[-2:]
	    # print(month)
	    
	    lower_bound, upper_bound = turn_difficulty_to_range(int(difficulty))
	    article_number = random.randrange(upper_bound,lower_bound)
	    top_link = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{}/{}/all-days'.format(year, month)
	    print(top_link)
	    articles = get_top_articles(top_link)
	    specific_article = get_specific_article(article_number,articles)
	    wikipedia_page = get_wikipedia_article(specific_article)
	    first_sentence, second_sentence = create_question_from_article(wikipedia_page)
	    answer, question = hide_word_and_return_question(first_sentence)
	    
	    # print('Your question is...')
	    # print(question)

	    # print('The hint is...')
	    # print(second_sentence)
	    
	    # time.sleep(10)
	    # print('The answer is: ')
	    # print(answer)
	    
	    return question, second_sentence, answer

	# specify the streamlit scaffolding
	st.title('Auto Question App')


	# now create widgets and then generate the question

	# Add a slider to the sidebar:
	difficulty = st.sidebar.slider(
	    'Select a difficulty from 1-10',
	    1, 10, (1)
	)

	year = st.sidebar.slider(
	    'Select a year to base the question on',
	    2016, 2020, (2020)
	)

	month = st.sidebar.slider(
	    'Select a month for the question',
	    1, 12, (6)
	)


	# show_answer = st.sidebar.button('Want the answer?')

	# get_new_question = st.sidebar.button('Get a new question?')

	#create cache object for the "chat"
	# @st.cache(allow_output_mutation=True)
	# def get_random_seed():
	#     return []

	# hardcode month and year for testing
	# year = '2020'
	# month = '06'

	# try and get it not to rerun when the user inputs that they want the answer
	# answer_time	= 'no'

	# if not st.button('Want the answer?'):
	# could define some function that doesn't change unless the button is not clicked?
	# @st.cache(suppress_st_warning=True)
	# def increment_change_var(change_flag):
	# 	return change_flag + 1


	# try five times before giving up
	i = 0
	while i < 5:
		try:
			question, second_sentence, answer = get_quiz_question(year, month, difficulty)
			i = 5
		except:
			st.write('sorry, error, trying again')
			question, second_sentence, answer = get_quiz_question(year, month, difficulty)
			i += 1
		else:
			pass


	st.write('And your question is....')
	st.write(question)

	st.write('Need a hint?')
	st.write(second_sentence)

	# if st.button('Want the answer?'):
	# testing = st.button('Want the answer?')

	for i in range(5,0,-1):
		output_string = "Showing answer in {}....".format(i)
		st.write(output_string)
		time.sleep(i)

	# st.write(show_answer)
	st.write('Answer:')
	st.write(answer)

	st.balloons()

	# answer_time = st.text_input('Want the answer? (type yes)')
	# if answer_time == 'yes':
	# 	st.write('Answer:')
	# 	st.write(answer)
	# else:
	# 	st.write('Waiting')

if __name__ == "__main__":
    main()