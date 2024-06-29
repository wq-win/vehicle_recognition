from User.models import User
from Vehicle.models import Plate

# plate = Plate.objects.get(pk=1)
# print(plate.p_plate)
# print(plate.p_roads.r_name)
"""
    all返回的是一个query set    User.objects.all().first() 也是一个model对象
    get返回的是model对象        eg: User.objects.get(pk=1)
    filter返回的是model对象列表  eg: User.objects.filter(pk=1)[0] 与上面等价
"""

# 正向
# plate = Plate.objects.get(pk=1)
# print(plate.p_username.u_username)
# # 反向
# user = User.objects.get(pk=10)
# for plate in user.plate_set.all():
#     print(plate.p_plate)

# # 正向， 属性名称
# p = Plate.objects.filter(pk=1).first()
# print(p.p_username.u_username)
# # 反向， 小写类名_set
# user = User.objects.filter(u_username='test1').first()
# for plate in user.plate_set.all():
#     print(plate.p_plate)

# print(User.objects.all().first())
# plate = Plate.objects.filter(p_plate='赣F8888').first()
# print(type(plate))
# if type(plate) == type(None):
#     print('a')
# else:
#     print('b')
# print(isinstance(plate, type(None)))
# print(plate.p_username.u_username)
# print(plate.p_username_id)
a = []
users = User.objects.all()
for user in users:
    # print(user.u_username)
    a.append(user.u_username)
print(a)
# c = predict.CardPredictor()
# c.train_svm()
# r, roi, color = c.predict("vehicle/5.jpg")
# print(r)