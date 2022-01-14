# My_webcrawler
未来可能会面对很多需要爬虫的情况，不出意外的话都会汇总到这个仓里，并形成一定的记录

## [Pokemondb](https://pokemondb.net/pokedex/all)

- 将整张页面爬下来，并汇总成csv格式
- 环境依赖：requests、pillow、openpyxl、bs4、pandas
- 下载源码可以发现，所有信息都存放在id="pokedex"的table中，稍微观察观察便可以找到各项信息所在的位置，处理之后便可以生成相应的csv和excel

