import warnings
from os import listdir, makedirs
from os.path import isdir, join

import matplotlib.pyplot as plt
import numpy as np
from shutil import rmtree
from tools.decorators import string2numpy

warnings.simplefilter("error")

demo_data="""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

demo_result=31

start_symbol=242
end_symbol=228
directions = np.array([[0,0],[1,0],[0,1],[-1,0],[0,-1]])

def plot_map(*maps):
    fig, axes = plt.subplots(len(maps),1,sharex=True,sharey=True)
    for ax,m in zip(np.ravel([axes]),maps):
        ax.imshow(m)
    return fig,axes

def save_img(*args,**kwargs):
    fig, axes = plot_map(*args,**kwargs)
    outdir = "plots"
    if not isdir(outdir):
        makedirs(outdir)
    n = len(listdir(outdir))
    fig.savefig(join(outdir,"%05d.jpg"%n))
    plt.close(fig)
    

def compute_dist(map):
    dist_map = np.zeros_like(map,dtype=np.uint64)+np.inf
    dist_map[map==end_symbol]=0
    all_indexes = np.transpose(np.unravel_index(np.arange(dist_map.size),dist_map.shape))
    all_neightboors = np.clip(all_indexes[:,None]+directions[None,:,:],0,np.array(dist_map.shape)[None,None]-1)

    while not np.all(dist_map<np.inf):
        # Get the indexes where the distance is finite and that have neightboors where distance is infinite
        selector = np.logical_and((dist_map<np.inf).ravel(),(dist_map[all_neightboors[:,:,0],all_neightboors[:,:,1]]==np.inf).any(-1))
        # selector = (dist_map<np.inf).ravel()
        indexes = all_indexes[selector,:]
        # For each index, get its neightboors
        neightboors = indexes[:,None]+directions[None,:,:]
        # filter neightboors that are inside the map
        neightboors_clip = neightboors.clip(0,np.array(dist_map.shape)[None,None]-1)
        valid_neightboor = (neightboors_clip==neightboors).all(-1)
        # get height of neightboors
        height = map[neightboors_clip[:,:,0],neightboors_clip[:,:,1]]
        # Find which neightboors allow to reach the current point
        delta = height[:,0,None]-height[:,1:]
        is_valid = ((delta <=1) + (height[:,1:]==start_symbol) + (height[:,1:]==(ord('z')-ord('a'))))*valid_neightboor[:,1:]
        assert is_valid.any()
        # Mark distance of valid neightboors
        indexes_valid = indexes[np.broadcast_to(np.arange(indexes.shape[0])[:,None],is_valid.shape)[is_valid],:]
        base_dist = dist_map[indexes_valid[:,0],indexes_valid[:,1]]
        selected = neightboors[:,1:,:][np.broadcast_to(is_valid[:,:,None],neightboors[:,1:,:].shape)].reshape((-1,2))

        # Find unique
        selected_unique = np.unique(selected,axis=0)
        selector = (selected_unique[:,None,:]==selected[None,:,:]).all(-1)
        base_dist = np.broadcast_to(base_dist[None,:],(selector.shape))
        base_dist=np.where(selector,base_dist,np.nan)
        base_dist = np.nanmin(base_dist,axis=1)
        previous_dist_values = dist_map.ravel()[np.ravel_multi_index(selected_unique.T,map.shape)]
        new_value = np.min([base_dist + 1,previous_dist_values],axis=0)
        update = (previous_dist_values != new_value).any()
        if not update:
            break
        dist_map.ravel()[np.ravel_multi_index(selected_unique.T,map.shape)]=new_value
    return dist_map


def main(data_str):
    try:
        rmtree("plots")
    except Exception:
        pass
    map = (np.frombuffer(data_str.replace("\n","").encode("utf-8"),dtype=np.uint8).reshape((-1,data_str.find("\n")))-ord('a')).astype(np.int64)
    dist_map = compute_dist(map)
    res1 = int(dist_map[map==start_symbol].ravel()[0])-2
    res2 = int(np.nanmin(dist_map[map==0]))-2
    return res1,res2
