-- Chinook database
-- https://github.com/lerocha/chinook-database

--TITLE Artists with most albums
select
    Name,
    count(*) as Albums
from Album
left join Artist
using (ArtistId)
group by ArtistId
having Albums > 1
order by Albums desc;

--TITLE Countries with most orders
select
    BillingCountry as Country,
    count(distinct(CustomerId)) as Customers,
    count(*) as Invoices
from Invoice
group by BillingCountry
order by Invoices desc;
