# -*- coding: UTF-8 -*-
from sqlalchemy import or_
from .modelDB import *
from .studentCourseDB import getPassedCoursesByStudenID, getCreditStatistic


def setOtherFiles(otherFiles, studentID):
    for file in otherFiles:
        print('insert', file)
        otherfile = OtherFile(studentID, file)
        db.session.add(otherfile)
        db.session.commit()


def setSpecialities(specialities, studentID):
    for file in specialities:
        print('insert', file)
        specialityFile = Speciality(studentID, file)
        db.session.add(specialityFile)
        db.session.commit()


def getApplicationByIdName(name, openID, studentId):
    """根据姓名/微信编号/学号查询申请表信息"""
    application = Application.query.filter_by(or_(studentId == studentId, name == name, openID == openID))
    # return list(map(lambda x:x.cId,application))
    return application


def getApplicationByOpenID(openID):
    """根据姓名/微信编号/学号查询申请表信息"""
    application = Application.query.filter_by(openID=openID).first()
    # return list(map(lambda x:x.cId,application))
    application.courses = getPassedCoursesByStudenID(application.studentID)
    return application


def insertApplicqtion(openID, studentName, studentID, institute, major, grade, downGrade, choiceAfterGraduating, doctor,
                      ID, courses, CET, CETScore, GPA, academicRecord, CETRecord):
    """插入一个申请表信息"""
    application = Application(openID=openID, name=studentName, studentID=studentID, institute=institute,
                              major=major, grade=grade, downGrade=downGrade,
                              choiceAfterGraduating=choiceAfterGraduating, doctor=doctor, ID=ID, CET=CET,
                              CETScore=CETScore, GPA=GPA, academicRecord=academicRecord, CETRecord=CETRecord)
    db.session.add(application)
    db.session.commit()


def deleteApplication(name, openID, studentId):
    """根据姓名/微信编号/学号删除一个申请表信息"""
    Application.query.filter_by(or_(openID == openID, name=name, studentId=studentId)).delete()


def deleteOtherFile(studentID):
    OtherFile.query.filter_by(studentID=studentID).delete()


def deleteSpecialities(studentId):
    Speciality.query.filter_by(studentID=studentId).delete()


def updateApplicationByOpenID(openID, name, studentID, institute, major, grade, downGrade, choiceAfterGraduating,
                              doctor, ID,
                              courses, CET, CETScore, GPA, academicRecord, CETRecord):
    """修改指定姓名用户的姓名"""
    Application.query.filter_by(openID=openID).update(
        {'name': name, 'studentID': studentID, 'institute': institute, 'major': major, 'grade': grade,
         'downGrade': downGrade,
         'choiceAfterGraduating': choiceAfterGraduating, 'doctor': doctor, 'ID': ID, 'CET': CET, 'CETScore': CETScore,
         'GPA': GPA, 'academicRecord': academicRecord, 'CETRecord': CETRecord})


def updateOtherFile(otherFiles, studentID):
    OtherFile.query.filter_by()

def getAllApplication():
    """获取所有申请信息"""
    applications = Application.query.all()
    for application in applications:
        application.courses = getPassedCoursesByStudenID(application.studentID)
    print("len", len(applications))
    return applications


def getSexStatistic():
    res = list(Application.query.all())
    resC = list(map(lambda x: int(x.ID[16:17]) % 2, res))
    return {"male": resC.count(1), "female": resC.count(0)}


def getGradeStatistic():
    result = list(db.session.execute('SELECT grade,COUNT(*) as num from application GROUP BY grade'))
    return list(map(lambda x: ({str(x.grade): x.num}), result))


def getMajorStatistic():
    result = list(db.session.execute('SELECT major,COUNT(*) as num from application GROUP BY major'))
    return list(map(lambda x: ({str(x.major): x.num}), result))


def getTotalStudent():
    return len(Application.query.all())


def getSpecialStudentStatistic():
    return list(db.session.execute('select count(*) as count from application where speciality=0'))[0].count


def getStatisticData():
    data = {'totalNum': getTotalStudent(), 'sex': getSexStatistic(), 'grade': getGradeStatistic(),
            'major': getMajorStatistic(), 'specialStudent': getSpecialStudentStatistic(),
            'credit': getCreditStatistic()}
    return data
