from PIL import Image
from skimage.metrics import structural_similarity as ssim
import cv2
import glob
import imagehash
import numpy as np
import praw
import ssl
import urllib.request


def load_image(path: str):
    if path.startswith('http'):
        req = urllib.request.urlopen(path, context=ssl.SSLContext())
        return Image.open(req)

        # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        # img = cv2.imdecode(arr, -1)  # 'Load it as it is'

    else:
        return Image.open(path)
        # img = cv2.imread(path)

    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def _compare_images(a, b):
    # target_size = (min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1]))
    #
    # a_resized = cv2.resize(a, target_size)
    # b_resized = cv2.resize(b, target_size)
    #
    # return ssim(a_resized, b_resized)

    print(len(str(imagehash.average_hash(a))))
    print(imagehash.average_hash(b))
    return imagehash.average_hash(a) - imagehash.average_hash(b)


gold_images = [(img_path, load_image(img_path)) for img_path in glob.iglob('images/**')]


def compare_to_gold(img):
    for gold_img_path, gold_img in gold_images:
        score = _compare_images(gold_img, img)
        # print(gold_img_path, score)

        if score < 5:
            return gold_img_path, score

        # if score > 0.9:
        #     return gold_img_path, score


reddit = praw.Reddit()

for subreddit_name in ('nrubin29',):
    subreddit = reddit.subreddit(subreddit_name)
    for post in subreddit.new():
        if hasattr(post, 'post_hint') and post.post_hint == 'image':
            print(post.title)
            print(post.url)

            image = load_image(post.url)
            flag = compare_to_gold(image)

            if flag:
                print('>> FLAG:', *flag)
