import msgpack
from deeppavlov.models.embedders.elmo_embedder import ELMoEmbedder
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity
import string
from database import Dialog, db
import numpy

elmo = ELMoEmbedder("http://files.deeppavlov.ai/deeppavlov_data/elmo_ru-news_wmt11-16_1.5M_steps.tar.gz")


async def create_vector(answer: str):
    ques = answer.lower()
    ques = ques.translate(str.maketrans('', '', string.punctuation))
    ques = ques.lower().split(' ')
    enc1 = elmo([ques])
    return enc1.tolist()


async def get_answer(questions: str):
    ques = questions.lower()
    ques = ques.translate(str.maketrans('', '', string.punctuation))
    ques = ques.lower().split(' ')
    enc1 = elmo([ques])
    matches = []
    async with db.transaction():
        async for encoding_ in Dialog.query.gino.iterate():
            encoding__ = msgpack.unpackb(encoding_.vector, use_list=False, raw=False)
            similarity = 1 - distance.cdist(encoding__, enc1, 'cosine')
            if similarity >= 0.5:
                matches.append({'answer': encoding_.answer, 'similarity': similarity})
    matches = sorted(matches, key=lambda x: x['similarity'])
    if len(matches) == 0:
        return 'Ивините, не могу ответить на ваш вопрос. Обратитесь к оператору.'
    else:
        return matches[-1].get('answer')
