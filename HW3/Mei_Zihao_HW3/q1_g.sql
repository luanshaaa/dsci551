use sakila;
select first_name,last_name from actor,(select actor_id,count(film_id) as film_count from film_actor group by actor_id) as B where actor.actor_id=B.actor_id and B.film_count>30 order by first_name,last_name;

