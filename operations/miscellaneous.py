import os

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


def resize_image(input_folder, size_f_t, output_folder):
    global new_height, output_filepath
    if input_folder[-1] != '/':
        input_folder = input_folder + '/'
    all_images = os.listdir(input_folder)
    if output_folder[-1] != '/':
        output_folder = output_folder + '/'

    for a in all_images:
        image_path = input_folder + a

        if a.endswith(".jpg") or a.endswith(".png"):

            fixed_full_height = 900
            fixed_thumbnail_height = 200

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
                filename = image.filename
                new_name = filename.split('.')
                file_name = new_name[0].split('\\')[-1]
                file_name_filled_space = file_name.replace(' ', '-')
                # new_filename = file_name_filled_space + '.jpg'
                # extension = new_filename.pop()

                if size_f_t == 'f':
                    new_filename = f"{file_name_filled_space}-f.jpg"
                    output_filepath = output_folder + new_filename
                elif size_f_t == 't':
                    new_filename = f"{file_name_filled_space}-t.jpg"
                    output_filepath = output_folder + new_filename

                ratio = (new_height / float(height))
                new_width = int(float(width * ratio))

                image = image.resize((new_width, new_height))
                image = image.convert('RGB')
                if not os.path.exists(output_folder):
                    os.mkdir(output_folder)
                image.save(output_filepath)

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




