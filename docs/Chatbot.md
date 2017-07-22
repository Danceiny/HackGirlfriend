# 依存关系的五条公理
1. 一个句子中只有一个成分是独立的

2. 其他成分直接依存于某一成分

3. 任何一个成分都不能依存于两个或两个以上的成分

4. 如果A成分直接依存于B成分，而C成分在句子中位于A和B之间，那么C或者直接依存于B，或者直接依存于A和B之间的某一成分

5. 中心成分左右两面的其他成分相互不发生关系

 

什么地方存在依存关系呢？比如合成词（如：国内）、短语（如：英雄联盟）很多地方都是.
 

## LTP依存关系标记
![](http://opkk27k9n.bkt.clouddn.com/17-7-22/64253013.jpg)

# http://www.ltp-cloud.com/
MyApiKey: D1o3M1a8J87nFcyMjmiQYK2uQcQN3POA8lcuPAXL

`curl -i "http://api.ltp-cloud.com/analysis/?api_key=YourApiKey&text=我是中国人。&pattern=dp&format=plain"`

pattern
- ws 分词
- pos 词性标注
- sdp 语义依存分析
- srl 语义角色标注


