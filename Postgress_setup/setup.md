### **PostgreSQL Setup**

1. **Install PostgreSQL**  
   - Visit [https://www.postgresql.org/download/](https://www.postgresql.org/download/) and follow the installation steps for your operating system.  
   - The project is running on macOS, and PostgreSQL has native app support on this platform.

2. **Verify Installation**  
   - To check if PostgreSQL is installed correctly, open the terminal and type:
     ```bash
     psql --version
     ```

3. **Learn PostgreSQL Basics**  
   - For an introduction to PostgreSQL, check out the official tutorial: [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial-createdb.html).  
   - Alternatively, you can find helpful YouTube videos for beginners.

Here’s the rewritten version of your instructions, with clearer organization and some slight refinement for better readability:

---

### Accessing External Hard Disk

1. **List available disks:**
   ```
   % diskutil list
   ```
   This command displays all available disks (e.g., `/dev/disk0` for internal, physical disks).

2. **List all volumes:**
   ```
   % ls /Volumes
   ```
   This shows all mounted volumes, including external drives. The path to an external drive would look like `/Volumes/{volume_name}`.


### Creating a Tablespace on External Disk for PostgreSQL

1. **Create a directory on the external drive:**
   ```
   % mkdir /Volumes/Drive_OO/GEODATA
   ```

2. **Set appropriate permissions:**
   ```
   % sudo chown $(whoami) /Volumes/Drive_OO/GEODATA
   % chmod 700 /Volumes/Drive_OO/GEODATA
   ```

3. **Create tablespace in PostgreSQL:**
   Run this in PostgreSQL's SQL terminal:
   ```
   % CREATE TABLESPACE my_tablespace LOCATION '/Volumes/Drive_OO/GEODATA';
   ```

---

### Showing List of Tablespaces

To list all existing tablespaces in PostgreSQL:
```
% \db
```

**Syntax for creating a tablespace:**
```sql
CREATE TABLESPACE tablespace_name
OWNER user_name
LOCATION directory_path;
```

---

### Creating PostgreSQL Database with `osm2pgsql`

**Command to Import OSM Data into PostgreSQL:**
```bash
osm2pgsql -c -d osmdb -U username -H localhost -P 5432 -S default.style /Users/username/Desktop/mini/western-zone-latest.osm.pbf -W -C 2000
```

---

### Creating a New Database

To create a new database with the previously created tablespace:
```sql
CREATE DATABASE osm TABLESPACE my_tablespace;
```

---

### Installing Extensions

To install the necessary extensions in PostgreSQL, run:
```sql
CREATE EXTENSION postgis;
CREATE EXTENSION hstore;
```

---
### **macOS Installation For osm2pgsql**

1. **Install `osm2pgsql` using Homebrew:**

   To install `osm2pgsql` via Homebrew, run the following command:
   ```bash
   brew install osm2pgsql
   ```

2. **Verify the installation:**

   After installation, verify it by checking the version with:
   ```bash
   osm2pgsql --version
   ```

---

### **Windows Installation for osm2pgsql**

 For a step-by-step guide on installing osm2pgsql on Windows, refer to this : YouTube video [Link](https://www.youtube.com/watch?v=6GDc-3s67Tg).

---

### Example Commands for `osm2pgsql`

1. **Using the default style script:**
   ```bash
   osm2pgsql -c -d osm -U username -H localhost -P 5432 -S 
   /opt/homebrew/Cellar/osm2pgsql/1.11.0_2/share/osm2pgsql/default.style 
   --tablespace-main-data=my_tablespace 
   --tablespace-main-index=my_tablespace --latlong 
   --hstore /Users/username/path/
   Data_file_download_from_https://download.geofabrik.de/.osm.pbf
    -W -C 2000
   ```

2. **Using a custom road style script:**
   ```bash
   osm2pgsql -c -d osm -U username -H localhost -P 5432 -O flex -S /Users/username/path/road_style.lua --tablespace-main-data=my_tablespace --tablespace-main-index=my_tablespace --latlong --hstore /Users/username/path/Data_file_download_from_https://download.geofabrik.de/.osm.pbf -W -C 2000
   ```

---
**Note:**
Make sure to update the path in the bash command to point to the correct `style.lua` file (use `road_style.lua` for this project to store only road data) and the `osm.pbf` file, which you can download from Geofabrik 
, as it is regularly updated.

Geofabrik  : https://download.geofabrik.de/

We have used **western-zone-lastset.osm** file for the region nagpur, maharasthra , India

---
### Creating a Lua Config File for Flex Output

Refer to this link for more details: [Flex Config Lua File](https://github.com/osm2pgsql-dev/osm2pgsql/blob/master/flex-config/generic.lua#L12)

Here's an example Lua configuration for extracting roads:

```lua
local srid = 4326

local tables = {}

-- Define a table for roads
tables.roads = osm2pgsql.define_way_table('roads', {
    { column = 'tags', type = 'jsonb' },
    { column = 'geom', type = 'linestring', projection = srid, not_null = true },
})

-- Function to determine if a way is a road
local function is_road(tags)
    return tags.highway or tags['highway:']  -- Adjust based on desired tags
end

-- Clean tags function
local delete_keys = { 'attribution', 'comment', 'created_by', 'fixme', 'source' }
local clean_tags = osm2pgsql.make_clean_tags_func(delete_keys)

function osm2pgsql.process_way(object)
    if clean_tags(object.tags) then
        return
    end

    if is_road(object.tags) then
        tables.roads:insert({
            tags = object.tags,
            geom = object:as_linestring()
        })
    end
end
```

---
### Querying the Database

To list the column names and their types from the `planet_osm_roads` table:
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'planet_osm_roads';
```

---

### Indexing Geometries

To create a GiST index on the `geom` column for efficient spatial queries:
```sql
CREATE INDEX idx_features_geom ON features USING GIST (geom);
```

---

### Query to Find Nearby Roads

To find roads within a 50-degree radius of a given point (lat: 21.116877, lon: 79.043073):
```sql
SELECT *
FROM roads
WHERE ST_DWithin(
    geom,
    ST_SetSRID(ST_MakePoint(21.116877, 79.043073), 4326),  -- Replace with your lat/lon
    50  -- Distance in degrees
);
```

**Note:** The `ST_DWithin` function uses GiST (Generalized Search Tree) indexing for efficient spatial queries.

---

### Data Visualization

For visualizing the data, you can use the following DeckGL layers:

- [Column Layer](https://deckgl.readthedocs.io/en/latest/gallery/column_layer.html)
- [Heatmap Layer](https://deckgl.readthedocs.io/en/latest/gallery/heatmap_layer.html)

---

### Common Error: ST_X/ST_Y Type Casting

**Error:**
```
ST_X((ST_DumpPoi...
HINT: No function matches the given name and argument types. You might need to add explicit type casts.
```

**Fix:**
Ensure proper type casting when working with geographic points:
```sql
SELECT rating, public.ST_X(geom::geometry) AS lon, public.ST_Y(geom::geometry) AS lat
FROM features
WHERE ST_DWithin(
    geom::geometry,
    ST_SetSRID(ST_MakePoint(79.054860, 21.127504), 4326),
    0.006  -- Distance in degrees (approx. 6 km)
);
```

