from datetime import datetime, timedelta, timezone
from PIL import Image
import dateutil.parser
import imagehash
import praw
import ssl
import sys
import urllib.request

from django.conf import settings

if 'local' in sys.argv:
    from backend import settings_local as backend

else:
    from backend import settings as backend

settings.configure(INSTALLED_APPS=backend.INSTALLED_APPS, DATABASES=backend.DATABASES)

import django
django.setup()

from backend_app.models import HashedImage, ImageMatch

try:
    with open('last_run.txt', 'r') as f:
        last_run = dateutil.parser.parse(f.readline())
except FileNotFoundError:
    last_run = (datetime.now() - timedelta(days=365)).replace(tzinfo=timezone.utc)

with open('last_run.txt', 'w') as f:
    f.write(datetime.now(timezone.utc).astimezone().isoformat())

gold_images = [(image, imagehash.hex_to_hash(image.image_hash)) for image in HashedImage.objects.all()]


def load_image(url: str):
    req = urllib.request.urlopen(url, context=ssl.SSLContext())
    return Image.open(req)


def compare_to_gold(img):
    img_hash = imagehash.average_hash(img)

    for gold_image, gold_hash in gold_images:
        score = img_hash - gold_hash

        if score < 5:
            return gold_image, score


reddit = praw.Reddit()

with open('subreddits_to_check.txt', 'r') as f:
    subreddits = [line.strip() for line in f.readlines()]

for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    for post in subreddit.new(limit=None):
        if hasattr(post, 'post_hint') and post.post_hint == 'image':
            created_utc = datetime.utcfromtimestamp(post.created_utc).replace(tzinfo=timezone.utc)

            # if created_utc < last_run:
            #     break

            print(post.title)
            print(post.url)
            print(created_utc)

            image = load_image(post.url)
            flag = compare_to_gold(image)

            if flag:
                ImageMatch.objects.create(hashed_image=flag[0], permalink=post.permalink)
