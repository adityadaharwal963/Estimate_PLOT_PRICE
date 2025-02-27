from flask import Flask, jsonify, request
from flask_cors import CORS 
import joblib
import numpy as np
import psycopg2  # Import the psycopg2 library
import pandas as pd
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  


# Load the trained model
model = joblib.load('linear_model.pkl')


# Haversine formula to calculate distance between two points on the Earth's surface
def haversine(lon1, lat1, lon2, lat2):
    # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r * 1000 # distance in meter

def find_shortest_points(src_lat, src_lon, df,nPoints):
    # Calculate the distance for each point in the DataFrame
    df['distance'] = df.apply(lambda row: haversine(src_lon, src_lat, row['lon'], row['lat']), axis=1)
    
    # Sort the DataFrame by distance and return the n closest points
    closest_points = df.nsmallest(nPoints, 'distance')

    return df


def get_shortest_point_and_mean(dict,tag,src_lat, src_lon,nPoints):
   
    df_temp = find_shortest_points(src_lat, src_lon, dict[tag],nPoints)
    # print(df_temp.distance.min(),df_temp.distance.mean(),tag)
    return df_temp.distance.min(),df_temp.distance.mean()


def split_dataframe_by_road_type(df):
    # Create a dictionary to hold DataFrames for each road type
    road_type_dfs = {}
    
    # Set unique road types 
    unique_road_types = ['tertiary','tertiary_link','secondary','secondary_link','primary','primary_link','trunk','trunk_link']
    
    # Iterate over unique road types and create a separate DataFrame for each
    for road_type in unique_road_types:
        road_type_dfs[road_type] = df[df['tag'] == road_type].reset_index(drop=True)
    
    return road_type_dfs


def split_dataframe_by_features_type(df):
    # Create a dictionary to hold DataFrames for each road type
    features_type_dfs = {}
    
    # Set unique road types 
    unique_features_types = ['college','govt_institute','hotel','luxury_hotel','prime_hotel','malls','schools','it_companies','tourist_spot','hospital']
    
    # Iterate over unique road types and create a separate DataFrame for each
    for features_type in unique_features_types:
        features_type_dfs[features_type] = df[df['tag'] == features_type].reset_index(drop=True)
    
    return features_type_dfs


# Function to fetch data from the PostgreSQL database
def fetch_database_values(lat,lng):
    # Connect to your PostgreSQL database
    try:
        conn = psycopg2.connect(database = "osm", 
                        user = "adityadaharwal", 
                        host= 'localhost',
                        password = "1234",
                        port = 5432)

        cursor = conn.cursor()
        
        # get road data (all types of road execpt residential)
        cursor.execute(f"""
            SELECT way_id, tags->>'highway' AS tag, ST_X((ST_DumpPoints(geom)).geom) AS lon, ST_Y((ST_DumpPoints (geom)).geom) AS lat
            FROM roads
            WHERE ST_DWithin(
                geom,
                ST_SetSRID(ST_MakePoint({lng},{lat}), 4326),
                0.03  -- Distance in degree = (3 km)
                ) and tags->>'highway' != 'residential' and tags->>'highway'!= 'service';
            """)

        # Fetch the result
        result = cursor.fetchall()

        # Check if result is found
        if result:
            # Get column names
            colnames = [desc[0] for desc in cursor.description]
            # Create a DataFrame
            df_highway = pd.DataFrame(result , columns=colnames)
            # spilt dataframe by category
            road_type_dfs = split_dataframe_by_road_type(df_highway)

        else:
            raise ValueError("No data found for the given parameters.")


        # get features data   
        cursor.execute(f"""
            SELECT review_count, rating, tag, public.ST_X(geom::geometry) AS lon, public.ST_Y(geom::geometry) AS lat 
            FROM features
            WHERE ST_DWithin(
                geom::geometry,
                ST_SetSRID(ST_MakePoint({lng},{lat}), 4326),
                0.06  -- Distance in degree = ( 6 km)
                );
            """)
        # Fetch the result
        result = cursor.fetchall()
        
        # Check if result is found
        if result:
            # Get column names
            colnames = [desc[0] for desc in cursor.description]
            # Create a DataFrame
            df_features = pd.DataFrame(result, columns=colnames)
            # spilt dataframe by category
            features_type_dfs =  split_dataframe_by_features_type(df_features)
            
            return road_type_dfs, features_type_dfs
        else:
            raise ValueError("No data found for the given parameters.")


        cursor.close()
        conn.close()


    except Exception as e:
        print(f"Database error: {str(e)}")

