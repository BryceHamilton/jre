import os
import pandas as pd

def load_pods_into_dataframe():

    pod_data = dict()

    guest_folder = 'guests'
    transcript_folder = 'transcripts'
    for filename in os.listdir(guest_folder):

        pod_num = filename.split('.')[0]

        file_path = os.path.join(guest_folder, filename)
        with open(file_path, 'r') as f:
            guest = f.read()
            pod_data[pod_num] = [pod_num, guest]

        file_path = os.path.join(transcript_folder, filename)
        with open(file_path, 'r') as f:
            transcript = f.read()
            pod_data[pod_num].append(transcript)

    df = pd.DataFrame.from_dict(pod_data, orient='index',
                    columns=['pod_num', 'guest', 'transcript'])

    df = df.sort_values('pod_num').reset_index(drop=True)

    print(df.head(5))

    df.to_csv("jre.csv")

if __name__ == '__main__':
    load_pods_into_dataframe()