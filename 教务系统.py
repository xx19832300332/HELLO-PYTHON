class Student:
    def __init__(self,name:str,Chinese:int | float,math:int | float,English:int | float):
        self.name=name
        self.Chinese=Chinese
        self.math=math
        self.English=English
    def __str__(self):
        return f"姓名:{self.name} | 语文:{self.Chinese} | 数学:{self.math} | 英语:{self.English}"
    def update(self,Chinese,math,English):
        if Chinese is not None:
            self.Chinese=Chinese
        if math is not None:
            self.math=math
        if English is not None:
            self.English=English
class Edumanagement:
    edu_system="1.0.0"
    system_name="教务管理系统"
    def __init__(self):
        self.student_list=[]
    def add_student(self):
        name=input("请输入添加学生的姓名:")
        for s in self.student_list:
            if s.name==name:
                print("该学生已存在!无法添加!")
                return
        Chinese=int(input("请输入语文成绩:"))
        math=int(input("请输入数学成绩:"))
        English=int(input("请输入英语成绩:"))
        if 0<=Chinese<=100 and 0<=math<=100 and 0<=English<=100:
            stu=Student(name,Chinese,math,English)
            self.student_list.append(stu)
            print(stu)
            print("添加成功!~")
    def update_student(self):
        name = input("请输入添加学生的姓名:")
        for s in self.student_list:
            if s.name==name:
                Chinese = int(input("请输入语文成绩:"))
                math = int(input("请输入数学成绩:"))
                English = int(input("请输入英语成绩:"))
                if 0 <= Chinese <= 100 and 0 <= math <= 100 and 0 <= English <= 100:
                    s.update(Chinese,math,English)
                    print(s)
                    print("修改完成!!~")
                    return
        print("该学生不存在!无法修改!")
        return
    def delete_student(self):
        name = input("请输入添加学生的姓名:")
        for s in self.student_list:
            if s.name==name:
                self.student_list.remove(s)
                print("删除成功!~")
    def get_student(self):
        name=input("请输入查询学生的姓名:")
        for s in self.student_list:
            if s.name == name:
                print(s)
                return
        print("该学生不存在!无法查询!")
        return
    def get_all_student(self):
        for s in self.student_list:
            print(s)
    def run(self):
        while True:
            print("欢迎使用教务系统!")
            print("1.添加学生  2.修改学生  3. 删除学生  4.查询学生  5.查询所有学生  6.退出系统")
            choice = input("请输入您要执行的服务:")
            match choice:
                case "1":
                    self.add_student()
                case "2":
                    self.update_student()
                case "3":
                    self.delete_student()
                case "4":
                    self.get_student()
                case "5":
                    self.get_all_student()
                case "6":
                    print("退出系统!")
                    break
                case _:
                    print("输入有误!请重新输入!")
if __name__ == "__main__":
    edumanagement=Edumanagement()
    edumanagement.run()