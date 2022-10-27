# My_Little_Project
一些很小的，用于练手的玩具项目。

## Pokemon

- 将整张页面爬下来，并汇总成csv格式

- 环境依赖：requests、pillow、openpyxl、bs4、pandas

- 下载源码可以发现，所有信息都存放在`id="pokedex"`的table中，稍微观察观察便可以找到各项信息所在的位置，处理之后便可以生成相应的csv和excel

- [博客地址](https://micro-han.github.io/2022/01/14/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E6%95%B0%E6%8D%AE%E5%BA%93%E7%88%AC%E8%99%AB/)

  [宝可梦数据库网站](https://pokemondb.net/pokedex/all)

## SearchPlanning

- 在别人写好的可视化迷宫框架里写一个自己的自动寻路Robot
- 分为单目标和多目标两种情况，单目标情况为一个出发点和一个终点，多目标情况为一个出发点和多个终点，需要依次到达且总步数尽可能短
- 代码文件结构：重点需要关注的是`Environment.java`，`Robot.java`，`Position.java`和`VisualizeSimulation.java`；其中`Position.java`为迷宫里点的类，`Environment.java`为迷宫环境类，`VisualizeSimulation.java`为可视化的程序。我们只需要修改`Robot.java`即可。
- 使用BFS和Astar来求解，单目标就不说了。对于多目标的情况：BFS每到达的第一个目标点，就以该点为新的起点继续进行BFS；Astar则是每次计算所有目标点到起点的评价函数值，选择最优的一个作为此轮的终点和下一轮的起点，重复即可。

## CatsVSDogs

- 猫狗识别，非常简单的入门级别项目，本项目采用torch框架开发入门
- 处理图像数据：Resize图像、读入图像标签 转换成tensor张量供训练
  模型：简单CNN网络，俩卷积层后面跟着三全连接层；简单的前向传播和二值化函数
  训练：甚至没有用gpu训练，常规的写法
- 总体感觉对于浅度学习有点登堂入室的感觉了
- [代码魔改自该链接](https://github.com/xbliuHNU/DogsVsCats)
