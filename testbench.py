import theano
import theano.tensor
import numpy as np
import cPickle
from random import randrange
from ModelFactory import *
#from output48_39 import *
from map_1001to5 import *
'''
f_acc = open('f_acc.txt','w')
#f_cost = open('f_cost.txt','w')
'''

####################Load Parameter####################
W_parm_data = file('parameter_W_1225.txt','rb')
B_parm_data = file('parameter_B_1225.txt','rb')
vW_parm_data = file('parameter_vW_1225.txt','rb')
vB_parm_data = file('parameter_vB_1225.txt','rb')
W_parm = cPickle.load(W_parm_data)
B_parm = cPickle.load(B_parm_data)
vW_parm = cPickle.load(vW_parm_data)
vB_parm = cPickle.load(vB_parm_data)
################################################

'''
########################################Train Part########################################

train_ques_data = open('dataset/word_vector.txt','r')
train_imag_data = file('dataset/img_train146962.txt','rb')
ans_1001_data = open('dataset/fixanswer.train','r')
ans_ABCDE_data = open('dataset/pack/answer.train_sol','r')

train_ques = []
train_imag = cPickle.load(train_imag_data)

ans_1001 = [] 
for line in ans_1001_data:
	x = line.split('\t')
	if x[0]!='img_id':
		xx = x[2].split('\n')[0].split(',')
		ans_1001.append(xx)
		if len(xx)!=1001:
			print 'fuck you yang' 

for line in train_ques_data:
	x = line.split()
	x = [np.float32(i) for i in x]
	train_ques.append(x)
	if len(x)!=1200:
			print 'fuck you Patrick'

ans_ABCDE = []
for line in ans_ABCDE_data:
	x = line.split('\t')
	if x[0]!='img_id':
		xx = x[2].split('\n')[0]
		ans_ABCDE.append(xx)
print 'Data Read Completed.'

train = []
for i in range( len(train_ques) ):
	train.append( np.concatenate( (train_ques[i], train_imag[i]), axis=1) )
print 'Data Concatenate Completed.'

W_number_list = [1024,1024]
input_dimension = 2200  # Dimension of input vector
output_dimension = 1001 # Dimension of output vector
batch_number = 4 # Number of batch size
LR = 0.001

train_number = 100000#140000 
validation_num = 146962 - train_number #146962

test = ModelFactory(input_dimension, output_dimension, W_number_list, batch_number, LR)
test.load_parm(W_parm,B_parm,vW_parm,vB_parm)
X = None
Y = None
i=train_number
ACC = 0.0
ACC1 = 0.0
W_new = []
B_new = [] 
c = MAP_1001TO5()
epoch = 0
try:
	while True:
		X = []
		yy= []
		for k in range(batch_number):
			num = randrange(0,train_number)
			if i>=train_number:#i>=1124823:
				i=0
				err=0.0
				err1=0.0
				for m in range(validation_num):
					if m % 10000 == 0:
						print m
					Ya= test.y_evaluated_function([train[train_number+m].astype(dtype = theano.config.floatX)] , Y)[0]
						#[train_ques[train_number+m],train_imag[train_number+m]], Y)[0]
					#if [c.Map_Five_Ans(Ya,train_number+m+1)]!=[str(ans_ABCDE[train_number+m])]:
					#	err = err+1.0
					if [c.Map_Know_Ans(Ya,train_number+m+1)]!=[str(ans_ABCDE[train_number+m])]:
						err1 = err1+1.0
						#print 'c.Map_Five_Ans',[c.Map_Five_Ans(Ya,train_number+m+1)]
						#print 'ans_ABCDE',[str(ans_ABCDE[train_number+m])]
				#ACC = 1.0-err/validation_num
				#print 'ACC = %f'%(ACC)
				ACC1 = 1.0-err1/validation_num
				print 'ACC1 = %f'%(ACC1)
				test.lr_decade()
				epoch = 1
				#f_acc.write(str(ACC))
			#print len(ans_1001[num])
			yy.append(np.array(ans_1001[num]).astype(dtype = theano.config.floatX))
			X.append(train[num].astype(dtype = theano.config.floatX) )

			#typeidx = anstype.index(str(ans[num][1].split('\n')[0]))
			#y=[0]*48
			#y[typeidx]=1
			#yy.append(np.array(y).astype(dtype = theano.config.floatX))
			#X.append(train[num][1:70])
			i=i+1	
			if i % 5000 == 0 :
				print i 
		Y=yy

		test.train_one(X,Y)
		if epoch==1:
			print test.cost_function(X,Y)
			epoch=0

except KeyboardInterrupt:
	pass


f = file('parameter_W_0102.txt', 'wb')
cPickle.dump(test.W_array, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
f = file('parameter_B_0102.txt', 'wb')
cPickle.dump(test.B_array, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
f = file('parameter_vW_0102.txt', 'wb')
cPickle.dump(test.vW_array, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
f = file('parameter_vB_0102.txt', 'wb')
cPickle.dump(test.vB_array, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
#f_acc.close()
'''
##########################################################################################


