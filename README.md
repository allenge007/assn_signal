# 信号与系统实验集

本项目包含多个信号处理与探索实验，主要用于学习与实践信号相关的算法和编程实现。项目内容包括：

- **代码**：在 [code/](code/lab1.ipynb) 目录下给出了所有实验代码（ipynb 或 py 格式）。
- **参考资料**：在 [ref/](ref/) 中整理了一些参考资料。
- **综合实验报告**：在 [report/](report/) 目录下给出了实验报告。

## 环境配置

### 使用 conda 安装环境

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

### 相关依赖

- python >= 3.10
- jupyter
- matplotlib
- ipykernel
- numpy

## 项目结构

```
assn_signal
├── README.md
├── code
│   ├── example.ipynb
│   └── example.py
├── env.yml
├── ref
│   └── ref.md
├── report
│   ├── img
│   ├── lab1.typ
│   ├── lab2.typ
│   ├── lab3.typ
│   ├── lab4.typ
│   ├── main.typ
│   └── template.typ
└── task
    └── 综合-探索实验.pdf
```

## 其他

请根据项目的具体要求和后续更新完善本 README，确保能清晰传达项目目的与操作说明。