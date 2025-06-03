#import "template.typ": *

= 数学模型

== 音频信号预处理

为保证后续实验的一致性和可比性，需要对原始音频信号进行预处理。既符合机器学习模型的输入要求，又能保证数值的稳定性。

=== 信号采样与标准化

设原始音频信号为连续时间信号 $x(t)$，经过采样频率 $f_s = 22050$ Hz 的均匀采样后得到离散时间信号：

$ x[n] = x(n T_s), quad n = 0, 1, 2, ... $

其中 $T_s = 1/f_s$ 为采样周期。

为确保输入信号长度一致性，对音频信号进行固定长度截取或零填充@mcfee2015librosa：

$ x_"norm"[n] = cases(
  x[n] & "if" space n < L,
  0 & "if" space n >= L "and" |x| < L,
  x[n] & "if" space n < L "and" |x| >= L
) $

其中 $L = f_s times T_"dur" = 22050 times 5 = 110250$ 为目标信号长度，$T_"dur" = 5$s 为音频时长。

== 短时傅立叶变换 (STFT)

短时傅里叶变换（STFT）是经典的时频分析方法@allen1977unified。考虑到直接对音频信号进行傅立叶变换处理会丢失音频信号在时域上的信息，而时域信息对于分辨一个声音而言也是十分重要的，因此我们采用短时傅立叶变换（STFT）对音频信号进行时频域转换，同时提取声音信号在时域和频域上的特征。

STFT 流程为：对长信号分帧、加窗（见下文），再对每一帧做傅里叶变换（FFT），最后将每一帧的频谱结果沿时间轴堆叠，得到二维的时频谱图。STFT的每一步都依赖于前面的加窗操作。

=== STFT 数学模型

短时傅立叶变换通过滑动窗口对信号进行局部频谱分析@allen1977unified，其数学表达式为：

$ X(m, k) = sum_(n=0)^(N-1) x[n + m H] dot w[n] dot e^(-j 2 pi k n / N) $

其中：
- $m$ 为时间帧索引
- $k$ 为频率bin索引，$k = 0, 1, ..., N/2$  
- $H$ 为帧移（hop length），取值 $H = 512$
- $N$ 为FFT窗口长度，取值 $N = 2048$
- $w[n]$ 为窗函数

=== 窗函数设计

本系统采用汉宁窗（Hann Window）进行加窗处理@harris1978windows：

$ w[n] = 0.5 (1 - cos((2 pi n)/(N-1))), quad n = 0, 1, ..., N-1 $

汉宁窗具有良好的频谱泄漏抑制特性，其主瓣宽度为 $4 pi / N$，旁瓣峰值约为-31.5 dB。

#figure(
  image("./fig/hann.png", width: 100%),
  caption: [hann 函数示意图]
)

=== 幅度谱计算

STFT结果为复数矩阵，计算其幅度谱：

$ |X(m, k)| = sqrt("Re"^2[X(m, k)] + "Im"^2[X(m, k)]) $

对数功率谱密度：

$ S_"dB"(m, k) = 20 log_10 ((|X(m, k)|) / (|X|_"max")) $

其中 $|X|_"max"$ 为幅度谱的最大值，用于归一化。

== Mel 频率变换

梅尔频谱是基于STFT得到的频谱，通过Mel滤波器组将频谱能量映射到Mel尺度上，模拟人耳听觉特性@stevens1937scale。本项目目标是对环境声音进行分类识别，以便将来进一步对环境噪声进行分析和处理，因此对于环境噪声的识别应当符合人类对声音的感知。传统的线性频谱不能很好地反映人耳对声音的主观感知，Mel频谱则通过非线性变换（见下文）更贴合听觉系统。具体优势分析可见数据处理章节。

Mel 频谱的计算流程为：将 STFT 处理后的信号通过Mel滤波器组和能量积分得到Mel谱图。

=== Mel 刻度转换

