# 机器学习+深度学习+数据挖掘课程

- BP.ipynb 为手动实现单个神经元的bp神经网络（相当于一个线性回归）鸢尾花数据集
- BPnote.py 为BP jupyter的py文件版本
- cat_dog_50.ipynb 为使用CNN进行猫狗分类（CNN 为李宏毅老师助教中的HW3给出的示例CNN模型）图像输入为50x50
- cat_dog_128.ipynb 同cat_dog_50.ipynb，只是图像进行了随机旋转，翻转等图像增强，并且图像输入为128x128
- DL_ex1.ipynb 为使用keras和torch 进行mnist 手写数字数据集的分类识别(使用CNN模型)
- DM_linear_2.ipynb 为mnist数据集分类（仅使用Linear） 即逻辑回归
- dtplot.py 决策树可视化工具函数
- DTREE.ipynb 手动实现ID3，C4.5 CART 三种决策树进行分类 并给出正确率（数据集：UCI-herbeman）
- Ele_lstm.ipynb 通过keras 库的LSTM 预测用电量 （可能跑不起来）
- multi-label-classification-with-resnet50by-torch.ipynb 使用pytorch的resnet50预训练模型进行电影多标签分类，计算指标为mAP,AUC,F1 score
- PCA_Kmeans.ipynb 对digit和iris数据集进行 手动PCA降维和kmeans 聚类
- recommend.ipynb 为使用pytorch框架 WideAndDeep 模型对用户观看的下一部电影进行预测
- sklearn_Dtree.ipynb 使用sklearn库和graphviz 建立决策树并可视化

# 数据集

- iris,wine,harbeman数据集均在 [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/index.php)
- 猫狗分类数据集 [Cats-vs-Dogs | Kaggle](https://www.kaggle.com/datasets/shaunthesheep/microsoft-catsvsdogs-dataset)
- ele_lstm 的数据集为raw_data.csv
- 电影多标签分类数据集 [下载地址](https://drive.google.com/file/d/1EILvXrzYJTlk4XMVnaEopqxAVUtLyUEh/view?usp=sharing)
- 推荐系统数据集 [MovieLens 100K Dataset | Kaggle](https://www.kaggle.com/datasets/prajitdatta/movielens-100k-dataset)
