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

Naming conventions
==================

Python
------

http://stackoverflow.com/a/160830/1760643

David Goodger (in "Code Like a Pythonista" here) describes the PEP 8 recommendations as follows:

    joined_lower for functions, methods, attributes, variables

    joined_lower or ALL_CAPS for constants

    StudlyCaps for classes (but joined_lowercase.py for modules)

    camelCase only to conform to pre-existing conventions

(end of citation)

http://www.alberton.info/dbms_identifiers_and_case_sensitivity.html

Database
--------

PostgreSql is NOT case-sensitive and quoted identifiers are pain so conventions for databases:

table names: joined_lower, singular (as in drupal)
fields: joined_lower, singular

If identifier already exists in database management system, use underscore at the end of identifier: joined_lower_. Why at the end? Because for autocompletion by first letter. 