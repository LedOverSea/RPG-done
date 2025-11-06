# 1. python简介

python是一门解释型语言

# 2. 使用python解释器

## 2.1 唤出解释器

```powershell
python
python -c command
python -m module
python -i
```

### 2.1.1 传入参数

`sys.argv` 参数列表

### 2.1.2 交互模式

`>>>`主提示符

`...`次要提示符

唤出解释器不加参数时默认在交互模式下运行

## 2.2 解释器的运行环境

### 2.2.1 源文件的字符编码

默认情况下是utf-8

# 3. python速览

## 3.1 python用作计算器

### 3.1.1 数字

交互模式下，上次输出的结果会赋值给变量`_`，建议把这个变量当作只读类型，不要显式赋值

### 3.1.2 文本

转义字符：在前面增加`\`

如果不希望转义，可以使用原始字符串，在字符串前加`r`，如`print(r'C:\some\name')`

Python 字符串不能修改，是immutable的。

### 3.1.3 列表

列表是mutable可变类型

切片会返回列表的浅拷贝

# 4. 更多控制流工具

## 4.1 if语句

## 4.2 for语句

## 4.3 range() 函数

返回的是一个可迭代对象iterable，而非具体的列表

## 4.4 break和continue语句

## 4.5 循环的else子句

## 4.6 pass语句

## 4.7 match语句

“变量名” `_` 被作为 *通配符* 并必定会匹配成功

形如解包赋值的模式可被用于绑定变量：

```python
# point 是一个 (x, y) 元组
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("Not a point")
```

请仔细学习此代码！第一个模式有两个字面值，可视为前述字面值模式的扩展。接下来的两个模式结合了一个字面值和一个变量，变量 *绑定* 了来自主语（`point`）的一个值。第四个模式捕获了两个值，使其在概念上与解包赋值 `(x, y) = point` 类似。

## 4.8 定义函数

函数内的第一条语句是字符串时，该字符串就是文档字符串，也称为 *docstring*，详见 [文档字符串](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#tut-docstrings)。利用文档字符串可以自动生成在线文档或打印版文档，还可以让开发者在浏览代码时直接查阅文档；Python 开发者最好养成在代码中加入文档字符串的好习惯。

函数在 *执行* 时使用函数局部变量符号表，所有函数变量赋值都存在局部符号表中；引用变量时，首先，在局部符号表里查找变量，然后，是外层函数局部符号表，再是全局符号表，最后是内置名称符号表。

return` 语句不带表达式参数时，返回 `None`。函数执行完毕退出也返回 `None

## 4.9 函数定义详解

### 4.9.1 默认值参数

默认值在函数定义时计算

### 4.9.2 关键字参数

位置参数必须在关键字参数之前

形参`**name`接收字典，对应关键字参数；`*name`接收元组，对应位置参数

### 4.9.4. 任意实参列表

例子

```python
def concat(*args, sep="/"):
    return sep.join(args)

concat("earth", "mars", "venus")

