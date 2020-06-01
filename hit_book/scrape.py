
import requests	
import json 

def get_image_from_tag(tag,page=1):  #  get images to the tag entered 
	data = requests.get(f'https://api.unsplash.com/search/photos?query={tag}&orientation=landscape&per_page=12&page={page}&client_id=11f2ff5a50fcce4df43aa4c897d132d3f5ad4a84ed0aec7be67718deb5120192')
	data = json.loads(data.text)# convert the string we got into json. 
	total_num_of_images = data['total']
	num_of_pages = data['total_pages']
	urls = []
	if total_num_of_images == 0:# 
		return None 
	result = data['results']
	for i in range(len(result)):
		res = []  # storing both the resolutions so that i can use smaller resoultions to load multiple images , basically optimizing the loading speed of the  website
		res.append(result[i]['urls']['small'])
		res.append(result[i]['urls']['regular'])
		urls.append(res)
	if total_num_of_images <= 12: # return total pages 1
		return {
			'urls': urls, 
			'page_num':page, # for keeping track of the curent page the user is on basically the current page 
			'total_pages':1 # for paginaition , ie the total num of pages available 
		}
	else:  # return total pages num_of_pages 
		return {
			'urls': urls, 
			'page_num':page, # basically the current page
			'total_pages':num_of_pages # for paginaition , ie the total num of pages available 
		}
