#import "template.typ": *
#import "lab1.typ"
#import "lab2.typ"
#import "lab3.typ"
#import "lab4.typ"

#show: project.with(
  course: "计算机网络",
  lab_name: "TCP/IP实验",
  lab_name2: "实现TCP/IP协议栈",
  stu_name: "丁真",
  stu_num: "114514",
  major: "土木工程",
  department: "火星土木学院",
  date: (2077, 1, 1),
  show_content_figure: false,
  watermark: "SYSU",
)

= 测试

== 数学公式测试

#mitex(`
  \sum_{i=1}^{n} i = \frac{n(n+1)}{2}
`)

#lab1
#lab2
#lab3
#lab4

= 参考文献