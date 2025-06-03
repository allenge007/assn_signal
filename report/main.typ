#import "template.typ": *
#import "chapter1.typ" as ch1
#import "chapter2.typ" as ch2
#import "chapter3.typ" as ch3

#show: project.with(
  course: "信号与系统",
  lab_name: "探索实验",
  lab_name2: "环境声音分类",
  stu_name: "陈政宇、程嘉耀、甘善铭、陈淏泉",
  stu_num: "114514",
  major: "计算机科学与技术",
  department: "教学大楼-B202",
  date: (2025, 6, 3),
  show_content_figure: false,
  watermark: "",
)

= 摘要

环境声音分类作为音频信号处理领域的重要研究方向，在智能监控、环境感知和人机交互等应用中具有广泛的实用价值。本项目基于ESC-50开源环境声音数据集，构建了一个完整的环境声音自动分类系统。

系统采用短时傅立叶变换(STFT)对时域音频信号进行时频域转换，通过Mel滤波器组将线性频谱映射至符合人耳感知特性的Mel频率刻度，提取对数Mel频谱图作为音频特征表示。该特征提取方法充分利用了人类听觉系统的感知机制，在低频区域保持高分辨率，在高频区域适当降低分辨率，有效压缩了特征维度的同时保留了关键的音频信息。

在机器学习模型方面，本项目实现并对比了多种分类算法的性能表现，包括传统机器学习方法和深度学习模型。通过在ESC-50数据集上的实验验证，系统能够有效识别动物声音、自然声音、人为声音、室内外声音等50类环境声音，为环境声音的自动识别与分类提供了可行的技术方案。

本项目的主要贡献包括：

(1) 构建了完整的环境声音分类pipeline，从数据预处理到模型训练的全流程实现；

(2) 深入分析了STFT和Mel频谱变换的数学原理及其在音频特征提取中的应用；

(3) 系统性比较了不同分类算法在环境声音识别任务上的性能差异。

研究结果表明，基于Mel频谱特征的深度学习方法在环境声音分类任务中具有良好的分类精度和泛化能力。

*关键词：* 环境声音分类；短时傅立叶变换；Mel频谱；机器学习；ESC-50数据集

= 小组分工

#figure(
  table(
    columns: (0.6fr, 0.6fr, 2fr),
    align: center + horizon,
    stroke: 0.5pt,
    table.header(
      [*学号*], [*姓名*], [*主要负责内容*]
    ),
    [23336003], [陈政宇], [项目总体架构设计、论文撰写],
    [23330018], [程嘉耀], [模型构建及数学推导], 
    [23336005], [甘善铭], [数据集处理及分析], 
    [22335009], [陈淏泉], [机器学习模型训练与评估],
  ),
  caption: "小组成员分工情况"
)

#pagebreak()

#ch1
#ch2
#ch3

// ...existing code...

= 感想

*陈政宇（项目总体架构设计、论文撰写）：*

作为项目的总体架构设计者，这次环境声音分类实验让我深刻体会到了系统性思维的重要性。从最初的需求分析、技术选型到最终的系统实现，每一个环节都需要统筹考虑。

在架构设计过程中，我认识到模块化设计的价值。我们将整个系统分解为数据预处理、特征提取、模型训练和性能评估四个核心模块，每个模块都具有明确的输入输出接口，这不仅便于团队协作，也为后续的功能扩展奠定了基础。特别是在机器学习模块设计中，我们采用了可配置的参数化接口，使得不同机器学习模型可以快速验证和比较。

论文撰写过程中，我深深感受到技术表达的挑战性。如何将复杂的STFT变换和Mel滤波器组的数学原理用清晰易懂的语言表达出来，如何平衡技术深度与可读性，这些都需要反复斟酌。通过大量文献调研，我学会了如何构建完整的技术叙述框架，从理论基础到实验验证的逻辑链条必须环环相扣。

最让我印象深刻的是实验结果的意外性。最初我们预期ResNet会在深度特征提取方面表现最佳，但实验结果显示Siamese网络的综合表现更优。这提醒我在系统设计时不能过度依赖先验假设，必须通过充分的实验验证来指导决策。

这次项目也让我认识到跨学科知识的重要性。环境声音分类不仅涉及信号处理和机器学习，还需要了解人因工程等领域的知识。Mel频率刻度的设计就体现了人类听觉感知特性在技术实现中的应用，这种生物启发的工程设计思想值得深入学习。

*程嘉耀（模型构建及数学推导）：*

作为负责模型构建和数学推导的团队成员，这次实验让我对深度学习模型的设计原理有了更深层次的理解。

