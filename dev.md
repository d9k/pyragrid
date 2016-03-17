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

### user_
id, login, name, email, group, email_check_code, email_checked

### article
id, name, systemPath

### article_revision
id, article_id, code, datetime, user_id

### good
id, name, price, is_egood, file_path

### order
id, status, total, paid_amount, refund_amount, user_id

### order_good
id, order_id, _good_id, price, count, refund_count, total, paid_amount,refund_amount, status

### order_good_status
id, order_good_id, date_time, (succeed), is_last, status, shop_money_delta, money_transaction_id

### reject
id, orderId, reason, status, total

### reject_order_good
id, rejectId, order_good_id, count, total, status

### egood_download_link
id, domain, egood_id, download_code, for_user_id, expires

### money_transaction
id, orderGoodId, type (buy/reject) , shop_money_delta, order_id, ended, succeed, status

### money_transaction_status
id, money_transaction_id, provider, status, date_time, request_data, answer_data, error

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