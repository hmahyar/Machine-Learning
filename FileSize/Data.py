
import numpy as np
import hashlib



logfile = open('../../../DataSet/Cache/W1/model.csv')
Udacity = open('../../../DataSet/Cache/W1/Udacity.csv','w')
#Udacity.write('Host'+'\t'+'Extention'+'\t'+'DataType'+'\t'+'IsMobile'+'\t'+'FileSize'+'\n')
c=0
for line in logfile:
	if c<=500000:
		url= line.split('\t')[1].lower().split('/')[2].strip()
		if len(line.split('\t')[1].split('/')[-1].split('.')[-1])<4 \
			and not url.startswith('ec-media.soundcloud')\
			and not url.startswith('ec-hls-media.soundcloud') \
			and not url.startswith('wpc.a310.edgecastcdn')\
			and not url.startswith('wac.a310.edgecastcdn')\
			and not url.startswith('fc09.deviantart')\
			and not url.startswith('wpc.970a.edgecastcdn')\
			and not url.startswith('wpc.970A.edgecastcdn')\
			and not url.startswith('wpc.573d.edgecastcdn')\
			and not url.startswith('fc03.deviantart')\
			and not url.startswith('fc00.deviantart')\
			and not url.startswith('fc02.deviantart')\
			and line.split('\t')[0]!='-':
				#try:
					data = line.split('\t')
					if(int(data[0]))>0:
						
						host  = data[1].split('/')[2].lower().strip()
						extention = data[1].split('/')[-1].split('.')[-1].lower().strip()
						IsMobile = data[2].lower().strip()
						data_type = data[3].lower().strip()
						file_size=int(np.ceil(np.log2(int(data[0].lower().strip()))))
						if file_size<19:
							file_size=19
						if file_size>28:
							file_size=28
						hst = hashlib.md5(host)
						Udacity.write(hst.hexdigest()+'\t'+extention+'\t'+data_type+'\t'+IsMobile+'\t'+str(file_size)+'\n')
						c+=1;
						print c
				#except:
				#	pass
					
	else:
		break