########################################test_part########################################
test_ans = open('test_ans_0102.csv','w')
test_ques_data = open('dataset/word_vector_test.txt','r')
test_imag_data = file('dataset/imag40504','rb')
name_data = open('dataset/pack/question.test','r')


test_imag = cPickle.load(test_imag_data)
test_ques = []
count = 0
for line in test_ques_data:
	count = count+1
	x = line.split()
	x = [np.float32(i) for i in x]
	test_ques.append(x)
	if len(x)!=1200:
		print 'count',count
		print 'fuck you Patrick'

name = []
for line in name_data:
	x = line.split('\t')
	if x[0]!='img_id':
		name.append(x[1])

test_array = []
for i in range( len(test_ques) ):
	test_array.append( np.concatenate( (test_ques[i], test_imag[i]), axis=1) )

test_c = MAP_1001TO5(1)
Y=None
test_ans.write('q_id,ans\n')

W_number_list = [1024,1024]
input_dimension = 2200  # Dimension of input vector
output_dimension = 1001 # Dimension of output vector
batch_number = 4 # Number of batch size
LR = 0.001

test = ModelFactory(input_dimension, output_dimension, W_number_list, batch_number, LR)
test.load_parm(W_parm,B_parm,vW_parm,vB_parm)

count_others = 0
for i in range(len(test_ques)):
	#Ya= test.y_evaluated_function([test_array[i][1:70]], Y)[0]
	Ya= test.y_evaluated_function([test_array[i].astype(dtype = theano.config.floatX)] , Y)[0]
	test_ans.write(name[i])
	test_ans.write(',')
	word = test_c.Map_Know_Ans(Ya,i+1)
	#if word =='Z':
	#	test_ans.write(feng_ans[i])
	#	count_others = count_others+1
	#else:
	test_ans.write(word)
	if i!=len(test_ques)-1:
		test_ans.write('\n')

#print count_others

test_ans.close()
########################################################################################


'''
##################################Test Wrong Question#####################################

ques_train_data = open('dataset/pack/question.train','r')
ques_train = ques_train_data.readlines()

train_ques_data = open('dataset/word_vector.txt','r')
ans_1001_data = open('dataset/fixanswer.train','r')
ans_ABCDE_data = open('dataset/pack/answer.train_sol','r')
train_imag_data = file('dataset/img_train146962.txt','rb')
train_ques = []
train_imag = cPickle.load(train_imag_data)

ans_1001 = [] 
for line in ans_1001_data:
	x = line.split('\t')
	if x[0]!='img_id':
		xx = x[2].split('\n')[0].split(',')
		ans_1001.append(xx)
		if len(xx)!=1001:
			print 'fuck you yang' 

for line in train_ques_data:
	x = line.split()
	x = [np.float32(i) for i in x]
	train_ques.append(x)
	if len(x)!=1200:
			print 'fuck you Patrick'

ans_ABCDE = []
for line in ans_ABCDE_data:
	x = line.split('\t')
	if x[0]!='img_id':
		xx = x[2].split('\n')[0]
		ans_ABCDE.append(xx)
print 'Data Read Completed.'

train = []
for i in range( len(train_ques) ):
	train.append( np.concatenate( (train_ques[i], train_imag[i]), axis=1) )
print 'Data Concatenate Completed.'

test_c = MAP_1001TO5(0)
Y=None

W_number_list = [1024,1024]
input_dimension = 2200  # Dimension of input vector
output_dimension = 1001 # Dimension of output vector
batch_number = 4 # Number of batch size
LR = 0.001
test = ModelFactory(input_dimension, output_dimension, W_number_list, batch_number, LR)
test.load_parm(W_parm,B_parm,vW_parm,vB_parm)

count_others = 0
for i in range(len(train)):
	#Ya= test.y_evaluated_function([test_array[i][1:70]], Y)[0]
	Ya= test.y_evaluated_function([train[i].astype(dtype = theano.config.floatX)] , Y)[0]
	word = test_c.Map_Know_Ans(Ya,i+1)
	if [word]!=[str(ans_ABCDE[i])]:
		print ques_train[i+1]
######################################################################################################
'''
'''
c = MAP_1001TO5()
for i in range(400):
	#print [train[i][1:70]]
	Ya = test.y_evaluated_function([train[i][1:70]], Y)[0]
	print c.map(Ya)
'''

#print test.train_one(X, Y)
