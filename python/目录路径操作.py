
print(os.getcwd()) #是工作目录
print(os.path.abspath(os.path.dirname(__file__))) # 当前脚本的路径
os.path.realpath(__file__) #是脚本所在的绝对路径，

'***获取上级目录***'
print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
print(os.path.abspath(os.path.dirname(os.getcwd())))
print(os.path.abspath(os.path.join(os.getcwd(), "..")))

# 返回上2级目录
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  
print(os.path.abspath(os.path.join(__file__, "../../")))    