#writing in a file 
file = open('first.txt','w')
print("file is written mode")
file.write("hey")
file.write("It allows us to write in a particular file  \n")
#reading from a file 
#print(file.read())
#appending content in file 
file1=open('first.txt','a')
file.write("this is appending text \n")
file.close()
file = open ('first.txt','r')
print("file is read mode")
print(file.read())
#spliting file content
with open('first.txt','r') as file:
         data=file.readlines()
         for line in data:
              word = line.split()
              print (word)
#creating a new file
f=open("C:\\Users\\JANVI\\python\\second.txt","w")
f.write("hey")
f.close()
f=open("C:\\Users\\JANVI\\python\\second.txt",'r')
print("starting of second file")
print(f.read())

