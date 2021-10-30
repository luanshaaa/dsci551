Use sakila;
drop view if exists Comedy_film;
create view Comedy_film as select FID as film_id, title from film_list where category="Comedy";
select actor_id,first_name,last_name from actor where actor_id in (select actor_id from film_actor join Comedy_film where film_actor.film_id=Comedy_film.film_id) order by actor_id desc;

