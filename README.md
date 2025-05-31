# 环境声音分类系统

一个模块化的环境声音分类系统，使用ESC-50数据集，采用STFT特征和CNN模型（包括ResNet、孪生网络和注意力机制）。

## 功能特点

- **多种模型架构**：ResNet、孪生网络、注意力机制和基础CNN
- **高级音频处理**：STFT和梅尔频谱特征提取
- **模块化设计**：数据处理、模型训练和评估模块分离
- **全面评估**：训练曲线、混淆矩阵和性能对比
- **可复现结果**：随机种子管理和配置系统

## 环境配置

### 方案1：使用Conda（推荐）

```bash
# 创建conda环境
conda env create -f environment.yml

# 激活环境
conda activate esc50_classification
```

### 方案2：使用pip和virtualenv

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 方案3：直接使用pip

```bash
# 直接安装依赖
pip install -r requirements.txt
```

## 系统要求

- **Python版本**：3.8-3.10（推荐3.9）
- **内存**：至少8GB（推荐16GB）
- **存储空间**：约2GB用于ESC-50数据集
- **GPU**：非必需但推荐用于加速训练

### 额外系统依赖

#### 音频处理(ffmpeg)：

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
从https://ffmpeg.org/download.html下载

## 快速开始

1. **配置环境**（见上文）

2. **运行系统:**
```bash
# 自动下载数据集并训练所有模型
python -m code.main --model_type all --download_dataset

# 训练特定模型
python -m code.main --model_type resnet --feature_type mel

# 自定义训练参数
python -m code.main --model_type attention --epochs 50 --batch_size 64 --learning_rate 0.0005
```

3. **可用模型类型:**
   - `resnet`: 基于ResNet的架构
   - `attention`: 带自注意力机制的CNN
   - `siamese`: 孪生网络
   - `simple_cnn`: 基准CNN模型
   - `all`: 训练并比较所有模型

## 项目结构

```
assn_signal/
├── code/
│   ├── __init__.py          # 包初始化
│   ├── config.py            # 配置管理
│   ├── data_processing.py   # ESC-50数据加载和预处理
│   ├── models.py            # 模型架构
│   ├── training.py          # 训练和评估流程
│   ├── utils.py             # 工具函数
│   └── main.py              # 主执行脚本
├── data/                    # 数据集存储（自动创建）
├── models/                  # 保存的模型（自动创建）
├── results/                 # 实验结果（自动创建）
├── plots/                   # 生成的图表（自动创建）
├── requirements.txt         # Python依赖
├── environment.yml          # Conda环境
└── README.md               # 本文件
```

## 使用示例

### 基础用法
```python
from code.data_processing import ESC50DataProcessor
from code.training import ModelTrainer

# 处理数据
processor = ESC50DataProcessor()
features, labels, class_names = processor.prepare_dataset()

# 训练模型
trainer = ModelTrainer(model_type="resnet")
trainer.prepare_model(num_classes=50)
# ... 训练代码
```

### 配置修改
```python
from code.config import config

# 修改配置
config.training.epochs = 100
config.training.batch_size = 64
config.data.sample_rate = 22050
```

## 结果输出

系统将生成：
- 训练/验证曲线
- 混淆矩阵
- 性能对比图表
- 模型评估报告
- 保存的训练模型

## 故障排除

### 常见问题

1. **音频加载错误**：确保ffmpeg正确安装
2. **内存不足**：减小配置中的batch_size或使用更大内存的机器
3. **未检测到GPU**：安装tensorflow-gpu或确保CUDA配置正确
4. **数据集下载失败**：检查网络连接或手动下载ESC-50

### 性能优化建议

- 使用GPU加速训练
- 如有足够内存可增大batch_size
- 使用梅尔频谱加速处理
- 对大模型启用混合精度训练

## 引用

如果在研究中使用本代码，请引用ESC-50数据集：

```
Piczak, K. J. (2015). ESC: Dataset for Environmental Sound Classification. 
Proceedings of the 23rd ACM international conference on Multimedia (pp. 1015-1018).
```