# API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    app.logger.info("hello")
    try:
        # Get JSON data from the request
        data = request.get_json()
        # Extract the input feature
        land_type = data['Type']
        sqft = data['Sqft']
        bhk = int(data['Bhk'])
        lat = data['Lat']
        lng = data['Lng']
       
        # Fetch GIS values from the database
        road_type_dfs, features_type_dfs = fetch_database_values(lat, lng)
        
        # 'Type_ Land/Plot' change onehot encoding
        if(land_type == 'Land'or land_type == 'Plot'):
            land_type = 1
        else:
            land_type = 0
        # 'Sqft',
        # 'Bhk',

        #road features
        tertiary_road_dist, tertiary_road_mean_dist = get_shortest_point_and_mean(road_type_dfs,'tertiary',lat,lng,500)
        tertiary_link_dist, tertiary_link_mean_dist = get_shortest_point_and_mean(road_type_dfs,'tertiary_link',lat ,lng,10)
        secondary_road_dist, secondary_road_mean_dist = get_shortest_point_and_mean(road_type_dfs,'secondary',lat,lng,500)
        secondary_link_dist, secondary_link_mean_dist = get_shortest_point_and_mean(road_type_dfs,'secondary_link',lat,lng,10)
        primary_road_dist, primary_road_mean_dist = get_shortest_point_and_mean(road_type_dfs,'primary',lat,lng,500)
        primary_link_dist, primary_link_mean_dist = get_shortest_point_and_mean(road_type_dfs,'primary_link',lat,lng,10)
        trunk_road_dist, trunk_road_mean_dist = get_shortest_point_and_mean(road_type_dfs,'trunk',lat,lng,500)
        trunk_link_dist, trunk_link_mean_dist = get_shortest_point_and_mean(road_type_dfs,'trunk_link',lat,lng,10)

        #amenity 
        college_dist, college_mean_dist =  get_shortest_point_and_mean(features_type_dfs,'college',lat,lng,30)
        govt_institute_dist, govt_institute_mean_dist = get_shortest_point_and_mean(features_type_dfs,'govt_institute',lat,lng,30)
        hotel_dist, hotel_mean_dist = get_shortest_point_and_mean(features_type_dfs,'hotel',lat,lng,30)
        luxury_hotel_dist, luxury_hotel_mean_dist = get_shortest_point_and_mean(features_type_dfs,'luxury_hotel',lat,lng,30)
        prime_hotel_dist, prime_hotel_mean_dist = get_shortest_point_and_mean(features_type_dfs,'prime_hotel',lat,lng,30)
        malls_dist, malls_mean_dist = get_shortest_point_and_mean(features_type_dfs,'malls',lat,lng,30)
        schools_dist, schools_mean_dist = get_shortest_point_and_mean(features_type_dfs,'schools',lat,lng,30)
        it_companies_dist, it_companies_mean_dist = get_shortest_point_and_mean(features_type_dfs,'it_companies',lat,lng,30)
        tourist_spot_dist, tourist_spot_mean_dist = get_shortest_point_and_mean(features_type_dfs,'tourist_spot',lat,lng,30)
        hospital_dist, hospital_mean_dist = get_shortest_point_and_mean(features_type_dfs,'hospital',lat,lng,30)

        X_input = [land_type, sqft, bhk]
        X_database = [tertiary_road_dist,tertiary_road_mean_dist,
          tertiary_link_dist,tertiary_link_mean_dist,
          secondary_road_dist,secondary_road_mean_dist,
          secondary_link_dist,secondary_link_mean_dist,
          primary_road_dist,primary_road_mean_dist,
          primary_link_dist, primary_link_mean_dist,
          trunk_road_dist, trunk_road_mean_dist,
          trunk_link_dist,trunk_link_mean_dist,
          college_dist, college_mean_dist,
          govt_institute_dist, govt_institute_mean_dist,
          hotel_dist,hotel_mean_dist,
          luxury_hotel_dist, luxury_hotel_mean_dist,
          prime_hotel_dist, prime_hotel_mean_dist,
          malls_dist,malls_mean_dist,
          schools_dist,schools_mean_dist,
          it_companies_dist, it_companies_mean_dist,
          tourist_spot_dist,tourist_spot_mean_dist,
          hospital_dist, hospital_mean_dist]
        # Combine the features into a single input array
        X_input = np.concatenate((X_input, X_database))
        X_input = X_input.reshape(1, -1)  # Reshape for model input
        X_input = X_input.astype(float)
        # Make prediction using the loaded model
        prediction = model.predict(X_input)
        app.logger.info(prediction)
        # Return the prediction as JSOÑ
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0',port=5001)
