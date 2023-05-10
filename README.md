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