在数学建模过程中，我深刻体会到了理论与实践的差距。数学理论看似简洁，在实际实现时需要考虑窗函数选择、重叠率设置、零填充等众多工程细节。我学会了如何在数学严谨性和工程可行性之间找到平衡点。

模型架构设计是最具挑战性的部分。我理解了为什么这种架构能够学习到更具判别性的特征表示。相比传统的分类损失，对比损失直接优化特征空间中的距离度量，这为相似样本和不相似样本提供了更明确的优化目标。

在注意力机制的实现中，我对自注意力的数学机制有了全新认识。我理解了softmax归一化在保证权重概率分布特性中的作用。更重要的是，我学会了如何通过梯度分析来理解模型的学习动态，这对调试复杂网络架构非常有帮助。

残差连接的数学分析让我认识到网络深度与性能的非线性关系。我理解了残差连接如何缓解梯度消失问题，但在音频任务中，这种深度优势并不总是转化为性能提升，这提醒我模型设计必须考虑具体任务特性。

这次经历让我认识到数学建模不仅是工具，更是思维方式。通过严格的数学推导，我能够预测模型行为、分析失效模式、指导超参数调优，这种量化分析能力对于深度学习研究至关重要。

*甘善铭（数据集处理及分析）：*

作为数据集处理和分析的负责人，这次实验让我深刻认识到"数据为王"这一理念的重要性。

在ESC-50数据集分析过程中，我发现了许多有趣的现象。通过统计分析，我发现不同类别的音频长度分布存在显著差异，动物声音类别（如frog、crickets）普遍较短，而机械声音类别（如engine、airplane）相对较长。这种不平衡分布对模型训练产生了微妙影响，促使我们采用了时间规整和数据增强策略。

特征提取的工程实现充满了挑战。Mel滤波器组的构建看似简单，但在处理边界条件时需要格外小心。我深入研究了librosa库的实现细节，发现其在处理Nyquist频率附近的频点时采用了特殊的插值策略，这避免了频谱泄漏问题。这让我认识到工程实现的细节往往决定系统的最终性能。

数据预处理pipeline的设计让我学会了如何平衡效率与质量。最初我们采用了在线实时特征提取，但发现训练速度过慢。后来改为离线批量预处理并缓存特征，训练效率提升了3倍以上。这个经历让我深刻理解了I/O瓶颈在深度学习训练中的重要性。

在数据增强策略的探索中，我尝试了时间拉伸、音调变换、背景噪声添加等多种方法。最有效的是SpecAugment技术——在频谱图上随机遮掩时间段和频率段。这种方法的成功让我认识到，针对具体数据模态设计的增强策略往往比通用方法更有效。

数据质量分析是最具启发性的部分。通过人工听取和频谱可视化，我发现ESC-50中存在一些标注错误和边界模糊的样本。例如，某些"rain"样本实际包含了明显的"wind"成分，这种标注噪声解释了为什么某些类别容易混淆。这让我深刻认识到数据质量比数据数量更重要，高质量的小数据集往往比低质量的大数据集更有价值。

这次经历让我从一个全新角度理解了机器学习：模型只能学到数据中包含的信息，数据的质量和表示方式直接决定了模型性能的上限。

*陈淏泉（机器学习模型训练与评估）：*

通过本次音频分类实验，我不仅加深了对深度学习模型在实际任务中应用的理解，也进一步掌握了从数据预处理、模型训练到评估和可视化的完整流程。在实验过程中，我对不同类型的神经网络架构（如 CNN、ResNet、Attention 和 Siamese 网络）在音频信号处理中的表现差异有了直观的认识。
尤其值得一提的是，在实验前我原以为较为复杂的模型（如 ResNet）一定会带来更好的效果，但实际结果显示，Siamese 网络在本任务中表现最为出色，这让我意识到模型选择应更贴合具体任务特点，而不仅仅依赖模型复杂度。同时，在模型训练过程中，参数设置（如学习率、batch size）、正则化策略（如 dropout）以及早停机制等，都对最终性能产生了显著影响，让我更加体会到训练策略的重要性。
此外，在评估阶段，通过混淆矩阵、分类报告以及可视化工具对模型表现进行了深入分析，这些过程锻炼了我对模型“诊断”的能力，也让我意识到在准确率之外，精确率、召回率和 F1 分数等指标在衡量模型综合性能方面的重要性。
总的来说，这次实验不仅提升了我的编程能力和模型调试技巧，也让我在实际操作中体会到了理论与实践的结合。未来我希望能继续探索更复杂的音频理解任务，如事件检测、语音识别等，并尝试更多创新型网络结构与优化策略。

