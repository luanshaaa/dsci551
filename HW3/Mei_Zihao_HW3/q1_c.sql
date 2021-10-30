use sakila;
select actor.actor_id, actor.first_name, actor.last_name, film.film_id, film.title from actor,film,film_actor where actor.actor_id=1 and actor.actor_id=film_actor.actor_id and film.film_id=film_actor.film_id;
