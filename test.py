# import matplotlib.pyplot as plt

# # 数据
# labels = ['0', '1', '2']
# sizes = [7405, 21542, 18668]
# colors = ['gold', 'lightcoral', 'lightskyblue']
# explode = (0.1, 0, 0)  # 突出显示第二部分

# # 生成饼状图
# plt.pie(sizes, explode=explode, labels=labels, colors=colors,
# autopct='%1.1f%%', shadow=True, startangle=140)

# plt.axis('equal')  # 保证饼状图是圆形的
# plt.title('Data distribution of training set and validation set')
# plt.show()

# 画数据占比
# import matplotlib.pyplot as plt

# # 数据
# # labels = ['0', '1', '2']
# labels = ['neg', 'neu', 'pos']
# # sizes = [7405, 21542, 18668] # train and val
# sizes = [7093, 20673, 17849] # test
# colors = ['gold', 'lightcoral', 'lightskyblue']
# explode = (0.1, 0, 0)  # 突出显示第二部分

# # 生成饼状图
# plt.pie(sizes, explode=explode, labels=labels, colors=colors,
# autopct=lambda p: '{:.0f}\n({:.1f}%)'.format(p * sum(sizes) / 100, p),
# shadow=True, startangle=140)

# plt.axis('equal')  # 保证饼状图是圆形的
# plt.title('Test Set')

# # 添加图例
# plt.legend(labels, loc='upper right')

# plt.show()


