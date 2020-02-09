from json import JSONDecodeError

import msgpack
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from requests import session
from fake_useragent import UserAgent
import base64

from scipy.spatial import distance

from database import Photo, db
import cv2
import numpy


session = session()
alg = cv2.KAZE_create()
vector_size = 32
ua = UserAgent()
blueprint_photos = Blueprint('photos', url_prefix='/photos', strict_slashes=True)


def parse_category(product_name):
    category = session.get('https://old.zakupki.mos.ru/api/Cssp/Sku/GetEntity', params={'id': product_name.get('name')},
                           headers={'accept': '*/*', 'user-agent': ua.chrome})
    try:
        z = category.json()
        return f'https://old.zakupki.mos.ru/#/sku/product/{z.get("productionDirectoryId")}',\
            z.get('productionDirectoryName')
    except JSONDecodeError:
        return None


@blueprint_photos.post('')
async def domain(request: Request):
    photo = request.json.get('photo')
    encoding = get_encodings(photo)
    matches = []
    async with db.transaction():
        async for encoding_ in Photo.query.gino.iterate():
            encoding__ = msgpack.unpackb(encoding_.vector, use_list=False, raw=False)
            encoding__ = numpy.reshape(encoding__, (1, -1))
            similarity = 1 - distance.cdist(encoding__, encoding.reshape(1, -1), 'cosine')
            if similarity >= 0.7:
                matches.append({'name': encoding_.name, 'similarity': similarity})
    l = sorted(matches, key=lambda x: x['similarity'])
    l.reverse()
    best_l = l[:5]
    categories = {parse_category(photo) for photo in best_l}
    categories = {category for category in categories if category}
    return json(categories)


def get_encodings(photo):
    rav_b64 = base64.b64decode(photo)
    image_array = numpy.frombuffer(rav_b64, dtype=numpy.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    img = cv2.resize(image, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kps = alg.detect(img)
    kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
    kps, dsc = alg.compute(img, kps)
    encoding1 = dsc.flatten()
    needed_size = (vector_size * 16)
    if dsc.size < needed_size:
        encoding1 = numpy.concatenate([dsc, numpy.zeros(needed_size-dsc.size)])
    return encoding1
