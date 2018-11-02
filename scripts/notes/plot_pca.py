import csv, uuid
import matplotlib; matplotlib.use('agg')
import pylab as plt
plt.ioff()
from utils import isfile, save_data, load_data
import numpy as np
from sklearn.decomposition import PCA
import pickle
import os

def plot_pca_explained_var(user_matrix, comp_range, comp_step, img_path, pca_format):
    user_matrix = np.array(user_matrix)
    num_comp = comp_range[0]
    explained_var_list = []
    num_comp_list = []

    while num_comp <= comp_range[1]:
        pca_file = pca_format.format(num_comp)
        if isfile(pca_file):
            print("Load 'pca' from:", pca_file)
            pca = load_data(pca_file)
        else:
            print("Create 'pca' at:", pca_file)
            pca = PCA(n_components=num_comp)
            pca.fit(user_matrix)
            save_data(pca_file, pca)
        explained_var_list += [sum(pca.explained_variance_ratio_)]
        num_comp_list += [num_comp]
        num_comp += comp_step

    percentage_explained_var_list = [x*100 for x in explained_var_list]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(num_comp_list, percentage_explained_var_list, 'b*-')
    ax.set_ylim((0, 100))
    plt.grid(True)
    plt.xlabel('Number of principle components')
    plt.ylabel('Percentage of variance explained (%)')
    plt.savefig(img_path)

if __name__ == "__main__":
	data_file = "dept.p"
	with open(data_file, "rb") as f:
		data, _, __= pickle.load(f)
	data_matrix = []
	for d in data:
		print(d[0])
		data_matrix.append(d[0])
	plot_pca_explained_var(user_matrix=data_matrix,
                           comp_range=[10, 200], comp_step=10, img_path="pca_explained_variance.png", pca_format="pca_dir/pca_{}.pickle")
