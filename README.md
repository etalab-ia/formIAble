## Installation de l'environnement

### Installation avec conda

Vérifier l'installation de conda avec `conda --version`, puis créer un environnement `formIAble` avec: <br>
```
conda create -n formIAble -y python=3.8
conda activate formIAble
pip install -r requirements.txt
```

### Installation de paddleOCR

Python 3.8 est requis.

#### MacOS: installation de PyMuPDF

Vérifier l'installation de homebrew: `brew help` <br>
Pour installer homebrew: https://brew.sh <br>
Puis installer les dépendances:
```
brew install swig freetype
pip install PyMuPDF
``` 

#### Ubuntu (notamment pour les images du [SSP Cloud](https://www.sspcloud.fr)): installation des librairies système
```
sudo apt-get update && sudo apt-get -y install libgl1
sudo apt-get -y install libglib2.0-0
```

#### Installation de cargo (prérequis):

Vérifier l'installation de cargo avec `cargo help` <br>
Si cargo n'est pas installé, l'installer avec:
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

#### Installation de paddlepaddle (prérequis):

Installation via pip:
```
pip install paddlepaddle
```

#### Installation de paddleocr (dernière étape)

Installation via pip:
```
pip install paddleocr
```

### Installation de MMOCR

```
pip install openmim
mim install mmengine
mim install mmcv
mim install mmdet
mim install mmocr
```

## Annotation d'images

### Pré-annotation avec Doctr

`python3 -m src.data.labeling.label_images projet-formiable/data/ls_data/ projet-formiable/data/ls_prelabels/`