import numpy as np
import theano
import theano.tensor as T
from random import randrange
__author__= 'jason'

class MAP_1001TO5:
	def __init__(self,train_or_test=0):
		self.train_or_test = train_or_test
		self.map_data = open('dataset/most1000','r')

		if train_or_test==0:
			self.choices = open('dataset/pack/choices.train','r')
			self.question_data = open('dataset/pack/question.train','r')
			self.feng_ans_data = open('dataset/Feng_train_softmax.txt','r')
			print 'This is choices of train data'
		else:
			self.choices = open('dataset/pack/choices.test','r')
			self.question_data = open('dataset/pack/question.test','r')
			self.feng_ans_data = open('dataset/predict_word.csv','r')
			feng_softmax_data = open('dataset/test_softmax_out.txt','r')
			print 'This is choices of test data'

		self.ans_A = []	
		self.ans_B = []	
		self.ans_C = []	
		self.ans_D = []	
		self.ans_E = []	
		not_first = 0
		for line in self.choices:
			xx = line.split('\t')
			x = xx[2].split('  ')
			if not_first==1:
				self.ans_A.append(x[0].split('(A)')[1])
				self.ans_B.append(x[1].split('(B)')[1])
				self.ans_C.append(x[2].split('(C)')[1])
				self.ans_D.append(x[3].split('(D)')[1])
				self.ans_E.append(x[4].split('(E)')[1])
			not_first = 1

		self.most1000 = []
		for line in self.map_data:
			x = line.split(':  ')
			self.most1000.append(x[0].split('"')[1].split('"')[0])
		#print self.most1000 

		self.question = []
		first = 1
		for line in self.question_data:
			if(first==0):
				x = line.split('\t"')[1].split('"\n')[0]
				self.question.append(x)
			first = 0

		# Is there "color" in the question
		self.Is_color = []
		for i in range(len(self.question)):
			word = self.question[i].split(' ')
			color_word = 0
			for ii in range( len(word) ):
				if (word[ii] == "color"):
					color_word = 1	
			if (color_word == 1):
				self.Is_color.append(1)
			else:
				self.Is_color.append(0)


		self.feng_ans = []
		temp = self.feng_ans_data.readlines()
		for i in range ( len(temp) ):
			if(self.train_or_test ==0):
				if (i>1):
					x = temp[i].split(',')[1]
					if(x == 'A'):
						self.feng_ans.append(0)
					elif(x == 'B'):
						self.feng_ans.append(1)
					elif(x == 'C'):
						self.feng_ans.append(2)
					elif(x == 'D'):
						self.feng_ans.append(3)
					elif(x == 'E'):
						self.feng_ans.append(4)
			else:
				if (i>0):
					x = temp[i].split(',')[1].split('\n')[0]
					if(x == 'A'):
						self.feng_ans.append(0)
					elif(x == 'B'):
						self.feng_ans.append(1)
					elif(x == 'C'):
						self.feng_ans.append(2)
					elif(x == 'D'):
						self.feng_ans.append(3)
					elif(x == 'E'):
						self.feng_ans.append(4)

		feng_softmax_1 = feng_softmax_data.readlines()
		i = 0
		self.feng_softmax_min = []
		min_ans = 0
		while (i < len(feng_softmax_1) ):
			min_v_1 = []
			for ii in range (5):
				x = feng_softmax_1[i].split(',')[2].split('\n')[0]
				min_v_1.append(x)
				i = i+1
			min_v = min(min_v_1)
			min_ans = min_v_1.index(min_v)
			if min_v != '0.2':
				self.feng_softmax_min.append(min_ans)
			else:
				self.feng_softmax_min.append('NON')

	def Map_Five_Ans(self,z,q_index):
		candidates = [self.ans_A[q_index-1],self.ans_B[q_index-1],self.ans_C[q_index-1],self.ans_D[q_index-1],self.ans_E[q_index-1]]
		candidates_pos = []
		candidates_score = []
		candidates_score_know_only = []
		for i in range(5) :
			try:
				candidates_pos.append( self.most1000.index(candidates[i]) )
				candidates_score.append( z[candidates_pos[i]] )
				candidates_score_know_only.append( z[candidates_pos[i]] )
			except:
				candidates_pos.append(1000)
				candidates_score.append( z[1000] )
				candidates_score_know_only.append( -1.0 )
		case = candidates_score.index( max(candidates_score) ) 
		if(case==0):
			return 'A'
		elif(case ==1):
			return 'B'
		elif(case ==2):
			return 'C'
		elif(case ==3):
			return 'D'
		elif(case ==4):
			return 'E'

	def Map_Know_Ans(self,z,q_index):
		candidates = [self.ans_A[q_index-1],self.ans_B[q_index-1],self.ans_C[q_index-1],self.ans_D[q_index-1],self.ans_E[q_index-1]]
		
		answer_to_choose = [1,1,1,1,1] 

		if self.feng_softmax_min[q_index-1]!='NON':
			answer_to_choose[self.feng_softmax_min[q_index-1]]=0

		for i in range (5): # Check for the same answer
			for ii in range (5):
				if ii != i:
					if(candidates[i] == candidates[ii]):
						answer_to_choose[i]=0
						answer_to_choose[ii]=0

		candidates_score_know_only = []
		for i in range(5) :
			try:
				if(answer_to_choose[i]==1):
					candidates_score_know_only.append( z[self.most1000.index(candidates[i])] )
				else:
					candidates_score_know_only.append( -100.0 )
					#print "Same Answer, q_id = ", q_index 
			except:
				candidates_score_know_only.append( -1.0 )

		case = candidates_score_know_only.index( max(candidates_score_know_only) ) 
		
		if max(candidates_score_know_only) == -1:
			if self.train_or_test == 0:
				case = randrange(0,5)
			else:
				case = 5

		if (case == 5):
			case = self.feng_ans[q_index-1]

		#if self.Is_color[q_index-1] == 1:
		#	case =  self.feng_ans[q_index-1]
			#print 'Q:',self.question[q_index-1]

		if(case==0):
			return 'A'
		elif(case ==1):
			return 'B'
		elif(case ==2):
			return 'C'
		elif(case ==3):
			return 'D'
		elif(case ==4):
			return 'E'

'''
f = open('fixanswer.train','r')
a = f.readlines()
#a2 = a[2].split('\t')[2].split('\n')[0].split(',')
a2 = np.random.normal(0, 1, (1, 1001) )[0]
#print a2
test = MAP_1001TO5()
ans = test.Map_Five_Ans(a2,6)
print ans
'''