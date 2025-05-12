# 信号与系统实验集

本项目包含多个信号处理与探索实验，主要用于学习与实践信号相关的算法和编程实现。项目内容包括：

- **代码**：在 [code/](code/) 目录下给出了所有实验代码（ipynb 或 py 格式）。
- **参考资料**：在 [ref/](references/) 中整理了一些参考资料。
- **综合实验报告**：在 [report/](report/) 目录下给出了实验报告。

## 项目结构

<!-- readme-tree start -->
<!-- readme-tree end -->

## 环境配置

### 使用 conda 安装环境

1. 使用 env.yml 中指定的依赖创建环境：
    ```sh
    conda env create -f env.yml
    ```

2. 激活新创建的环境：
    ```sh
    conda activate
    ```
    
3. 在新环境中安装 IPython 内核，以便在 Jupyter Notebook 中使用该环境： 

    ```sh
    python -m ipykernel install --user --name signal_system
    ```

4. 示例是一个 Jupyter Notebook。完成上述步骤后，你可以通过以下命令启动：
    ```sh
    jupyter notebook example.ipynb
    ```
    
5. 为确保使用正确的环境，请在 example.ipynb 的工具栏中点击 Kernel -> Change kernel，在下拉菜单中选择 signal_system。

6. 若要停用当前环境，请使用：
    ```sh
    conda deactivate
    ```

### 相关依赖

- python >= 3.10
- jupyter
- matplotlib
- ipykernel
- numpy

## 其他

请根据项目的具体要求和后续更新完善本 README，确保能清晰传达项目目的与操作说明。

allenge007: 这是什么 markdown 语法

GitHub Copilot: 这是一种扩展的 Markdown 语法，通常被称为 *admonition*（警示框）语法。在像 MkDocs 或 MkDocs Material 这样的文档工具中，它常用于创建提示、警告等信息框。

具体来说，`!!! tip` 用于创建一个“提示”类型的信息框，可以帮助突出显示相关内容。

allenge007: 帮我根据文件内容生成一篇 README

GitHub Copilot: 下面是一份示例 README 内容，你可以根据需要进行调整：

````markdown
# 信号实验集

本项目包含多个信号处理与探索实验，主要用于学习与实践信号相关的算法和编程实现。项目内容包括：

- **代码**：在 [code/lab1.ipynb](code/lab1.ipynb) 中有一个示例 Lab，用于展示基础的 Python 编程（例如打印 "hello, world"）。
- **参考资料**：在 [ref/ref_lab3.md](ref/ref_lab3.md) 中整理了一些参考资料和学习笔记。
- **综合实验报告**：项目中还包含综合探索实验的 PDF 文档（文件名：综合-探索实验.pdf），详细描述了实验过程和结果。

## 运行方法

1. 打开 Jupyter Notebook 或 VS Code 中的 Jupyter 插件，运行 `lab1.ipynb` 以体验实验示例。
2. 查看参考资料和实验报告获取更多背景信息。

## 环境要求

- Python 3.x
- 相关信号处理库（如 NumPy、SciPy 等，根据后续实验需要安装）

## 项目结构

```
assn_signal/
├── code/
│   └── lab1.ipynb
├── ref/
│   └── ref_lab3.md
└── 综合-探索实验.pdf
```

## 其他

请根据项目的具体要求和后续更新完善本 README，确保能清晰传达项目目的与操作说明。
````

allenge007: 什么命令可以打印出当前目录下结构

GitHub Copilot: 你可以使用 `tree .` 命令打印当前目录下的目录结构。如果提示命令不存在，可以通过 Homebrew 安装：

````bash
brew install tree
````

安装后，再运行 `tree .` 即可查看结构。

allenge007: 将该实验可能需要用到的依赖用 env.yml 的形式写出来

GitHub Copilot: 下面提供一个示例的 env.yml 文件，该文件列举了在“综合-探索实验”中可能用到的一些常见依赖包（如数值计算、数据处理、绘图以及机器学习相关的包）。请根据具体实验内容和需求进行适当调整。

-----------------------------------------------------------
# 示例 env.yml 文件

name: 综合探索实验环境
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.8           # 可根据需求调整 Python 版本
  - numpy                # 数值计算库
  - scipy                # 科学计算和工程算法
  - pandas               # 数据处理与分析
  - matplotlib           # 绘图库
  - seaborn              # 数据可视化
  - scikit-learn         # 机器学习工具包
  - jupyterlab           # 交互式开发环境
  - ipykernel            # Jupyter 内核支持
  # 如有特殊需求，还可添加如下 pip 包
  - pip
  - pip:
      - requests         # 网络请求库（示例）
      - pyyaml           # YAML 文件处理

-----------------------------------------------------------

说明：
1. 环境名称（name）可以根据喜好修改。
2. 渠道（channels）里除了 defaults，也增加了 conda-forge 以便获取更多最新版本的软件包。
3. 如果实验中涉及其他特定需求（例如数据爬取、深度学习、可视化工具等），可在 dependencies 部分添加相应的软件包。

将该文件保存为 env.yml 后，可通过以下 conda 命令创建环境：
  conda env create -f env.yml

这样就能确保实验过程中用到的依赖一致性。

allenge007: !!!
    1. Create an environment with dependencies specified in env.yml:
        ```sh
        conda env create -f env.yml
        ```

    1. Activate the new environment:
        ```sh
        conda activate
        ```
        
    2. Inside the new environment, install IPython kernel so we can use this environment in jupyter notebook: 
    
        ```sh
        python -m ipykernel install --user --name signal_system
        ```

    3. Example is a Jupyter Notebook. With the above done you should be able to get underway by typing:
        ```sh
        jupyter notebook example.ipynb
        ```
        
    5. To make sure we are using the right environment, go to the toolbar of example.ipynb, click on Kernel -> Change kernel, you should see and select signal_system in the drop-down menu.

    6. To deactivate an active environment, use
        ```sh
        conda deactivate
        ```翻译为中文，格式不要变

GitHub Copilot: ````markdown
!!!
    1. 使用 env.yml 中指定的依赖创建环境：
        ```sh
        conda env create -f env.yml
        ```

    1. 激活新创建的环境：
        ```sh
        conda activate
        ```
        
    2. 在新环境中安装 IPython 内核，以便在 Jupyter Notebook 中使用该环境： 
    
        ```sh
        python -m ipykernel install --user --name signal_system
        ```

    3. 示例是一个 Jupyter Notebook。完成上述步骤后，你可以通过以下命令启动：
        ```sh
        jupyter notebook example.ipynb
        ```
        
    5. 为确保使用正确的环境，请在 example.ipynb 的工具栏中点击 Kernel -> Change kernel，在下拉菜单中选择 signal_system。

    6. 若要停用当前环境，请使用：
        ```sh
        conda deactivate
        ```