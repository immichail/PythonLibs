from utils import *

def load_data(filepath):

    def line_to_data(s):
        s = s.split(',')
        if (len(s) == 8):
            s.append(0)
        
        try:
            for i in range(1, 7):
                s[i] = int(s[i])
        except:
            return None

        return s

    dataset = []

    with open(filepath, 'r') as f:
        for line in f:
            data_item = line_to_data(line)
            if (data_item):
                dataset.append(data_item)

    return dataset

def convert_to_darknet_format(filepath):
    
    train_file = open('rooter.txt', 'w')

    dataset = load_data(filepath)
    categories = load_categories('categories.txt')

    categories = {cat : i for i, cat in enumerate(categories)}

    dataset_darknet = []

    for item in dataset:
        if (len(item) < 8):
            continue
        id = item[0]
        x1 = item[1]
        y1 = item[2]
        x2 = item[3]
        y2 = item[4]
        w = item[6]
        h = item[5]
        cat = item[7].strip()
        center_x = float(abs(x1 + x2) / 2 / w)
        if (center_x > 1):
            center_x = 1
        if (center_x < 0):
            center_x = 0
        center_y = float(abs(y1 + y2) / 2 / h)
        if (center_y > 1):
            center_y = 1
        if (center_y < 0):
            center_y = 0
        box_w = float(abs(x1 - x2) / w)
        if (box_w > 1):
            box_w = 1
        if (box_w < 0):
            box_w = 0
        box_h = float(abs(y1 - y2) / h)
        if (box_h > 1):
            box_h = 1
        if (box_h < 0):
            box_h = 0
        dataset_darknet_item = [
            categories[cat], 
            center_x,
            center_y,
            box_w,
            box_h
        ]
        dataset_darknet_item = [str(d) for d in dataset_darknet_item]
        dataset_darknet.append(dataset_darknet_item)
        with open("./labels/" + id.replace(".jpg", "") + '.txt', "a+") as f:
            f.write(" ".join(dataset_darknet_item) + "\n")
        train_file.write("../rooter/images/" + id + "\n")

    train_file.close()
    return dataset_darknet

if __name__ == "__main__":
    dataset = convert_to_darknet_format('box.csv')
