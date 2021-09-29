SELECT name, ST_SetSRID(ST_Point(x::float,y::float),4326) as geom
FROM
(SELECT name, replace(split_part(coords, ',', 1),'(','') y, replace(split_part(coords, ',', 2),')','') x
FROM schema1.zdj_coords) foo