use sakila;
select address_id,address,address.city_id from address join city where country_id=6 and address.city_id=city.city_id;