concat("earth", "mars", "venus", sep=".")
```

### 4.9.5. 解包实参列表

列表/元组，用*

字典，用**

### 4.9.6. Lambda 表达式

用于创建小巧的匿名函数

### 4.9.7 文档字符串

以下是文档字符串内容和格式的约定。

第一行应为对象用途的简短摘要。为保持简洁，不要在这里显式说明对象名或类型，因为可通过其他方式获取这些信息（除非该名称碰巧是描述函数操作的动词）。这一行应以大写字母开头，以句点结尾。

文档字符串为多行时，第二行应为空白行，在视觉上将摘要与其余描述分开。后面的行可包含若干段落，描述对象的调用约定、副作用等。

### 4.9.8. 函数注解

可选的用户自定义函数类型的元数据完整信息

# 5. 数据结构

## 5.1 列表详解

## 5.2 del语句

## 5.3 元组和序列

序列类型：list，tuple，range，str

元组tuple是不可变对象

## 5.4 集合

创建集合用花括号或 `set()`函数

## 5.5 字典

字典用键作为索引，键可以是任何不可变类型

## 5.6 循环的技巧

字典 items()

序列 enumerate()

对于两个或多个序列 zip()

去除序列中的重复元素 set()

## 5.7 深入条件控制

## 5.8 序列和其他类型的比较

序列对象可以与相同序列类型的其他对象比较。这种比较使用 *字典式* 顺序

# 6. 模块

模块是包含 Python 定义和语句的文件。其文件名是模块名加后缀名 `.py` 。在模块内部，通过全局变量 `__name__` 可以获取模块名（即字符串）。

## 6.1 模块详解

import 最后的内容会加载到命名空间

比如`from fibo import fib, fib2`将fib，fib2加载到命名空间，而fibo未定义

### 6.1.1 以脚本方式执行模块

可以用以下方式运行 Python 模块：

```
python fibo.py <arguments>
```

这项操作将执行模块里的代码，和导入模块一样，但会把 `__name__` 赋值为 `"__main__"`。 也就是把下列代码添加到模块末尾：

```
if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))
```

### 6.1.2 模块搜索路径

### 6.1.3 “已编译的”python文件

为了快速加载模块，Python 把模块的编译版本缓存在 `__pycache__` 目录中，文件名为 `module.version.pyc`，version 对编译文件格式进行编码，一般是 Python 的版本号

## 6.2 标准模块

python自带一个标准模块的库

## 6.3 dir()函数

查找模块定义的名称

## 6.4 包

需要有 `__init__.py` 文件才能让 Python 将包含该文件的目录当作包来处理

### 6.4.1 从包中导入*

不建议使用此语法

[`import`](https://docs.python.org/zh-cn/3/reference/simple_stmts.html#import) 语句使用如下惯例：如果包的 `__init__.py` 代码定义了列表 `__all__`，运行 `from package import *` 时，它就是被导入的模块名列表

### 6.4.2 相对导入

需要注意的是，相对导入是基于当前模块所属包的名称进行的。由于主模块（即直接运行的脚本）没有所属包，因此那些打算作为 Python 应用程序主模块使用的模块，必须始终使用绝对导入。

### 6.4.3 多目录中的包

# 7. 输入与输出

## 7.1 更复杂的输出格式

格式化输出包括以下几种方法。

- 使用 [格式化字符串字面值](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#tut-f-strings) ，要在字符串开头的引号/三引号前添加 `f` 或 `F` 。在这种字符串中，可以在 `{` 和 `}` 字符之间输入引用的变量，或字面值的 Python 表达式。

  ```python
  year = 2016
  event = 'Referendum'
  f'Results of the {year} {event}'
  'Results of the 2016 Referendum'
  ```

- 字符串的 [`str.format()`](https://docs.python.org/zh-cn/3/library/stdtypes.html#str.format) 方法需要更多手动操作。 你仍将使用 `{` 和 `}` 来标记变量将被替换的位置并且可以提供详细的格式化指令，但你还需要提供待格式化的信息。 下面的代码块中有两个格式化变量的例子：

  ```python
  yes_votes = 42_572_654
  total_votes = 85_705_149
  percentage = yes_votes / total_votes
  '{:-9} YES votes  {:2.2%}'.format(yes_votes, percentage)
  ' 42572654 YES votes  49.67%'
  ```

  请注意Notice how the `yes_votes` 填充了空格并且只为负数添加了负号。 这个例子还打印了 `percentage` 乘以 100 的结果，保留 2 个数位并带有一个百分号 (请参阅 [格式规格迷你语言](https://docs.python.org/zh-cn/3/library/string.html#formatspec) 了解详情)。

### 7.1.1 格式化字符串字面值

### 7.1.2 字符串format()方法

### 7.1.3 手动格式化字符串

### 7.1.4 旧式字符串格式化方法

format % values

## 7.2 读写文件

`open(filename, mode, encoding=None)`

*mode* 的值包括 `'r'` ，表示文件只能读取；`'w'` 表示只能写入（现有同名文件会被覆盖）；`'a'` 表示打开文件并追加内容，任何写入的数据会自动添加到文件末尾。`'r+'` 表示打开文件进行读写。*mode* 实参是可选的，省略时的默认值为 `'r'`

在处理文件对象时，最好使用 [`with`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#with) 关键字。优点是，子句体结束后，文件会正确关闭，即便触发异常也可以

### 7.2.1 文件对象的方法

### 7.2.2 使用json保存结构化数据

标准库模块 [`json`](https://docs.python.org/zh-cn/3/library/json.html#module-json) 可以接受带有层级结构的 Python 数据，并将其转换为字符串表示形式；这个过程称为 *serializing*。 根据字符串表示形式重建数据则称为 *deserializing*。 在序列化和反序列化之间，用于代表对象的字符串可以存储在文件或数据库中，或者通过网络连接发送到远端主机。

# 8. 错误和异常

错误至少分为两种：语法错误和异常

## 8.1 语法错误

## 8.2 异常

## 8.3 异常的处理

可以编写程序处理选定的异常。下例会要求用户一直输入内容，直到输入有效的整数，但允许用户中断程序（使用 Control-C 或操作系统支持的其他操作）；注意，用户中断程序会触发 [`KeyboardInterrupt`](https://docs.python.org/zh-cn/3/library/exceptions.html#KeyboardInterrupt) 异常。

```
while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
```

[`try`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#try) 语句的工作原理如下：

- 首先，执行 *try 子句* （[`try`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#try) 和 [`except`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#except) 关键字之间的（多行）语句）。
- 如果没有触发异常，则跳过 *except 子句*，[`try`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#try) 语句执行完毕。
- 如果在执行 [`try`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#try) 子句时发生了异常，则跳过该子句中剩下的部分。 如果异常的类型与 [`except`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#except) 关键字后指定的异常相匹配，则会执行 *except 子句*，然后跳到 try/except 代码块之后继续执行。
- 如果发生的异常与 *except 子句* 中指定的异常不匹配，则它会被传递到外层的 [`try`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#try) 语句中；如果没有找到处理器，则它是一个 *未处理异常* 且执行将停止并输出一条错误消息。

## 8.4. 触发异常

[`raise`](https://docs.python.org/zh-cn/3/reference/simple_stmts.html#raise) 语句支持强制触发指定的异常

## 8.5 异常链

## 8.6 用户自定义异常

异常应该从Exception类派生

## 8.7 定义清理操作

finally子句

## 8.8 预定义的清理操作

## 8.9 引发和处理多个不相关的异常

内置的 [`ExceptionGroup`](https://docs.python.org/zh-cn/3/library/exceptions.html#ExceptionGroup) 打包了一个异常实例的列表，这样它们就可以一起被引发。它本身就是一个异常，所以它可以像其他异常一样被捕获

## 8.10 用注释细化异常情况

# 9. 类

## 9.1 名称和对象

## 9.2 python作用域和命名空间

*namespace* （命名空间）是从名称到对象的映射

点号之后的名称是 **属性**



作用域虽然是被静态确定的，但会被动态使用。执行期间的任何时刻，都会有 3 或 4 个“命名空间可直接访问”的嵌套作用域：

- 最内层作用域，包含局部名称，并首先在其中进行搜索
- 那些外层闭包函数的作用域，包含“非局部、非全局”的名称，从最靠内层的那个作用域开始，逐层向外搜索。
- 倒数第二层作用域，包含当前模块的全局名称
- 最外层（最后搜索）的作用域，是内置名称的命名空间

### 9.2.1 作用域和命名空间示例

## 9.3 初探类

### 9.3.1 类定义语法

### 9.3.2 Class对象

类对象支持两种操作：属性引用和实例化

### 9.3.3 实例对象

实例对象所能理解的唯一操作是属性引用。 有两种有效的属性名称：数据属性和方法。

### 9.3.4 方法对象

总而言之，方法的运作方式如下。 当一个实例的非数据属性被引用时，将搜索该实例所属的类。 如果名称表示一个属于函数对象的有效类属性，则指向实例对象和函数对象的引用将被打包为一个方法对象。 当传入一个参数列表调用该方法对象时，将基于实例对象和参数列表构造一个新的参数列表，并传入这个新参数列表调用相应的函数对象

### 9.3.5 类和实例变量

一般来说，实例变量用于每个实例的唯一数据，而类变量用于类的所有实例共享的属性和方法

## 9.4 补充说明

## 9.5 继承

Python有两个内置函数可被用于继承机制：

- 使用 [`isinstance()`](https://docs.python.org/zh-cn/3/library/functions.html#isinstance) 来检查一个实例的类型: `isinstance(obj, int)` 仅会在 `obj.__class__` 为 [`int`](https://docs.python.org/zh-cn/3/library/functions.html#int) 或某个派生自 [`int`](https://docs.python.org/zh-cn/3/library/functions.html#int) 的类时为 `True`。
- 使用 [`issubclass()`](https://docs.python.org/zh-cn/3/library/functions.html#issubclass) 来检查类的继承关系: `issubclass(bool, int)` 为 `True`，因为 [`bool`](https://docs.python.org/zh-cn/3/library/functions.html#bool) 是 [`int`](https://docs.python.org/zh-cn/3/library/functions.html#int) 的子类。 但是，`issubclass(float, int)` 为 `False`，因为 [`float`](https://docs.python.org/zh-cn/3/library/functions.html#float) 不是 [`int`](https://docs.python.org/zh-cn/3/library/functions.html#int) 的子类。

### 9.5.1 多重继承

python允许多继承，会自动调整顺序

## 9.6 私有变量

由于存在对于类私有成员的有效使用场景（例如避免名称与子类所定义的名称相冲突），因此存在对此种机制的有限支持，称为 *名称改写*。 任何形式为 `__spam` 的标识符（至少带有两个前缀下划线，至多一个后缀下划线）的文本将被替换为 `_classname__spam`，其中 `classname` 为去除了前缀下划线的当前类名称。 这种改写不考虑标识符的句法位置，只要它出现在类定义内部就会进行。

## 9.7 杂项说明

## 9.8 迭代器

[`for`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#for) 语句会在容器对象上调用 [`iter()`](https://docs.python.org/zh-cn/3/library/functions.html#iter)。 该函数返回一个定义了 [`__next__()`](https://docs.python.org/zh-cn/3/library/stdtypes.html#iterator.__next__) 方法的迭代器对象，此方法将逐一访问容器中的元素。 当元素用尽时，[`__next__()`](https://docs.python.org/zh-cn/3/library/stdtypes.html#iterator.__next__) 将引发 [`StopIteration`](https://docs.python.org/zh-cn/3/library/exceptions.html#StopIteration) 异常来通知终止 `for` 循环。 你可以使用 [`next()`](https://docs.python.org/zh-cn/3/library/functions.html#next) 内置函数来调用 [`__next__()`](https://docs.python.org/zh-cn/3/library/stdtypes.html#iterator.__next__) 方法

## 9.9 生成器

[生成器](https://docs.python.org/zh-cn/3/glossary.html#term-generator) 是一个用于创建迭代器的简单而强大的工具。 它们的写法类似于标准的函数，但当它们要返回数据时会使用 [`yield`](https://docs.python.org/zh-cn/3/reference/simple_stmts.html#yield) 语句。 每次在生成器上调用 [`next()`](https://docs.python.org/zh-cn/3/library/functions.html#next) 时，它会从上次离开的位置恢复执行（它会记住上次执行语句时的所有数据值）。 一个显示如何非常容易地创建生成器的示例如下:

```python
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]
```

## 9.10 生成器表达式

某些简单的生成器可以写成简洁的表达式代码，所用语法类似列表推导式，但外层为圆括号而非方括号。 这种表达式被设计用于生成器将立即被外层函数所使用的情况。 生成器表达式相比完整的生成器更紧凑但较不灵活，相比等效的列表推导式则更为节省内存。

```python

```

- 











- 
