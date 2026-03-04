import geopandas as gpd
from sqlalchemy import create_engine
import rasterio

# Database connection parameters
host = "localhost"
port = "5432"
dbname = "gme221_exer3"
user = "ajdcc"
password = "gme221_db"

conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(conn_str)

# Minimal SQL Query (no spatial processing)
sql_roads = "SELECT gid, geom FROM public.roads"

roads = gpd.read_postgis(sql_roads, engine, geom_col="geom")

# The SRID of the geometry from PostGIS is already in 3123
roads = roads.set_crs(epsg=3123, allow_override=True)

# print(roads.head())
# print(roads.crs)
# print(roads.geometry.type.unique())

# Load DEM data
dem = rasterio.open("data/dem.tif")

print("DEM CRS:", dem.crs)
print("DEM Resolution", dem.res)
print("DEM Bounds:", dem.bounds)