# Mode d'emploi

## Pour faire fonctionner l'application streamlit il faut:
- uploder yoloV5 sur son ordinateur
- Créer un conteneur mongodb à l'aide du docker-compose et lancer le conteneur
- Changer les chemins relatifs dans app/essai_app.py lignes 32,33,34,35 et les adapter aux chemins de sa machine

## Sur l'application on peut ensuite :
- Charger une image (jpeg) d'incendie qui est présente sur son ordinateur et visualiser la détection
- Mettre un lien web vers une vidéo pour effectuer une détection
- Capturer les images d'une webcam (pendant quelques secondes) 
- Il est également possible d'acceder aux archives des images et vidéos 

### PS: Il faut changer le codec de la ligne 203 dans le fichier detect.py de yolo pour que streamlit puisse lire les vidéos (*'mp4v' -> *'avc1')
---
---
# Transfert learning:
## Pour entrainer YoloV5 à reconnaitre du feu et/ou de la fumée nous avons labélisé des images grâce makesens.ai nous avons ensuite stocké ces images dans un dossier Donnees comme ci-dessous
![image](https://github.com/rastakoer/app_detection_feu_streamlit/assets/65788781/b45e16f0-50e1-4e32-90a7-605f81bf48c9)


## Nous avons ensuite crée un fichier feu.yaml pour que yolo ait le chemin vers nos images et nos labels dans yoloV5>data

## Nous avons ensuite utilisé google colab pour entrainer notre modèle avec les commandes suivantes:
```!python yolov5/train.py --data yolov5/data/feu.yaml --epochs 15 --batch-size 16```
## Et enfin nous avons réalisé un test en ajoutant des images dans le dossier test et executé la ligne ci-dessous pour effectuer la detection:
```!python yolov5/detect.py --weights yolov5/runs/train/exp3/weights/best.pt --source Donnees/test```

