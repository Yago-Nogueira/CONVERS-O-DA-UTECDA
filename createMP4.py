import os, cv2, imageio, winsound
from datetime import datetime
import moviepy.editor as mp					
import pandas as pd

path = r"D:\IP&D\DADOS\CMN\2021\Contorno_ROT_2021-07-02"

# _data_inicio = datetime.strptime("02/07/2021 13:30:00", '%d/%m/%Y %H:%M:%S')
# _data_fim = datetime.strptime("02/07/2021 15:30:00", '%d/%m/%Y %H:%M:%S')
# _PERIODO_MAPA = pd.date_range(start = _data_inicio, end = _data_fim, freq=('1T'))
# _PERIODO_MAPA_dias = pd.date_range(start = _data_inicio.date(), end = _data_fim.date(), freq='D')
# print(_PERIODO_MAPA)

# pngs = os.listdir(path)
# pngs.sort()
# print(pngs)


images = [os.path.join(path, img) for img in os.listdir(path) if img.endswith(".png")]
images.sort()
videoDir = os.path.join(path,path.split("\\")[-1] + ".gif")
with imageio.get_writer(videoDir, mode='I') as writer:
    for filename in images:
        image = imageio.imread(filename)
        writer.append_data(image)
clip = mp.VideoFileClip(videoDir)
clip.write_videofile(videoDir.replace("gif","mp4"))


# image_folder = path
# video_name = 'video.avi'
# images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
# images.sort()
# frame = cv2.imread(os.path.join(image_folder, images[0]))
# height, width, layers = frame.shape
# video = cv2.VideoWriter(video_name, 0, 10, (width,height))
# for image in images:
#     video.write(cv2.imread(os.path.join(image_folder, image)))
# cv2.destroyAllWindows()
# video.release()



# from PIL import Image

# def get_concat_h(im1, im2):
#     ajuste = 95
#     dst = Image.new('RGB', (im1.width + im2.width-ajuste, im1.height))
#     dst.paste(im1, (0, 0))
#     dst.paste(im2, (im1.width-ajuste, 0))
#     return dst
# imgs = filenames
# for img in imgs:
#     im1 = Image.open(filedir_VTEC+img)
#     im2 = Image.open(filedir_ROTI+img)
#     save = (filedir_concat+img)
#     get_concat_h(im1, im2).save(save)
#     print(img)

frequency = 100 #2500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)