Mel刻度基于人耳听觉感知特性@stevens1937scale，其与线性频率的转换关系为：

$ m = 2595 log_10 (1 + f/700) $

$ f = 700 (10^(m/2595) - 1) $

其中 $m$ 为Mel频率，$f$ 为线性频率（Hz）。

=== Mel 滤波器组设计

Mel滤波器组由 $M = 128$ 个三角形带通滤波器组成@davis1980comparison，第 $i$ 个滤波器的频率响应为：

$ H_i(k) = cases(
  0 & "if" space f[k] < f[i-1],
  (f[k] - f[i-1])/(f[i] - f[i-1]) & "if" space f[i-1] <= f[k] <= f[i],
  (f[i+1] - f[k])/(f[i+1] - f[i]) & "if" space f[i] <= f[k] <= f[i+1],
  0 & "if" space f[k] > f[i+1]
) $

其中 $f[k] = k dot f_s / N$ 为第 $k$ 个频率bin对应的频率，$f[i]$ 为第 $i$ 个滤波器的中心频率。

=== Mel 频谱计算

Mel频谱通过滤波器组与STFT功率谱的卷积得到@davis1980comparison：

$ M(m, i) = sum_(k=0)^(N/2) H_i(k) dot |X(m, k)|^2 $

对数Mel频谱：

$ M_"dB"(m, i) = 10 log_10 (M(m, i) / M_"max") $

#figure(
  image("./fig/mel.png", width: 100%),
  caption: [Mel 滤波器组示意图]
)

== 机器学习模型

为了得到更好的分类效果，我们采用了几种经典的机器学习模型进行训练。以下是每种模型的数学原理和实现细节。

=== 卷积神经网络 (CNN) 模型

采用深度卷积神经网络进行特征学习和分类@lecun2015deep@piczak2015environmental，网络结构如下：

*输入层：* 
$ bold(X)_"input" in RR^(B times H times W times C) $

其中 $B$ 为批次大小，$H = 128$（Mel频道数），$W = 216$（时间帧数），$C = 1$（通道数）。

*卷积层：*
第 $l$ 层卷积操作@goodfellow2016deep：

$ bold(Y)^((l)) = sigma(bold(W)^((l)) * bold(X)^((l-1)) + bold(b)^((l))) $

其中 $*$ 表示卷积操作，$sigma$ 为ReLU激活函数：

$ sigma(x) = max(0, x) $

*池化层：*
最大池化操作@goodfellow2016deep：

$ y_(i,j)^((l)) = max_(p,q in P_(i,j)) x_(p,q)^((l-1)) $

其中 $P_(i,j)$ 为池化窗口区域。

*全连接层：*
$ bold(z)^((l)) = sigma(bold(W)^((l)) bold(x)^((l-1)) + bold(b)^((l))) $

*输出层：*
采用Softmax函数进行多分类：

$ p_i = (e^(z_i))/(sum_(j=1)^K e^(z_j)) $

其中 $K = 50$ 为类别总数。

// *网络架构：*
// - 卷积层1：32个 $3 times 3$ 卷积核，步长1，ReLU激活
// - 批量归一化 + $2 times 2$ 最大池化
// - 卷积层2：64个 $3 times 3$ 卷积核，步长1，ReLU激活  
// - 批量归一化 + $2 times 2$ 最大池化
// - 卷积层3：128个 $3 times 3$ 卷积核，步长1，ReLU激活
// - 批量归一化 + $2 times 2$ 最大池化
// - 卷积层4：256个 $3 times 3$ 卷积核，步长1，ReLU激活
// - 批量归一化 + 全局平均池化
// - Dropout层（丢弃率0.5）
// - 全连接层：128个神经元，ReLU激活
// - Dropout层（丢弃率0.5）
// - 输出层：50个神经元，Softmax激活

=== ResNet 残差网络模型

ResNet通过引入残差连接解决深度网络的梯度消失问题@he2016resnet，其核心思想是学习残差映射而非直接映射。

