# Investigating a DVD rental database


## Does the length of a film title affect the number of times a film is rented?

### Findings
![image](https://github.com/Hannahllmm/DVD-Rental-Database/assets/39679731/20acc91e-c865-472c-90cb-b1cdcb944e80)

It could be said that the shortest film titles result in less rentals, however the variance between data points is too small to draw a conclusion. To explore this further we could test this query on a larger data sample, or we could split the title length into smaller subdivisions. We could also approach this question from a slightly different angle, as shown in the next slide.

### SQL Code
```sql
WITH 
film_length_quartile AS 
(SELECT  
	NTILE(4) OVER (ORDER BY LENGTH(title)) AS quartile,
	film_id
FROM film f)

SELECT 
	flq.quartile,
	COUNT(*) rental_count  
FROM film_length_quartile flq
JOIN inventory i
ON i.film_id=flq.film_id
JOIN rental r
ON r.inventory_id=i.inventory_id
GROUP BY 1
ORDER BY 2;
```
### Comments
Because I split the length of the film title into quartiles, there were 250 films in each quartile, this meant I could take the count of the rentals rather than taking the average like I do in the next query. A downside of putting the film title lenth into quartiles is that there will be some overlap where films with the same title lengh are in different quartiles.


### Findings
![image](https://github.com/Hannahllmm/DVD-Rental-Database/assets/39679731/43753c2a-c14c-48d6-8646-e2cf508f5ce7)

We can see there appears to be no correlation between a films title length and the number of times it is rented. There are two noticeable outliers, a title length of 23 and 27 characters. This is probably because there are few films with this length of title, so a very popular or unpopular film will have more impact on the average. For example, Arachnophobia Rollercoaster is the only film with 27 characters in its name and it happens to be a popular film.

### SQL Code

```SQL
WITH film_rentals AS (
SELECT 
	COUNT(*) rental_count,
	LENGTH (f.title) title_length,
	f.title
FROM film f
FULL OUTER JOIN inventory i
ON i.film_id=f.film_id
FULL OUTER JOIN rental r
ON r.inventory_id=i.inventory_id
GROUP BY 2, 3)

SELECT title_length,
AVG(rental_count) avg_rental
FROM film_rentals
GROUP BY 1
ORDER BY 1;
```

### Comments
In this query I used a FULL OUTER JOIN because if a film had never been rented, I wanted that 0 value to be included in the average number of rentals. In the previous query this wasn't needed because if a film had never been rented I didnt want it included in the count of the number of rentals. To find the Arachnophobia Rollercoaster outlier mentioned in the slide I ran the film_rentals sub query, ordered by title_length to see what was going on.

## Who are the 10 customers that have rented the most films?

### Findings
![image](https://github.com/Hannahllmm/DVD-Rental-Database/assets/39679731/d9156586-256e-4255-afa3-598f94ff92eb)

We can see Eleanor Hunt is the most frequent customer. She has rented 46 films, with Karl Seal closely following, having rented 45 film.

### SQL Code
```sql
SELECT 
	CONCAT(c.first_name,' ',c.last_name) customer,
	COUNT(*) rental_count
FROM customer c
JOIN  rental r
ON r.customer_id=c.customer_id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
```

## Looking at the top 100 most frequent customers, and the film category they each rented the most from, which category was the most popular?
### Findings
![image](https://github.com/Hannahllmm/DVD-Rental-Database/assets/39679731/c2a77237-1aa6-40a6-95fc-ade6593b9e70)

It’s clear that the most popular category among the top100 customers is Animation. There are 16 categories overall, so all categories were the most popular for at least one top 100 customer, with horror being the least popular. It is worth noting that although we looked at the most popular category of film for each of the top 100 customers, some customers had more than one category they rented the most from. For example Barry Lovelace rented 4 animation films and 4 games, so both of these are counted. The information in this chart could be useful if the rental companies wanted to create a promotional offer, for example half price on animation rentals. Frequent customers are more likely to make the most of promotional offers than one off customers.

### SQL Code
```sql
-- Takes a count of the rentals each customer has had then filters out the top 10
WITH tbl1 AS (
SELECT 
	CONCAT(c.first_name,' ',c.last_name) customer,
	c.customer_id, 
	COUNT(*) rental_count
FROM customer c
JOIN rental r
ON r.customer_id=c.customer_id
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 100),

-- Takes those top 10 customers and for each customer works out the number of films they have rented in each category
tbl2 AS (
SELECT 
	tbl1.customer, 
	cat.name category,
	COUNT(*) category_count
FROM tbl1
JOIN rental r
ON tbl1.customer_id=r.customer_id
JOIN inventory i
ON i.inventory_id=r.inventory_id
JOIN film_category fc
ON fc.film_id=i.film_id
JOIN category cat
ON cat.category_id=fc.category_id
GROUP BY 1 , 2
ORDER BY 1, 3 DESC)

-- The subquery ranking_tbl ranks the number of films rented in each category for each customer
-- The number 1 ranked categories for each of the top 100 customers are then counted by category to see the most popular overall

SELECT category, COUNT(*) category_tally
FROM (SELECT 
		customer, 
		category, 
		category_count, 
		RANK() OVER (PARTITION BY customer ORDER BY category_count DESC ) AS ranking
	FROM tbl2
	GROUP BY 1, 2, 3) AS ranking_tbl
WHERE ranking=1
GROUP BY 1
ORDER BY 2 DESC, 1;
```
### Comments
I used the results from tbl2 to find the example of a customer that had more than one favrouite rental.
