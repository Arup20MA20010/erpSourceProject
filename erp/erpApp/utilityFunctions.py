from erpApp.models import Department, Course, Enrollments
from users.models import Student
from .constants import gradeMap


def getAllEnrollmentsForGivenStudent(rollNo):
    student = Student.objects.get(rollNo=rollNo)
    enrollmentList = student.enrollments.all()
    return enrollmentList


def getAllEnrollmentsForGivenSemester(rollNo, semester):
    student = Student.objects.get(rollNo=rollNo)
    enrollmentList = student.enrollments.filter(courseData__semester=semester)
    return enrollmentList


def getInfoFromEnrollment(enrollment):
    infoDict = {}
    infoDict['course'] = enrollment.courseData.courseName
    infoDict['credits'] = enrollment.courseData.credits_score
    infoDict['semester'] = enrollment.courseData.semester
    infoDict['rollNo'] = enrollment.studentData.rollNo
    infoDict['name'] = f"{enrollment.studentData.firstName} {enrollment.studentData.lastName}"
    if enrollment.grade:
        infoDict['grade'] = enrollment.grade
    else:
        infoDict['grade'] = '-1'
    return infoDict


def getInfoFromEnrollments(enrollmentList):
    infoList = []
    for enrollment in enrollmentList:
        infoList.append(getInfoFromEnrollment(enrollment))
    return infoList


def getSGPA(rollNo, semester):
    enrollmentList = getAllEnrollmentsForGivenSemester(rollNo, semester)
    enrollmentInfo = getInfoFromEnrollments(enrollmentList)
    sumScore = 0
    totalCredits = 0
    for details in enrollmentInfo:
        credit = details['credits']
        gradeScore = gradeMap[details['grade']]
        sumScore += gradeScore*credit
        totalCredits += credit
    if totalCredits > 0:
        sgpa = sumScore/totalCredits
    else:
        sgpa = 0

    sgpa = round(sgpa, 2)
    return (sgpa, totalCredits)


def getCGPA(rollNo, semester):
    totalCredit = 0
    totalScore = 0
    for sem in range(1, semester+1):
        sgpa = getSGPA(rollNo, sem)
        totalCredit += sgpa[1]
        totalScore += sgpa[0]*sgpa[1]

    if (totalCredit > 0):
        cgpa = totalScore/totalCredit
    else:
        cgpa = 0

    cgpa = round(cgpa, 2)
    return (cgpa, totalCredit)


def ifCouseTaken(rollNo, courseName):
    student = Student.objects.get(rollNo=rollNo)
    if len(student.enrollments.filter(courseData__courseName=courseName)) > 0:
        return True
    return False


def getDepartmentFromRollNo(rollNo):
    depCode = rollNo[2:4]
    department = Department.objects.filter(depCode=depCode)
    if len(department) > 0:
        return department[0]
    else:
        return None


def getStudentsFromAGivenDepartment(department):
    depCode = department.depCode
    studentList = Student.objects.filter(rollNo__icontains=depCode)
    return studentList


def getMaxSemesterRegistered(rollNo):
    student = Student.objects.get(rollNo=rollNo)
    maxSem = 0
    enrollmentList = student.enrollments.all()
    for enrollment in enrollmentList:
        maxSem = max(enrollment.courseData.semester, maxSem)

    return maxSem


def getFacultyList(Faculty):
    facultyChoice = []
    faculties = Faculty.objects.all()
    for faculty in faculties:
        facultyChoice.append(
            (faculty, f"{faculty.firstName} {faculty.lastName} ({faculty.department})"))
    return facultyChoice


def getSemeseterCourses(rollNo, semester):
    if semester > 2:
        department = getDepartmentFromRollNo(rollNo)
        if department is not None:
            courseList = Course.objects.filter(
                deptId=department, semester=semester)
            return courseList

        return None
    else:
        courseList = Course.objects.filter(semester=semester)
        return courseList
