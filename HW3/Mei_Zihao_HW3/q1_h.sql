use sakila;
select name from language where language_id not in (select language_id from film) order by name;
