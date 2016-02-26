#Creating The Model With ID3

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime 
from collections import defaultdict
from collections import Counter
from itertools import izip_longest
import random

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class FileSize(object):
	def __init__(self):
		self.byDefault=0
		self.default_label=19
		self.report  = np.zeros((10,10), dtype=int)
	def FeatureExtraction(self,data):
		try:
			file_size=1
			if data[0]!='-':
				file_size = int(np.ceil(np.log2(int(data[0]))))
				if file_size<19:
					file_size=19
					
			else:
				file_size=19
	
			host  = data[1].split('/')[2]
			extention = data[1].split('/')[-1].split('.')[-1]
			IsMobile = data[2]
			data_type = data[3]
			UrlLen = len(data[1])
			return [host,extention,data_type,IsMobile,file_size]
		except:
			return None
	
	def UpdateTree(self,node,features):
		if features != None:
			if features[0] in node:
				if len(features)>1:
					self.UpdateTree(node[features[0]],features[1:])
				else:
					node[features[0]]+=1
			else:
				if len(features)==1:
					if features[0] in node:
						node[features[0]]+=1
					else:
						node[features[0]]=1
				else:
					node[features[0]] = defaultdict(dict)
					self.UpdateTree(node[features[0]],features[1:])
	
	def loadData(self,TrainingPath):
		data = pd.read_csv(TrainingPath,error_bad_lines=False,header=0,sep='\t')
		from sklearn.cross_validation import train_test_split
		return train_test_split(data, test_size = 0.2 ,random_state=5)

	def Build_ID3_Tree(self,data):
		print 'Start Building Tree at: ',datetime.now()
		self.tree = defaultdict(object)
		for i,v in data.iterrows():
			self.UpdateTree(self.tree,list(v))

		print 'Number of Fist level Nodes: ',len(self.tree)
		return self.tree
		
	def prediction(self,node,features):
		if features != None:
				if len(features)>1:
					if features[0] in node:
						return self.prediction(node[features[0]],features[1:])
					else:
						self.byDefault+=1
						return 0
				else:
					if features[0] in node:
						if(len(sorted(Counter(node[features[0]]).most_common(),key=lambda x:-x[1])))>3:
							#print len(sorted(Counter(node[features[0]]).most_common(),key=lambda x:-x[1]))
							#raw_input('\n----\n')
							pass
						result =  sorted(Counter(node[features[0]]).most_common(),key=lambda x:-x[1])[0][0]
						return result
					else:
						self.byDefault+=1
						return 0

	def reports(self,report):
		print '----------------------------Report-------------------------------'
		print '-----------------------------------------------------------------\n\n'
		line = 'H\t     '
		for header in range(len(report)):
			line +=  str(header)+'|'+'\t     '
		print color.GREEN+color.BOLD+line+'Recall'+color.END
		line =''
		f1 =[]
		precisionlist=[]
		TotalPrecision = 0
		TotalRecal = 0
		TotalF1=0
		for x in range(len(report)):
				recal=[0,0]
				precision =[0,0]
				for y in range(len(report)):
				    if x!=y:
				        line += str("{:6.0f}".format(report[x][y]))+'\t'
				        recal[0]+=report[x][y]
				        precision[0]+=report[y][x]

				    else:
				        line += color.RED+color.BOLD+str("{:6.0f}".format(report[x][y]))+color.END+'\t'
				        recal[1]+=report[x][y]
				        precision[1]+=report[y][x]

				prec = float('%.2f'%((precision[1]*100.0)/(precision[0]+precision[1])))
				rec =  float('%.2f'%((recal[1]*100.0)/(recal[0]+recal[1])))
				print color.YELLOW+color.BOLD+str(x)+color.END+'\t',line,'      -',rec
				precisionlist.append(prec)
				line =''
		line =''
		for p in precisionlist:
			line += str('%.2f'%p)+'|'+'  '          
		print 'Precision:',line
		print '\n\n-----------------------------------------------------------------'
		print '-----------------------------------------------------------------'

	def test(self,test_data):
		for i,v in test_data.iterrows():
			v = list(v)
			result = self.prediction(self.tree,v[:-1])
			if result==0:
				self.UpdateTree(tree, v)	
				result = self.default_label

			label = v[-1]
			self.report[label-19][result-19]+=1
		self.reports(self.report)





if len(sys.argv) == 1:
	sys.argv.append('Udacity.csv')	
fs = FileSize()
train_data,test_data = fs.loadData(sys.argv[1])
print 'Train Size: ',len(train_data)
print 'Test Size : ',len(test_data)
tree  = fs.Build_ID3_Tree(train_data)
print 'Tree Size',sys.getsizeof(tree)
print 'Start Prediction Tree at: ',datetime.now()
fs.test(test_data)
#print fs.report

	
