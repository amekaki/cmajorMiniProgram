import json

from flask import Blueprint, request, session

from model.applicationDB import insertApplicqtion, updateApplicationByOpenID, getApplicationByOpenID
# from model.couresDB import getCoursesByStudentId
from model.studentCourseDB import setCourseByStudentID, getPassedCoursesByStudenID, updateCourseByStudentID, \
    getCreditStatistic
from model.studentDB import getStudentUserByUserName, insertStudent, deleteStudent, updateStudentInfo
from model.modelDB import StudentUser
from server.studentServer import checkUser

student = Blueprint("student", __name__)  # 实例化student蓝图


@student.route('/getInfo', methods=["GET"])
def getStudentInfo():
    user = getStudentUserByUserName(request.args['username'])
    return user.to_json()


@student.route('/insertStudentUser', methods=['GET'])
def insertStudentUser():
    username=request.args['username']
    student_id=request.args['student_id']
    insertStudent(username,student_id)
    return "OK"

@student.route('/deleteStudentUser',methods=['GET'])
def deleteStudentUser():
    student_id=request.args['student_id']
    deleteStudent(student_id)
    return "OK"


@student.route('/updateStudentInfo', methods=['GET'])
def updateStudentUserInfo():
    username = request.args['username']
    student_id = request.args['student_id']
    updateStudentInfo(student_id, username)
    return "OK"


# @student.route('/getPassedCourseByStudentID', methods=['GET'])
# def getCourse():
#     student_id = request.args['student_id']
#     # courses = getCoursesByStudentId(student_id)
#     return json.dumps(list(map(lambda x: x.cId, courses)))


@student.route('/setSession', methods=['GET'])
def setSession():
    session.permanent = True
    session['username'] = 'sess'
    return 'sessionTest'


@student.route('/checkSession', methods=['GET'])
def checkSession():
    return session.get('username')


# openID=ooo&studentName=courseTest&studentID2018141531004&institute=wangan&major=wangan&grade=2018&downGrade=1&choiceAfterGraduating=1&doctor=1&ID=341602200008087181&courses=["107032030","10711500"]
# TODO 课程修读情况处理及存储
@student.route('/setApplication', methods=['POST'])
def setApplication():
    if checkUser("111") is False:
        return 0
    studentName = request.form.get("studentName")
    # print("student", studentName)
    openID = request.form.get("openID")
    studentID = request.form.get("studentID")
    institute = request.form.get("institute")
    major = request.form.get("major")
    grade = request.form.get("grade")
    downGrade = int(request.form.get("downGrade"))
    # print("dwonGrade", downGrade)
    choiceAfterGraduating = int(request.form.get("choiceAfterGraduating"))
    doctor = int(request.form.get("doctor"))
    ID = int(request.form.get("ID"))
    courses = request.form.get("courses")
    CET = request.form.get("CET")
    CETScore = request.form.get("CETScore")
    GPA = request.form.get("GPA")
    setCourseByStudentID(courses, studentID)
    insertApplicqtion(openID, studentName, studentID, institute, major, grade, downGrade, choiceAfterGraduating, doctor,
                      ID, courses, CET, CETScore, GPA)
    return "OK"

@student.route('/updateApplication', methods=['POST'])
def updateApplication():
    studentName = request.form.get("studentName")
    print("student", studentName)
    openID = request.form.get("openID")
    studentID = request.form.get("studentID")
    institute = request.form.get("institute")
    major = request.form.get("major")
    downGrade = int(request.form.get("downGrade"))
    grade = request.form.get("grade")
    print("dwonGrade", downGrade)
    choiceAfterGraduating = int(request.form.get("choiceAfterGraduating"))
    doctor = int(request.form.get("doctor"))
    ID = int(request.form.get("ID"))
    courses = request.form.get("courses")
    CET = request.form.get("CET")
    CETScore = request.form.get("CETScore")
    GPA = request.form.get("GPA")
    print("studentID", studentID)
    print("getCourses (UPdate", courses)
    updateApplicationByOpenID(openID, studentName, studentID, institute, major, grade, downGrade,
                              choiceAfterGraduating, doctor, ID, courses, CET, CETScore, GPA)
    updateCourseByStudentID(courses, studentID)
    return getApplicationByOpenID(openID).to_json()


@student.route('/getApplicationByOpenID', methods=['GET'])
def getAppli():
    openID = request.args.get("openID")
    return getApplicationByOpenID(openID).to_json()

@student.route('/login', methods=['GET'])
def login():
    code = request.args['code']


@student.route('/getApplication', methods=['GET'])
def getApplication():
    openID = request.args.get("openID")
    appli = getApplicationByOpenID(openID)
    appli.courses = getPassedCoursesByStudenID(appli.studentId)
    return appli.to_json()
