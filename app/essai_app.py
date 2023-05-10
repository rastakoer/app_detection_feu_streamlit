import cv2
import numpy as np
from PIL import Image
import streamlit as st
import subprocess
import os, shutil
import pymongo
from pymongo import MongoClient
import datetime
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import tempfile
import imageio.v3 as iio
import ffmpeg

st.set_page_config(layout="wide")

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# CONFIG MONGO
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def get_db():
    client = pymongo.MongoClient("mongodb://root:pass@localhost:27019/")
    db = client["detect_db"] 
    return db



#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# CHEMIN POUR YOLO
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
detect = "C:/Users/utilisateur/workspace/yolo_feu/yolov5/detect.py"
weight = "C:/Users/utilisateur/workspace/yolo_feu/yolov5/runs/train/exp3/weights/best.pt"
dir_save_image = "C:/Users/utilisateur/workspace/BRIEF_DETECTION_INCENDIE/app/temp/"


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# FONCTION POUR EFFECTUER UNE COMMANDE EN CONSOLE
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    print(result.stdout.decode())
    return



#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# HOME PAGE
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def home():
    st.subheader("Bienvenue FIRE DETECTOR")
    st.markdown("""Partie 1 : Base de données  
Vous devrez labéliser la DataSet fournie pour le modèle Yolo.    
Partie 2 : Transfer Learning   
Cette deuxième partie est réservée pour réaliser un Transfer Learning sur l\'architecture de Yolov5.     
Partie 3 : Application   
Vous êtes censés à développer une application Streamlit qui sera capable de :   
Charger et exécuter la détection à partir d\'une image, vidéo ou d\'une Webcam.   
Permettre de stocker les détections dans une bdd")""")

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# PAGE POUR DETECTION SUR UNE IMAGE
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def image():
    global detect
    global weight
    global dir_save_image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Sauvegarde de l'image dans un dossier :
        image.save(dir_save_image + "temp.jpg")
        # Appel de la fonction de detection avec les poids du transfert learning
        run_command("python " + detect + " --weights " +  weight + " --source " + dir_save_image)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Image d\'origine')
            image= np.array(image)
            st.image(image)
        
        with col2:
            st.subheader('Avec detection')
            # Recherche de l'image crée avec la détection
            path='C:/Users/utilisateur/workspace/yolo_feu/yolov5/runs/detect'
            contents_exp = os.listdir(path)
            contents_exp = sorted(contents_exp, key=lambda x: os.path.getctime(os.path.join(path, x)), reverse=True)
            path="C:/Users/utilisateur/workspace/yolo_feu/yolov5/runs/detect/" + contents_exp[0]
            contents_img = os.listdir(path)
            image2 = Image.open(path+"/"+contents_img[-1])
            #Affichage de l'image
            image2= np.array(image2)
            st.image(image2)

        # fonction pour stocker en bdd la date et l'image d'origine et celle avec les détections
        db=get_db()
        collection = db["image"]
        with open(dir_save_image+"temp.jpg", 'rb') as f:
            img_binary = f.read()
        with open(path+"/"+contents_img[-1], 'rb') as f:
            img_binary_tranfom = f.read()
        maintenant = datetime.datetime.now()
        date = maintenant.strftime("%d/%m/%Y %H:%M:%S")
        collection.insert_one({"date":date,"image": img_binary, "imageTransform":img_binary_tranfom})

    
        
    else : 
        st.header("detection d'incendie")
        st.markdown("- Faite glisser une image dans le file uploader")
        st.markdown("- Puis cliquer sur VISUALISER LA DETECTION")

def videos():
    st.write("Voici la page video")

    # Vérifie si l'URL est valide
    if url is not None:
        # Appel de la fonction de detection avec les poids du transfert learning
        run_command("python " + detect + " --weights " +  weight + " --source " + url)

        # Récupération infos avant stockage
        maintenant = datetime.datetime.now()
        date = maintenant.strftime("%d/%m/%Y %H:%M:%S")
        # Recherche de l'image crée avec la détection
        path='C:/Users/utilisateur/workspace/yolo_feu/yolov5/runs/detect'
        contents_exp = os.listdir(path)
        contents_exp = sorted(contents_exp, key=lambda x: os.path.getctime(os.path.join(path, x)), reverse=True)
        path="C:/Users/utilisateur/workspace/yolo_feu/yolov5/runs/detect/" + contents_exp[0]
        liens_video = os.listdir(path)
        lien= path+"/"+liens_video[-1]


        # Sauvegarde en bdd
        db=get_db()
        collection = db["video"]
        collection.insert_one({"date":date,"Original":url,"AvecDetection":lien})



    else:
        st.write('Entrez une URL valide de YouTube.')

