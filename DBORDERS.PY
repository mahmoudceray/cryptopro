#ينشئ قاعدة بيانات جديدة باسم يحدده المستخدم
# في حال لم يكن هناك قاعدة بيانات أصلاً بهذاالإسم.

def CREATE_DATABASE(name):
    return "CREATE DATABASE IF NOT EXISTS {};".format(name)



#يحذف قاعدة بيانات  باسم يحدده المستخدم
# في حال كان هناك قاعدة بيانات أصلاً بهذا الإسم

def del_DATABASE(name):
    return "DROP DATABASE IF EXISTS {};".format(name)

