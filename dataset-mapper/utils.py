def load_categories(filepath):

	categories = []

	with open(filepath, 'r') as f:
		for line in f:
			categories.append(line.strip())
	return categories

def get_stats(filename = "box.csv"):

	box_data = open(filename, 'r')

	imgs = []
	categories = set()

	def find_img_by_name(name):
		for i in range(len(imgs)):
			if (imgs[i]['name'] == name):
				return i
		return -1

	for line in box_data:
		line_splitted = line.split(',')
		if (len(line_splitted) < 8):
			continue
		else:
			img_index = find_img_by_name(line_splitted[0])
			if (img_index == -1):
				imgs.append({
					"name": line_splitted[0],
					'categories': list()
				})
				img_index = len(imgs) - 1

			imgs[img_index]['categories'].append(line_splitted[7])
			categories.add(line_splitted[7])

	categories_stats = { cat : {'total' : 0, 'unique' : 0} for cat in categories}

	for img in imgs:
		categories_set = set(img['categories'])

		for cat in img['categories']:
			categories_stats[cat]['total'] += 1

		for cat in categories_set:
			categories_stats[cat]['unique'] += 1

	return categories_stats

if __name__ == "__main__":

	stats = get_stats()

	for cat, stat in stats.items():
		print(cat)
		print(stat)


	
