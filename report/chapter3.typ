#import "template.typ": *

= 模型训练评估

== 评估指标体系

为全面评估模型在环境声音分类任务中的性能，本研究采用多维度评估指标体系@powers2011evaluation，确保评估结果的客观性和全面性。

=== 分类性能指标

*准确率（Accuracy）：*
表示模型正确分类的样本占总样本的比例：

$ "Accuracy" = (T P + T N) / (T P + T N + F P + F N) $

其中 $T P$、$T N$、$F P$、$F N$ 分别表示真正例、真负例、假正例、假负例。

*精确率（Precision）：*
表示被模型判定为正类中实际为正类的比例：

$ "Precision" = T P / (T P + F P) $

*召回率（Recall）：*
表示实际为正类的样本中被模型正确识别的比例：

$ "Recall" = T P / (T P + F N) $

*F1分数（F1-Score）：*
精确率和召回率的调和平均数，综合反映模型性能：

$ "F1-Score" = 2 times ("Precision" times "Recall") / ("Precision" + "Recall") $

*宏平均F1分数：*
对于多分类问题，计算各类别F1分数的算术平均：

$ "Macro-F1" = 1/K sum_(i=1)^K "F1"_i $

其中 $K = 50$ 为类别总数。

=== 混淆矩阵分析

采用混淆矩阵可视化分类结果，矩阵元素 $C_(i,j)$ 表示真实类别为 $i$ 但被预测为类别 $j$ 的样本数量：

$ C_(i,j) = sum_(k=1)^N I(y_k^"true" = i "and" y_k^"pred" = j) $

其中 $I(·)$ 为指示函数，$N$ 为测试样本总数。

== 实验设置

=== 数据集划分

ESC-50数据集按照8:1:1的比例随机划分为训练集、验证集和测试集：

#figure(
  table(
    columns: (1fr, 1fr, 1fr, 1fr),
    align: center + horizon,
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*数据集*], [*样本数*], [*比例*], [*用途*]
    ),
    table.hline(stroke: 0.8pt),
    [训练集], [1600], [80%], [模型参数学习],
    [验证集], [200], [10%], [超参数调优],
    [测试集], [200], [10%], [最终性能评估],
    table.hline(stroke: 0.8pt),
  ),
  caption: "数据集划分详情"
)

=== 训练配置参数

设定统一的训练配置：

#figure(
  table(
    columns: (1fr, 1fr, 1fr),
    align: center + horizon,
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*参数名称*], [*数值*], [*说明*]
    ),
    table.hline(stroke: 0.8pt),
    [优化器], [Adam], [自适应学习率优化],
    [初始学习率], [0.001], [基于经验设定],
    [批次大小], [32], [平衡内存与梯度稳定性],
    [最大训练轮数], [200], [充分训练保证],
    [Dropout率], [0.5], [防止过拟合],
    [早停耐心值], [10], [连续10轮无改善则停止],
    [学习率衰减], [ReduceLROnPlateau], [验证损失停滞时衰减],
    table.hline(stroke: 0.8pt),
  ),
  caption: "模型训练超参数配置"
)

=== 正则化策略

为防止过拟合，采用多种正则化技术@srivastava2014dropout：

1. *Dropout正则化*：在全连接层前添加dropout层，随机丢弃50%的神经元连接
2. *批量归一化*：在卷积层后添加BatchNorm层，稳定训练过程
3. *早停机制*：监控验证集损失，防止过度训练
4. *权重衰减*：L2正则化系数设为 $10^(-4)$

== 训练过程分析

=== 损失函数收敛性

各模型在训练过程中的损失函数变化趋势如下：

#figure(
  grid(
    columns: 2,
    gutter: 1em,
    figure(
      image("./final-result/simple_cnn_training_history.png", width: 100%),
      caption: [Simple CNN训练曲线]
    ),
    figure(
      image("./final-result/resnet_training_history.png", width: 100%),
      caption: [ResNet训练曲线]
    ),
    figure(
      image("./final-result/attention_training_history.png", width: 100%),
      caption: [Attention模型训练曲线]
    ),
    figure(
      image("./final-result/siamese_training_history.png", width: 100%),
      caption: [Siamese网络训练曲线]
    )
  ),
  caption: "各模型训练过程损失与准确率变化"
)

=== 收敛特性分析

通过训练曲线分析，各模型呈现以下特征：

#figure(
  table(
    columns: (1fr, 1fr),
    align: center + horizon,
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*模型*], [*收敛轮数*]
    ),
    table.hline(stroke: 0.8pt),
    [Simple CNN], [45],
    [ResNet], [60],
    [Attention], [30],
    [Siamese], [40],
    table.hline(stroke: 0.8pt),
  ),
  caption: "各模型训练收敛特性对比"
)

