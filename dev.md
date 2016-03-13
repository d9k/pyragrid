Замечания по реализации
=======================

SQL Alchemy/Alembic
-------------------

Были использованы ненативные Enum (`native_enum=False`) потому что PostrgreSQL хоть и умеет добавлять возможные значения в тип данных enum (`ALTER TYPE enum_type ADD VALUE 'new_value';`), ДО СИХ ПОР НЕ УМЕЕТ УДАЛЯТЬ ИЗ ENUM ЗНАЧЕНИЯ (FFFUUUUUU~), потому миграции на тип Enum не представляются возможными.

см. http://stackoverflow.com/questions/1771543/postgresql-updating-an-enum-type

TODO
====

TODO check this:

	pip freeze > requirements.txt

        //TODO: how to install ColanderAlchemy simplier?

//	pip install ColanderAlchemy
//	cd venv/lib/python3.4/site-packages
//	unzip ColanderAlchemy-0.3.3-py3.4.egg
//	rm -r EGG-INFO

DB
===

### articles
id, name, systemPath

### articles revisions
id, articleId, code, datetime, userId

### goods
id, name, price, total, isEgood, filePath

### orders
id, status, total, paid, rejected, userId

### orders_goods
id, price, count, rejectedCount, total, status, goodId

### orders_goods_statuses
id, order_good_id, dateTime, (succeed), isLast, status, rejectCount, moneyTransactionId, moneyTransactionStatusId

### rejects
id, orderId, reason, status, total

### rejects_orders_goods
id, rejectId, order_good_id, count, total, status

### egoodsDownloadLinks
id, domain, goodId, downloadCode, forUserId, expires

### moneyTransactions
id, orderGoodId, type (buy/reject) , shopMoneyDelta, orderId, ended, succeed, status

### moneyTransactionStatus
id, moneyTransactions, provider, status, dateTime, requestData, answerData, error

