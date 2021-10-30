use sakila;
select actor_id from film_actor,film_list where length<48 and film_actor.film_id=film_list.FID order by actor_id asc;
