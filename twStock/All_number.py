import requests
import datetime
import os
import pandas as pd
import codecs
import csv
import time




def today_format():
	today_f = datetime.date.today()
	print(today_f)
	#today_f = str(today_f).replace('-','')
	if today_f.month < 10:
		new_today = str(today_f.year) + '0' + str(today_f.month)
	else:
		new_today = str(today_f.year) + str(today_f.month)
		
	if today_f.month - 1 < 10:
		old_today = str(today_f.year) + '0' + str(today_f.month - 1)
	else:
		old_today = str(today_f.year) + str(today_f.month - 1)
	return new_today, old_today

def transtime(filetime):
	tyear = filetime.tm_year
	tmonth = filetime.tm_mon
	if tmonth < 10:
		tmonth = '0' + str(tmonth)
	tday = filetime.tm_mday
	if tday < 10:
		tday = '0' + str(tday)
	
	n_date = str(tyear) + str(tmonth) + str(tday)
	return n_date
	
def todaytime():
	today_nf = datetime.date.today()
	tt_year = today_nf.year
	tt_month = today_nf.month
	tt_day = today_nf.day
	if tt_month < 10:
		tt_month = '0' + str(tt_month)
		
	if tt_day < 10:
		tt_day = '0' + str(tt_day)
		
	tt_day = str(tt_year) + str(tt_month) + str(tt_day)
	return tt_day

def get_all_num_csv(type):
	now_date, old_date = today_format()
	print(now_date, '  ', old_date)


	csv_path = './'
	now_file_name = ''
	old_file_name = ''
	if type == 'twse':
		now_file_name = now_date + '_twse.csv'
		old_file_name = old_date + '_twse.csv'
	elif type == 'tpex':
		now_file_name = now_date + '_tpex.csv'
		old_file_name = old_date + '_tpex.csv'
	else:
		now_file_name = now_date + '.csv'
		old_file_name = old_date + '.csv'
		
	if os.path.isfile(csv_path + old_file_name):
		os.remove(csv_path + old_file_name)
	else:
		print('No old csv!!!')
		
	today_time = todaytime()
	if os.path.isfile(csv_path + now_file_name):
		nowfile_time = time.localtime(os.stat(csv_path + now_file_name).st_ctime)
		nowfile_time = transtime(nowfile_time)
		print('hgggsss111222, ', nowfile_time, ', yyy, ', today_time)
		if str(nowfile_time) == str(today_time):
			print("The day of file ", now_file_name, ' is today!!! Do not download again!!')
		else:
			print("Remove and download again!!!")
			os.remove(csv_path + now_file_name)
			

		
		
	print(csv_path + now_file_name)
	if os.path.isfile(csv_path + now_file_name):
		print('Do not download csv!!! File is existing!!!')
	else:
		print('Download csv!!!')
		#strMode=4 上櫃, strMode=2, 上市
		httpname = ''
		if type == 'twse':
			httpname = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
		elif type == 'tpex':
			httpname = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
		else:
			httpname = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
		res = requests.get(httpname)
		df = pd.read_html(res.text)[0]
		df.to_csv(csv_path + now_file_name,index=False,encoding="big5hkscs")
		

def check_int(value):
	try:
		value = int(value)
		return True
	except Exception as e:
		#write_txt.write_log('read_csv_error.txt', 'check int Num: ' + str(new_tpex_num) + ' error! Errr: ' + str(e))
		#print(value, '  ', str(e))
		
		return False	
		
def trans_date(date):
	date = date.split('/')
	new_date = ''
	#[0]年 [1]月 [2]日
	for i in range(len(date)):
		new_date = new_date + date[i]
	return new_date
		
def is_date(date,num):
	date= str(date)
	#print('sss=',date)
	try:
		time.strptime(date, "%Y/%m/%d")
		return trans_date(date)
	except Exception as e:
		#print('date error=', e)
		msg = str(num) + ' has error time! error=' + str(e)
		write_log('date_error.txt',msg)
		return 'xxxxxx'
		
		
def get_csv_data(type):
	now_date, old_date = today_format()
	file_name = ''
	if type == 'twse':
		file_name = str(now_date) + "_twse.csv"
	elif type == 'tpex':
		file_name = str(now_date) + "_tpex.csv"
	else:
		file_name = str(now_date) + ".csv"
	open_csv = codecs.open(file_name, "r", encoding='big5hkscs')
	rows = csv.reader(open_csv)
	row_list = list()
	all_num_list = list()
	all_num_type = list()
	all_num_s_time = list() #股票發行時間
	for row in rows:
		row_list.append(row)
	for i in range(len(row_list)):
		tpex_name = row_list[i][0]
		tpex_number = tpex_name.split('　')
		new_tpex_num = tpex_number[0]
		#second split, check special name, ex. 6497 亞獅康-KY
		if ' ' in new_tpex_num:
			#print(new_tpex_num)
			new_tpex_num = new_tpex_num.split(' ')
			new_tpex_num = new_tpex_num[0]
			#print(new_tpex_num)
		try:
			if check_int(new_tpex_num):
				if len(str(new_tpex_num)) == 4:
					#write_txt.write(num_txt,new_tpex_num)
					#print(new_tpex_num, ' ## ', row_list[i][4])
					if len(str(row_list[i][4])) != 0:
						all_num_list.append(new_tpex_num)
						all_num_type.append(str(row_list[i][4]))
						date_public = is_date(str(row_list[i][2]), new_tpex_num)
						all_num_s_time.append(date_public)
						#print(new_tpex_num, ' ## ', row_list[i][4])
		except Exception as e:
			#write_txt.write_log('read_csv_error.txt', 'trans tpex Num: ' + str(new_tpex_num) + ' error! Errr: ' + str(e))
			print(str(e))
	open_csv.close()
	del rows, row_list
	print('**all_number_list**, \n', all_num_list)
	print('**all_number_list len**, \n', len(all_num_list))
	print('**all_number_type len**, \n', len(all_num_type))
	print('**all_number_type set**, \n', set(all_num_type))
	print('**all_number_type set len**, \n', len(set(all_num_type)))
	return all_num_list, all_num_type, all_num_s_time
		
def main(type):
	get_all_num_csv(type)
	all_numbers, all_number_types, all_number_public = get_csv_data(type)
	return all_numbers, all_number_types, all_number_public
	