from os.path import basename


def extract_image_name_from_path(image_path):
    file_name = basename(image_path)
    index = file_name.rfind('.')
    return file_name[:index]


def save_file_to_path(file, path):
    file.save(path)
    print(f"Saved file: {path}")
