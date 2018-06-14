from sys import *
import sys

from scipy.optimize import newton
from scipy.special import zeta
import scipy as sp
import numpy as np
from scipy.stats import uniform
import matplotlib.pyplot as plt
import pandas as pd
import powerlaw as pl

filename = argv[1]
p_type = bool(argv[2])
prior=argv[3]
df = pd.read_csv(filename, names=['item'])
items = np.array(df.item)

bic_df=pd.DataFrame(index=range(10),columns=['bic1','bic2','bic3'])
final_array1_g=np.array([])
final_array2_g = np.array([])
final_array3_g = np.array([])

final_array2_w = np.array([])
final_array3_w = np.array([])

for i in range(10):
    fit1= pl.Fit_Bayes(items, mixed=1, discrete=p_type,prior=prior)
    fit2 = pl.Fit_Bayes(items, mixed=2, discrete=p_type , prior=prior)
    fit3 = pl.Fit_Bayes(items, mixed=3, discrete=p_type, prior=prior)
    gammas1, weights1=fit1.posterior()
    gammas2, weights2 = fit2.posterior()
    gammas3, weights3 = fit3.posterior()
    bic_df.bic1.iloc[i]= fit1.bic(gammas1,weights1)
    bic_df.bic2.iloc[i] = fit2.bic(gammas2, weights2)
    bic_df.bic3.iloc[i] = fit3.bic(gammas3, weights3)
    final_array1_g=np.append(final_array1_g,gammas1)
    final_array2_g = np.append(final_array2_g, gammas2)
    final_array3_g = np.append(final_array3_g, gammas3)

    final_array2_w = np.append(final_array2_w, weights2)
    final_array3_w = np.append(final_array3_w, weights3)

df_gammas1 = pd.DataFrame(final_array1_g, columns=['exponent'])
df_gammas2 = pd.DataFrame(final_array2_g, columns=['exponent'])
df_gammas3 = pd.DataFrame(final_array3_g, columns=['exponent'])

df_weight2 = pd.DataFrame(final_array2_w, columns=['weight'])
df_weight3 = pd.DataFrame(final_array3_w, columns=['weight'])

df_gammas1.to_csv('gamma1_' + filename + '_' + prior, index=False)
df_gammas2.to_csv('gamma2_' + filename+'_'+prior, index=False)
df_gammas3.to_csv('gamma3_' + filename + '_' + prior, index=False)

df_weight2.to_csv('weight2_' + filename + '_' + prior, index=False)
df_weight3.to_csv('weight3_' + filename + '_' + prior, index=False)

bic_df.to_csv('bic_'+filename+'_'+prior,index=False)