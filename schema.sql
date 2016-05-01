drop table if exists refunds;
create table refunds (
    id text primary key,
    date text not null,
    sku text not null,
    transtype text not null,
    detail text not null,
    amount integer not null,
    title text not null
);