def webcam():
    cap = cv2.VideoCapture(0)

    # Function to read video frame and convert it to RGB
    def get_frame():
        _, frame = cap.read()
        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame

    # Streamlit app
    st.title("Webcam Example")

    # Display webcam video stream in real-time
    start_time = time.time()
    frames = []
    stop_button = st.button("Stop", key='stop_button')  # Add unique key to the button

    while True:
        frame = get_frame()
        # st.image(frame, channels="RGB")

        # Save frames for 2 seconds
        if time.time() - start_time < 2:
            frames.append(frame)
        else:
            break

        # Check if the stop button is pressed
        if stop_button:
            break

        # Limit frame rate to 30 FPS
        time.sleep(0.033)

    # Release the video capture and close Streamlit app
    cap.release()
    cv2.destroyAllWindows()

    # Save frames as a video clip
    if len(frames) > 0:
        frames_per_second = int(len(frames) / 2)  # 2 seconds duration
        height, width, _ = frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        # fourcc = 0x00000021
        out = cv2.VideoWriter("webcam_clip1.mp4", fourcc, frames_per_second, (width, height))
        for frame in frames:
            out.write(frame)
        out.release()

        run_command("python " + detect + " --weights " +  weight + " --source C:/Users/utilisateur/workspace/BRIEF_DETECTION_INCENDIE/app/webcam_clip1.mp4")

        # Récupération infos avant stockage
        maintenant = datetime.datetime.now()
        date = maintenant.strftime("%d/%m/%Y %H:%M:%S")
        # Recherche de l'image crée avec la détection
        path='C:/Users/utilisateur/workspace/yolo_feu/yolov5/runs/detect'
        contents_exp = os.listdir(path)
        contents_exp = sorted(contents_exp, key=lambda x: os.path.getctime(os.path.join(path, x)), reverse=True)
        path="C:/Users/utilisateur/workspace/yolo_feu/yolov5/runs/detect/" + contents_exp[0]
        liens_video = os.listdir(path)
        lien= path+"/"+liens_video[-1]

        video_file = open(lien, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)


    else:
        st.warning("No frames were captured to save as a video clip.")
    
    # Sauvegarde en bdd
    db=get_db()
    collection = db["video"]
    collection.insert_one({"date":date,"Original":"WEBCAM","AvecDetection":lien})

def archives_images():
    db = get_db()

    collection = db["image"]
    images = collection.find({})
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Date d\'enregistrement')
    with col2:
        st.subheader('Image d\'origine')
    with col3:
        st.subheader('Avec detection')
    for image in images:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(image['date'])
        with col2:
            img_binary = image["image"]
            image_np = np.asarray(bytearray(img_binary), dtype="uint8")
            image_origine = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            st.image(image_origine, channels="BGR")
        with col3:
            img_binary = image['imageTransform']
            image_np = np.asarray(bytearray(img_binary), dtype="uint8")
            image_detec = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            st.image(image_detec, channels="BGR")

       
        
def archives_videos():
    db=get_db()
    collection = db["video"]
    videos = collection.find({})

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Date d\'enregistrement')
    with col2:
        st.subheader('Video d\'origine')
    with col3:
        st.subheader('Video avec detection')

    for video in videos:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(video['date'])
        with col2:
            st.write(video['Original'])
        with col3:
            video_file= open(video['AvecDetection'],'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# BARRE LATERALE DE L'APPLI
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
st.sidebar.markdown("<h1 style='text-align: center; color: red;'>Detecteur incendie</h1>", unsafe_allow_html=True)
st.sidebar.button("Accueil", on_click=home, use_container_width=True)

st.sidebar.markdown("---")

st.sidebar.markdown("<h2 style='text-align: center; color: blue;'>Detecteur avec image</h2>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("(fichier jpg uniquement)", type='jpg')
st.sidebar.button("VISUALISER LA DETECTION", on_click=image, use_container_width=True)

st.sidebar.markdown("---")

st.sidebar.markdown("<h2 style='text-align: center; color: blue;'>Detection sur vidéo</h2>", unsafe_allow_html=True)
url = st.sidebar.text_input('Entrez l\'URL de la vidéo', '')
st.sidebar.button("VISUALISER LA VIDEOS", on_click=videos, use_container_width=True)

st.sidebar.markdown("---")

st.sidebar.button("Detection par webcam", on_click=webcam, use_container_width=True)

st.sidebar.markdown("---")

st.sidebar.button("ARCHIVES IMAGES", on_click=archives_images, use_container_width=True)

st.sidebar.button("ARCHIVES VIDEOS & WEBCAM", on_click=archives_videos, use_container_width=True)

