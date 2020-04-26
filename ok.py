import utils
import botify
import configs
import requests
sql= utils.DBHelper()
#
name="easyguy"
userid =907856
group_title ="Test"
# botify.create_student(userid=userid,name=name)
#
# student=utils.Student(userid=userid,language=configs.LANGUAGE).get_data()
# africa=student[0]['fortunas']
# apollo =student[0]['fortunas']
# utils.CUMessages(userid=userid,language=configs.LANGUAGE).get_data()
# position =utils.StudentPosition(userId=userid).get_position()
# messages =utils.GetMessages(userid=userid,language=configs.LANGUAGE).get_data()
# student_point = utils.GetFortuna(userid,configs.LANGUAGE).get_data()
"""Levels Data"""
level =utils.Levels().get_data()
elementarypts=level[0]['points']
intermediatepts=level[1]['points']
advancedpts=level[2]['points']
"""RANKS DATA"""
ranks =utils.Ranks().get_data()
studentmsg=ranks[0]['messages']
studentpts=ranks[0]['points']
apprenticemsg=ranks[1]['messages']
apprenticepts=ranks[1]['points']
followermsg=ranks[2]['messages']
followerpts=ranks[2]['points']
instructormsg=ranks[3]['messages']
instructorpts=ranks[3]['points']
mentormsg=ranks[4]['messages']
mentorpts=ranks[4]['points']
teachermsg=ranks[5]['messages']
teacherpts=ranks[5]['points']
scholarmsg=ranks[6]['messages']
scholarpts=ranks[6]['points']
mastermsg=ranks[7]['messages']
masterpts=ranks[7]['points']
eminencemsg=ranks[8]['messages']
eminencepts=ranks[8]['points']
gurumsg=ranks[9]['messages']
gurupts=ranks[9]['points']
titanmsg=ranks[10]['messages']
titanpts=ranks[10]['points']


user_messages =20000
totalpts=40000


# If a is more than 10 but less than 20, print this:
# if 10 < a < 20:
if (studentmsg<=user_messages<apprenticemsg) and (studentpts<=totalpts<apprenticepts):
    print("student")
elif(apprenticemsg<=user_messages<followermsg) and (apprenticepts<=totalpts<followerpts):
    print("apprentice")
elif(followermsg <=user_messages<instructormsg) and(followerpts<=totalpts<instructorpts):
    print('follower')
elif(instructormsg<=user_messages<mentormsg) and (instructorpts<=totalpts<mentorpts):
    print('instructor')
elif(mentormsg<=user_messages<teachermsg) and (mentorpts<=totalpts<teacherpts):
    print('mentor')
elif(teachermsg<=user_messages<scholarmsg) and (teacherpts<=totalpts<scholarpts):
    print("teacher")
elif(scholarmsg<=user_messages<mastermsg) and (scholarpts<=totalpts<masterpts):
    print('scholar')
elif(mastermsg<=user_messages<eminencemsg) and (masterpts<=totalpts<eminencepts):
    print("master")
elif(eminencemsg<=user_messages<gurumsg) and (eminencepts<=totalpts<gurupts):
    print("eminence")
elif (gurumsg<=user_messages<titanmsg) and(gurupts>=totalpts<titanpts):
    print("guru")
elif (user_messages>=titanmsg) and (totalpts>=titanpts):
    print('titan')