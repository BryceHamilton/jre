import os


def textfile(name):
    return f"{name}.txt"


def get_abs_path(dir):
    curr_dir = os.path.dirname(__file__)
    data_dir = os.path.join(curr_dir, "data")
    return os.path.abspath(os.path.join(data_dir, dir))


def write_to_file(folder, filename, doc):
    dir = get_abs_path(folder)
    file_path = os.path.join(dir, filename)
    with open(file_path, "w") as f:
        f.write(doc)


def write_all(pod_num, guest_desc, date, guest, transcript):
    file_name = textfile(pod_num)
    write_to_file("guest_descs", file_name, guest_desc)
    write_to_file("dates", file_name, date)
    write_to_file("guests", file_name, guest)
    write_to_file("transcripts", file_name, transcript)
