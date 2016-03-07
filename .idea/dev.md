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
id, name, price, egood, filePath, downloadPath

### orders
id, status, shopCartId, username, email, status

### orderStatuses
id, dateTime, orderId, status, data

### shopCarts
id, createTime, status, total, isRejectCart,

### shopCartItems
id, price, total, shopCartId, goodId, addTime

### egoodsDownloadLinks
id, domain, link, forUserId, expires

### transactions
id, type, status, shopCashflow, orderId, requestData, answerData


