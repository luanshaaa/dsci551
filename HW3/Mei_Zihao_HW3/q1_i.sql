use sakila;
select count(distinct category) as number_of_categories from film_list where actors like "%Ed Chase%";
