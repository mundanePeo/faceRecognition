from App.exts import model


class People(model.Model):

    info_id = model.Column(model.Integer, primary_key=True, autoincrement=True)
    area = model.Column(model.Integer)
    cam = model.Column(model.Integer)
    face_id = model.Column(model.String(10))
    face_path = model.Column(model.String(100))
    feature_path = model.Column(model.String(100))


# 增加
def add(INFO):
    face = People()
    face.area = INFO[0]
    face.cam = INFO[1]
    face.face_id = INFO[2]
    face.face_path = INFO[3]
    face.feature_path = INFO[4]

    model.session.add(face)
    model.session.commit()
    return 'add Success!'


# 查找
def get(filter_num):
    result = []
    # 返回的是BaseQuery类型
    faces = People.query.filter(People.area.__eq__(filter_num))
    for face in faces:
        result.append([face.cam, face.face_id, face.face_path, face.feature_path])
    # print(result)
    return result


# 增加多条记录
# def adds():
#     students = []
#     for i in range(10):
#         student = Student()
#         student.s_name = '小明%d' % random.randrange(100)
#         students.append(student)
#     model.session.add_all(students)
#     model.session.commit()
#     return 'add Success!'


# 删除
def delete(face_id):
    # 查找第一条记录
    del_face = model.query.filter(model.face_id.__eq__(face_id))
    # 删除
    model.session.delete(del_face)
    model.session.commit()
    return 'delete Success!'


# 修改
# def modify_student():
#     # 查找第一条记录
#     student = Student.query.first()
#     # 修改
#     student.s_name = '小红'
#     model.session.add(student)
#     model.session.commit()
#     return 'modify Success!'
