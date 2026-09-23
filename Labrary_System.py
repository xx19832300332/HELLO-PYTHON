from abc import ABC,abstractmethod
import json
#书籍类
class Book(ABC):
    def __init__(self, book_id, title, author, num):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.num = num
        self.available_num = num
    def borrow_book(self):
        if self.available_num > 0:
            self.available_num -= 1
            return True
        else:
            return False
    def return_book(self):
        if self.available_num < self.num:
            self.available_num += 1
    def get_available_num(self):
        return self.available_num
class Member(ABC):
    def __init__(self,member_id,name,password):
        self.member_id = member_id
        self.name = name
        self.__password = password
        self.__borrowed_books = {}
    def borrow_book(self,book : Book):
        #判断借书数量是否达到最大限制.
        if len(self.__borrowed_books) >= self.get_max_books():
            print("借书数量已达到最大限制，无法借书。")
            return False
        #判断书籍是否可以借阅
        if book.borrow_book():
            if book.book_id not in self.__borrowed_books.keys():
                print(f"{self.name}已成功借阅了{book.title}")
                self.__borrowed_books[book.book_id] = book
                return True
            else:
                print(f"借阅失败,{book.title}已被借完!")
    def return_book(self,book : Book):
        if book.book_id in self.__borrowed_books:
            book.return_book()
            del self.__borrowed_books[book.book_id]
            print(f"{self.name}已成功归还了{book.title}")
        else:
            print(f"{self.name}未借阅过{book.title},无法归还")
    def get_password(self):
        return self.__password
    def get_borrowed_books(self):
        return self.__borrowed_books
    @abstractmethod
    def get_max_books(self):
        pass
class NormalMember(Member):
    def get_max_books(self):
        return 3
    
class VIPMember(Member):
    def __init__(self, member_id, name, password, vip_level = 1):
        super().__init__(member_id, name, password)
        self.vip_level = vip_level
    def get_max_books(self):
        return int(self.vip_level) + 6
class LibrarySystem():
    def __init__(self):
        self.books = {}
        self.members = {}
        self.current_member: Member|None = None
        self.load_books()
        self.load_numbers()
    def load_books(self):
        with open("./图书信息.json",'r',encoding = 'utf-8') as f:
            books = json.load(f)
        for book in books:
            self.books[book['编号']] = Book(book['编号'],book['标题'],book['作者'],book['数量'])
        print('加载图书数据成功!')
    def load_numbers(self):
        with open("./会员信息.json",'r',encoding = 'utf-8') as f:
                    members = json.load(f)
        for member in members:
            if member['卡号'].startswith('N'):
                self.members[member['卡号']] = NormalMember(member['卡号'],member['姓名'],member['密码'])
            elif member['卡号'].startswith('V'):
                self.members[member['卡号'] ] = VIPMember(member['卡号'],member['姓名'],member['密码'],member['会员等级'])  
        print('加载会员信息成功!')
    def login(self):
        while True:
            print("<<请输入账号密码登录!>>")
            member_id = input('请输入账号:')
            password = input('请输入密码:')
            if member_id not in self.members:
                print('会员信息不存在!')
                continue
            
            if password == self.members[member_id].get_password():
                print('登陆成功!')
                self.current_member = self.members[member_id]
                return True
            else:
                print('密码错误!登陆失败!')
                continue
    def borrow_book(self):
        print('以下是图书列表:')
        for book in self.books.values():
            print(f"编号:{book.book_id},标题:{book.title},作者:{book.author},数量:{book.num},可用:{book.available_num}")
        book_id = input('请输入借阅的图书编号')
        if book_id not in self.books.keys():
            print('该图书不存在!')
            return
        self.current_member.borrow_book(self.books[book_id])
    def return_book(self):
        borrowed_books = self.current_member.get_borrowed_books()
        print('已经借阅的图书列表')
        for book in borrowed_books.values():
            print(f"图书编号:{book.book_id},标题:{book.title},作者:{book.author}")
        book_id = input('请输入要归还的图书编号')
        if book_id not in borrowed_books.keys():
            print('还书失败,该图书不存在!')
            return
        self.current_member.return_book(self.books[book_id])
    def check_book(self):
        borrowed_books = self.current_member.get_borrowed_books()
        if borrowed_books:
            for book in borrowed_books.values():
                print(f'编号:{book.book_id},标题:{book.title},作者:{book.author}')
        else:
            print('您无借阅书籍!')
            return
    def run(self):
        if self.login():
            while True:
                print('1.借阅图书')
                print('2.归还图书')
                print('3.查看借阅')
                print('4.退出系统')

                choice = input('你要执行的操作:')
                match choice:
                    case "1":
                        self.borrow_book()
                    case "2":
                        self.return_book()
                    case "3":
                        self.check_book()
                    case "4":
                        print('bye~bye~,欢迎下次使用!')
                        break
                    case _:
                        print('无效输入!')
if __name__ == '__main__':
    ls = LibrarySystem()
    ls.run()