
##基于scrapy,scrapy-redis实现的一个分布式网络爬虫,爬取了新浪房产的楼盘信息,实现了常用的爬虫功能需求.
1.'sinahouse.pipelines.MongoPipeline' 实现数据持久化到mongodb  
2.'sinahouse.middlewares.UserAgentMiddleware','sinahouse.middlewares.ProxyMiddleware' 分别实现用户代理UserAgent变换和IP代理变换  
3.通过设置setting中的scrapy-redis的相关参数,实现爬虫的分布式运行,或者单机多进程运行.无redis环境时,可以注释掉相关参数,转化为普通的  scrapy爬虫程序  
4.运行日志保存

其他说明. 更多相关信息请查阅scrapy以及scrapy-redis文档
  
  爬取目标网站:[新浪房产](http://data.house.sina.com.cn/sc/search/)  
