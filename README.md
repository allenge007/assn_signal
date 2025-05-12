# 信号与系统实验集

本项目包含多个信号处理与探索实验，主要用于学习与实践信号相关的算法和编程实现。项目内容包括：

- **代码**：在 [code/](code/) 目录下给出了所有实验代码（ipynb 或 py 格式）。
- **参考资料**：在 [ref/](references/) 中整理了一些参考资料。
- **综合实验报告**：在 [report/](report/) 目录下给出了实验报告。

## 项目结构

```
.
├── .github
│   └── workflows
│       └── readme_tree.yml
├── README.md
├── code
│   ├── example.ipynb
│   └── example.py
├── env.yml
├── references
│   └── ref.md
├── report
│   ├── lab1.typ
│   ├── lab2.typ
│   ├── lab3.typ
│   ├── lab4.typ
│   ├── logo
│   │   ├── demo.png
│   │   ├── demo.svg
│   │   ├── sysu-logo.png
│   │   ├── sysu-logo.svg
│   │   └── sysu-logo2.pdf
│   ├── main.typ
│   └── template.typ
└── task
    └── 综合-探索实验.pdf
 
8 directories, 19 files
```

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