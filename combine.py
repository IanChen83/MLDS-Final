import cPickle
import numpy as np
out_f = np.array([])#store 146962*4096 element

caffe_data = file('./dataset/caffe_data/caffe_train11.txt','rb')
caffe = cPickle.load(caffe_data)
out_f = caffe
caffe_data.close()
print '11 finished'
caffe_data = file('./dataset/caffe_data/caffe_train12.txt','rb')
caffe = cPickle.load(caffe_data)
out_f = np.concatenate((out_f,caffe))
caffe_data.close()
print '12 finished'
caffe_data = file('./dataset/caffe_data/caffe_train13.txt','rb')
caffe = cPickle.load(caffe_data)
out_f = np.concatenate((out_f,caffe))
caffe_data.close()
print '13 finished'
caffe_data = file('./dataset/caffe_data/caffe_train14.txt','rb')
caffe = cPickle.load(caffe_data)
out_f = np.concatenate((out_f,caffe))
caffe_data.close()
print '14 finished'
caffe_data = file('./dataset/caffe_data/caffe_train21.txt','rb')
caffe = cPickle.load(caffe_data)
out_f = np.concatenate((out_f,caffe))
caffe_data.close()
print '21 finished'
caffe_data = file('./dataset/caffe_data/caffe_train22.txt','rb')
caffe = cPickle.load(caffe_data)
out_f = np.concatenate((out_f,caffe))
caffe_data.close()
print '22 finished'
caffe_data = file('./dataset/caffe_data/caffe_train23.txt','rb')
caffe = cPickle.load(caffe_data)
out_f = np.concatenate((out_f,caffe))
caffe_data.close()
print '23 finished'
caffe_data = file('./dataset/caffe_data/caffe_train24.txt','rb')
caffe = cPickle.load(caffe_data)
out_f = np.concatenate((out_f,caffe))
caffe_data.close()
print '24 finished'
'''
print out_f.shape
f = file('./dataset/caffe_data/caffe_train.txt', 'wb')
cPickle.dump(out_f, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
'''
