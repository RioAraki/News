TODOs:
1. 仔细研究并考虑清楚一个通用的filter的schema是怎么样的。
2. 搞清楚如何建立数据库存filter。
3. web ui solution to create/edit filter
4. jag ui to reflect the filter change
5. How to publish news -> record the last news/ or use websocket?
6. Redis should persist News's id, so that if news server get shut down intraday, it can recover without showing duplicate news


Pre-mortem:

1. News downloader dead intraday
2. News server dead intraday
3. Redis dead intraday
4. News UI dead intraday
