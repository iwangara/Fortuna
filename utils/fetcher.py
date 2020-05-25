import operator

import requests
import utils
import configs
import json

sql = utils.DBHelper()
from .liner import SCHED

sched = SCHED

BASE_URL="http://88.80.148.116:5000"
# BASE_URL ="http://127.0.0.1:5000"
class Sessions(object):
    def __init__(self, language, url=f"{BASE_URL}/sessions/"):
        self.language = language
        self.url = url
        self.conn = requests.get(url=url + language)

    def get_sessions(self):
        return self.conn.json()


class BotMessages(object):
    def __init__(self, id, url=f'{BASE_URL}/bot_messages'):
        self.id = id
        self.url = url
        self.con = requests.get(url=f"{url}/{id}")

    def get_message(self):
        message = f"{self.con.json()['bot_text_content']}"
        return message


class Questions(object):
    def __init__(self, id, url=f'{BASE_URL}/questions'):
        self.id = id
        self.url = url
        self.con = requests.get(url=f"{url}/{id}")

    def get_questions(self):
        return self.con.json()


class GetStudent(object):
    def __init__(self, userid, language, exercise, url=f'{BASE_URL}/student'):
        self.userid = userid
        self.language = language
        self.exercise = exercise
        self.url = url
        header = {"content-type": "application/json"}
        data = {"exercise": exercise, "language": language, "userid": userid}

        self.con = requests.get(url=url, data=json.dumps(data), headers=header)

    def get_data(self):
        return self.con.json()

    def create(self, name):
        header = {"content-type": "application/json"}
        data = {"exercise": self.exercise, "language": self.language, "userid": self.userid, 'name': name}
        req = requests.get(url=f'{BASE_URL}/student/new', data=json.dumps(data), headers=header)
        return req.json()


class Student(object):
    def __init__(self, userid, language, url=f'{BASE_URL}/student/language'):
        self.userid = userid
        self.language = language
        self.url = url
        header = {"content-type": "application/json"}
        data = {"language": language, "userid": userid}

        self.con = requests.get(url=url, data=json.dumps(data), headers=header)

    def get_data(self):
        return self.con.json()


class CreateStudent(object):
    def __init__(self, userid, language, exercise, name, url=f'{BASE_URL}/student/new'):
        self.userid = userid
        self.name = name
        self.language = language
        self.exercise = exercise
        self.url = url
        header = {"content-type": "application/json"}
        data = {"exercise": exercise, "language": language, "userid": userid, 'name': name}

        self.con = requests.post(url=url, data=json.dumps(data), headers=header)

    def get_data(self):
        return self.con.json()['success']


class AddFortunas(object):
    def __init__(self, userid,  exercise,language=configs.LANGUAGE, url=f'{BASE_URL}/student/point'):
        self.userid = userid
        self.language = language
        self.exercise = exercise
        self.url = url
        header = {"content-type": "application/json"}
        data = {"exercise": exercise, "language": language, "userid": userid}

        self.con = requests.post(url=url, data=json.dumps(data), headers=header)

    def get_data(self):
        return self.con.json()


class GetFortuna(object):
    def __init__(self, userid, language, url=f'{BASE_URL}/student/total'):
        self.userid = userid
        self.language = language
        self.url = url
        data = f"{url}/{language}/{userid}"
        self.con = requests.get(url=data)

    def get_data(self):
        return self.con.json()['total']


class GetMessages(object):
    def __init__(self, userid, language, url=f'{BASE_URL}/student/messages'):
        self.userid = userid
        self.language = language
        self.url = url
        data = f"{url}/{language}/{userid}"
        self.con = requests.get(url=data)

    def get_data(self):
        return self.con.json()['messages']


class CUMessages(object):
    def __init__(self, userid, language, url=f'{BASE_URL}/student/messages'):
        self.userid = userid
        self.language = language
        self.url = url
        header = {"content-type": "application/json"}
        data = {"language": language, "userid": userid}

        self.con = requests.post(url=url, data=json.dumps(data), headers=header)

    def get_data(self):
        return self.con.json()


class Admin(object):
    def __init__(self, userid, language, url=f'{BASE_URL}/admins'):
        self.userid = userid
        self.language = language
        self.url = url
        header = {"content-type": "application/json"}
        data = f'{url}/{language}/{userid}'
        self.con = requests.get(url=data, headers=header)

    def get_data(self):
        if len(self.con.json()) > 0:
            return True
        else:
            return False


