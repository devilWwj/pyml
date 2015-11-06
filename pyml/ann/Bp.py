#coding:gbk
# Back-Propagation Neural Networks
# 

import math
import random
import string

random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
#ʹ��˫���к�������logistic����
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
# ˫���к����ĵ���������ȡ���������ز��������ʱ����õ�
def dsigmoid(y):
    return 1.0 - y**2

class NN:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        # ����㣬���ز㣬��������������������
        self.ni = ni + 1 # +1 for bias node
        self.nh = nh
        self.no = no

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no
        
        # create weights
        #����Ȩ�ؾ���ÿһ�������ڵ�����ز�ڵ㶼����
        #ÿһ�����ز�ڵ�������ڵ�����
        #��С��self.ni*self.nh
        self.wi = makeMatrix(self.ni, self.nh)
        #��С��self.ni*self.nh
        self.wo = makeMatrix(self.nh, self.no)
        # set them to random vaules
        #����Ȩ�أ���-0.2-0.2֮��
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)
        print "wi :"
        print self.wi
        print "wo"
        print self.wo
        # last change in weights for momentum 
        #?
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)
        print "ci:"
        print self.ci
        print "co:"
        print self.co

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError('wrong number of inputs')

        # input activations
        # ����ļ����������y=x;
        for i in range(self.ni-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        # hidden activations
        #���ز�ļ����,���Ȼ��ʹ��ѹ������
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                #sum���ǡ�ml�����е�net
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)

        # output activations
        #����ļ����
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]

    #���򴫲��㷨 targets����������ȷ�����
    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        #��������������� 
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            #����k-o
            error = targets[k]-self.ao[k]
            #�������й�ʽ4.14
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # calculate error terms for hidden
        #�������ز������ʹ�á�ml�����еĹ�ʽ4.15
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        # ����������Ȩ�ز���
        # ������Կ���������ʹ�õ��Ǵ��С����ӳ������BPANN
        # ���У�NΪѧϰ���� MΪ������Ĳ��� self.coΪ������
        # N: learning rate
        # M: momentum factor
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                #print N*change, M*self.co[j][k]

        # update input weights
        #�����������Ȩ�ز���
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        #����E(w)
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error

    #���Ժ��������ڲ���ѵ��Ч��
    def test(self, patterns):
        for p in patterns:
            print(p[0], '->', self.update(p[0]))

    def weights(self):
        print('Input weights:')
        for i in range(self.ni):
            print(self.wi[i])
        print()
        print('Output weights:')
        for j in range(self.nh):
            print(self.wo[j])

    def train(self, patterns, iterations=1000, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if i % 100 == 0:
                print('error %-.5f' % error)


def demo():
    # Teach network XOR function
    pat = [
        [[0,0], [0, 1]],
        [[0,1], [1, 0]],
        [[1,1], [1, 0]],
        [[1,1], [0, 1]]
    ]
    
    pat1 = [
        [[0,0], [0]],
        [[0,1], [0]],
        [[1,0], [0]],
        [[1,1], [1]]
    ]

    # create a network with two input, two hidden, and one output nodes
    n = NN(2, 2, 1)
    # train it with some patterns
    n.train(pat)
    # test it
    n.test(pat)



if __name__ == '__main__':
    demo()
