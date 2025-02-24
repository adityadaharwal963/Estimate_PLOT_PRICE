local srid = 4326

local tables = {}

-- Define a table for roads
tables.roads = osm2pgsql.define_way_table('roads', {
    { column = 'tags', type = 'jsonb' },
    { column = 'geom', type = 'linestring', projection = srid, not_null = true },
})

-- Function to determine if a way is a road
local function is_road(tags)
    return tags.highway or tags['highway:'] -- Adjust based on desired tags
end

-- Define delete_keys
local delete_keys = {
    'attribution',
    'comment',
    'created_by',
    'fixme',
    'source',
    -- Add any other keys you want to remove
}

-- Clean tags function
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