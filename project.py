#0183507 Dana Ghazal
#0185264 Baraa AbuAsfar
#0189980 Aya Al-ali
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
data_path = r'C:\Users\DELL\Desktop\vmtable.csv'
headers=['vmid','subscriptionid','deploymentid','vmcreated', 'vmdeleted', 'maxcpu', 'avgcpu', 'p95maxcpu', 'vmcategory', 'vmcorecountbucket', 'vmmemorybucket']
data = pd.read_csv(data_path, header=None, index_col=False,names=headers,delimiter=',')
cores=data[data['vmcorecountbucket']==('8')]
avg=cores['avgcpu']
counts_AVG =(data.groupby(avg).size().rename('Freq')).reset_index()
counts_AVG = counts_AVG.rename(columns={'avgcpu': 'Bucket'})
counts_AVG['cum'] = counts_AVG['Freq'].cumsum() / counts_AVG['Freq'].sum() * 100
ax = counts_AVG.plot(x='Bucket', y='cum',linestyle='-',label='Average')
ax.set_xlabel('CPU Utilization')
ax.set_ylabel('CDF')
ax.set_xlim([1, 100])
ax.legend()
plt.title('VM CPU Utilization for machines with only 8 cores')
plt.show()
print('****************************************************************')
memory=data[data['vmmemorybucket']==('2')]
maxcpup95=memory['p95maxcpu']
counts_P95 = (data.groupby(maxcpup95).size().rename('Freq')).reset_index()
counts_P95 = counts_P95.rename(columns={'p95maxcpu': 'Bucket'})
counts_P95['cum'] = counts_P95['Freq'].cumsum() / counts_P95['Freq'].sum() * 100
ax= counts_P95.plot(x='Bucket', y='cum', linestyle='--', logx=False, color='darkmagenta',label='P95 Max')
ax.set_xlabel('CPU Utilization')
ax.set_ylabel('CDF')
ax.set_xlim([1, 100])
ax.legend()
plt.title('VM CPU Utilization for machines with only 2 GB memory')
plt.show()
print('*******************************************************************')
data['lifetime'] = np.maximum((data['vmdeleted'] - data['vmcreated']),300)/ 3600
counts_lifetime = (data.groupby('lifetime').size().rename('Freq')).reset_index()
counts_lifetime = counts_lifetime.rename(columns={'lifetime': 'bucket'})
counts_lifetime['cum'] = counts_lifetime['Freq'].cumsum() / counts_lifetime['Freq'].sum() * 100
ax = counts_lifetime[0:2500].plot(x='bucket', y='cum',linestyle='-', color='darkmagenta',label='lifetime')
ax.set_xlabel('Lifetime in Hours')
ax.set_ylabel('CDF')
ax.legend()
plt.title('VM lifetime in hours')
plt.show()
print('*******************************************')
category0=data[data['vmcategory']==('Interactive')]
maxcpu=category0['maxcpu']
counts_P95 = (data.groupby(maxcpu).size().rename('Freq')).reset_index()
counts_P95 = counts_P95.rename(columns={'maxcpu': 'Bucket'})
counts_P95['cum'] = counts_P95['Freq'].cumsum() / counts_P95['Freq'].sum() * 100
ax= counts_P95.plot(x='Bucket', y='cum', linestyle='--', logx=False, color='b',label='Max')
ax.set_xlabel('CPU Utilization')
ax.set_ylabel('CDF')
ax.set_xlim([1, 100])
ax.legend()
plt.title('VM CPU Utilization for machines that type Interactive')
plt.show()
print('**************************************************')
datapath=r'C:\Users\DELL\Desktop\deployments (1).csv'
deployment_headers=['deploymentid','deploymentsize']
deployment = pd.read_csv(datapath, header=None, index_col=False,names=deployment_headers,delimiter=',')
counts_deployment = pd.DataFrame(deployment.groupby('deploymentsize').size().rename('Freq')).reset_index()
mu = 0
sigma = 1
counts_deployment['cum'] = (1 / (np.sqrt(2 * np.pi * np.power(sigma, 2)))) * \
    (np.power(np.e, -(np.power((counts_deployment['Freq'] - mu), 2) / (2 * np.power(sigma, 2)))))
counts_deployment = counts_deployment.rename(columns={'deploymentsize': 'bucket'})
ax = counts_deployment[0:50].plot(x='bucket', y='cum', linestyle='-', color='b',label='probability')
plt.title('VM Deployment Size')
ax.set_xlabel('# VMs')
ax.set_ylabel('PDF')
ax.legend()
plt.show()
print('**************************************************')
category1=data[data['vmcategory']==('Delay-insensitive')]
coress=category1['vmcorecountbucket']
counts_mm =(data.groupby(coress).size().rename('Freq')).reset_index()
counts_mm = counts_mm.rename(columns={'vmcorecountbucket': 'Bucket'})
counts_mm['cum']= (counts_mm['Freq']*100).sort_index()
ax = counts_mm.plot(x='Bucket', y='cum',linestyle='-',label='percentage')
ax.set_xlabel('core count bucket')
ax.set_ylabel('% of VMs')
ax.legend()
plt.title('VM Cores Distribution for machines that type Delay-insensitive')
plt.show()
print('************************************************************************')
category2=data[data['vmcategory']==('Interactive')]
memor=category2['vmmemorybucket']
counts_cc =(data.groupby(memor).size().rename('Freq')).reset_index()
counts_cc = counts_cc.rename(columns={'vmmemorybucket': 'Bucket'})
counts_cc['cum']= (counts_cc['Freq']*100).sort_index()
ax = counts_cc.plot(x='Bucket', y='cum',linestyle=':',color='darkmagenta',label='percentage')
ax.set_xlabel('Memory Size (GB) Bucket')
ax.set_ylabel('% of VMs')
ax.legend()
plt.title('VM Memory Distribution for machines that type Interactive')
plt.show()
print('*********************************************************************')
max_value_vmcorecountbucket = 30
max_value_vmmemorybucket = 70
data = data.replace({'vmcorecountbucket':'>24'},max_value_vmcorecountbucket)
data = data.replace({'vmmemorybucket':'>64'},max_value_vmmemorybucket)
data = data.astype({"vmcorecountbucket": int, "vmmemorybucket": int})
data['corehour'] = data['lifetime'] * data['vmcorecountbucket']
data.head()
count_cate = pd.DataFrame(data.groupby('vmcategory')['corehour'].sum().rename('Freq')).reset_index()
count_cate = count_cate.rename(columns={'vmcategory': 'Bucket'})
count_cate['cum'] = count_cate['Freq'] / count_cate['Freq'].sum() * 100
ax = count_cate.plot(x='Bucket', y='cum',linestyle='-.',label='percentage')
ax.set_xlabel('vm category')
ax.set_ylabel('% of core hours')
ax.legend()
plt.title('VM Category Distribution')
plt.show()
print('**************************************************************************')
print(data.shape)
print(deployment.shape)