class StudentPosition(object):
    def __init__(self, userId):
        self.userId = userId

    def get_position(self):
        try:
            data = []
            dist = requests.get(url=f'{BASE_URL}/student/dist/{configs.LANGUAGE}').json()

            for userId in dist:
                points = requests.get(
                    url=f"{BASE_URL}/student/total/{configs.LANGUAGE}/{userId['userid']}").json()
                data.append((points['userid'], points['total']))
            scoreboard = dict((x, y) for x, y in data)
            scoreboard_x = sorted(scoreboard.items(), key=operator.itemgetter(1), reverse=True)
            point = requests.get(url=f"{BASE_URL}/student/total/{configs.LANGUAGE}/{self.userId}").json()
            position = scoreboard_x.index((self.userId, point['total']))
            position += 1
            return position
        except:
            return "Not on scoreboard!"





class Levels(object):
    def __init__(self, url=f'{BASE_URL}/levels'):
        self.url = url
        self.con = requests.get(url=url)

    def get_data(self):
        return self.con.json()


class UpdateLevel(object):
    def __init__(self, userid, language, url=f'{BASE_URL}/student/level'):
        self.userid = userid
        self.language = language
        self.url = url
        header = {"content-type": "application/json"}
        data = {"language": language, "userid": userid}
        self.con = requests.post(url=url, data=json.dumps(data), headers=header)
    def get_data(self):
        return self.con.json()

class Ranks(object):
    def __init__(self, url=f'{BASE_URL}/ranks'):
        self.url = url
        self.con = requests.get(url=url)

    def get_data(self):
        return self.con.json()


class UpdateRank(object):
    def __init__(self, userid, language, rank, url=f'{BASE_URL}/student/rank'):
        self.userid = userid
        self.language = language
        self.rank = rank
        self.url = url
        header = {"content-type": "application/json"}
        data = {"language": language, "userid": userid, "rank": rank}
        self.con = requests.post(url=url, data=json.dumps(data), headers=header)

    def get_data(self):
        return self.con.json()

class Commands(object):
    def __init__(self, url=f'{BASE_URL}/commands'):
        self.url = url
        self.con = requests.get(url=url)

    def get_data(self):
        return self.con.json()


class Classrooms(object):
    def __init__(self, url=f'{BASE_URL}/classrooms'):
        self.url = url
        self.con = requests.get(url=url)

    def get_data(self):
        return self.con.json()


class Studyrooms(object):
    def __init__(self, url=f'{BASE_URL}/studyrooms'):
        self.url = url
        self.con = requests.get(url=url)

    def get_data(self):
        return self.con.json()

class Teachers(object):
    def __init__(self,language=configs.LANGUAGE, url=f'{BASE_URL}/teachers'):
        self.url = url
        self.language=language
        data =f"{url}/{language}"
        self.con = requests.get(url=data)

    def get_data(self):
        return self.con.json()

def topten(language=configs.LANGUAGE):
    lev1 = []
    lev2 = []
    lev3 = []
    dist = requests.get(url=f'{BASE_URL}/student/dist/{language}').json()
    # print(dist)
    for userId in dist:
        user_level = utils.Student(userid=userId['userid'], language=language).get_data()[0]['level']
        # print(user_level)
        if user_level == 1:
            points = requests.get(
                url=f"{BASE_URL}/student/total/{language}/{userId['userid']}").json()

            lev1.append((points['name'], points['total']))
        elif user_level == 2:
            points = requests.get(
                url=f"{BASE_URL}/student/total/{language}/{userId['userid']}").json()
            lev2.append((points['name'], points['total']))
        elif user_level == 3:
            points = requests.get(
                url=f"{BASE_URL}/student/total/{language}/{userId['userid']}").json()
            lev3.append((points['name'], points['total']))
    scoreboard1 = dict((x, y) for x, y in lev1)
    scoreboard2 = dict((x, y) for x, y in lev2)
    scoreboard3 = dict((x, y) for x, y in lev3)
    scoreboard_1 = sorted(scoreboard1.items(), key=operator.itemgetter(1), reverse=True)[:10]
    scoreboard_2 = sorted(scoreboard2.items(), key=operator.itemgetter(1), reverse=True)[:10]
    scoreboard_3 = sorted(scoreboard3.items(), key=operator.itemgetter(1), reverse=True)[:10]
    position = 0
    score1 = []
    for each in scoreboard_1:
        position += 1
        if each[1] > 0:
            score1.append(f"<b>{position}</b>.  @{each[0]} earned <b>{each[1]}</b> points")
    score2 = []
    position2 = 0
    for each in scoreboard_2:
        position2 += 1
        if each[1] > 0:
            score2.append(f"<b>{position2}</b>.  @{each[0]} earned <b>{each[1]}</b> points")
    score3 = []
    position3 = 0
    for each in scoreboard_3:
        position3 += 1
        if each[1] > 0:
            score3.append(f"<b>{position3}</b>.  @{each[0]} earned <b>{each[1]}</b> points")
    return score1, score2, score3



