import os
from difflib import SequenceMatcher
from PIL import Image
from datetime import datetime
import random
from captcha.image import ImageCaptcha
import base64


def log(text, category):
    today = str(datetime.today())
    if category == 'error':
        text = f"        <p style='line-height:0.1;'> {today} - <span style='color:red;'>{text}</span> </p>\n"
    elif category == 'success':
        text = f"        <p style='line-height:0.1;'> {today} - <span style='color:green;'>{text}</span> </p>\n"
    elif category == 'routine':
        text = f"        <p style='line-height:0.1;'> {today} - <span style='color:yellow;'>{text}</span> </p>\n"
    elif category == 'none':
        text = f"        <p style='line-height:0.1;'> {today} - <span style='color:white;'>{text}</span> </p>\n"
    with open("./routes/templates/manager/log.html", "r") as f:
        contents = f.readlines()
        lines = len(contents)
        index = lines - 3
        contents.insert(index, text)
    with open("./routes/templates/manager/log.html", "w") as f:
        contents = "".join(contents)
        f.write(contents)
        f.close()
    print("logged into log.txt successfully")


def delete_log(date):
    try:
        with open("./routes/templates/manager/log.html", "r") as f:
            contents = f.readlines()
        with open("./routes/templates/manager/log.html", "w") as f:
            for line in contents:
                if "<p" in line:
                    log_date = log_date.replace("<p style='line-height:0.1;'> ", "")
                    log_date = log_date.replace(" - <span style='color:red;'>", "")
                    log_date = log_date.replace("</span> <p>", "")
                    log_date = log_date.split(" ")
                    log_date = log_date[0]
                    if not log_date <= date:
                        f.write(line)
                else:
                    f.write(line)
        f.close()
        log("Successfully deleted log", "success")
    except Exception as e:
        log("Error in deleting log", "error")


def resize_image(folder, size_f_t):
    global new_height, output_filepath, input_folder, new_filename

    if folder[-1] != '/':
        input_folder = folder + '/'
    all_images = os.listdir(folder)

    output_full_folder = 'full/'
    output_thumbnail_folder = 'thumbnail/'
    output_full_path = input_folder + output_full_folder
    output_thumbnail_path = input_folder + output_thumbnail_folder

    for a in all_images:
        image_path = input_folder + a
        execute = False

        if os.path.isfile(image_path):
            if a.endswith(".jpg") or a.endswith(".png"):

                fixed_full_height = 1536
                fixed_thumbnail_height = 300

                if size_f_t == 'f':
                    new_height = fixed_full_height
                elif size_f_t == 't':
                    new_height = fixed_thumbnail_height
                else:
                    pass
                try:
                    image = Image.open(image_path)
                    width = image.width
                    height = image.height
                    filename = a
                    new_name = filename.split('.')
                    file_name = new_name[0].split('\\')[-1]
                    file_name_filled_space = file_name.replace(' ', '-')
                    # new_filename = file_name_filled_space + '.jpg'
                    # extension = new_filename.pop()

                    if size_f_t == 'f':
                        new_filename = f"{file_name_filled_space}-f.jpg"
                        output_filepath = output_full_path + new_filename
                        if not os.path.exists(output_full_path):
                            os.mkdir(output_full_path)
                        if new_filename not in os.listdir(output_full_path):
                            execute = True
                        else:
                            print('File already resized')
                    elif size_f_t == 't':
                        new_filename = f"{file_name_filled_space}-t.jpg"
                        output_filepath = output_thumbnail_path + new_filename
                        if not os.path.exists(output_thumbnail_path):
                            os.mkdir(output_thumbnail_path)
                        if new_filename not in os.listdir(output_thumbnail_path):
                            execute = True
                        else:
                            print('File already resized')
                    if execute:
                        ratio = (new_height / float(height))
                        new_width = int(float(width * ratio))

                        image = image.resize((new_width, new_height))
                        image = image.convert('RGB')

                        image.save(output_filepath)
                        print('Image saved')

                except Exception as e:
                    pass
            else:
                pass


def generate_captcha():
    captcha_num = str(random.randrange(100000, 999999))
    img = ImageCaptcha()
    captcha_io = img.generate(captcha_num)
    binary_data = captcha_io.getvalue()
    encoded_data_bytes = base64.b64encode(binary_data)
    encoded_string = encoded_data_bytes.decode('utf-8')
    captcha_uri = f"data:image/png;base64, {encoded_string}"
    return captcha_num, captcha_uri

def text_match(target, options_list):
    def similarity_ratio(a, b):
        return SequenceMatcher(None, a, b).ratio()

    best_match = max(options_list, key=lambda option: similarity_ratio(target, option))
    match_ratio = f'{int(similarity_ratio(target, best_match)*100)}%'
    return best_match, match_ratio


