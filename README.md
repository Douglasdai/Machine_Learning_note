## Machine_Learning_note
### 复现李宏毅深度学习2020作业，并且完成CQU机器学习作业，外加完成一些ML，或DL的任务
+  HW_1 不光有李宏毅的作业1，还有自己手动实现的线性回归和逻辑回归，外加使用torch模型进行训练
+  HW_7包含了 7-9的
+  DM 是数据挖掘，包含爬虫，爬取了ASOS 网站
+  DM_ex2 为数据可视化的一些操作 使用了 echart 库，并对数据进行逻辑回归，进行离职员工的预测
+  NLP 文件夹中包含了对[fake and true news](https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset) 数据集的分类任务
    + 带有bert 的文件需要在大显存的条件下运行，否则爆显存
    + bert 文件以复现kaggle的 代码，目前没有什么改动，主要任务为看懂 了解nlp的几种方法
    + 其他的可以正常运行
+  DL_train_all 该文件夹很杂乱，包含了很多内容
    +  BP 为 BP网络对电力预测 
    +  cat_dog_50 为使用了kaggle cat vsdog 数据集，对数据二分类，读取数据时截取为50*50的灰度图像
    +  cat_dog_128 则是读取数据时128*128 的灰度图像进行训练，CNN 的准确率在95% 左右
    +  DL_ex1 跑了一个mnist 的分类 使用cnn
    +  DM_liear_2 也是mnist 的分类，使用了逻辑回归 和cnn 等模型
    +  Dtree 是使用了 UCI-herbeman 数据集,使用决策树算法进行分类(ID3 ，C4.5 CART 算法)，并包含了预剪枝和后剪枝，但是有点问题
    +  ele_2016 对2016年电赛数模电力负荷数据进行电力预测，使用LSTM模型(kearas框架)，但是没跑出来
    +  ele_bp 同2016 也没跑出来
    +  ele_lstm 对power.csv 进行电力预测，成功运行，有可视化
    + PCA_Kmeans 手动实现PCA 降维，然后喂到K_means中去，进行聚类，使用数据集（iris,wine,digits）
    + sklearn_Dtree 使用了 sklearn中的决策树函数，并对所建的决策树进行可视化，直观看到决策树

+ Brain包含了对脑肿瘤的分类和分割代码，使用的数据集为[kaggle数据集(分类)](https://www.kaggle.com/datasets/navoneel/brain-mri-images-for-brain-tumor-detection/code)和[数据集2(用于分割)](https://www.kaggle.com/datasets/awsaf49/brats20-dataset-training-validation),目的：完成非限作业.
  
