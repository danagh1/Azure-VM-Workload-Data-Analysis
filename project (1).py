import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#Baraa Abu Asfar
#Dana Ghazal
#Aya Alali
#from 195 file
data_path = r'C:\Users\dell\Desktop\vm_cpu_readings-file-133-of-195.csv'
headers=['timestamp','vm id','min cpu','max cpu','avg cpu']
data = pd.read_csv(data_path, header=None, index_col=False,names=headers,delimiter=',')
time=data[data['timestamp']==(1759800)]
maxcpu=time['max cpu']
counts_MAX =(data.groupby(maxcpu).size().rename('Freq')).reset_index()
counts_MAX = counts_MAX.rename(columns={'max cpu': 'Bucket'})
counts_MAX['cum'] = counts_MAX['Freq'].cumsum() / counts_MAX['Freq'].sum() * 100
ax = counts_MAX.plot(x='Bucket', y='cum',linestyle='-',label='Max')
ax.set_xlabel('CPU Utilization')
ax.set_ylabel('CDF')
ax.set_xlim([1, 100])
ax.legend()
plt.title('VM CPU Utilization for machines that timestamp equal 1759800')
plt.show()
avg=data[data['avg cpu'] > 10]
mincpu=avg['min cpu']
counts_MIN = (data.groupby(mincpu).size().rename('Freq')).reset_index()
counts_MIN = counts_MIN.rename(columns={'min cpu': 'Bucket'})
counts_MIN['cum'] = counts_MIN['Freq'].cumsum() / counts_MIN['Freq'].sum() * 100
ax= counts_MIN.plot(x='Bucket', y='cum', linestyle='--', logx=False, color='g',label='Min')
ax.set_xlabel('CPU Utilization')
ax.set_ylabel('CDF')
ax.set_xlim([1, 100])
ax.legend()
plt.title('VM CPU Utilization for machines that average CPU greater than 10')
plt.show()
print(data.shape)