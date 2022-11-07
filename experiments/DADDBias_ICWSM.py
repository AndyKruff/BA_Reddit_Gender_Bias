import pandas as pd
import gensim 
from gensim.models import FastText
import numpy as np
import nltk
import time
from scipy import spatial

# Source: https://github.com/xfold/LanguageBiasesInReddit/blob/master/DADDBias_ICWSM.py

def GetTopMostBiasedWords(modelpath, topk, c1, c2, pos = ['JJ','JJR','JJS'], verbose = True):
	'''
	modelpath <str> : path to skipgram w2v model
	topk <int> : topk words
	c1 list<str> : list of words for target set 1
	c2 list<str> : list of words for target set 2
	pos list<str> : List of parts of speech we are interested in analysing
	verbose <bool> : True/False
	'''

	def calculateCentroid(model, words):
        #  Calculate frequencies for male and female terms for weighted centroids
        
		freq = []
		for i in words:
			if i in model.wv.key_to_index:
    				freq.append(model.wv.get_vecattr(i, "count"))
			else:
				freq.append(0)
		
		# Calculate the weighted centroid
		centroid = np.ma.average([model.wv[w] for w in words], weights=freq ,axis=0) 

		return centroid
       
    
	def getCosineDistance(embedding1, embedding2):       
		return spatial.distance.cosine(embedding1, embedding2)


	#select the interesting subset of words based on Part of Speech (POS)
	model = FastText.load(modelpath)
	words_sorted = sorted( [(k,model.wv.get_index(k) ,model.wv.get_vecattr(k, "count")) for k in model.wv.key_to_index] ,  key=lambda x: x[1], reverse=False)
	words = [w for w in words_sorted if nltk.pos_tag([w[0]])[0][1] in pos]

	if len(c1) < 1 or len(c2) < 1 or len(words) < 1:
		print('[!] Not enough word concepts to perform the experiment')
		return None
    
	# Calculate the weighted centroids for male and female words

	centroid1, centroid2 = calculateCentroid(model, c1),calculateCentroid(model, c2)
	winfo = []
	for i, w in enumerate(words):
		word = w[0]
		freq = w[2]
		rank = w[1]
		pos = nltk.pos_tag([word])[0][1]
		wv = model.wv[word]
		#sent = sid.polarity_scores(word)['compound']
		#estimate cosinedistance diff
		d1 = getCosineDistance(centroid1, wv)
		d2 = getCosineDistance(centroid2, wv)
		bias = d2-d1

		winfo.append({'word':word, 'bias':bias, 'freq':freq, 'pos':pos, 'wv':wv, 'rank':rank} ) #, 'sent':sent

		if(i%100 == 0 and verbose == True):
			print('...'+str(i), end="")

	#Get max and min topk biased words...
	biasc1 = sorted( winfo, key=lambda x:x['bias'], reverse=True )[:min(len(winfo), topk)]
	biasc2 = sorted( winfo, key=lambda x:x['bias'], reverse=False )[:min(len(winfo), topk)]
    #move the ts2 bias to the positive space
	for w2 in biasc2:
		w2['bias'] = w2['bias']*-1
    
	return [biasc1, biasc2]


