
# coding: utf-8

# # Задание: Бэггинг и случайный лес

# In[10]:

import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
matplotlib.style.use('ggplot')
get_ipython().magic('matplotlib inline')
get_ipython().magic("config InlineBackend.figure_format = 'retina'")
# from sklearn.datasets import load_digits
from sklearn import cross_validation, datasets, tree, ensemble #, metrics 


# In[2]:

import sys
sys.path.append('../..')
from lib import *


# In[3]:

digits = datasets.load_digits()


# In[4]:

X = digits.data
y = digits.target 


# In[9]:

plt.gray() 
plt.matshow(digits.images[0]) 
plt.show() 


# Для оценки качества далее нужно будет использовать cross_val_score из sklearn.cross_validation с параметром cv=10. Эта функция реализует k-fold cross validation c k равным значению параметра cv. Мы предлагаем использовать k=10, чтобы полученные оценки качества имели небольшой разброс, и было проще проверить полученные ответы. На практике же часто хватает и k=5. Функция cross_val_score будет возвращать numpy.ndarray, в котором будет k чисел - качество в каждом из k экспериментов k-fold cross validation. Для получения среднего значения (которое и будет оценкой качества работы) вызовите метод .mean() у массива, который возвращает cross_val_score.

# Создайте DecisionTreeClassifier с настройками по умолчанию и измерьте качество его работы с помощью cross_val_score. Эта величина и будет ответом в пункте 1.

# In[6]:

clf = tree.DecisionTreeClassifier(random_state=0)


# In[7]:

get_ipython().magic('time cvs = cross_validation.cross_val_score(clf, X, y, cv=10)')


# In[8]:

pf('w4-as1-1', cvs.mean())


# Воспользуйтесь BaggingClassifier из sklearn.ensemble, чтобы обучить бэггинг над DecisionTreeClassifier. Используйте в BaggingClassifier параметры по умолчанию, задав только количество деревьев равным 100.
# 
# Качество классификации новой модели - ответ в пункте 2. Обратите внимание, как соотносится качество работы композиции решающих деревьев с качеством работы одного решающего дерева.

# In[11]:

clf = ensemble.BaggingClassifier(n_estimators=100, random_state=0)
get_ipython().magic('time cvs = cross_validation.cross_val_score(clf, X, y, cv=10)')
pf('w4-as1-2', cvs.mean())


# Теперь изучите параметры BaggingClassifier и выберите их такими, чтобы каждый базовый алгоритм обучался не на всех d признаках, а на d‾‾√ случайных признаков. Качество работы получившегося классификатора - ответ в пункте 3. Корень из числа признаков - часто используемая эвристика в задачах классификации, в задачах регрессии же часто берут число признаков, деленное на три. Но в общем случае ничто не мешает вам выбирать любое другое число случайных признаков.m

# In[17]:

max_features = int(X.shape[1] ** 0.5)
# max_features
clf = ensemble.BaggingClassifier(n_estimators=100, random_state=0, max_features=max_features)
get_ipython().magic('time cvs = cross_validation.cross_val_score(clf, X, y, cv=10)')
pf('w4-as1-3', cvs.mean())


# Наконец, давайте попробуем выбирать случайные признаки не один раз на все дерево, а при построении каждой вершины дерева. Сделать это несложно: нужно убрать выбор случайного подмножества признаков в BaggingClassifier и добавить его в DecisionTreeClassifier. Какой параметр за это отвечает, можно понять из документации sklearn, либо просто попробовать угадать (скорее всего, у вас сразу получится). Попробуйте выбирать опять же d‾‾√ признаков. Качество полученного классификатора на контрольной выборке и будет ответом в пункте 4.

# In[18]:

max_features = int(X.shape[1] ** 0.5)
# max_features
est = tree.DecisionTreeClassifier(random_state=0, max_features=max_features)
clf = ensemble.BaggingClassifier(est, n_estimators=100, random_state=0)
get_ipython().magic('time cvs = cross_validation.cross_val_score(clf, X, y, cv=10)')
pf('w4-as1-4', cvs.mean())


# Полученный в пункте 4 классификатор - бэггинг на рандомизированных деревьях (в которых при построении каждой вершины выбирается случайное подмножество признаков и разбиение ищется только по ним). Это в точности соответствует алгоритму Random Forest, поэтому почему бы не сравнить качество работы классификатора с RandomForestClassifier из sklearn.ensemble. Сделайте это, а затем изучите, как качество классификации на данном датасете зависит от количества деревьев, количества признаков, выбираемых при построении каждой вершины дерева, а также ограничений на глубину дерева. Для наглядности лучше построить графики зависимости качества от значений параметров, но для сдачи задания это делать не обязательно.

# На основе наблюдений выпишите через пробел номера правильных утверждений из приведенных ниже в порядке возрастания номера (это будет ответ в п.5)
# 
# 1) Случайный лес сильно переобучается с ростом количества деревьев
# 
# 2) При очень маленьком числе деревьев (5, 10, 15), случайный лес работает хуже, чем при большем числе деревьев
# 
# 3) С ростом количества деревьев в случайном лесе, в какой-то момент деревьев становится достаточно для высокого качества классификации, а затем качество существенно не меняется.
# 
# 4) При большом количестве признаков (для данного датасета - 40, 50) качество классификации становится хуже, чем при малом количестве признаков (5, 10). Это связано с тем, что чем меньше признаков выбирается в каждом узле, тем более различными получаются деревья (ведь деревья сильно неустойчивы к изменениям в обучающей выборке), и тем лучше работает их композиция.
# 
# 5) При большом количестве признаков (40, 50, 60) качество классификации лучше, чем при малом количестве признаков (5, 10). Это связано с тем, что чем больше признаков - тем больше информации об объектах, а значит алгоритм может делать прогнозы более точно.
# 
# 6) При небольшой максимальной глубине деревьев (5-6) качество работы случайного леса намного лучше, чем без ограничения глубины, т.к. деревья получаются не переобученными. С ростом глубины деревьев качество ухудшается.
# 
# 7) При небольшой максимальной глубине деревьев (5-6) качество работы случайного леса заметно хуже, чем без ограничений, т.к. деревья получаются недообученными. С ростом глубины качество сначала улучшается, а затем не меняется существенно, т.к. из-за усреднения прогнозов и различий деревьев их переобученность в бэггинге не сказывается на итоговом качестве (все деревья преобучены по-разному, и при усреднении они компенсируют переобученность друг-друга).

# In[19]:

pf('w4-as1-5', "2 3 4 7")


# In[ ]:



