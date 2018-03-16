import os
import pandas as pd


data_col_names = ['date', 
                  'min_temp', 'max_temp', 
                  'rainfall', 'evaporation', 'sunshine', 
                  'max_wind_dir', 'max_wind_speed', 'max_wind_time',
                  '9am_temp', '9am_rel_hum', '9am_clouds', '9am_wind_dir',
                  '9am_wind_speed', '9am_msl_pres', 
                  '3pm_temp', '3pm_rel_hum', '3pm_clouds', '3pm_wind_dir',
                  '3pm_wind_speed', '3pm_msl_pres']

direction_map = {'N':  0, 'NNE':  1, 'NE':  2, 'ENE':  3,
                 'E':  4, 'ESE':  5, 'SE':  6, 'SSE':  7,
                 'S':  8, 'SSW':  9, 'SW': 10, 'WSW': 11,
                 'W': 12, 'NNW': 13, 'NW': 14, 'WNW': 15
                 }


def get_data(data_dir):
    all_data_frames = []
    for file_name in os.listdir(data_dir):
        full_file_name = os.path.join(data_dir, file_name)
        data = pd.read_csv(full_file_name, 
                           header=0,
                           names=data_col_names,
                           skiprows=[0,1,2,3,4],
                           usecols=[x for x in range(1, 22)],
                           encoding='cp1252')
        all_data_frames.append(data)
    all_data = pd.concat(all_data_frames, ignore_index=True)
    all_data = clean_data(all_data)
    return all_data

def clean_data(df):
    df = df.fillna(0.0)
    df['max_wind_dir'] = df['max_wind_dir'].map(direction_map)
    df['9am_wind_dir'] = df['9am_wind_dir'].map(direction_map)
    df['3pm_wind_dir'] = df['3pm_wind_dir'].map(direction_map)
    df['max_wind_speed'] = df['max_wind_speed'].astype(str).replace('Calm', '0').astype(float)
    df['9am_wind_speed'] = df['9am_wind_speed'].astype(str).replace('Calm', '0').astype(float)
    df['3pm_wind_speed'] = df['3pm_wind_speed'].astype(str).replace('Calm', '0').astype(float)
    return df

def get_darwin_airport():
    data_dir = './data/IDCJDW8014/'
    return get_data(data_dir)


if __name__ == '__main__':
    data = get_darwin_airport()
    
    from matplotlib import pyplot as plt
    plt.plot_date(data['date'], data['rainfall'], '-b', label='rainfall (mm)')
    plt.plot_date(data['date'], data['min_temp'], '-g', label='min_temp (C)')
    plt.plot_date(data['date'], data['max_temp'], '-r', label='max_temp (C)')
    plt.plot_date(data['date'], data['sunshine'], '-y', label='sunshine (Hr)')
    plt.legend()
    plt.show()
