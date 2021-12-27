import os
import pandas as pd

BASE_FOLDER = os.path.join("scrapers", "data")
FOLDERS = {
    "guests": os.path.join(BASE_FOLDER, "guests"),
    "dates": os.path.join(BASE_FOLDER, "dates"),
    "guest_descs": os.path.join(BASE_FOLDER, "guest_descs"),
    "transcripts": os.path.join(BASE_FOLDER, "transcripts"),
}


def read_from(folder, filename):
    file_path = os.path.join(folder, filename)
    with open(file_path, "r") as f:
        return f.read()


def load_pods_into_dataframe():

    pod_data = dict()

    for pod_file in os.listdir(FOLDERS["guests"]):

        pod_num = pod_file.split(".")[0]
        pod_data[pod_num] = [pod_num]

        guest = read_from(FOLDERS["guests"], pod_file)
        pod_data[pod_num].append(guest)

        guest_desc = read_from(FOLDERS["guest_descs"], pod_file)
        pod_data[pod_num].append(guest_desc)

        transcript = read_from(FOLDERS["transcripts"], pod_file)
        pod_data[pod_num].append(transcript)

        date = read_from(FOLDERS["dates"], pod_file)
        pod_data[pod_num].append(date)

    columns = ["pod_num", "guest", "guest_desc", "transcript", "date"]
    df = pd.DataFrame.from_dict(pod_data, orient="index", columns=columns)

    df = df.sort_values("pod_num").reset_index(drop=True)

    print(df.head(5))

    df.to_csv("jre.csv")


if __name__ == "__main__":
    load_pods_into_dataframe()
