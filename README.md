# pyiikocloudapi - python iiko Cloud API сервис

![](https://www.python.org/static/img/python-logo.png) 

Установка
============

Пользуем pip:
    
```
pip install pyiikocloudapi
```

Зависимости

    requests
    pydantic

Начиная с версии _0.0.20_

    requests
    pydantic>=2.9.2
    
Как использовать
============
Все названия методов соответствуют названию в ссылке (смотрите документацию iiko Transport).


**Пример названия метода:** 

- _/api/1/auth/        - `access_token`_
- _/api/1/order/create - `order_create`_



Если вам нужно чтобы ответ был в dict - то либо 
    
    api = IikoTransport(api_login, return_dict=True)

    # Либо
    api.return_dict = True

Example
============
    from pyiikocloudapi import IikoTransport
    from pyiikocloudapi.models import CouriersModel

    # инициализация класса 
    api = IikoTransport(api_login)

    # получаем организации получить из можно api.organizations_ids: dict or api.organizations_ids_models: OrganizationsModel
    api.organizations()

    # получаю список курьеров организации
    couriers: CouriersModel = api.couriers(api.organizations_ids)

Каждый метод проверяет время жизни маркера доступа, если время жизни маркера прошло то будет автоматически запрошен заново.

**Время жизни маркера доступа равно ~60 минутам.**


###Дополнительная информация
iiko Transport(iiko Cloud API) по словам _**разработчиков**_ это по сути горячие хранилище без доступа к данным БД

`sourceKey` это "Источник заказа" из настроек в iikoWeb


### Реализованные методы iiko Transport(iiko Cloud API) 
- Authorization
  - [x] [Retrieve session key for API user.](https://api-ru.iiko.services/#tag/Authorization/paths/~1api~11~1access_token/post)
- Notifications
  - [x] [Send notification to external systems (iikoFront and iikoWeb).](https://api-ru.iiko.services/#tag/Notifications/paths/~1api~11~1notifications~1send/post)
- Organizations
  - [x] [Returns organizations available to api-login user.](https://api-ru.iiko.services/#tag/Organizations/paths/~1api~11~1organizations/post)
- Terminal groups
  - [x] [Method that returns information on groups of delivery terminals.](https://api-ru.iiko.services/#tag/Terminal-groups/paths/~1api~11~1terminal_groups/post)
  - [x] [Returns information on availability of group of terminals.](https://api-ru.iiko.services/#tag/Terminal-groups/paths/~1api~11~1terminal_groups~1is_alive/post)
- Dictionaries
  - [x] [Delivery cancel causes.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1cancel_causes/post)
  - [x] [Order types.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1deliveries~1order_types/post)
  - [x] [Discounts / surcharges.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1discounts/post)
  - [x] [Payment types.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1payment_types/post)
  - [x] [Removal types (reasons for deletion).](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1removal_types/post)
  - [x] [Get tips tipes for api-login`s rms group.](https://api-ru.iiko.services/#tag/Dictionaries/paths/~1api~11~1tips_types/post)
- Menu
  - [x] [Menu.](https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1nomenclature/post)
  - [x] [External menus with price categories.](https://api-ru.iiko.services/#tag/Menu/paths/~1api~12~1menu/post)
  - [x] [Retrieve external menu by ID.](https://api-ru.iiko.services/#tag/Menu/paths/~1api~12~1menu~1by_id/post)
  - [x] [Out-of-stock items.](https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1stop_lists/post)
  - [x] [Get combos info](https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1combo/post)
  - [x] [Calculate combo price](https://api-ru.iiko.services/#tag/Menu/paths/~1api~11~1combo~1calculate/post)
  - [ ] [WebHook notification about stop list update. Webhook ???](https://api-ru.iiko.services/#tag/Menu/paths/iikoTransport.PublicApi.Contracts.WebHooks.StopListUpdateWebHookEventInfo/post)
- Operations
  - [x] [Get status of command.](https://api-ru.iiko.services/#tag/Operations/paths/~1api~11~1commands~1status/post)
- Deliveries: Create and update
  - [x] [Create delivery.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1create/post)
  - [ ] [Update order problem.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1update_order_problem/post)
  - [x] [Update delivery status.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1update_order_delivery_status/post)
  - [ ] [Update order courier.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1update_order_courier/post)
  - [ ] [Add order items.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1add_items/post)
  - [ ] [Close order.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1close/post)
  - [ ] [Cancel delivery order.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1cancel/post)
  - [ ] [Change time when client wants the order to be delivered.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1change_complete_before/post)
  - [ ] [Change order's delivery point information.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1change_delivery_point/post)
  - [ ] [Change order's delivery type.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1change_service_type/post)
  - [ ] [Change order's payments.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1change_payments/post)
  - [ ] [Change delivery comment.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1change_comment/post)
  - [ ] [Print delivery bill.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1print_delivery_bill/post)
  - [x] [Confirm delivery.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1confirm/post)
  - [x] [Cancel delivery confirmation.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1cancel_confirmation/post)
  - [ ] [Assign/change the order operator.](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/~1api~11~1deliveries~1change_operator/post)
  - [ ] [WebHook notification about delivery order update. Webhook ???](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/iikoTransport.PublicApi.Contracts.WebHooks.DeliveryOrderUpdateWebHookEventInfo/post)
  - [ ] [WebHook notification about delivery order saving error. Webhook ???](https://api-ru.iiko.services/#tag/Deliveries:-Create-and-update/paths/iikoTransport.PublicApi.Contracts.WebHooks.DeliveryOrderErrorWebHookEventInfo/post)
- Deliveries: Retrieve
  - [x] [Retrieve orders by IDs.](https://api-ru.iiko.services/#tag/Deliveries:-Retrieve/paths/~1api~11~1deliveries~1by_id/post)
  - [x] [Retrieve list of orders by statuses and dates.](https://api-ru.iiko.services/#tag/Deliveries:-Retrieve/paths/~1api~11~1deliveries~1by_delivery_date_and_status/post)
  - [ ] [Retrieve list of orders changed from the time revision was passed.](https://api-ru.iiko.services/#tag/Deliveries:-Retrieve/paths/~1api~11~1deliveries~1by_revision/post)
  - [ ] [Retrieve list of orders by telephone number, dates and revision.](https://api-ru.iiko.services/#tag/Deliveries:-Retrieve/paths/~1api~11~1deliveries~1by_delivery_date_and_phone/post)
  - [x] [Search orders by search text and additional filters (date, problem, statuses and other).](https://api-ru.iiko.services/#tag/Deliveries:-Retrieve/paths/~1api~11~1deliveries~1by_delivery_date_and_source_key_and_filter/post)
- Addresses
  - [x] [Regions.](https://api-ru.iiko.services/#tag/Addresses/paths/~1api~11~1regions/post)
  - [x] [Cities.](https://api-ru.iiko.services/#tag/Addresses/paths/~1api~11~1cities/post)
  - [x] [Streets by city.](https://api-ru.iiko.services/#tag/Addresses/paths/~1api~11~1streets~1by_city/post)
- Delivery restrictions
  - [ ] [Retrieve list of delivery restrictions.](https://api-ru.iiko.services/#tag/Delivery-restrictions/paths/~1api~11~1delivery_restrictions/post)
  - [ ] [Update delivery restrictions.](https://api-ru.iiko.services/#tag/Delivery-restrictions/paths/~1api~11~1delivery_restrictions~1update/post)
  - [ ] [Get suitable terminal groups for delivery restrictions.](https://api-ru.iiko.services/#tag/Delivery-restrictions/paths/~1api~11~1delivery_restrictions~1allowed/post)
- Employees
  - [ ] [Method of obtaining drivers' coordinates history.](https://api-ru.iiko.services/#tag/Employees/paths/~1api~11~1employees~1couriers~1locations~1by_time_offset/post)
  - [x] [Returns list of all employees which are delivery drivers in specified restaurants.](https://api-ru.iiko.services/#tag/Employees/paths/~1api~11~1employees~1couriers/post)
  - [ ] [Returns list of all employees which are delivery drivers in specified restaurants, and checks whether each employee has passed role.](https://api-ru.iiko.services/#tag/Employees/paths/~1api~11~1employees~1couriers~1by_role/post)
  - [ ] [Returns list of all active (courier session is opened) courier's locations which are delivery drivers in specified restaurant and are clocked in on specified delivery terminal.](https://api-ru.iiko.services/#tag/Employees/paths/~1api~11~1employees~1couriers~1active_location~1by_terminal/post)
  - [ ] [Returns list of all active (courier session is opened) courier's locations which are delivery drivers in specified restaurants.](https://api-ru.iiko.services/#tag/Employees/paths/~1api~11~1employees~1couriers~1active_location/post)
  - [ ] [Returns employee info.](https://api-ru.iiko.services/#tag/Employees/paths/~1api~11~1employees~1info/post)
- wMarketing sources
  - [ ] [Marketing sources.](https://api-ru.iiko.services/#tag/Marketing-sources/paths/~1api~11~1marketing_sources/post)
- Drafts
  - [ ] [Retrieve order draft by ID.](https://api-ru.iiko.services/#tag/Drafts/paths/~1api~11~1deliveries~1drafts~1by_id/post)
  - [ ] [Retrieve order drafts list by parameters.](https://api-ru.iiko.services/#tag/Drafts/paths/~1api~11~1deliveries~1drafts~1by_filter/post)
  - [ ] [Store order draft changes to DB.](https://api-ru.iiko.services/#tag/Drafts/paths/~1api~11~1deliveries~1drafts~1save/post)
  - [ ] [Admit order draft changes and send them to Front.](https://api-ru.iiko.services/#tag/Drafts/paths/~1api~11~1deliveries~1drafts~1commit/post)
- Orders
  - [x] [Create order.](https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1create/post)
  - [ ] [Retrieve orders by IDs.](https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1by_id/post)
  - [ ] [Retrieve orders by tables.](https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1by_table/post)
  - [ ] [Add order items.](https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1add_items/post)
  - [ ] [Close order.](https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1close/post)
  - [ ] [Change table order's payments.](https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1change_payments/post)
  - [ ] [Init orders, created in the front.](https://api-ru.iiko.services/#tag/Orders/paths/~1api~11~1order~1init_by_table/post)
  - [ ] [WebHook notification about table order update. Webhook ???](https://api-ru.iiko.services/#tag/Orders/paths/iikoTransport.PublicApi.Contracts.WebHooks.TableOrderUpdateWebHookEventInfo/post)
  - [ ] [WebHook notification about table order saving error. Webhook ???](https://api-ru.iiko.services/#tag/Orders/paths/iikoTransport.PublicApi.Contracts.WebHooks.TableOrderErrorWebHookEventInfo/post)
- Banquets/reserves
  - [ ] [Returns all organizations of current account (determined by Authorization request header) for which banquet/reserve booking are available.](https://api-ru.iiko.services/#tag/Banquetsreserves/paths/~1api~11~1reserve~1available_organizations/post)
  - [ ] [Returns all terminal groups of specified organizations, for which banquet/reserve booking are available.](https://api-ru.iiko.services/#tag/Banquetsreserves/paths/~1api~11~1reserve~1available_terminal_groups/post)
  - [ ] [Returns all restaurant sections of specified terminal groups, for which banquet/reserve booking are available.](https://api-ru.iiko.services/#tag/Banquetsreserves/paths/~1api~11~1reserve~1available_restaurant_sections/post)
  - [ ] [Returns all banquets/reserves for passed restaurant sections.](https://api-ru.iiko.services/#tag/Banquetsreserves/paths/~1api~11~1reserve~1restaurant_sections_workload/post)
  - [ ] [Create banquet/reserve.](https://api-ru.iiko.services/#tag/Banquetsreserves/paths/~1api~11~1reserve~1create/post)
  - [ ] [Retrieve banquets/reserves statuses by IDs.](https://api-ru.iiko.services/#tag/Banquetsreserves/paths/~1api~11~1reserve~1status_by_id/post)
  - [ ] [WebHook notification about reserve update. Webhook ???](https://api-ru.iiko.services/#tag/Banquetsreserves/paths/iikoTransport.PublicApi.Contracts.WebHooks.ReserveUpdateWebHookEventInfo/post)
  - [ ] [WebHook notification about reserve saving error. Webhook ??? ](https://api-ru.iiko.services/#tag/Banquetsreserves/paths/iikoTransport.PublicApi.Contracts.WebHooks.ReserveErrorWebHookEventInfo/post)
- [Discounts and promotions](https://api-ru.iiko.services/#tag/Discounts-and-promotions)
  - [ ] [Calculate discounts and other loyalty items for an order.](https://api-ru.iiko.services/#tag/Discounts-and-promotions/paths/~1api~11~1loyalty~1iiko~1calculate/post)
  - [ ] [Get all organization's manual conditions.](https://api-ru.iiko.services/#tag/Discounts-and-promotions/paths/~1api~11~1loyalty~1iiko~1manual_condition/post)
  - [ ] [Get all loyalty programs for organization.](https://api-ru.iiko.services/#tag/Discounts-and-promotions/paths/~1api~11~1loyalty~1iiko~1program/post)
  - [x] [Get information about the specified coupon.](https://api-ru.iiko.services/#tag/Discounts-and-promotions/paths/~1api~11~1loyalty~1iiko~1coupons~1info/post)
  - [x] [Get a list of coupon series in which there are not deleted and not activated coupons.](https://api-ru.iiko.services/#tag/Discounts-and-promotions/paths/~1api~11~1loyalty~1iiko~1coupons~1series/post)
  - [ ] [Get list of non-activated coupons.](https://api-ru.iiko.services/#tag/Discounts-and-promotions/paths/~1api~11~1loyalty~1iiko~1coupons~1by_series/post)
- [Customers](https://api-ru.iiko.services/#tag/Customers)
  - [x] [Get customer info by specified criterion.](https://api-ru.iiko.services/#tag/Customers/paths/~1api~11~1loyalty~1iiko~1customer~1info/post)
  - [x] [Create or update customer info by id or phone or card track.](https://api-ru.iiko.services/#tag/Customers/paths/~1api~11~1loyalty~1iiko~1customer~1create_or_update/post)
  - [x] [Add new customer for program.](https://api-ru.iiko.services/#tag/Customers/paths/~1api~11~1loyalty~1iiko~1customer~1program~1add/post)
  - [x] [Add new card for customer.](https://api-ru.iiko.services/#tag/Customers/paths/~1api~11~1loyalty~1iiko~1customer~1card~1add/post)
  - [x] [Delete existing card for customer.](https://api-ru.iiko.services/#tag/Customers/paths/~1api~11~1loyalty~1iiko~1customer~1card~1remove/post)
  - [x] [Hold customer's money in loyalty program. Payment will be process on POS during processing of an order.](https://api-ru.iiko.services/#tag/Customers/paths/~1api~11~1loyalty~1iiko~1customer~1wallet~1hold/post)
  - [x] [Refill customer balance.](https://api-ru.iiko.services/#tag/Customers/paths/~1api~11~1loyalty~1iiko~1customer~1wallet~1topup/post)
  - [x] [Withdraw customer balance.](https://api-ru.iiko.services/#tag/Customers/paths/~1api~11~1loyalty~1iiko~1customer~1wallet~1chargeoff/post)
- ....