def fetchSessions():
    sessions = utils.Sessions(language=configs.LANGUAGE).get_sessions()
    for session in sessions:
        # check if session is already save in the db
        sess_check = sql.check_session(session['id'])
        if sess_check == False:
            sess_id = session['id']
            group_language = session['language']
            bot = session['type']
            lesson = session['session']
            each_time = session['each_time']
            total_time = session['total_time']
            start_time = session['start_time'].replace('/', '-')
            qlevel = session['level']
            questions = session['questions']
            session_name = session['session_name']
            status = session['status']
            """Save session"""
            print(f"{session_name} saved")
            print('start time',start_time)
            sql.save_sessions(sess_id, group_language, bot, lesson, each_time, total_time, start_time, qlevel,
                              questions, session_name, status)
            # queue the notification a minute earlier
            amin_time = utils.liner.session_time(start_time=start_time, period=60)
            after_time =utils.liner.post_time(start_time=start_time, period=60)
            # print(amin_time)
            # '''todo activate dynamic time'''
            # Que Notification to the group a min before the session starts

            sched.add_job(utils.Notify().session_start, 'date', run_date=amin_time, args=[bot, questions,qlevel,session_name, total_time])
            sched.add_job(utils.Notify().session_ongoing, 'date', run_date=after_time,
                          args=[bot, questions, qlevel, session_name, total_time])
            print("starting session",amin_time)
            utils.mr_logger(f"starting session{amin_time}")
            # sched.add_job(utils.Notify().session_start, 'date', run_date='2020-04-01 23:21:10',
            #                              args=[session_name, questions, total_time])
            # get apollo questions
            if bot == 'Apollo':
                apollos = utils.Questions(id=int(sess_id)).get_questions()
                stime = 0
                # post every minute 50+10 seconds
                post_time = int(each_time) + 10
                for apollo in apollos:
                    apollo_id = apollo['id']
                    apollo_language = apollo['language']
                    apollo_question = apollo['question']
                    apollo_answer = apollo['answer']
                    apollo_level = apollo['level']
                    sql.save_apollo(sess_id=sess_id, quesId=apollo_id, question=apollo_question, answer=apollo_answer,
                                    qlevel=apollo_level, qlanguage=apollo_language)
                    print(f"saving apollo {session_name} questions")
                    stime += int(post_time)
                    net_time = utils.liner.post_time(start_time=start_time, period=int(stime))
                    print("start time", stime)
                    print("actual start", net_time)
                    sched.add_job(utils.Notify().apollo_post, 'date', run_date=net_time,
                                  args=[apollo_id, apollo_question],id=str(apollo_id))

                print(f'Finished saving apollo {session_name} session')
            elif bot =='Seshat':
                seshats=utils.Questions(id=int(sess_id)).get_questions()
                stime = 0
                # post every minute 50+10 seconds
                post_time = int(each_time) + 5
                for seshat in seshats:
                    seshat_id = seshat['id']
                    seshat_language = seshat['language']
                    seshat_question = seshat['question']
                    seshat_answer = seshat['answer']
                    seshat_instruction = seshat['instruction']
                    seshat_level = seshat['level']
                    seshat_gif = seshat['img_path']
                    sql.save_seshat(sess_id=sess_id, quesId=seshat_id, question=seshat_question, answer=seshat_answer,
                                    instruction=seshat_instruction, gif=seshat_gif, qlevel=seshat_level,
                                    qlanguage=seshat_language)
                    print(f"saving seshat {session_name} questions")
                    stime += int(post_time)
                    net_time = utils.liner.post_time(start_time=start_time, period=int(stime))
                    print("start time", stime)
                    print("actual start", net_time)
                    sched.add_job(utils.Notify().seshat_post, 'date', run_date=net_time,
                                  args=[seshat_id, seshat_question,seshat_instruction,seshat_gif], id=str(seshat_id))
            elif bot == 'Tyche':
                tyches = utils.Questions(id=int(sess_id)).get_questions()
                stime = 0
                # post every minute 50+10 seconds
                post_time = int(each_time) + 5
                for tyche in tyches:
                    tyche_id = tyche['id']
                    tyche_language = tyche['language']
                    tyche_question = tyche['hint']
                    tyche_answer = tyche['question']
                    tyche_level = tyche['level']
                    sql.save_tyche(sess_id=sess_id, quesId=tyche_id, question=tyche_question, answer=tyche_answer,
                                   qlevel=tyche_level, qlanguage=tyche_language)
                    print(f"saving tyche {session_name} questions")
                    stime += int(post_time)
                    net_time = utils.liner.post_time(start_time=start_time, period=int(stime))
                    print("start time", stime)
                    print("actual start", net_time)
                    sched.add_job(utils.Notify().tyche_post, 'date', run_date=net_time,
                                  args=[tyche_id, tyche_question],id=str(tyche_id))

                print(f'Finished saving Tyche {session_name} session')

            elif bot == 'Leizi':
                leizis = utils.Questions(id=int(sess_id)).get_questions()
                stime = 0
                # post every minute 50+10 seconds
                post_time = int(each_time) + 5
                for leizi in leizis:
                    leizi_id = leizi['id']
                    leizi_language = leizi['language']
                    leizi_question = leizi['question']
                    leizi_answer1 = leizi['answer1']
                    leizi_answer2 = leizi['answer2']
                    leizi_instruction = leizi['instruction']
                    leizi_level = leizi['level']
                    sql.save_leizi(sess_id=sess_id, quesId=leizi_id, question=leizi_question, answer1=leizi_answer1,
                                   answer2=leizi_answer2, instruction=leizi_instruction,
                                   qlevel=leizi_level, qlanguage=leizi_language)
                    print(f"saving leizi {session_name} questions")
                    stime += int(post_time)
                    net_time = utils.liner.post_time(start_time=start_time, period=int(stime))
                    print("start time", stime)
                    print("actual start", net_time)
                    sched.add_job(utils.Notify().leizi_post, 'date', run_date=net_time,
                                  args=[leizi_id, leizi_question,leizi_instruction], id=str(leizi_id))

            elif bot == 'Odin':
                odins = utils.Questions(id=int(sess_id)).get_questions()
                stime = 0
                # post every minute 50+10 seconds
                post_time = int(each_time) + 10
                for odin in odins:
                    odin_id = odin['id']
                    odin_language = odin['language']
                    odin_question = odin['question']
                    odin_meaning =odin['meaning']
                    odin_level = odin['level']
                    sql.save_odin(sess_id=sess_id, quesId=odin_id, question=odin_question,meaning=odin_meaning, qlevel=odin_level,
                                  qlanguage=odin_language)
                    print(f"saving odin {session_name} questions")
                    stime += int(post_time)
                    net_time = utils.liner.post_time(start_time=start_time, period=int(stime))
                    print("start time", stime)
                    print("actual start", net_time)
                    sched.add_job(utils.Notify().odin_post, 'date', run_date=net_time,
                                  args=[odin_id], id=str(odin_id))

            elif bot == 'Zamo':
                zamos = utils.Questions(id=int(sess_id)).get_questions()
                stime = 0
                # post every minute 50+10 seconds
                post_time = int(each_time) + 10
                for zamo in zamos:
                    zamo_id = zamo['id']
                    zamo_language = zamo['language']
                    zamo_question = zamo['path']
                    zamo_answer = zamo['question']
                    zamo_level = zamo['level']
                    sql.save_zamo(sess_id=sess_id, quesId=zamo_id, answer=zamo_answer, question=zamo_question,
                                  qlevel=zamo_level, qlanguage=zamo_language)
                    print(f"saving zamo {session_name} questions")
                    stime += int(post_time)
                    net_time = utils.liner.post_time(start_time=start_time, period=int(stime))
                    print("start time", stime)
                    print("actual start", net_time)
                    sched.add_job(utils.Notify().zamo_post, 'date', run_date=net_time,
                                  args=[zamo_id,zamo_question], id=str(zamo_id))

            elif bot == 'Africa':
                africas = utils.Questions(id=int(sess_id)).get_questions()
                stime = 0
                # post every minute 50+10 seconds
                post_time = int(each_time) + 10
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
                    pick = [africa_answer1, africa_answer2, africa_answer3, africa_answer4]
                    print(pick, type(pick))
                    sql.save_africa(sess_id=sess_id, quesId=africa_id, question=africa_question, answer=africa_answer,
                                    answer1=africa_answer1, answer2=africa_answer2, answer3=africa_answer3,
                                    answer4=africa_answer4,
                                    qlevel=africa_level, qlanguage=africa_language)
                    print(f"saving africa {session_name} questions")
                    stime += int(post_time)
                    net_time = utils.liner.post_time(start_time=start_time, period=int(stime))
                    print("start time", stime)
                    print("actual start", net_time)
                    sched.add_job(utils.Notify().africa_post, 'date', run_date=net_time,
                                  args=[africa_id, africa_question,pick], id=str(africa_id))

        else:
            print("no new sessions found")