== 性能评估结果

=== 整体性能对比

在测试集上的综合性能评估结果：

#figure(
  table(
    columns: (1fr, 1fr, 1fr, 1fr, 1fr),
    align: center + horizon,
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*模型*], [*Accuracy*], [*Precision*], [*Recall*], [*F1-Score*]
    ),
    table.hline(stroke: 0.8pt),
    [Simple CNN], [70.0%], [73.0%], [70.0%], [69.0%],
    [ResNet], [73.0%], [74.0%], [73.0%], [72.0%],
    [Attention], [74.0%], [77.0%], [74.0%], [73.0%],
    [*Siamese*], [*80.0%*], [*83.0%*], [*80.0%*], [*80.0%*],
    table.hline(stroke: 0.8pt),
  ),
  caption: "各模型在测试集上的性能指标对比"
)

#figure(
  image("./final-result/all_models_results.png", width: 80%),
  caption: [模型性能对比可视化图表]
)

== 模型复杂度分析

=== 计算复杂度对比

从理论计算复杂度和实际推理时间两个维度评估模型效率：

#figure(
  table(
    columns: (1fr, 1fr, 1fr),
    align: center + horizon,
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*模型*], [*参数量*], [*推理时间 (s/epoch)*]
    ),
    table.hline(stroke: 0.8pt),
    [Simple CNN], [0.41M], [1.10],
    [ResNet], [10.69M], [1.89],
    [Attention], [1.69M], [2.78],
    [Siamese], [1.62M], [1.68],
    table.hline(stroke: 0.8pt),
  ),
  caption: "各模型计算复杂度与资源消耗对比"
)

=== 效率-性能平衡分析

定义效率-性能比值来量化模型的综合优势：

$ "Efficiency-Performance Ratio" = "F1-Score" / ("Parameters(M)" times "Inference Time(s/epoch)") $

其中综合代价反映模型的整体计算成本，效率比值越高表示模型在单位计算成本下的性能表现越好。

#figure(
  table(
    columns: (1fr, 1fr, 1fr, 1fr),
    align: center + horizon,
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*模型*], [*F1-Score*], [*综合代价*], [*效率比*]
    ),
    table.hline(stroke: 0.8pt),
    [Simple CNN], [0.69], [0.451], [1.530],
    [ResNet], [0.72], [20.204], [0.036],
    [Attention], [0.73], [4.698], [0.155],
    [Siamese], [0.80], [2.722], [0.294],
    table.hline(stroke: 0.8pt),
  ),
  caption: "模型效率-性能综合评估"
)

=== 性能优势分析

通过实验结果分析，各模型表现出以下特点：

#grid(
  columns: (1fr, 1fr),
  gutter: 1.5em,
  
  // 左列
  [
    #box(
      fill: gray.lighten(90%),
      inset: 1em,
      radius: 6pt,
      stroke: 1pt + gray.darken(20%),
      width: 100%
    )[
      *#text(size: 12pt)[Siamese]*
      
      #set par(leading: 0.8em)
      #set text(size: 10pt)
      
      • *性能全面领先*：F1-Score达到0.80，在所有指标上均为最优
      
      • *共享权重机制*：有效提取可比较的特征表示，减少参数冗余
      
      • *对比学习策略*：增强特征判别能力，提升类间分离度
      
      • *效率平衡*：在高性能与合理计算成本间取得最佳平衡（效率比0.294）
    ]
    
    #v(1em)
    
    #box(
      fill: gray.lighten(95%),
      inset: 1em,
      radius: 6pt,
      stroke: 1pt + gray.darken(10%),
      width: 100%
    )[
      *#text(size: 12pt)[ResNet]*
      
      #set par(leading: 0.8em)
      #set text(size: 10pt)
      
      • *梯度流优化*：残差连接有效解决深度网络梯度消失问题
      
      • *性能中等*：F1-Score为0.72，相比Simple CNN有改善
      
      • *计算开销高*：参数量达10.69M，综合代价最高（20.204）
      
      • *效率比最低*：仅为0.036，性价比不佳
    ]
  ],
  
  // 右列  
  [
    #box(
      fill: gray.lighten(93%),
      inset: 1em,
      radius: 6pt,
      stroke: 1pt + gray.darken(15%),
      width: 100%
    )[
      *#text(size: 12pt)[Attention]*
      
      #set par(leading: 0.8em)
      #set text(size: 10pt)
      
      • *精确率突出*：在精确率指标上表现优异（77%），F1-Score为0.73
      
      • *自适应权重*：智能关注关键频谱区域，突出重要特征
      
      • *模型解释性*：可视化注意力权重，增强可解释性
      
      • *推理效率*：推理时间较长（2.78s/epoch），影响实际部署
    ]
    
    #v(1em)
    
    #box(
      fill: white,
      inset: 1em,
      radius: 6pt,
      stroke: 1.5pt + gray.darken(30%),
      width: 100%
    )[
      *#text(size: 12pt)[Simple CNN]*
      
      #set par(leading: 0.8em)
      #set text(size: 10pt)
      
      • *效率最优*：效率比高达1.530，计算成本最低
      
      • *结构简洁*：参数量仅0.41M，推理时间1.10s/epoch
      
      • *性能基础*：F1-Score为0.69，提供性能下界参考
      
      • *实用价值*：在极度资源受限环境下仍具备应用价值
    ]
  ]
)

