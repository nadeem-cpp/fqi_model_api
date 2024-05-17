import joblib
import numpy as np
from sklearn.cluster import KMeans
import warnings
from io import BytesIO
from PIL import Image
from rembg import remove

# Filter out specific warnings
warnings.filterwarnings("ignore", message="Explicit initial center position passed", category=RuntimeWarning)

# Suppress warnings from specific categories
warnings.filterwarnings("ignore", category=UserWarning)


def cluster_image(pic):
    pic2 = pic.reshape(-1, 3)
    km = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10,
        init=np.array([[0, 0, 0], [97.00881952, 72.17407544, 44.85307902], [108.71433554, 60.85790536, 49.73037811]])
    )
    km.fit(pic2)
    cluster_labels = km.labels_
    centroids = km.cluster_centers_
    points_centroid1 = pic2[cluster_labels == 1]
    points_centroid2 = pic2[cluster_labels == 2]
    return [
        centroids[1][0],
        centroids[1][1],
        centroids[1][2],
        centroids[2][0],
        centroids[2][1],
        centroids[2][2],
        len(points_centroid1),
        len(points_centroid2)
    ]


def preprocess_img(img: Image) -> Image:
    return remove(img).convert('RGB')


def model(img):
    # convert img object to bytesIo --> then open it
    pic = Image.open(BytesIO(img.read()))
    # preprocess image
    processed_img = preprocess_img(pic)
    res = cluster_image(np.array(processed_img))
    mdl = joblib.load('model.pkl')
    return mdl.predict([res])
