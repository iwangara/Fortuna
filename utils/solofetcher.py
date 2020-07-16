import requests
import utils
import configs
import json

sql = utils.DBManager()
BASE_URL=configs.BASE_URL


def fetch_africa():
    url = f"{BASE_URL}solo/africa/{configs.LANGUAGE}"
    africas = requests.get(url=url).json()
    if len(africas)>0:
        for africa in africas:
            africa_id = africa['id']
            africa_language = africa['language']
            africa_question = africa['question']
            africa_answer = africa['answer1']
            africa_answer1 = africa['answer1']
            africa_answer2 = africa['answer2']
            africa_answer3 = africa['answer3']
            africa_answer4 = africa['answer4']
            africa_level = africa['level']
            sql.save_africa(quesId=africa_id, question=africa_question, answer=africa_answer,
                            answer1=africa_answer1, answer2=africa_answer2, answer3=africa_answer3,
                            answer4=africa_answer4,
                            qlevel=africa_level, qlanguage=africa_language)
    else:
        return False


def fetch_apollo():
    url = f"{BASE_URL}solo/apollo/{configs.LANGUAGE}"
    apollos = requests.get(url=url).json()
    if len(apollos) > 0:
        for apollo in apollos:
            apollo_id = apollo['id']
            apollo_language = apollo['language']
            apollo_question = apollo['question']
            apollo_answer = apollo['answer']

            apollo_level = apollo['level']
            sql.save_apollo(quesId=apollo_id, question=apollo_question, answer=apollo_answer,
                            qlevel=apollo_level, qlanguage=apollo_language)
    else:
        return False

def fetch_gaia():
    url = f"{BASE_URL}solo/gaia/{configs.LANGUAGE}"
    gaias = requests.get(url=url).json()
    if len(gaias) > 0:
        for gaia in gaias:
            gaia_id = gaia['id']
            gaia_language = gaia['language']
            gaia_answer = gaia['question']
            gaia_level = gaia['level']
            gaia_question = gaia['path']
            sql.save_gaia(quesId=gaia_id, question=gaia_question, answer=gaia_answer,
                            qlevel=gaia_level, qlanguage=gaia_language)
    else:
        return False


def fetch_kadlu():
    url = f"{BASE_URL}solo/kadlu/{configs.LANGUAGE}"
    kadlus = requests.get(url=url).json()
    if len(kadlus) > 0:
        for kadlu in kadlus:
            kadlu_id = kadlu['id']
            kadlu_language = kadlu['language']
            kadlu_main_id = kadlu['sub_question_id']
            kadlu_main_question = kadlu['path']
            kadlu_question = kadlu['sub_question']
            kadlu_answer = kadlu['answer1']
            kadlu_answer1 = kadlu['answer1']
            kadlu_answer2 = kadlu['answer2']
            kadlu_answer3 = kadlu['answer3']
            kadlu_answer4 = kadlu['answer4']
            kadlu_level = 'Elementary'
            sql.save_kadlu(quesId=kadlu_id, main_id=kadlu_main_id, main_question=kadlu_main_question,question=kadlu_question, answer=kadlu_answer, answer1=kadlu_answer1, answer2=kadlu_answer2, answer3=kadlu_answer3, answer4=kadlu_answer4, qlevel=kadlu_level, qlanguage=kadlu_language )
    else:
        return False