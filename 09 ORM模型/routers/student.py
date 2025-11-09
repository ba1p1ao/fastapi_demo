from typing import List
from fastapi import APIRouter, HTTPException

# 需要区分 ORM 模型（数据库操作）与 pydantic 模型（数据验证/序列化）
from models.models import (
    Student as dbStudent,
    Course as dbCourse,
    Clas as dbClas,
    Teacher as dbTeacher,
)
from schemas.student import StudentCreate

student = APIRouter()


@student.get("/")
async def getAllStudent():

    # 查询所有
    students = await dbStudent.all().prefetch_related(
        "clas", "courses"
    )  # 预加载关联数据
    # print(students)
    # # 异步直接返回的不是列表，是一个promise对象，await是为了等到promise对象返回queryset响应
    # # 异步协程肯定单线程，一个线程一应一个事件循环，事件循环里的所有任务都由这一个线程完成，IO密集型场景又快又节省系统资源
    # for s in students:
    #     print(s.name, s.id)

    # # 过滤查询
    # students = await dbStudent.filter(clas_id=1)

    # # 条件查询
    # students = await dbStudent.filter(sno__gte=2023003) [QuerySet(),QuerySet()]
    # students = await dbStudent.filter(sno__range=(2023001, 2023003))

    # # values 查询
    # students = await dbStudent.all().values("name", "sno") # [{"name": ..., "sno": ...}, {...}, {}]

    # 一对多， 多对多 查询
    # stu_cui = await dbStudent.get(name="cui")
    # print(stu_cui.name)
    # print(stu_cui.sno)

    # 一对多 查询
    # 查询 cui 是哪个班的，得到班级名称
    # # 方法一通过 dbClas.filter 过滤
    # print(await dbClas.filter(id=stu_cui.clas_id)) # [<Clas: 3>]
    # print(await dbClas.filter(id=stu_cui.clas_id).values("name")) # [{'name': '二年级一班'}]

    # 方法二通过 stu_cui.clas，直接对clas表做操作
    # print(await stu_cui.clas.values())
    # # {'id': 3, 'name': '二年级一班'}

    # print(await stu_cui.clas.values("name"))
    # # {'name': '二年级一班'}

    # print(await stu_cui.courses.all())
    # # [<Course: 1>, <Course: 2>]

    # print(await stu_cui.courses.all().values())
    # # [{'id': 1, 'name': '高等数学', 'addr': '', 'teacher_id': 1}, {'id': 2, 'name': 'Python编程', 'addr': '', 'teacher_id': 2}]

    # print(await stu_cui.courses.all().values("name", "teacher__name"))
    # # 通过 cui 对应的所有 courses 数据，对应 该课程对应的教师名称信息
    # # 之所以可以这样写是因为 course 的 teacher 是 teacher = fields.ForeignKeyField("models.Teacher", related_name="courses")关联的外健
    # # [{'name': '高等数学', 'teacher__name': '张教授'}, {'name': 'Python编程', 'teacher__name': '李老师'}]

    # # 多对多查询
    # # 查询多个学生的班级信息
    # print(await dbStudent.all())
    # # [<Student: 1>, <Student: 2>, <Student: 3>, <Student: 4>, <Student: 10>]

    # ### 错误写法 print(await stu_all.values("name", "clas")) # 因为 await 完成之后 stu_all 变成了 List类型， 而不是 QueryList

    # print(await dbStudent.all().values("name", "clas__name"))
    # # 通过 clas__name, 两个 _ 的方式，可以直接获取到clas表的name字段信息
    # # [{'name': '小明', 'clas__name': '一年级一班'}, {'name': '小红', 'clas__name': '一年级一班'}, {'name': '小刚', 'clas__name': '一年级二班'}, {'name': '小丽', 'clas__name': '二年级一班'}, {'name': 'cui', 'clas__name': '二年级一班'}]

    # stu_all = await dbStudent.all().values("name", "clas__name", "courses__name")
    # print(stu_all)

    return {"操作": "查看所有的学生", "data": students}


@student.get("/{sid}")
async def getOneStudent(sid: int):
    student = await dbStudent.get(id=sid)
    return {"操作": f"查看id={sid}的学生", "data": student}


@student.post("/")
async def addStudent(
    student: StudentCreate,
):
    # 添加学生数据，应该调用schemas/中的student 进行pydantic 模型（数据验证/序列化）
    print(student)
    # # 方式一
    # stu = dbStudent(
    #     name=student.name,
    #     pwd=student.pwd,
    #     sno=student.sno,
    #     clas_id=student.clas_id,
    # )
    # await stu.save() # 异步操作

    # 方式二
    # 执行数据库写入操作
    stu = await dbStudent.create(
        name=student.name,
        pwd=student.pwd,
        sno=student.sno,
        clas_id=student.clas_id,
    )

    # 多对多添加数据，关系绑定
    choose_courses = await dbCourse.filter(id__in=student.courses)
    # stu 为 await dbStudent.create 返回的数据
    # 采用 stu.courses 的方式引用 ManyToManyField 中的各种方法，对ORM自动生成的多对多表 student_course表做操作
    # choose_courses 是一个列表的形式，使用 *choose_courses，对数据进行打散
    await stu.courses.add(*choose_courses)

    return {"操作": "添加的学生", "data": stu}


@student.put("/{sid}")
async def updateStudent(sid: int, student: StudentCreate):
    stu = await dbStudent.get(id=sid)
    print(stu)

    # exclude=["courses"] 向 update 传参数的时候不包含 courses
    update_student_dict = student.model_dump(exclude=["courses"])
    await dbStudent.filter(id=sid).update(**update_student_dict)

    # 多对多修改
    # 先找到 dbCourse 符合 student.courses 的列表
    choose_courses = await dbCourse.filter(id__in=student.courses)

    # 建议使用事务后使用 courses.set(). clear() 和 add() 并行操作可能数据会有异常
    # 先将student_course id__in=courses中多对多的数据清除
    await stu.courses.clear()

    # 再添加，因为choose_courses是一个列表形式所以使用*choose_courses
    await stu.courses.add(*choose_courses)

    return {"操作": "修改的学生", "data": stu}


    # """更新学生信息 优化版本"""
    # # 检查学生是否存在
    # stu = await dbStudent.get_or_none(id=sid)
    # if not stu:
    #     raise HTTPException(status_code=404, detail="学生不存在")
    
    # # 使用事务确保数据一致性
    # async with in_transaction():
    #     # 更新基础信息
    #     update_data = student.model_dump(exclude=["courses"])
    #     await dbStudent.filter(id=sid).update(**update_data)
        
    #     # 处理课程关系（如果有提供课程信息）
    #     if student.courses:
    #         # 查询有效的课程
    #         valid_courses = await dbCourse.filter(id__in=student.courses)
    #         # 直接设置课程关系（会自动清除旧关系）
    #         await stu.courses.set(valid_courses)
    
    # # 返回更新后的完整信息
    # updated_student = await dbStudent.get(id=sid).prefetch_related("courses")
    # return {"操作": "修改成功", "data": updated_student}


@student.delete("/{sid}")
async def deleteStudent(sid: int):
    # dbStudent.filter(id=sid).delete() 的返回值为删除几个数据，
    # 如果为0，说明没有数据可以删除，也就是不存在查找的数据
    delete_count = await dbStudent.filter(id=sid).delete()
    if not delete_count:
        raise HTTPException(status_code=404, detail=f"id={sid}学生不存在") 
    return {"操作": f"删除id={sid}的学生", "data": delete_count}
