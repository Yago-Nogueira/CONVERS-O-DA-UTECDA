# Mapa = "Africa"
Mapa = "Brasil"
dia = 8

# from PIL import Image

# def get_concat_h(im1, im2):
#     ajuste = 95
#     dst = Image.new('RGB', (im1.width + im2.width-ajuste, im1.height))
#     dst.paste(im1, (0, 0))
#     dst.paste(im2, (im1.width-ajuste, 0))
#     return dst



# filedir_VTEC = "C:\\Users\\NASA_Matieuz\\Desktop\\DADOS RELAT IC\\%s\\%s_Contorno_VTEC_2017-09-0%i\\"%(Mapa,Mapa,dia)
# filedir_ROTI = "C:\\Users\\NASA_Matieuz\\Desktop\\DADOS RELAT IC\\%s\\%s_Contorno_ROTI_2017-09-0%i\\"%(Mapa,Mapa,dia)
filedir_concat = "C:\\Users\\NASA_Matieuz\\Desktop\\DADOS RELAT IC\\%s\\%s_Contorno_VTEC_ROTI_2017-09-0%i\\"%(Mapa,Mapa,dia)
# # filedir_VTEC = "C:\\Users\\mateu\\Desktop\\DADOS RELAT IC\\Brasil Atualizado\\%s_Contorno_VTEC_2017-09-0%i\\"%(Mapa,dia)
# # filedir_ROTI = "C:\\Users\\mateu\\Desktop\\DADOS RELAT IC\\Brasil Atualizado\\%s_Contorno_ROTI_2017-09-0%i\\"%(Mapa,dia)
# # filedir_concat = "C:\\Users\\mateu\\Desktop\\DADOS RELAT IC\\Brasil Atualizado\\%s_Contorno_VTEC_ROTI_2017-09-0%i\\"%(Mapa,dia)

# imgs = filenames
# for img in imgs:
#     im1 = Image.open(filedir_VTEC+img)
#     im2 = Image.open(filedir_ROTI+img)
#     save = (filedir_concat+img)
#     get_concat_h(im1, im2).save(save)
#     print(img)





# # caminho = "C:\\Users\\NASA_Matieuz\\Desktop\\Nova pasta\\Brasil\\Brasil_Contorno_VTEC_ROTI_2017-09-07\\"
# # caminho = "C:\\Users\\NASA_Matieuz\\Desktop\\Nova pasta\\Brasil\\Brasil_Contorno_VTEC_ROTI_2017-09-08\\"
# # caminho = "C:\\Users\\NASA_Matieuz\\Desktop\\Nova pasta\\Africa\\Africa_Contorno_VTEC_ROTI_2017-09-07\\"
# # caminho = "C:\\Users\\NASA_Matieuz\\Desktop\\Nova pasta\\Brasil\\Brasil_Contorno_VTEC_ROTI_2017-09-08\\"
# # caminho = "C:\\Users\\mateu\\Desktop\\DADOS RELAT IC\\Brasil Atualizado\\Brasil_Contorno_VTEC_ROTI_2017-09-07\\"


# import imageio

# video_name = 'C:\\Users\\NASA_Matieuz\\Desktop\\DADOS RELAT IC\\%s\\%s_VTEC_ROTI_%i_SETEMBRO_2017.gif'%(Mapa,Mapa,dia)
# with imageio.get_writer(video_name, mode='I') as writer:
#     for filename in filenames:
#         image = imageio.imread(filedir_concat+filename)
#         writer.append_data(image)





# import cv2
# import os

# # image_folder = 'C:\\Users\\NASA_Matieuz\\Desktop\\DADOS RELAT IC\\Africa\\Africa_Contorno_VTEC_ROTI_2017-09-07'
# image_folder = filedir_concat
# #, '23-59-00.png']
# video_name = 'C:\\Users\\NASA_Matieuz\\Desktop\\DADOS RELAT IC\\%s\\%s_VTEC_ROTI_%i_SETEMBRO_2017.mp4'%(Mapa,Mapa,dia)

# frame = cv2.imread(os.path.join(image_folder, filenames[0]))
# height, width, layers = frame.shape

# video = cv2.VideoWriter(video_name, 0, 16, (width,height))

# for image in filenames:
#     video.write(cv2.imread(os.path.join(image_folder, image)))

# cv2.destroyAllWindows()
# video.release()








import moviepy.editor as mp
						
video_name = 'C:\\Users\\NASA_Matieuz\\Desktop\\DADOS RELAT IC\\%s\\%s_VTEC_ROTI_%i_SETEMBRO_2017.gif'%(Mapa,Mapa,dia)
clip = mp.VideoFileClip(video_name)
# video_name = 'C:\\Users\\NASA_Matieuz\\Desktop\\DADOS RELAT IC\\%s\\%s_VTEC_ROTI_%i_SETEMBRO_2017.gif'%(Mapa,Mapa,dia)
clip.write_videofile(video_name[:-3]+"mp4")


import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)