*残差块设计：*
残差块的数学表达式为：

$ bold(Y) = bold(F)(bold(X), {bold(W)_i}) + bold(X) $
$ bold(H) = sigma(bold(Y)) $

其中 $bold(F)(bold(X), {bold(W)_i})$ 为残差映射，$bold(X)$ 为恒等映射（跳跃连接）。

*残差映射：*
$ bold(F)(bold(X)) = bold(W)_2 sigma(bold(W)_1 bold(X) + bold(b)_1) + bold(b)_2 $

当输入输出维度不匹配时，采用 $1 times 1$ 卷积进行维度调整：

$ bold(Y) = bold(F)(bold(X)) + bold(W)_s bold(X) $

其中 $bold(W)_s$ 为 $1 times 1$ 卷积权重矩阵。

*批量归一化：*
$ hat(bold(x)) = gamma (bold(x) - mu) / sqrt(sigma^2 + epsilon) + beta $

其中 $mu$ 和 $sigma^2$ 分别为批次均值和方差，$gamma$ 和 $beta$ 为可学习参数。

// *网络架构：*
// - 初始卷积：64个 $7 times 7$ 卷积核，步长2
// - 批量归一化 + ReLU + $3 times 3$ 最大池化（步长2）
// - 残差块组1：2个残差块，64个特征图
// - 残差块组2：2个残差块，128个特征图，步长2
// - 残差块组3：2个残差块，256个特征图，步长2  
// - 残差块组4：2个残差块，512个特征图，步长2
// - 全局平均池化
// - Dropout层（丢弃率0.5）
// - 全连接层：50个神经元，Softmax激活

=== 注意力机制网络模型

注意力机制能够自适应地关注频谱图中的重要区域@vaswani2017attention，提升模型对关键特征的感知能力。

*自注意力机制：*
给定输入特征图 $bold(X) in RR^(H times W times D)$，首先将其重塑为序列形式 $bold(X)' in RR^(N times D)$，其中 $N = H times W$。

查询、键、值矩阵的计算：
$ bold(Q) = bold(X)' bold(W)^Q $
$ bold(K) = bold(X)' bold(W)^K $  
$ bold(V) = bold(X)' bold(W)^V $

其中 $bold(W)^Q, bold(W)^K, bold(W)^V in RR^(D times d_k)$ 为可学习的投影矩阵。

*注意力权重计算：*
$ "Attention"(bold(Q), bold(K), bold(V)) = "softmax"((bold(Q) bold(K)^T) / sqrt(d_k)) bold(V) $

注意力分数的计算：
$ alpha_(i,j) = (exp(bold(q)_i dot bold(k)_j / sqrt(d_k))) / (sum_(l=1)^N exp(bold(q)_i dot bold(k)_l / sqrt(d_k))) $

*输出特征：*
$ bold(o)_i = sum_(j=1)^N alpha_(i,j) bold(v)_j $

// *网络架构：*
// - 卷积层1：64个 $3 times 3$ 卷积核，步长1
// - 批量归一化 + ReLU + $2 times 2$ 最大池化
// - 卷积层2：128个 $3 times 3$ 卷积核，步长1
// - 批量归一化 + ReLU + $2 times 2$ 最大池化  
// - 卷积层3：256个 $3 times 3$ 卷积核，步长1
// - 批量归一化 + ReLU
// - 自注意力模块：256维特征注意力计算
// - 卷积层4：512个 $3 times 3$ 卷积核，步长1
// - 批量归一化 + ReLU + $2 times 2$ 最大池化
// - 全局平均池化
// - Dropout层（丢弃率0.5）
// - 全连接层：50个神经元，Softmax激活

=== 孪生网络模型

孪生网络通过共享权重的子网络学习输入的特征表示@koch2015siamese，能够有效提取可比较的特征向量。

*共享特征提取器：*
设计共享的特征提取网络 $f_theta(bold(x))$，其中 $theta$ 为共享参数：

