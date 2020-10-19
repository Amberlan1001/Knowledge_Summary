
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

### pandas 处理文本字符串 
* 拆分和替换字符串 [参考链接](https://www.pypandas.cn/docs/user_guide/text.html#%E6%8B%86%E5%88%86%E5%92%8C%E6%9B%BF%E6%8D%A2%E5%AD%97%E7%AC%A6%E4%B8%B2)
```python
In [16]:s2 = pd.Series(['a_b_c', 'c_d_e', np.nan, 'f_g_h'])
In [16]:s2.str.split('_')

Out[16]: 
0    [a, b, c]
1    [c, d, e]
2          NaN
3    [f, g, h]
dtype: object
```

切分后的列表中的元素可以通过 get 方法或者 [] 方法进行读取：
```python
In [17]: s2.str.split('_').str.get(1)
Out[17]: 
0      b
1      d
2    NaN
3      g
dtype: object

In [18]: s2.str.split('_').str[1]
Out[18]: 
0      b
1      d
2    NaN
3      g
dtype: object
```

使用expand方法可以轻易地将这种返回展开为一个数据表.
```python
In [19]: s2.str.split('_', expand=True)
Out[19]: 
     0    1    2
0    a    b    c
1    c    d    e
2  NaN  NaN  NaN
3    f    g    h
```

同样，我们也可以限制切分的次数：
```python
In [20]: s2.str.split('_', expand=True, n=1)
Out[20]: 
     0    1
0    a  b_c
1    c  d_e
2  NaN  NaN
3    f  g_h
```