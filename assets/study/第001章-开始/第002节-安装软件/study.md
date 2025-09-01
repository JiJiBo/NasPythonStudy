# VS Code的安装

- https://code.visualstudio.com/Download
- 本程序虽然自带写代码的组件，但是建议只在里面粘贴你写好的代码。
- 真正写代码，还得自己下个专业的软件。
- 我用的是pycharm，但是这个pycharm是付费的，太贵。破解又怕你们不会，而且不提倡破解。
- 所以，可以装一个另外一个流行的 **VS Code**。
- 点击上方链接，下载后，安装。
- visualstudio不是专门为 Python 开发的（他还支持好多语言。）。所以得配置一下。

# 安装步骤

## 一、下载

- 根据自己的系统和cpu架构，选择合适的版本
- ![img_1.png](./assets/01-02/img_1.png)

## 二、安装

- 双击下载好的安装包
  ![img.png](./assets/01-02/img.png)
- 选择同意
- 选择安装路径
  ![img_8.png](./assets/01-02/img_8.png)
  ![img_9.png](./assets/01-02/img_9.png)
- 下一步
  ![img_2.png](./assets/01-02/img_2.png)
- 再下一步
  ![img_3.png](./assets/01-02/img_3.png)
- 安装
  ![img_4.png](./assets/01-02/img_4.png)
- 完毕
  ![img_5.png](./assets/01-02/img_5.png)

# 语言设置

- 打开app
- 选择扩展，在扩展中搜索chinese中文语言包进行install安装
  ![img_10.png](./assets/01-02/img_10.png)
- 重启后，就是中文了
  ![img_11.png](./assets/01-02/img_11.png)

# 配置python解释器

- https://www.python.org/
- 在这里下载
  ![img_12.png](./assets/01-02/img_12.png)
- 打开安装包
  ![img_13.png](./assets/01-02/img_13.png)
- 直接一路安装就行了
  ![img_14.png](./assets/01-02/img_14.png)

# 配置python步骤

- 打开软件后，按照图上来，安装python插件
  ![img_6.png](./assets/01-02/img_6.png)
  ![img_7.png](./assets/01-02/img_7.png)
- 然后在硬盘里，准备一个文件夹，放你学习的代码。
  ![img_15.png](./assets/01-02/img_15.png)
- 用vscode打开
  ![img_16.png](./assets/01-02/img_16.png)
  ![img_17.png](./assets/01-02/img_17.png)
- 信任文件夹
  ![img_18.png](./assets/01-02/img_18.png)
- 新建一个空白文件
  ![img_19.png](./assets/01-02/img_19.png)
- 大概这个位置，选择一个编译器
  ![img_20.png](./assets/01-02/img_20.png)
  ![img_21.png](./assets/01-02/img_21.png)
- 然后把这个代码写在空白文件里

```python
print("Hello, World!")
```

- 右击文件，在弹出的对话框，选择执行。
  ![img_22.png](./assets/01-02/img_22.png)
- 顺利的话，会打印出 **hello world**
  ![img_23.png](./assets/01-02/img_23.png)

# 什么是hello world？

“Hello World”其实是程序设计领域的一个经典入门示例。它的核心目的非常简单：教你如何让计算机执行一条最基础的输出操作——在屏幕上显示文字
`"Hello, World!"`。

**背景和意义**：

1. **入门示例**：几乎每种编程语言的第一个程序都是打印“Hello World”。它可以帮初学者熟悉编程语言的语法结构、编译/运行流程。
2. **测试环境**：程序员也用它来验证开发环境是否正确配置——如果连 Hello World 都跑不起来，说明环境有问题。
3. **象征意义**：它象征着“从零开始学编程”的第一步，就像你第一次让计算机“说话”。

**不同语言的示例**：

* **Python**：

```python
print("Hello, World!")
```

* **C语言**：

```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

* **Java**：

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

可以看到，不同语言虽然语法不同，但核心都是把 `"Hello, World!"` 输出到屏幕上。
 