
# python 常用脚本

### 路径目录操作

``` python
print(os.getcwd()) #是工作目录
print(os.path.abspath(os.path.dirname(__file__))) # 当前脚本的路径
os.path.realpath(__file__) #是脚本所在的绝对路径，

# ***获取上级目录***
print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
print(os.path.abspath(os.path.dirname(os.getcwd())))
print(os.path.abspath(os.path.join(os.getcwd(), "..")))

# 返回上2级目录
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))  
print(os.path.abspath(os.path.join(__file__, "../../")))
```

#### 自动获取函数运行时间（装饰器方式）
``` python
import time
from functools import wraps

def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} time cost: {}'.format(func.__module__, func.__name__, round(end - start, 4)))
        return r
    return wrapper

@timethis
def add(a, b):
    return a + b
```

### 获取当前服务器 ip 和地址别名
```python
import socket

gethostname = socket.gethostname()
ip = socket.gethostbyname(gethostname)
print("地址别名", gethostname)
print("ip 地址")
```