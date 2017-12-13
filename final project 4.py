

#import necessary packages and get/set workdesk
import os
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt


#get and set wd

path = 'c:\\Users\wmj212\Documents\Data BC final proj'
os.chdir(path)
print(os.getcwd())

#%%

'''
setup of data
read csv
change data to strings
'''

#read .txt files of english3.txt, a 194433 list of all English words

english = pd.read_csv('english3.txt', header = None)


#rename first column into 'Words'

english = english.rename(columns={0: 'Words'})

#Change 'Words' to str
english['Words']=english['Words'].astype(str)


#%%

'''
Part 1

Removing all vowels

'''

#create a function 'removeVowels' which takes out all vowels in a word

def removeVowels(s):
    result = re.sub(r'[aeiou]', '', s)
    return result


#%%

#create new column 'Vowels Removed' by applying removeVowels function on 'Words'

english['Vowels Removed'] = english['Words'].apply(removeVowels)


#%%

'''
Part 2: Exceptions
A. First and Last Vowels

To allow for exceptions in removing vowels, some vowels will be capitalized (so that it is ignored by function removeVowels
Note: There are probably more efficient ways to do this i.e. create more functions that include exceptions without use of capitalization
'''

#create new function that capitalizes first and last letter
def capFirstLast(s):
    result = s[0].capitalize() + s[1:-1] + s[-1].capitalize()
    return result

#%%

#apply function capFirstLast to create a new column
english['Vowels Removed EXCPT First and Last'] = english['Words'].apply(capFirstLast)

#apply function removeVowels to remove all lowercase vowels
english['Vowels Removed EXCPT First and Last'] = english['Vowels Removed EXCPT First and Last'].apply(removeVowels)

#%%

'''
Part 2: Exceptions
B. Consecutive Vowels

Similar to the First and Last Vowels function, all consecutive vowels will be capitalized so they will not be removed
'''

#create function caps which capitalizes a string
def cap(s):
    return s.group(0).upper()

#create function consecVowels which capitalizes all consecutive vowels
def capConsecVowels(s):
    result = re.sub(r'([aeiou]){2,5}', cap, s)
    return result

#apply consecVowels function to create a new column
english['Vowels Removed EXCPT Consec'] = english['Words'].apply(capConsecVowels)


#apply function removeVowels to remove all lowercase vowels
english['Vowels Removed EXCPT Consec'] = english['Vowels Removed EXCPT Consec'].apply(removeVowels)



#%%

'''
Part 3: Putting Everything Together

The two exceptions will be applied to 'Words'
First and last vowels, consecutive vowels will be kept

Note: it is important that we apply capConsecVowels first: to avoid mistakes on words that start with two vowels
eg. aachen - if we cap first and last to AacheN, capConsecVowels will ignore 'Aa', because it is not 'aa'
'''

#apply capConsecVowels function
english['Vowels Removed with EXCPT A and B'] = english['Words'].apply(capConsecVowels)

#apply function capFirstLast
english['Vowels Removed with EXCPT A and B'] = english['Vowels Removed with EXCPT A and B'].apply(capFirstLast)

#apply function removeVowels
english['Vowels Removed with EXCPT A and B'] = english['Vowels Removed with EXCPT A and B'].apply(removeVowels)

#make all words lowercase for visibility into new column Final
english['FinalList'] = english['Vowels Removed with EXCPT A and B'].str.lower()



#%%

'''
Part 4: Same thing but on a smaller list
1000 common english words
'''

common = pd.read_csv('common1000.txt', header = None)


#rename first column into 'Words'

common = common.rename(columns={0: 'Words'})

#Change 'Words' to str
common['Words']= common['Words'].astype(str)

#apply capConsecVowels function
common['FinalList'] = common['Words'].apply(capConsecVowels)

#apply function capFirstLast
common['FinalList'] = common['FinalList'].apply(capFirstLast)

#apply function removeVowels
common['FinalList'] = common['FinalList'].apply(removeVowels)

#make all words lowercase for visibility into new column Final
common['FinalList'] = common['FinalList'].str.lower()


#%%
'''
Part 5: Analysis

How many DISTINCT words do we get? How many duplicates are made, as a result of vowels being removed?
'''

#For COMMON


#find count of how many distinct words we get
commonAnalysis = common.FinalList.value_counts()

#change Series into Dataframe
commonAnalysis = commonAnalysis.to_frame('Count')

#count how many of each unqiue value there are
commonCounter = commonAnalysis.apply(pd.value_counts)


#For ENGLISH

#find count of how many distinct words we get
englishAnalysis = english.FinalList.value_counts()

#change Series into Dataframe
englishAnalysis = englishAnalysis.to_frame('Count')

#count how many of each unqiue value there are
englishCounter = englishAnalysis.apply(pd.value_counts)

#%%

'''
charts
'''


#plot of duplicate words

#for COMMON
DuplicateWordsCommon = commonAnalysis.plot(x=commonAnalysis.index, y = 'Count', title = 'Duplicate Words', xticks =[], colormap='jet', figsize = (15,15))
DuplicateWordsCommon.set(xlabel="Vowel Removed Word (Word not shown)", ylabel="Count")

