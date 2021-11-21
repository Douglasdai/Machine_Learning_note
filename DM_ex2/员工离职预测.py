'''
@author：fc
@date：  2021/11/18
@contact：675435108@qq.com
'''
from sklearn.preprocessing import StandardScaler

"""
文件内容&功能简要：
#
"""
import pandas as pd
import numpy as np
df = pd.read_csv(r'./HR_comma_sep.csv')
pd.set_option('display.max_rows', 4)
print(df)

df.info()

# 3). 描述性统计
df.describe()
df.describe(include=['O']).T

pd.set_option('display.max_rows', None)
df.describe()

# 4. 数据预处理
import seaborn as sns
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1,5, figsize=(12, 2))
sns.boxplot(x=df.columns[0], data=df, ax=ax[0])
sns.boxplot(x=df.columns[1], data=df, ax=ax[1])
sns.boxplot(x=df.columns[2], data=df, ax=ax[2])
sns.boxplot(x=df.columns[3], data=df, ax=ax[3])
sns.boxplot(x=df.columns[4], data=df, ax=ax[4])

from pyecharts import Pie  # 这个包感觉和下面的包不兼容
attr = ["离职", "在职"]
v1 =[df.left.value_counts()[1], df.left.value_counts()[0]]
pie = Pie("该公司人力资源总体情况", title_pos='center')
pie.add(
    "",
    attr,
    v1,
    radius=[35, 65],
    label_text_color=None,
    is_label_show=True,
    legend_orient="vertical",
    legend_pos="left",
)
pie.render("该公司人力资源总体情况图.html")


from pyecharts import Boxplot
#字段重命名
df.columns=['satisfaction', 'evaluation', 'project', 'hours', 'years_work','work_accident', 'left', 'promotion', 'department', 'salary']
#绘制箱线图
boxplot = Boxplot("对公司满意度与是否离职关系图", title_pos='center')
x_axis = ['在职', '离职']
y_axis = [df[df.left == 0].satisfaction.values, df[df.left == 1].satisfaction.values]
boxplot.add("", x_axis, boxplot.prepare_data(y_axis))
boxplot.render("对公司满意度与是否离职关系图.html")


boxplot = Boxplot("最新评估与是否离职关系图", title_pos='center')
x_axis = ['在职', '离职']
y_axis = [df[df.left == 0].evaluation.values, df[df.left == 1].evaluation.values]
boxplot.add("", x_axis, boxplot.prepare_data(y_axis))
boxplot.render("最新评估与是否离职关系图.html")

from pyecharts import Bar, Pie, Grid
#按照项目数分组分别求离职人数和所有人数
project_left_1 = df[df.left == 1].groupby('project')['left'].count()
project_all = df.groupby('project')['left'].count()
#分别计算离职人数和在职人数所占比例
project_left1_rate = project_left_1 / project_all
project_left0_rate = 1 - project_left1_rate
attr = project_left1_rate.index
bar = Bar("所参加项目数与是否离职的关系图", title_pos='10%')
bar.add("离职", attr, project_left1_rate, is_stack=True)
bar.add("在职", attr, project_left0_rate, is_stack=True, legend_pos="left", legend_orient="vertical")
#绘制圆环图
pie = Pie("各项目数所占百分比", title_pos='center')
pie.add('', project_all.index, project_all, radius=[35, 60], label_text_color=None,
        is_label_show=True, legend_orient="vertical", legend_pos="67%")
grid = Grid(width=1200)
grid.add(bar, grid_right="67%")
grid.add(pie)
grid.render("所参加项目数与是否离职的关系图.html")



boxplot = Boxplot("平均每月工作时长与是否离职关系图", title_pos='center')
x_axis = ['在职', '离职']
y_axis = [df[df.left == 0].hours.values, df[df.left == 1].hours.values]
boxplot.add("", x_axis, boxplot.prepare_data(y_axis))
boxplot.render("平均每月工作时长与是否离职关系图.html")


from pyecharts import Bar, Pie, Grid
#按照工作年限分别求离职人数和所有人数
years_left_0 = df[df.left == 0].groupby('years_work')['left'].count()
years_all = df.groupby('years_work')['left'].count()
#分别计算离职人数和在职人数所占比例
years_left0_rate = years_left_0 / years_all
years_left1_rate = 1 - years_left0_rate
attr = years_all.index
bar = Bar("工作年限与是否离职的关系图", title_pos='10%')
bar.add("离职", attr, years_left1_rate, is_stack=True)
bar.add("在职", attr, years_left0_rate, is_stack=True, legend_pos="left" , legend_orient="vertical")
#绘制圆环图
pie = Pie("各工作年限所占百分比", title_pos='center')
pie.add('', years_all.index, years_all, radius=[35, 60], label_text_color=None,
        is_label_show=True, legend_orient="vertical", legend_pos="67%")
grid = Grid(width=1200)
grid.add(bar, grid_right="67%")
grid.add(pie)
grid.render("工作年限与是否离职的关系图.html")


#from pyecharts import Bar
accident_left = pd.crosstab(df.work_accident, df.left)
attr = accident_left.index
bar = Bar("是否发生工作事故与是否离职的关系图", title_pos='center')
bar.add("离职", attr, accident_left[1], is_stack=True)
bar.add("在职", attr, accident_left[0], is_stack=True, legend_pos="left" , legend_orient="vertical", is_label_show=True)
bar.render("是否发生工作事故与是否离职的关系图.html")


