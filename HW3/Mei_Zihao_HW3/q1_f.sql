use sakila;
select actor_id,count(film_id) as film_count from film_actor group by actor_id
order by film_count desc limit 5;