#for ENGLISH
DuplicateWordsEnglish = englishAnalysis.plot(x=englishAnalysis.index, y = 'Count', title = 'Duplicate Words', yticks= [2,4,6,8,10,12,14,16,18], xticks =[], colormap='jet', figsize = (15,15))
DuplicateWordsEnglish.set(xlabel="Vowel Removed Word (Word not shown)", ylabel="Count")


#The above graph is heavily skewed to words with a count of 1 (no duplicates), so we will ignore some of the data to get a better look
#These barplots also show the specific word

DuplicateWordsCommon = commonAnalysis.plot.barh(x=commonAnalysis.index, y = commonAnalysis['Count']>4, title = 'Duplicate Words' , colormap='jet', figsize = (10,20))
DuplicateWordsCommon.set(xlabel="Words", ylabel="Count")

#for ENGLISH
DuplicateWordsEnglish = englishAnalysis.plot.barh(x=englishAnalysis.index, y = englishAnalysis['Count'] >10, xticks = [2,4,6,8,10,12,14,16,18], title = 'Duplicate Words', colormap='jet', figsize = (10,20))
DuplicateWordsEnglish.set(xlabel="Words", ylabel="Count")



#%%

#Count of Number of Duplicate Words
CountDupWordsCommon = commonCounter.plot(kind='bar',x=commonCounter.index, y = 'Count', title = 'How many Duplicate Words are there?', figsize = (10,10))
CountDupWordsCommon.set(xlabel="Number of Words", ylabel="Count")
for i, label in enumerate(list(commonCounter.index)):
    score = commonCounter.ix[label]['Count']
    CountDupWordsCommon.annotate(str(score), (i -.2, score+ 100))
    


#%%





#%%

'''
Efficiency
'''
#length difference before and after
#This is asssuming all words are unique, which they are not
common['Length Before'] = common['Words'].str.len()
common['Length After'] = common['FinalList'].str.len()

#Creating a new DataFrame but summing all lengths Before/After
values = [common['Length Before'].sum(),common['Length After'].sum()]
BeforeAfterCommon = pd.DataFrame(values, index = ('Before','After'))

#creating a graph of the number of characters
BeforeAfterGraphCommon = BeforeAfterCommon.plot.bar(title = 'How many Characters are Eliminated?', figsize=(10,10))
BeforeAfterGraphCommon.set(ylabel="Number of Characters")
for i, label in enumerate(list(BeforeAfterCommon.index)):
    score = BeforeAfterCommon.ix[label][0]
    BeforeAfterGraphCommon.annotate(str(score), (i -.1, score+ 1000))

#%%


#length difference before and after
#This is asssuming all words are unique, which they are not
english['Length Before'] = english['Words'].str.len()
english['Length After'] = english['FinalList'].str.len()

#Creating a new DataFrame but summing all lengths Before/After
values = [english['Length Before'].sum(),english['Length After'].sum()]
BeforeAfterEnglish = pd.DataFrame(values, index = ('Before','After'))

#creating a graph of the number of characters
BeforeAfterGraphEnglish = BeforeAfterEnglish.plot.bar(title = 'How many Characters are Eliminated?', figsize=(10,10))
BeforeAfterGraphEnglish.set(ylabel="Number of Characters")
for i, label in enumerate(list(BeforeAfterEnglish.index)):
    score = BeforeAfterEnglish.ix[label][0]
    BeforeAfterGraphEnglish.annotate(str(score), (i -.1, score+ 10000))

#%%
'''
The above calculations ignore the fact that there are duplicates in the words that have vowels removed: hence vowels shouldnt be removed from those words.

We should calculate the sum of the length of words that have NO duplicates.

'''

nodup = commonAnalysis[commonAnalysis['Count'] == 1]
#Create a new dataframe of values that have NO DUPLICATES
#NoDupCommon= pd.DataFrame(nodup)





#length difference of only words that have no duplicates





#%%

'''
extraneous cuts
'''

#to search a word
english.loc[english['Words']=='abound']

#SUBSET KEY IMPORTANT

subset = df.loc[(df['count'] = 1)]




#sample

import re

def toLowercase(matchobj):
   return matchobj.group(1).lower()

s = 'start TT end'
re.sub(r'([A-Z]){2}', toLowercase, s)


#%%


english['Words']= english['Words']

#%%
for row in english.iterrows():
   english['VR'] = removeVowels(row['Words'])
    

#%%

#get and set wd
print(os.getcwd())

path='c:\\Users\wmj212\Documents\Data BC final proj'

os.chdir(path)

#%%





'''
potential problems

a lot of words have prefixes and suffixes
for example, un- prefix can throw off the comprehension of the word

unacceptable will turn into unccptble
the missing 'a' in the root word acceptable is critical

elemental will turn into elmntl
the missing 'a' in the suffix -al can be misleading

prefixes are a problem if the root word starts with a vowel
similarly, sufixes can be a problem if the the missing vowel of a suffix ending is important

perhaps a prefix and suffix fix by making more exceptions can resolve the problem
'''