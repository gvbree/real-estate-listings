def build_geo_kpi_query(ad_type:str, adm_div:str):
    if adm_div == "bundesland":
        cols = f"bundeslandgruppe, bundeslandgruppe_iso, {adm_div}_iso, {adm_div}"
    elif adm_div == "bezirk":
        cols = f"bundeslandgruppe, bundeslandgruppe_iso, bundesland, bundesland_iso, region, region_iso, {adm_div}_iso, {adm_div}"
    elif adm_div == "gemeinde":
        cols = f"bundeslandgruppe, bundeslandgruppe_iso, bundesland, bundesland_iso, region, region_iso, bezirk, bezirk_iso, {adm_div}_iso, {adm_div}"
    
    query = f"""
    WITH subq AS (
		SELECT {cols}
			, COUNT(adid) 							                                            AS n_ads
            , PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY price)                               AS price_median
            , PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY estate_size_living_area)             AS sqm_median
            , PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY (price / estate_size_living_area))   AS price_per_sqm_median
            , AVG(extract(day from (sys_load_ts - published_string)))                           AS dom_avg
		FROM ldl.{ad_type}
		GROUP BY {cols}
	)
	SELECT subq.*
		, ((n_ads * 10000)/ population) 			as n_ads_per_10000p
	FROM ldl.dim_population     pop
	LEFT JOIN subq
		ON pop.iso::text = subq.{adm_div}_iso::text
	WHERE pop.level = '{adm_div}'
	  AND pop.iso <> '900'
    """
        
    return query