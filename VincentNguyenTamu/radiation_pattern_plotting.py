import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# filepath = 'Y:\\joshruff\\NI_Coupled_Arrays\\Single_Patch_Radiation_Pattern.csv'
#filepath = 'Y:\\joshruff\\NI_Coupled_Arrays\\Patch_Array_Radiation_Pattern.csv'
filepath = '/Users/petervo/Documents/PycharmProjects/Single_Patch_Radiation_Pattern.csv'

test_df = pd.read_csv(filepath)

fig = plt.figure(figsize=(9,5))
#print(test_df.head)

for column in test_df:
    if column == "Theta [deg]":
        continue
    column_name = column.replace(" []","")

    if("Phi='0deg'" in column):
        ax = plt.subplot(121,projection= 'polar')
        #ax.set_ylim(-20,20)
        ax.set_rticks([-20,-10,0,10,20])
        ax.set_theta_zero_location("N")
        ax.plot(test_df['Theta [deg]']*np.pi/180,test_df[column],label=column_name)
        ax.legend(loc='center',bbox_to_anchor=(0.45, -0.15))

    if("Phi='90deg'" in column):
        ax2 = plt.subplot(122, projection='polar')
        #ax2.set_ylim(-20, 20)
        ax2.set_rticks([-20, -10, 0, 10,20])
        ax2.set_theta_zero_location("N")
        ax2.plot(test_df['Theta [deg]']*np.pi/180,test_df[column],label=column_name)
        ax2.legend(loc='center',bbox_to_anchor=(0.55, -0.15))
plt.show()
fig.savefig("Plots.png")