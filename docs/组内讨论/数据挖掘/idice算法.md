​	iDice算法要解决问题是从一组多维度时序数据中选出effective combination（有效组合），这些组合可能是系统异常的原因。数据具有多个维度，每个维度又有多个取值，因此combination有很多种。iDice通过Impact based Pruning（用支持度作为阈值）、Change Detection based Pruning（使用GLR: Generalized Likelihood Ratio 算法）、Isolation Power based Pruning（使用作者提出的基于信息熵的Isolation Power指标最为阈值）连续三个剪枝步骤，缩减combination数量，最后对筛选出来的combination进行排名（采用一个与Fisher distance相似的分数进行排名：R=pa*ln(pa/pb)，其中p=VXt/Vt作为指标）得出有效组合。

​	数据输入示例如下

| 时间  | 维度1 | 维度2 | 维度3 |
| ----- | ----- | ----- | ----- |
| time1 | 取值i | 取值j | 取值k |





- [MSRA AIOps多维指标突变定位: iDice](https://mp.weixin.qq.com/s/JDFpNnW77TJ1HxNfRE6Kig)

- [广义似然比检验--j简略](https://wenku.baidu.com/view/398903c28bd63186bcebbc56.html)

- [假设检验-详细](https://wenku.baidu.com/view/d40583e0dcccda38376baf1ffc4ffe473368fdf6.html?rec_flag=default&sxts=1589432143527)

