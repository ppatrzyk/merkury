-- Script ran against Chinook database
-- https://github.com/lerocha/chinook-database

select BillingCountry, count(*) as Invoices, sum(Total) as Total_spent from Invoice
group by BillingCountry
order by Invoices desc;

select Name, count(*) as Albums from Album
left join Artist using (ArtistId)
group by ArtistId
having Albums > 1
order by Albums desc;