= 参考文献

#bibliography(title: none, "ref.bib", style: "ieee")

// [1] Piczak, K. J. (2015). ESC: Dataset for environmental sound classification. In Proceedings of the 23rd ACM international conference on Multimedia (pp. 1015-1018).
// *应用位置：* 第2章数据集介绍，ESC-50数据集的基本信息和类别分布

// [2] McFee, B., Raffel, C., Liang, D., Ellis, D. P., McVicar, M., Battenberg, E., & Nieto, O. (2015). librosa: Audio and music signal analysis in python. In Proceedings of the 14th python in science conference (Vol. 8, pp. 18-25).
// *应用位置：* 第1章数学模型，第2章数据预处理流程，STFT和Mel频谱特征提取的实现

// [3] Allen, J. B., & Rabiner, L. R. (1977). A unified approach to short-time Fourier analysis and synthesis. Proceedings of the IEEE, 65(11), 1558-1564.
// *应用位置：* 第1章STFT数学模型，短时傅立叶变换的理论基础和数学表达式

// [4] Stevens, S. S., Volkmann, J., & Newman, E. B. (1937). A scale for the measurement of the psychological magnitude pitch. The journal of the acoustical society of america, 8(3), 185-190.
// *应用位置：* 第1章Mel频率变换，Mel刻度的心理声学理论基础

// [5] Davis, S., & Mermelstein, P. (1980). Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences. IEEE transactions on acoustics, speech, and signal processing, 28(4), 357-366.
// *应用位置：* 第1章Mel滤波器组设计，Mel频谱计算方法

// [6] Harris, F. J. (1978). On the use of windows for harmonic analysis with the discrete Fourier transform. Proceedings of the IEEE, 66(1), 51-83.
// *应用位置：* 第1章窗函数设计，汉宁窗的频谱泄漏特性分析

// [7] LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436-444.
// *应用位置：* 第1章CNN模型，深度学习在音频分类中的应用

// [8] Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning. MIT press.
// *应用位置：* 第1章卷积神经网络架构，激活函数和池化操作的理论基础

// [9] Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980.
// *应用位置：* 第1章优化算法，Adam优化器的数学原理和参数更新公式

// [10] Salamon, J., & Bello, J. P. (2017). Deep convolutional neural networks and data augmentation for environmental sound classification. IEEE Signal Processing Letters, 24(3), 279-283.
// *应用位置：* 第2章特征提取方法选择，环境声音分类中深度学习方法的有效性验证

// [11] Tokozume, Y., Ushiku, Y., & Harada, T. (2017). Learning from between-class examples for deep sound recognition. arXiv preprint arXiv:1711.10282.
// *应用位置：* 第2章数据处理方法，环境声音分类的数据增强技术

// [12] Barchiesi, D., Giannoulis, D., Stowell, D., & Plumbley, M. D. (2015). Acoustic scene classification: Classifying environments from the sounds they produce. IEEE Signal Processing Magazine, 32(3), 16-34.
// *应用位置：* 第2章声学特征分析标准，环境声音的分类体系和特征分析方法

// [13] Rabiner, L., & Schafer, R. (2010). Theory and applications of digital speech processing. Pearson.
// *应用位置：* 第1章音频信号预处理，数字信号处理的基础理论

// [14] Müller, M. (2015). Fundamentals of music processing: Audio, analysis, algorithms, applications. Springer.
// *应用位置：* 第1章STFT幅度谱计算，第2章时频分析方法

// [15] Virtanen, T., Plumbley, M. D., & Ellis, D. (2018). Computational analysis of sound scenes and events. Springer.
// *应用位置：* 第2章环境声音分类的整体框架，计算听觉场景分析理论

// [16] Piczak, K. J. (2015). Environmental sound classification with convolutional neural networks. In 2015 IEEE 25th International Workshop on Machine Learning for Signal Processing (MLSP) (pp. 1-6).
// *应用位置：* 第1章CNN模型设计，第2章Mel频谱特征在环境声音分类中的应用

// [17] Karol, J. P., Kumaran, G. C., & Raman, B. (2020). Environmental sound classification using convolutional neural networks. In 2020 International Conference on Communication and Signal Processing (ICCSP) (pp. 0665-0669).
// *应用位置：* 第2章实验设计和性能评估方法

// [18] Su, Y., Zhang, K., Wang, J., & Madani, K. (2019). Environment sound classification using a two-stream CNN based on decision-level fusion. Sensors, 19(7), 1733.
// *应用位置：* 第2章多特征融合方法，不同特征表示的对比分析