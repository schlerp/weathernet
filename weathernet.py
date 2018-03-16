import os
import pandas as pd

def get_data(data_dir):
    all_data_frames = [[pd.DataFrame()]]
    for file_name in os.listdir(data_dir):
        full_file_name = os.path.join(data_dir, file_name)
        data = pd.read_csv(full_file_name, 
                           header=5,
                           skiprows=[0,1,2,3,4]
                           usecols=[x for x in range(1, 21)])
        all_data_frames.append(data)
    return pd.concat(all_data_frames)

if __name__ == '__main__':
    data_dir = './data/IDCJDW8014/'
    data = get_data(data_dir)