import operator

import requests
import utils
import configs
import json
sql =  utils.DBHelper()
from .liner import SCHED

sched = SCHED
class Sessions(object):
    def __init__(self,language,url="http://127.0.0.1:5000/sessions/"):
        self.language=language
        self.url=url
        self.conn = requests.get(url=url+language)


    def get_sessions(self):
        return self.conn.json()



class BotMessages(object):
    def __init__(self,id,url='http://127.0.0.1:5000/bot_messages'):
        self.id=id
        self.url=url
        self.con = requests.get(url=f"{url}/{id}")

    def get_message(self):
        message =f"{self.con.json()['bot_text_content']}"
        return message


class Questions(object):
    def __init__(self,id,url='http://127.0.0.1:5000/questions'):
        self.id = id
        self.url = url
        self.con = requests.get(url=f"{url}/{id}")
    def get_questions(self):
        return self.con.json()

class GetStudent(object):
    def __init__(self,userid,language,exercise,url='http://127.0.0.1:5000/student'):
        self.userid = userid
        self.language=language
        self.exercise=exercise
        self.url = url
        header = {"content-type": "application/json"}
        data = {"exercise": exercise,"language": language, "userid": userid}

        self.con = requests.get(url=url,data=json.dumps(data),headers=header)
    def get_data(self):
        return self.con.json()

    def create(self,name):
        header = {"content-type": "application/json"}
        data = {"exercise": self.exercise, "language": self.language, "userid": self.userid,'name':name}
        req = requests.get(url='http://127.0.0.1:5000/student/new',data=json.dumps(data),headers=header)
        return req.json()

class CreateStudent(object):
    def __init__(self,userid,language,exercise,name,url='http://127.0.0.1:5000/student/new'):
        self.userid = userid
        self.name = name
        self.language=language
        self.exercise=exercise
        self.url = url
        header = {"content-type": "application/json"}
        data = {"exercise": exercise, "language": language, "userid": userid,'name':name}

        self.con = requests.post(url=url,data=json.dumps(data),headers=header)
    def get_data(self):
        return self.con.json()['success']


class AddFortunas(object):
    def __init__(self,userid,language,exercise,url='http://127.0.0.1:5000/student/point'):
        self.userid = userid
        self.language=language
        self.exercise=exercise
        self.url = url
        header = {"content-type": "application/json"}
        data = {"exercise": exercise, "language": language, "userid": userid}

        self.con = requests.post(url=url,data=json.dumps(data),headers=header)
    def get_data(self):
        return self.con.json()


class CUMessages(object):
    def __init__(self,userid,language,url='http://127.0.0.1:5000/student/messages'):
        self.userid = userid
        self.language=language
        self.url = url
        header = {"content-type": "application/json"}
        data = {"language": language, "userid": userid}

        self.con = requests.post(url=url,data=json.dumps(data),headers=header)
    def get_data(self):
        return self.con.json()

class Admin(object):
    def __init__(self,userid,language,url='http://127.0.0.1:5000/admins'):
        self.userid = userid
        self.language=language
        self.url = url
        header = {"content-type": "application/json"}
        data =f'{url}/{language}/{userid}'
        self.con = requests.get(url=data,headers=header)
    def get_data(self):
        if len(self.con.json())>0:
            return True
        else:
            return False

class StudentPosition(object):
    def __init__(self,userId):
        self.userId=userId


    def get_position(self):
        try:
            data = []
            dist = requests.get(url=f'http://127.0.0.1:5000/student/dist/{configs.LANGUAGE}').json()

            for userId in dist:
                points = requests.get(
                    url=f"http://127.0.0.1:5000/student/total/{configs.LANGUAGE}/{userId['userid']}").json()
                data.append((points['userid'], points['total']))
            scoreboard = dict((x, y) for x, y in data)
            scoreboard_x = sorted(scoreboard.items(), key=operator.itemgetter(1), reverse=True)
            point = requests.get(url=f"http://127.0.0.1:5000/student/total/{configs.LANGUAGE}/{self.userId}").json()
            position = scoreboard_x.index((self.userId, point['total']))
            position += 1
            return position
        except:
            return "Not on scoreboard!"

class Levels(object):
    def __init__(self, url='http://127.0.0.1:5000/levels'):
        self.url = url
        self.con = requests.get(url=url)

    def get_data(self):
        return self.con.json()


class Ranks(object):
    def __init__(self,url='http://127.0.0.1:5000/ranks'):
        self.url = url
        self.con = requests.get(url=url)

    def get_data(self):
        return self.con.json()


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
                start_time = session['start_time'].replace('/','-')
                qlevel = session['level']
                questions = session['questions']
                session_name = session['session_name']
                status = session['status']
                """Save session"""
                print(f"{session_name} saved")
                sql.save_sessions(sess_id, group_language, bot, lesson, each_time, total_time, start_time, qlevel,
                                  questions, session_name, status)
                #queue the notification a minute earlier
                amin_time =utils.liner.session_time(start_time=start_time,period=60)
                # print(amin_time)
                # '''todo activate dynamic time'''
                #Que Notification to the group a min before the session starts
                sched.add_job(utils.Notify().session_start,'date',run_date=amin_time,args=[bot, questions, total_time])
                # sched.add_job(utils.Notify().session_start, 'date', run_date='2020-04-01 23:21:10',
                #                              args=[session_name, questions, total_time])
                #get apollo questions
                if bot=='Apollo':

                    apollos =utils.Questions(id=int(sess_id)).get_questions()
                    stime =0
                    #post every minute 50+10 seconds
                    post_time =int(each_time)+10
                    for apollo in apollos:
                        apollo_id = apollo['id']
                        apollo_language=apollo['language']
                        apollo_question = apollo['question']
                        apollo_answer = apollo['answer']
                        apollo_level = apollo['level']
                        sql.save_apollo(sess_id=sess_id,quesId=apollo_id,question=apollo_question,answer=apollo_answer,qlevel=apollo_level,qlanguage=apollo_language)
                        print(f"saving apollo {session_name} questions")
                        stime += int(post_time)
                        net_time = utils.liner.post_time(start_time='2020-04-20 19:01', period=int(stime))
                        print("start time",stime)
                        print("actual start",net_time)
                        sched.add_job(utils.Notify().apollo_post,'date',run_date=net_time,args=[apollo_id,apollo_question])


                    print(f'Finished saving apollo {session_name} session')
            else:
                print("no new sessions found")


