def user1():
    f=open("C:\\Users\\JANVI\\python\\intro.txt","w")
    name=input("enter your name:")
    course=input("enter your course")
    f.write(name)
    f.write(course)
    f.close()
user1()

def user2():
    f=open("C:\\Users\\JANVI\\python\\intro.txt","r")
    print(f.read())
    f.close()
user2()


jassi2166@gmail.com
8968937272