$ bold(h) = f_theta(bold(x)) $

*特征提取网络结构：*
$ f_theta(bold(x)) = f_4(f_3(f_2(f_1(bold(x))))) $

其中每个 $f_i$ 代表一个卷积块：
$ f_i(bold(x)) = "MaxPool"("ReLU"("BatchNorm"("Conv"_i(bold(x))))) $

*特征相似度计算：*
对于两个输入 $bold(x)_1$ 和 $bold(x)_2$：

$ bold(h)_1 = f_theta(bold(x)_1) $
$ bold(h)_2 = f_theta(bold(x)_2) $

欧几里德距离：
$ d(bold(h)_1, bold(h)_2) = ||bold(h)_1 - bold(h)_2||_2 $

余弦相似度：
$ "sim"(bold(h)_1, bold(h)_2) = (bold(h)_1 dot bold(h)_2) / (||bold(h)_1||_2 ||bold(h)_2||_2) $

*分类头设计：*
$ bold(p) = "softmax"(bold(W)_"cls" bold(h) + bold(b)_"cls") $

// *网络架构：*
// - 共享特征提取器：
//   - 卷积层1：64个 $3 times 3$ 卷积核 + BatchNorm + ReLU + MaxPool
//   - 卷积层2：128个 $3 times 3$ 卷积核 + BatchNorm + ReLU + MaxPool  
//   - 卷积层3：256个 $3 times 3$ 卷积核 + BatchNorm + ReLU + MaxPool
//   - 卷积层4：512个 $3 times 3$ 卷积核 + BatchNorm + ReLU + 全局平均池化
//   - 全连接层：256个神经元，ReLU激活
//   - Dropout层（丢弃率0.5）
// - 分类头：全连接层，50个神经元，Softmax激活

// *对比学习损失：*
// $ L_"contrastive" = sum_(i,j) y_(i,j) d(bold(h)_i, bold(h)_j)^2 + (1-y_(i,j)) max(0, m - d(bold(h)_i, bold(h)_j))^2 $

// 其中 $y_(i,j) = 1$ 表示同类样本，$m$ 为边际参数。

=== 损失函数

采用交叉熵损失函数@goodfellow2016deep：

$ L = -sum_(i=1)^N sum_(j=1)^K y_(i,j) log(hat(y)_(i,j)) $

其中 $y_(i,j)$ 为真实标签的one-hot编码，$hat(y)_(i,j)$ 为模型预测概率。

=== 优化算法

采用Adam优化器进行参数更新@kingma2014adam：

$ m_t = beta_1 m_(t-1) + (1 - beta_1) g_t $
$ v_t = beta_2 v_(t-1) + (1 - beta_2) g_t^2 $
$ hat(m)_t = m_t / (1 - beta_1^t) $
$ hat(v)_t = v_t / (1 - beta_2^t) $
$ theta_t = theta_(t-1) - alpha dot hat(m)_t / (sqrt(hat(v)_t) + epsilon) $

其中 $alpha = 0.001$ 为学习率，$beta_1 = 0.9$，$beta_2 = 0.999$，$epsilon = 10^(-8)$。

=== 模型复杂度对比

#figure(
  table(
    columns: (1fr, 1fr, 1fr, 1fr),
    align: center + horizon,
    stroke: none,
    table.hline(stroke: 0.8pt),
    table.header(
      [*模型类型*], [*参数量*], [*计算复杂度*], [*特点*]
    ),
    table.hline(stroke: 0.8pt),
    [Simple CNN], [~0.41M], [O(N²)], [基础卷积结构，计算高效],
    [ResNet], [~10.69M], [O(N²)], [残差连接，解决梯度消失],
    [Attention], [~1.69M], [O(N²)], [自适应特征权重，关注重点区域],
    [Siamese], [~1.62M], [O(N²)], [共享权重，特征表示学习],
    table.hline(stroke: 0.8pt),
  ),
  caption: "不同模型的复杂度对比"
)