import math
import numpy as np 
import re

def main(closeList):
	bb_data = closeList
	ma20 = sum(bb_data[0:20])
	#print(len(bb_data))
	#print(ma20)
	High_array = list()
	Medium_array = list()
	Low_array = list()

	for i in range(len(bb_data) - 20):
		ma20 = sum(bb_data[(0 + i):(20 + i)])
		#print('ma20, ', i, ' = ', ma20)
		#ma20 = math.floor(ma20*10000)
		#ma20 = ma20 / 10000
		std_ma20 = np.std(bb_data[(0 + i):(20 + i)], ddof=1)
		#print('new ma20, ', i, ' = ', ma20)
		#print('ma20 std, ', i, ' = ', std_ma20)
		#std_ma20 = float('%.2f' % std_ma20)
		average_ma20 = ma20 / 20
		average_ma20 = float('%.2f' % average_ma20)
		High = math.floor((average_ma20 + (std_ma20*2))*100)
		High = High / 100
		Low = math.floor((average_ma20 - (std_ma20*2))*100)
		Low = Low / 100
		
		High_array.append(High)
		Medium_array.append(average_ma20)
		Low_array.append(Low)
		#print('new ma20 std, ', i, ' = ', std_ma20)
		#print('High = ', average_ma20 + (std_ma20*2))
		#print('High = ', High)
		#print('Medium = ', average_ma20)
		#print('Low = ', average_ma20 - (std_ma20*2))
		#print('\n')
	return High_array, Medium_array, Low_array