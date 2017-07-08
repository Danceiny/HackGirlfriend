# 一.数据处理

root <- "C:/Developer/workspaces/HackDay2017/Platform/QQChatCenter/"
file<-paste(root,"汪睿(1458110685).txt",sep="")

file.data<-scan(file,what="",sep="\n",encoding="UTF")

head(file.data)

file.data<-file.data[-1:-5]



#正则表达式解析时间time，发布人user，留言信箱,message,存储在一个data数据框中

time <- c();#时间
user <- c();#用户
message <- c();#消息
data<-data.frame(user=c(),time=c(),message=c())

#聊天记录里面消息和时间
for(i in 1:length(file.data))
{
  reglog <- regexpr('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]+:[0-9]+:[0-9]+',file.data[i])
  if(reglog[1]==1)
  {
    time[i] <- substr(file.data[i],1,19)
    user[i] <- substr(file.data[i],21,nchar(file.data[i]))
  }
  else
  {
    message[i] <- file.data[i]
  }
}


data<- data.frame(time=time,user=user,message=message[-1])
head(data)


for(i in 1:dim(data)[1])
  if(is.na(data[i,1]))
  {
    if(is.na(data[i,2]))
    {
      if(is.na(data[i,3]))
      {
        data<- data[-i,]
      }
    }
  }
head(data)

# 二. 分析讨论话题

library(rJava)
library(Rwordseg)
library(dplyr)
text<-as.character(data$message)
text<-enc2utf8(text) #转utf-8
text<-text[Encoding(text)!='unknown']#删除无法识别的字符
#下面这几个词在分词是会被分开
insertWords(c("何凯文","泪奔","卖萌","考研"),save=TRUE)
word.message<-segmentCN(text)#分词
#删除停用词
stop_words=readLines('停词.txt')
target_words <- unlist(word.message)
seg_word=target_words[which(is.element(target_words,stop_words)==FALSE)]

#分词结束，现在开始统计词频
p=as.data.frame(table(unlist(seg_word)))%>% arrange(desc(Freq))
head(p)
library(wordcloud2)
wordcloud2(p)

seg_word=gsub(pattern="[飘]","",seg_word);
q=as.data.frame(table(unlist(seg_word)))%>% arrange(desc(Freq))
wordcloud2(q)


# 三. .讨论时间点
user.time<-data$time
user.time<-as.character(user.time)
user.time.h<-c()
for(i in 1:length(user.time))
{
  user.time.h[i]<-substr(user.time[i],12,19)
}
#如果上面substr(user.time[i],12,19)写成substr(user.time[i],12,13)在
#后面会出错的，因为当时间在10点到23点之间没错，但如果是0点到9点，
#它也会把后面的那个冒号读进去。
user.time.h<- as.POSIXct(user.time.h,format="%H:%M:%S")   #提取时分秒
hour <- format(user.time.h,"%H")   #统计出小时发言
hour <- as.data.frame(table(hour))
library(ggplot2)
ggplot(data=hour,aes(x=hour,y=Freq,group=1))+geom_bar(stat = 'identity')+geom_line(color="red");#折线图和条形图叠加


# 四. 分析谁是话痨
#统计发言频率
user.n<-as.data.frame(table(user))
user.n.20<-user.n[order(user.n[,2],decreasing=T),]
user.n.20<-user.n.20[1:20,]
ggplot(data=user.n.20,aes(x=user,y=Freq))+
          geom_bar(stat='identity')+coord_flip()
#coord_flip()


（1）R语言如何画个性化词云图 地址：http://blog.csdn.NET/wzgl__wh/article/details/52420747
（2）快速学习ggplot2 地址：http://blog.csdn.Net/wzgl__wh/article/details/51901093
（3）使用R语言进行中文分词  地址：http://blog.csdn.net/wzgl__wh/article/details/52528925
（4）R语言之正则表达式 地址：http://blog.csdn.net/wzgl__wh/article/details/52938475

Pandas
http://www.jianshu.com/p/9f1166916960