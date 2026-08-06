use sql_analytics4;

select * from app_events;
select * from customers;
select * from digital_transfers;

-- Checking for Missing Values in app_events ----------------------------------------------------------------------
select 
sum(channel_type is null) as null_channel_type,
sum(action_performed is null) as null_action_performed,
sum(event_timestamp is null) as null_event_timestamp
from app_events;

-- Checking for Missing Values in Customers ----------------------------------------------------------------------
select 
sum(age_group is null) as null_age_group,
sum(region is null) as null_region,
sum(branch_code is null) as null_branch_code,
sum(registration_date is null) as null_registration_date
from customers;

-- Checking for Missing Values in digital_transfers ----------------------------------------------------------------------
select 
sum(payment_channel is null) as null_payment_channel,
sum(transaction_amount is null) as null_transaction_amount,
sum(transaction_status is null) as null_transaction_status,
sum(transaction_timestamp is null) as null_transaction_timestamp
from digital_transfers;

--  Auditing Messy Columns for Python Transformations in app_events
select distinct channel_type from app_events;

select distinct action_performed from app_events;

select event_timestamp from app_events
where event_timestamp not like '____-__-__ __:__:__';


--  Auditing Messy Columns for Python Transformations in customers
select distinct age_group from customers;

select distinct region from customers;

select branch_code from customers 
where branch_code not like '______';

select registration_date from customers 
where registration_date not like '____-__-__';


--  Auditing Messy Columns for Python Transformations in digital_transfers
select distinct payment_channel from digital_transfers;

select transaction_amount from digital_transfers
where transaction_amount like '%$%' or transaction_amount like '%Rs.%' 
or transaction_amount like '%,%' or transaction_amount < 0;

select distinct transaction_status from digital_transfers;

select transaction_timestamp from digital_transfers
where transaction_timestamp not like '____-__-__ __:__:__';

-- Identify Dublicate Rows
select event_id, count(*) as Dublicate_Count from app_events 
group by event_id
having count(*) > 1;

select customer_id, count(*) as Dublicate_Count from customers 
group by customer_id
having count(*) > 1;

select transaction_id, count(*) as Dublicate_Count from digital_transfers 
group by transaction_id
having count(*) > 1;

-- Excluding duplicate records -----------------------------
create table app_events_clean select distinct * from app_events;
create table customers_clean select distinct * from customers;
create table digital_transfers_clean select distinct * from digital_transfers;

-- View 1 ----------------------------------------------------------------------
create view v_transactions as
select
    t.customer_id,
    c.age_group,
    c.region,
    t.payment_channel,
    t.transaction_amount,
    t.transaction_status,
    t.transaction_timestamp
from digital_transfers_clean t
left join customers_clean c on t.customer_id = c.customer_id;

-- View 2 ----------------------------------------------------------------------
create view v_app_activity as
select
    e.customer_id,
    c.age_group,
    c.region,
    e.channel_type,
    e.action_performed,
    e.event_timestamp
from app_events_clean e
left join customers_clean c on e.customer_id = c.customer_id;