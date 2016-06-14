# -*-  coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import random
import math
import time
import pdb
"""
����������⣬���������Ż����⡣�Ż�����ʹ��optimization.py��ʹ�õ�
�����������ɽ����ģ���˻𷨡��Ŵ��㷨��. ������������֮ǰ�����⸴��
"""

st = time.time()

class dorm:
    def __init__(self, splice, type='works'):

        splice_lst = [46, 58, 70, 82, 94, 106, 118, 130, 142]
        works = [4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 18, 19, 20, 21]
        weeks = [9, 10, 16, 17]

        with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
            lines = file.readlines()
        self.rst = []
        for line in lines:
            lst = line.strip().split(',')
            if type == 'works':
                if int(lst[1].split('-')[-1]) not in works:
                    continue
                self.rst.append([int(lst[splice-2]), int(lst[splice-1]), int(lst[splice]), int(lst[splice+1])])
            else:
                if int(lst[1].split('-')[-1]) not in weeks:
                    continue
                self.rst.append([int(lst[splice-2]), int(lst[splice-1]), int(lst[splice]), int(lst[splice+1])])


    # �����������vec��ӡ������������䷽��
    # ע�⣬���һ���ۺ�����ò��Ѿ��ù����轫�ò�ɾ��
    def printsolution(self, vec):
        print vec


    # ���ۺ���: ���ѧ����ǰ���õ�����ʹ����ѡ�����Ϊ0�������ѡ�����Ϊ1���������Ϊ3
    # ע�⣬���һ���ۺ�����ò��Ѿ��ù����轫�ò�ɾ��
    def dormcost(self, vec):

        mape = 0.0
        total = 0
        for rs in self.rst:
            if not rs[-1]:
                total += 1
            else:
                mape += abs(max(((rs[0]*vec[0] + rs[1]*vec[1] + rs[2]*vec[2])/2), 1) - rs[3])/float(rs[3])
                total += 1

        return mape/total


    """
    ���к����� optimization �к�����ͬ��ֻ�������ۺ�������������ñ�������������
    """
    # ��������1: ��������㷨
    # ��������1000������²⣬��¼�ܴ�����͵ķ���. domainΪ����ŵķ�Χ��0-9��������5���ˣ���˹���10��
    def randomoptimize(self, num):
        best_sol = []
        bestcost = 99999
        for i in range(num):
            sol = [random.random(), random.random(), random.random()]

            # print sol[:]
            newcost = self.dormcost(sol)
            if newcost < bestcost:
                bestcost = newcost
                best_sol = sol
                print best_sol, bestcost
            else:
                continue
        self.printsolution(best_sol)
        print "��������㷨�Ľ������С�����ǣ�", bestcost
        return best_sol

    # �����㷨2����ɽ��
    # �������ѡ��һ������Ϊ���ӽ⣬ÿ��Ѱ�������������Ľ⣬�������Ľ��д��۸�С�Ľ⣬�������µĽ���Ϊ����
    # ����ѭ�����У���ѭ����ĳ���Ӹ����Ľⶼ�ȸ����ӵĴ��۴�ʱ��˵�������˾ֲ���Сֵ�㣬��������
    def hillclimb(self, domain):
        # �������һ������������Ϊ��ʼ����
        seed = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        while 1:
            neighbor = []
            # ѭ���ı���ÿһ��ֵ����һ���ٽ�����б�
            for i in range(len(domain)):
                # �����ж���Ϊ�˽�ĳһλ�Ӽ�1�󲻳���domain�ķ�Χ
                # print seed
                if seed[i] > domain[i][0]:
                    newneighbor = seed[0:i] + [seed[i] - 1] + seed[i + 1:]
                    # print newneighbor[:]
                    neighbor.append(newneighbor)
                if seed[i] < domain[i][1]:
                    newneighbor = seed[0:i] + [seed[i] + 1] + seed[i + 1:]
                    # print newneighbor[:]
                    neighbor.append(newneighbor)

            # �����е��ٽ��������ۣ����򣬵õ�������С�Ľ�
            neighbor_cost = sorted(
                [(s, self.dormcost(s)) for s in neighbor], key=lambda x: x[1])

            # ����µ���С���� > ԭ���Ӵ��ۣ�������ѭ��
            if neighbor_cost[0][1] > self.dormcost(seed):
                break

            # �µĴ��۸�С���ٽ�����Ϊ�µ�����
            seed = neighbor_cost[0][0]
            print "newseed = ", seed[:], " ���ۣ�", self.dormcost(seed)
        # ���
        self.printsolution(seed)
        print "��ɽ���õ��Ľ����С������", self.dormcost(seed)
        return seed

    # �����㷨4��ģ���˻��㷨
    # ������T����ԭʼ�¶ȣ�cool������ȴ�ʣ�step����ÿ��ѡ���ٽ���ı仯��Χ
    # ԭ���˻��㷨��һ�����������⿪ʼ����һ��������ʾ�¶ȣ���һ�¶ȿ�ʼʱ�ǳ��ߣ������𲽽���
    #      ��ÿһ�ε����ڼ䣬�㰡�����ѡ������е�ĳ�����֣�Ȼ��ĳ������仯������µĳɱ�ֵ��
    #      �ͣ����µ���⽫���ɵ�ǰ��⣬������ɽ�����ơ�����������ɱ�ֵ���ߵĻ������µ������
    #      �п��ܳ�Ϊ��ǰ��⣬���Ǳ���ֲ���Сֵ�����һ�ֳ��ԡ�
    # ע�⣺�㷨�ܻ����һ�����ŵĽ⣬�������˻�Ŀ�ʼ�׶λ���ܽϲ�Ľ⣬�����˻�Ĳ��Ͻ��У��㷨
    #      ԭ��Խ���ܽ��ܽϲ�Ľ⣬ֱ�������ֻ�ܽ��ܸ��ŵĽ⡣
    # �㷨���ܽϲ��ĸ��� P = exp[-(highcost-lowcost)/temperature]
    def annealingoptimize(self, T=10000.0, cool=0.99, step=10):
        # �����ʼ��ֵ
        # vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        vec = [random.random(), random.random(), random.random()]

        # ѭ��
        while T > 0.1:
            # ѡ��һ������ֵ
            i = random.randint(0, 2)
            # ѡ��һ���ı�����ֵ�ķ���
            c = random.randint(-step, step) * 0.015  # -1 or 0 or 1
            # �����µĽ�
            vecb = vec[:]
            vecb[i] += c
            vecb[i] = max(vecb[i], 0)

            # ���㵱ǰ�ɱ����µĳɱ�
            cost1 = self.dormcost(vec)
            cost2 = self.dormcost(vecb)

            # �ж��µĽ��Ƿ�����ԭʼ�� ���� �㷨����һ�����ʽ��ܽϲ�Ľ�
            if cost2 < cost1 or random.random() < math.exp(-(cost2 - cost1)*25 / T):
            # if cost2 < cost1:
                vec = vecb

            T = T * cool  # �¶���ȴ
            print vec[:], "����:", self.dormcost(vec)

        self.printsolution(vec)
        print "ģ���˻��㷨�õ�����С�����ǣ�", self.dormcost(vec)
        return vec

    # �����㷨5�� �Ŵ��㷨
    # ԭ�� �����������һ��⣬���ǳ�֮Ϊ��Ⱥ�����Ż����̵�ÿһ�����㷨�����������Ⱥ�ĳɱ�������
    #       �Ӷ��õ�һ���й����������б���������Ⱥ�����������һ����Ⱥ���������£�
    #       �Ŵ����ӵ�ǰ��Ⱥ��ѡ���������ŵ�һ���ּ�����һ����Ⱥ����Ϊ����Ӣѡ�Ρ�
    #       ���죺��һ�����н����΢С�ġ��򵥵ġ�������޸�
    #       ���棺ѡȡ���Ž��е������⣬����ĳ�ַ�ʽ���н��档�����е��㽻�棬��㽻��;��Ƚ���
    # һ����Ⱥ��ͨ�������Ž��������ı������Դ���������ģ����Ĵ�Сͨ����ɵ���Ⱥ��ͬ��������һ���̻�
    #       һֱ�ظ����С��������µ���Ⱥ����������һ����Ⱥ���������������ﵽָ���ĵ�������֮����ⶼû�е�
    #       ���ƣ��������̾ͽ�����
    # ������
    # popsize-��Ⱥ���� step-����ı�Ĵ�С mutprob-����ͱ���ı��� elite-ֱ���Ŵ��ı��� maxiter-����������
    def geneticoptimize(self, popsize=50, step=1, mutprob=0.5, elite=0.2, maxiter=200):
        # ��������ĺ���
        def mutate(vec):
            res = []
            # if random.random() < 0.34:
            #     res = [vec[0]-0.1, vec[1], vec[2]+0.1]
            #
            # elif random.random() < 0.67:
            #     res = [vec[0]+0.1, vec[1], vec[2]-0.1]
            # else:
            #     res = [vec[0]-0.1, vec[1]+0.1, vec[2]]
            res = [random.random(), random.random(), random.random()]
            return res

        # ��������ĺ��������㽻�棩
        def crossover(r1, r2):
            i = random.randint(0, len(r1) - 1)
            return r1[0:i] + r2[i:]

        # �����ʼ��Ⱥ
        pop = []
        for i in range(popsize):
            # vec = [random.random()/3, random.random()/2, random.random()]
            vec = [random.random(), random.random(), random.random()]
            pop.append(vec)
        # ÿһ�����ж���ʤ����
        topelite = int(elite * popsize)

        # ��ѭ��
        for i in range(maxiter):
            if [] in pop:
                print "***"
            try:
                scores = [(self.dormcost(v), v) for v in pop]
            except:
                print "pop!!", pop[:]
            scores.sort()
            # pdb.set_trace()
            ranked = [v for (s, v) in scores]  # �ⰴ�մ�����С���������


            # ���ʽ��Ŵ�����һ��
            pop = ranked[0: topelite]
            # �����ǰ��Ⱥ����С�ڼȶ�����������ӱ���ͽ����Ŵ�
            while len(pop) < popsize:
                # �����С�� mutprob ����죬���򽻲�
                if random.random() < mutprob:  # mutprob���ƽ���ͱ���ı���
                    # ѡ��һ������
                    c = random.randint(0, topelite)
                    # ����

                    temp = mutate(ranked[c])
                    if temp == []:
                        print "******", ranked[c]
                    else:
                        pop.append(temp)

                else:
                    # ���ѡ������������н���
                    c1 = random.randint(0, topelite)
                    c2 = random.randint(0, topelite)
                    pop.append(crossover(ranked[c1], ranked[c2]))
            # �����ǰ��Ⱥ�д�����С�Ľ�
            print scores[0][1], "���ۣ�", scores[0][0]
        self.printsolution(scores[0][1])
        print "�Ŵ��㷨��õ���С���ۣ�", scores[0][0]
        return scores[0][1]

if __name__ == '__main__':
    dormsol = dorm(94, type='weeks')
    #sol = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #dormsol.printsolution(sol)
    #dormsol.dormcost(sol)

    # ����1������²�
    dormsol.randomoptimize(30000)

    # ����2����ɽ��
    # dormsol.hillclimb(domain)

    # ����3��ģ���˻�
    # dormsol.annealingoptimize()

    # ����4���Ŵ��㷨
    # vec = dormsol.geneticoptimize(mutprob=0.8, maxiter=1000)
    # vec = [0.17, 0.34, 0.34]
    # vec1 = [0.15809659303455248, 0.31596469436756436, 0.3890133104417647]
    #
    # print dormsol.dormcost(vec)

ed = time.time()
print ed - st