promotion_left = pd.crosstab(df.promotion, df.left)
attr = promotion_left.index
bar = Bar("5年内是否升职与是否离职的关系图", title_pos='center')
bar.add("离职", attr, promotion_left[1], is_stack=True)
bar.add("在职", attr, promotion_left[0], is_stack=True, legend_pos="left" , legend_orient="vertical", is_label_show=True)
bar.render("5年内是否升职与是否离职的关系图.html")


from pyecharts import Bar
#按照薪资水平分别求离职人数和所有人数
salary_left = pd.crosstab(df.salary, df.left).sort_values(0, ascending = False)
attr = salary_left.index
bar = Bar("薪资水平和是否离职的关系图", title_pos='center')
bar.add("离职", attr, salary_left[1], is_stack=True)
bar.add("在职", attr, salary_left[0], is_stack=True, legend_pos="left" , legend_orient="vertical", is_label_show=True)
bar.render("薪资水平和是否离职的关系图.html")

# 6. 特征工程
#1. 离散型数据处理
#1) 定序
df['salary'] = df.salary.map({"low": 0, "medium": 1, "high": 2})
df.salary.unique()

#2) 定类
df_one_hot = pd.get_dummies(df, prefix="dep")
df_one_hot.shape

# 2. 连续型数据处理
#采用max-min归一化方法
hours = df_one_hot['hours']
df_one_hot['hours'] = df_one_hot.hours.apply(lambda x: (x-hours.min()) / (hours.max()-hours.min()))

#计算相关系数
correlation = df_one_hot.corr(method = "spearman")
plt.figure(figsize=(18, 10))
#绘制热力图
sns.heatmap(correlation, linewidths=0.2, vmax=1, vmin=-1, linecolor='w',fmt='.2f',
            annot=True,annot_kws={'size':10},square=True)

# 7. 逻辑回归模型
# 1. 划分数据集
from sklearn.model_selection import train_test_split
#划分训练集和测试集
X = df_one_hot.drop(['left'], axis=1)
y = df_one_hot['left']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# 2. 训练模型
from sklearn.linear_model import LogisticRegression
# LR = LogisticRegression()
# print(LR.fit(X_train, y_train))
# print("训练集准确率: ", LR.score(X_train, y_train))
# print("测试集准确率: ", LR.score(X_test, y_test))
#
# #指定随机梯度下降优化算法
# LR1 = LogisticRegression(solver='saga')
# print(LR1.fit(X_train, y_train))
# print("训练集准确率: ", LR1.score(X_train, y_train))
# print("测试集准确率: ", LR1.score(X_test, y_test))

#用准确率进行10折交叉验证选择合适的参数C
from sklearn.linear_model import LogisticRegressionCV
Cs = 10**np.linspace(-10, 10, 400)
lr_cv = LogisticRegressionCV(Cs=Cs, cv=10, penalty='l2', solver='saga',  max_iter=10000, scoring='accuracy')
lr_cv.fit(X_train, y_train)
print(lr_cv.C_)
#用该参数进行预测，此时需要将之前的LR模型注释，不然会报错,当你看到时请自行解开注释
LR = LogisticRegression(solver='saga', penalty='l2', C=25.52908068)
print(LR.fit(X_train, y_train))
print("训练集准确率: ", LR.score(X_train, y_train))
print("测试集准确率: ", LR.score(X_test, y_test))


# 4. 混淆矩阵
from sklearn import metrics
X_train_pred = LR.predict(X_train)
X_test_pred = LR.predict(X_test)
print('训练集混淆矩阵:')
print(metrics.confusion_matrix(y_train, X_train_pred))
print('测试集混淆矩阵:')
print(metrics.confusion_matrix(y_test, X_test_pred))

from sklearn.metrics import classification_report
print('训练集:')
print(classification_report(y_train, X_train_pred))
print('测试集:')
print(classification_report(y_test, X_test_pred))

# 8.朴素贝叶斯模型
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
#构建高斯朴素贝叶斯模型
gnb = GaussianNB()
gnb.fit(X_train, y_train)
print("训练集准确率: ", gnb.score(X_train, y_train))
print("测试集准确率: ", gnb.score(X_test, y_test))
X_train_pred =gnb.predict(X_train)
X_test_pred = gnb.predict(X_test)
print('训练集混淆矩阵:')
print(metrics.confusion_matrix(y_train, X_train_pred))
print('测试集混淆矩阵:')
print(metrics.confusion_matrix(y_test, X_test_pred))
print('训练集:')
print(classification_report(y_train, X_train_pred))
print('测试集:')
print(classification_report(y_test, X_test_pred))


#9. 模型评估之ROC曲线
from sklearn import metrics
from sklearn.metrics import roc_curve
#将逻辑回归模型和高斯朴素贝叶斯模型预测出的概率均与实际值通过roc_curve比较返回假正率, 真正率, 阈值
lr_fpr, lr_tpr, lr_thresholds = roc_curve(y_test, LR.predict_proba(X_test)[:,1])
gnb_fpr, gnb_tpr, gnb_thresholds = roc_curve(y_test, gnb.predict_proba(X_test)[:,1])
#分别计算这两个模型的auc的值, auc值就是roc曲线下的面积
lr_roc_auc = metrics.auc(lr_fpr, lr_tpr)
gnb_roc_auc = metrics.auc(gnb_fpr, gnb_tpr)
plt.figure(figsize=(8, 5))
plt.plot([0, 1], [0, 1],'--', color='r')
plt.plot(lr_fpr, lr_tpr, label='LogisticRegression(area = %0.2f)' % lr_roc_auc)
plt.plot(gnb_fpr, gnb_tpr, label='GaussianNB(area = %0.2f)' % gnb_roc_auc)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.title('ROC')
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.legend()
plt.show()