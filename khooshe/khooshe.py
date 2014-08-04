import os
import shutil
import csv
import numpy as np
from scipy.cluster.vq import kmeans,vq


def create_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    os.makedirs(folder_name)


def get_points_count(points_file):
    with open(points_file) as f:
        count = sum(1 for line in f)

    return count


def read_point_data(points_file, point_array):
    with open(points_file) as csv_f:
        reader = csv.reader(csv_f)
        try:
            for index, row in enumerate(reader):
                point_array[index] = [float(row[0]),float(row[1])]
        except:
            raise error("Cannot read data from point text file.")


def unique_array(point_array):
    a = np.ascontiguousarray(point_array)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))

    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def make_first_layer(unique_points, centroids_number):
    new_data = {}
    centroids,_ = kmeans(unique_points,centroids_number)
    idx,_ = vq(unique_points,centroids)
    shapes = []
    for each in range(len(centroids)):
        points = unique_points[idx==each]
        new_data['{0}'.format(each)] = points
        shapes.append(points.shape[0])
    create_folder('0')
    with open('0/0.csv','w') as csv_n:
        writer = csv.writer(csv_n, delimiter=',')
        writer.writerow(['latitude', 'longitude', 'label'])
        for index, centroid in enumerate(centroids):
            writer.writerow([centroid[0],centroid[1], shapes[index]])

    return centroids, shapes, new_data


def make_rest_of_layers(data, centroids, shapes, centroids_number):
    count = 1
    while True:
        create_folder(str(count))
        new_datas = {}
        for key in data.keys():
            if data[key].shape[0] < 10:
                with open('{0}/{1}.csv'.format(count, key), 'w') as csv_n:
                    writer = csv.writer(csv_n)
                    writer.writerow(['latitude', 'longitude', 'label'])
                    for point in data[key]:
                        writer.writerow([point[0], point[1], 'p'])
            else:
                centroids,_ = kmeans(data[key], centroids_number)
                idx,_ = vq(data[key],centroids)
                for each in range(len(centroids)):
                    points = data[key][idx==each]
                    new_datas['{0}_{1}'.format(key, each)] = points
                    shapes.append(points.shape[0])
                with open('{0}/{1}.csv'.format(count, key),'w') as csv_n:
                    writer = csv.writer(csv_n)
                    writer.writerow(['latitude', 'longitude', 'label'])
                    for a, cent in enumerate(centroids):
                        writer.writerow([cent[0], cent[1], shapes[a]])
                shapes = []
        data = 0
        data = new_datas
        new_datas = 0
        count += 1
        if data == {}:
            break


if __name__ == '__main__':
    CENTROIDS_NUMBER = 15
    POINTS_FILE = 'emp_sample.csv'
    points_count = get_points_count(POINTS_FILE)
    point_array = np.zeros([points_count,2])

    read_point_data(POINTS_FILE, point_array)
    print "Read points --> DONE."

    unique_points = unique_array(point_array)
    print "Find unique points --> DONE."

    centroids, shapes, new_data = make_first_layer(unique_points, CENTROIDS_NUMBER)

    make_rest_of_layers(new_data, centroids, shapes, CENTROIDS_NUMBER)
    print "Create layers --> DONE."