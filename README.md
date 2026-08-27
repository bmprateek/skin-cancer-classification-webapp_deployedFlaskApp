# Skin Cancer Prediction — Web App (Deployment)

A Flask web application that serves a trained melanoma-detection model: upload
a photo of a skin lesion, get back a melanoma / non-melanoma likelihood plus a
Class Activation Map (CAM) highlighting the region the model focused on.

This is the *deployment* repository — inference code only. Model training,
notebooks, and experiments live in the companion repository,
**[Skincancer-Prediction](https://github.com/bmprateek/Skincancer-Prediction)**.

## Table of contents

- [Overview](#overview)
- [How it works](#how-it-works)
- [Model](#model)
- [Repository structure](#repository-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Deployment](#deployment)

## Overview

| | |
|---|---|
| **Input** | A photo of a skin lesion (JPEG/PNG) |
| **Output** | Melanoma vs. non-melanoma percentage, plus a CAM overlay showing model focus |
| **Backend** | Flask |
| **Models** | MobileNet + InceptionV3 + Xception, averaged into one ensemble |
| **Hosting** | Configured for Vercel (`vercel.json`); also runs anywhere via `python app.py` |

**Upload page**

The user uploads a lesion image via a simple form.

**Results page**

The app returns a side-by-side view: the original lesion and a heatmap
(CAM) overlay, with the predicted melanoma / non-melanoma split.

## How it works

```
Browser  ──upload image──▶  Flask (app.py)
                                 │
                                 ▼
                     pal.py: preprocess image → tensor
                                 │
                                 ▼
                normalize + tensor → ensemble model (pal.py)
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
               MobileNet    InceptionV3    Xception
                    └────────────┼────────────┘
                        average softmax outputs
                                 │
                                 ▼
                  MobileNet CAM → static/result_images/
                                 │
                                 ▼
Browser  ◀── results.html (prediction % + CAM image) ──
```

1. The user uploads an image through `templates/index.html`.
2. `app.py` saves the upload and calls `pal.prediction_localisation(img_path)`.
3. `pal.py` builds all three backbones, loads their trained weights from
   `api/Saved models/`, and averages their predictions into an ensemble score.
4. `pal.py` also computes a Class Activation Map from the MobileNet backbone to
   visualize which part of the lesion drove the prediction.
5. Both the original image and the CAM overlay are saved to
   `static/result_images/` and rendered on `templates/results.html`.

## Model

The three backbones and their trained weights come from the
[development repo](https://github.com/bmprateek/Skincancer-Prediction), where
Adam hyperparameters were tuned per architecture using Particle Swarm
Optimization and the Bat Algorithm. The best single configuration found was
**Xception + Bat Algorithm at 94.5% validation accuracy** — see that repo's
[results notebook](https://github.com/bmprateek/Skincancer-Prediction/blob/main/notebooks/04_results_and_comparison.ipynb)
for the full comparison. This app serves an averaging ensemble of all three
tuned backbones rather than a single model, for more robust predictions.

Trained weight files (`.hdf5`) are tracked with **Git LFS** (see
`.gitattributes`) since they're binary model artifacts rather than source code.

## Repository structure

```
Skin-Cancer-Prediction-Melonoma/
├── api/
│   ├── app.py                  # Flask routes
│   ├── pal.py                  # Model loading, ensembling, CAM localization
│   ├── Saved models/           # Trained weights (Git LFS)
│   │   ├── weights.best.mobilenet.hdf5
│   │   ├── weights.best.inception.hdf5
│   │   └── weights.best.xception.hdf5
│   ├── templates/
│   │   ├── index.html          # Upload page
│   │   └── results.html        # Results page
│   └── static/
│       ├── css/main.css
│       ├── assets/              # Static images used by the UI
│       └── result_images/       # Generated prediction + CAM images
├── requirements.txt
├── runtime.txt                  # Python version pin for deployment
├── vercel.json                  # Vercel serverless deployment config
└── .gitattributes                # Git LFS config for model weights
```

## Setup

```bash
git clone https://github.com/bmprateek/Skin-Cancer-Prediction-Melonoma.git
cd Skin-Cancer-Prediction-Melonoma

# Pull the actual model weight binaries (tracked via Git LFS)
git lfs install
git lfs pull

python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
```

Requires Python 3.11 (see `runtime.txt`) and the dependencies pinned in
`requirements.txt` (Flask, TensorFlow/Keras, OpenCV, etc.).

> **Note**: `Saved models/*.hdf5` must contain the actual trained weight
> binaries (pulled via Git LFS above) before the app can serve predictions —
> without them, `pal.py` will fail to load the models.

## Usage

```bash
cd api
python app.py
```

Then open `http://localhost:5000` in a browser, upload a lesion image, and
submit — the results page will show the prediction and CAM overlay within a
few seconds (model loading + inference time).

## Deployment

This repo is configured for one-click deployment to **Vercel** via
`vercel.json`, which points to `api/app.py` as the serverless entry point. The
original project report describes deployment via **Heroku** as an alternative;
either works, since the app has no server-specific dependencies beyond Flask
and the model weights.

## License & disclaimer

This project is for educational/research purposes only and is **not** a
certified medical device. It must not be used as a substitute for professional
medical diagnosis — always consult a healthcare professional about any
concerning skin lesion.
