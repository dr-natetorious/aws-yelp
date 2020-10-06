select 
  b.business_id, 
  b.name, 
  count(*) as avail_photos, 
  sum(if(label ='food',1,0)) as food, 
  sum(if(label ='inside',1,0)) as inside, 
  sum(if(label ='outside',1,0)) as outside,
  sum(if(label ='menu',1,0)) as menu
from business as b
left outer join photo as p
on b.business_id = p.business_id
group by b.business_id, b.name
order by avail_photos desc