#v(1.5em)

#figure(
  table(
    columns: (1.2fr, 1fr, 1fr, 1fr, 1fr),
    align: center + horizon,
    stroke: none,
    fill: (_, y) => if calc.odd(y) { gray.lighten(95%) } else { white },
    table.hline(stroke: 2pt + black),
    table.header(
      text(weight: "bold")[*模型*], 
      text(weight: "bold")[*性能等级*], 
      text(weight: "bold")[*效率等级*], 
      text(weight: "bold")[*参数规模*], 
      text(weight: "bold")[*综合评价*]
    ),
    table.hline(stroke: 1pt + gray.darken(30%)),
    
    [Siamese], 
    [优秀 (0.80)], 
    [良好 (0.294)], 
    [中等 (1.62M)], 
    [最佳平衡],
    
    [Attention], 
    [良好 (0.73)], 
    [中等 (0.155)], 
    [中等 (1.69M)], 
    [可解释性强],
    
    [Simple CNN], 
    [基础 (0.69)], 
    [优秀 (1.530)], 
    [极小 (0.41M)], 
    [资源友好],
    
    [ResNet], 
    [中等 (0.72)], 
    [较低 (0.036)], 
    [大型 (10.69M)], 
    [计算密集],
    
    table.hline(stroke: 1pt + gray.darken(30%)),
  ),
  caption: "各模型综合特征对比矩阵"
)

=== 误分类分析

通过混淆矩阵分析，我们对各模型的分类错误模式进行了深入研究。混淆矩阵能够直观显示模型在各类别上的分类准确性以及易混淆的类别组合。

#figure(
  grid(
    columns: 2,
    gutter: 1em,
    figure(
      image("./06-03_14-38/simple_cnn_confusion_matrix.png", width: 100%),
      caption: [Simple CNN混淆矩阵]
    ),
    figure(
      image("./06-03_14-38/resnet_confusion_matrix.png", width: 100%),
      caption: [ResNet混淆矩阵]
    ),
    figure(
      image("./06-03_14-38/attention_confusion_matrix.png", width: 100%),
      caption: [Attention模型混淆矩阵]
    ),
    figure(
      image("./06-03_14-38/siamese_confusion_matrix.png", width: 100%),
      caption: [Siamese网络混淆矩阵]
    )
  ),
  caption: "各模型混淆矩阵对比分析"
)

=== 改进方向

基于实验结果，提出以下优化建议：
\
*数据层面改进：*
- 采用SpecAugment等音频数据增强技术
- 引入多尺度时频表示融合
- 收集更高质量的训练样本
- 平衡各类别的样本分布

*模型架构改进：*
- 探索Transformer架构在音频分类中的应用
- 设计多模态融合的网络结构
- 引入对抗训练提升模型鲁棒性
- 优化注意力机制的计算效率

*训练策略改进：*
- 采用课程学习策略渐进训练
- 引入知识蒸馏技术压缩模型
- 使用集成学习融合多个模型
- 设计更适合音频任务的损失函数

== 本章小结

本章通过系统的实验设计和全面的性能评估，对四种环境声音分类模型进行了深入分析。实验结果表明：

(1) *Siamese网络表现最优*：在准确率（80%）、F1分数（80%）等指标上均领先其他模型，验证了对比学习在音频特征提取中的有效性。

(2) *Attention机制具有潜力*：在精确率方面表现突出，证明了注意力机制在音频关键区域定位中的价值。

(3) *模型复杂度与性能平衡*：Siamese网络在保持较高性能的同时，具有相对较低的计算复杂度。

这些结果为环境声音分类模型的选择和优化提供了重要的实验依据和理论指导。