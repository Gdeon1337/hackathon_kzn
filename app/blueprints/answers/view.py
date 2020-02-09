import os

import msgpack
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
import json as js
import pandas as pd
from .neyrol import get_answer, create_vector
from database import Photo, Dialog

blueprint = Blueprint('answers', url_prefix='/answers', strict_slashes=True)


async def create_photos(raw):
    file = open(f'/home/gdeon/jsons/{raw}', 'r')
    json_ = js.load(file)
    for r in json_:
        await Photo.create(name=r.get('name'), vector=msgpack.packb(r.get('vector'), use_bin_type=True))


@blueprint.get('')
async def answer(request: Request):
    question = request.args.get('question')
    answer_ = await get_answer(question)
    return json({'answers': answer_})


@blueprint.post('')
async def create_answer(request: Request):
    question = request.args.get('question')
    answer_ = request.args.get('answer')
    vector = await create_vector(answer_)
    await Dialog.create(
        question=question, answer=answer_, vector=msgpack.packb(vector, use_bin_type=True))
    return json({'status': 'ok'})


async def cre(_, d):
    jsons = os.listdir('/home/gdeon/jsons')
    for json_ in jsons:
        await create_photos(json_)


async def crea_dialog(_, d):
    f = open('bad_answers.json', 'r')
    json_ = js.load(f)
    bad_vector = [enc.get('vector') for enc in json_]

    f = open('new_data_3.json', 'r')
    json_ = js.load(f)
    bad_answers = [enc.get('answer') for enc in json_]
    bad_question = [enc.get('question') for enc in json_]

    f = open('head_answers.json', 'r')
    json_ = js.load(f)
    good_vector = [enc.get('vector') for enc in json_]

    df = pd.read_csv('ildarkin_1.csv')
    good_answers = df['answer'].values.tolist()
    good_question = df['head_answer'].values.tolist()
    for an in range(len(bad_vector)):
        print(an)
        await Dialog.create(question=bad_question[an], answer=bad_answers[an], vector=msgpack.packb(bad_vector[an], use_bin_type=True))
    for an in range(len(good_vector)):
        print(an)
        await Dialog.create(question=good_question[an], answer=good_answers[an], vector=msgpack.packb(good_vector[an], use_bin_type=True))
