from model.modelDB import StudentCourse

def getCoursesByStudentId(studentId):
    """根据学号查询已修读课程"""
    courses = StudentCourse.query.filter_by(studentId=studentId)
    return list(map(lambda x:x.cId,courses))
