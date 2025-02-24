### Dataset Overview

The dataset is derived from real-world locations, sourced from Google Maps, and includes the following CSV files:

- `school.csv`
- `it_companies.csv`
- `malls.csv`
- `hotel.csv`
- `luxury_hotel.csv`
- `prime_hotel.csv`
- `schools.csv`
- `tourist_spot.csv`
- `govt_institutes.csv`
- `college.csv`
- `hospital.csv`
- `industry.csv`

Additionally, the **Custom Property Price Dataset** (`Custom_Property_Price_Dataset.csv`) contains land price data manually compiled by comparing various online websites through a specially designed UI application tailored for this task.

The road network data was obtained from [Geofabrik](https://download.geofabrik.de/) and stored in a PostgreSQL table named `planet_osm_roads`. The data includes different types of roads and road links (such as intersections and squares):

- Tertiary
- Secondary
- Primary
- Trunk

`**_test.csv**`: A sample of the final dataset compiled from the above datasets.

| Lat          | Lng          | Type       | Price    | Sqft | Bhk | tertiary_road_dist | tertiary_road_mean_dist | tertiary_link_dist | tertiary_link_mean_dist | secondary_road_dist | secondary_road_mean_dist | secondary_link_dist | secondary_link_mean_dist | primary_road_dist | primary_road_mean_dist | primary_link_dist | primary_link_mean_dist | trunk_road_dist | trunk_road_mean_dist | trunk_link_dist | trunk_link_mean_dist | college_dist | college_mean_dist | govt_institute_dist | govt_institute_mean_dist | hotel_dist | hotel_mean_dist | luxury_hotel_dist | luxury_hotel_mean_dist | prime_hotel_dist | prime_hotel_mean_dist | malls_dist | malls_mean_dist | schools_dist | schools_mean_dist | it_companies_dist | it_companies_mean_dist | tourist_spot_dist | tourist_spot_mean_dist | hospital_dist | hospital_mean_dist |
|--------------|--------------|------------|----------|------|-----|--------------------|-------------------------|--------------------|-------------------------|---------------------|--------------------------|---------------------|--------------------------|------------------|-----------------------|------------------|------------------------|-----------------|----------------------|-----------------|-----------------------|--------------|-------------------|-------------------|------------------------|------------|------------------|--------------------|------------------------|------------------|-----------------------|------------|------------------|---------------|-------------------|------------------|----------------------|-------------------|-------------------------|--------------|---------------------|
| 21.12750433  | 79.05485988  | Land/Plot  | 18000000 | 13333 | 0   | 297.39515805721237 | 1739.175054672102       | 2282.341509106695  | 2792.110049776672       | 297.39515805721237  | 941.9868678039929        | 830.4610324964924  | 847.3697533798155        | 1106.3867708090102 | 2435.4809806794046     | 1105.5217646740828 | 1603.6535556896572     | 2027.910000610484 | 2870.008668044689    | 2081.278681834842 | 2118.885545996921    | 746.8819049733947 | 2202.7507348301046    | 501.76262438751587 | 2163.4083532432783    | 688.4559397543064 | 2697.1258208392983    | 905.2457709170428 | 2966.9111817682215   | 544.824920352361  | 1894.645503468352   | 485.7378079213591 | 2070.420246128022   | 1004.730276060742 | 2010.278518322038   | 307.24468902122123 | 817.5894166541672    | 900.3108164441661 | 2081.101360085616 | 556.843272468316  | 1172.438692596444 |
| 21.12682945  | 79.05786762  | Apartment  | 30000000 | 3000  | 4   | 65.42837483900755  | 1682.2445055168414      | 2082.438246115905  | 2532.193133213763       | 209.74776997229017  | 890.9204123865863        | 590.7680943288456  | 605.4071577280417        | 1390.9461840087297 | 3250.3075335869876     | 1385.5572715130613 | 1802.9873985444124     | 1710.648619190319 | 2495.3586170968097    | 1780.4017529439905 | 1823.250590960075    | 783.5561635310513 | 2128.77560496935     | 440.63339782847896 | 2025.0195125139853   | 421.08688619728156 | 2632.7835275734947    | 589.9577519791451 | 2800.3686030300337   | 409.625169807422  | 1723.6885863534649   | 228.2102456573792 | 1947.9701616364334   | 999.3316716949608 | 1858.4285665513871   | 98.77777734465603  | 910.4642508505873    | 1026.222697669742 | 2106.291969617629   | 348.3727265391529  | 1008.9338161349633  |