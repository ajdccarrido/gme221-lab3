import geopandas as gpd
from sqlalchemy import create_engine
import rasterio
from shapely.geometry import LineString, MultiLineString
import numpy as np

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

# print("DEM CRS:", dem.crs)
# print("DEM Resolution", dem.res)
# print("DEM Bounds:", dem.bounds)

SAMPLE_STEP = 10 # meters (adjust later for sensitivity)

def densify_line(line: LineString, step: float):
    """Return points sampled along a line at a fixed distance spacing."""
    if line.length == 0:
        return []
    
    distances = list(range(0, int(line.length), int(step)))
    pts = [line.interpolate(d) for d in distances]
    pts.append(line.interpolate(line.length))
    return pts

def explode_to_lines(geom):
    if geom is None:
        return []
    if geom.geom_type == "LineString":
        return [geom]
    if geom.geom_type == "MultiLineString":
        return list(geom.geoms)
    return []

all_sample_points = [] 
for geom in roads.geometry: 
    parts = explode_to_lines(geom) 
    for line in parts: 
        pts = densify_line(line, SAMPLE_STEP) 
        for pt in pts: 
            all_sample_points.append(pt)

gdf_samples = gpd.GeoDataFrame(geometry=all_sample_points, crs=roads.crs)

# gdf_samples.to_file("output/road_sample_points.shp")
# print("Densified sample points exported")

band1 = dem.read(1) # read once
nodata = dem.nodata

def sample_dem_z(x, y):
    row, col = dem.index(x, y)
    z = band1[row, col]
    if nodata is not None and z == nodata:
        return None
    if np.isnan(z):
        return None
    return float(z)

roads_3d = []

for geom in roads.geometry:
    parts = explode_to_lines(geom)
    if not parts:
        roads_3d.append(None)
        continue

    line = parts[0] # simplest: first part if MultiLineString
    pts = densify_line(line, SAMPLE_STEP)

    coords_3d = []
    for pt in pts:
        z = sample_dem_z(pt.x, pt.y)
        if z is None:
            continue
        coords_3d.append((pt.x, pt.y, z))

    roads_3d.append(LineString(coords_3d) if len(coords_3d) >= 2 else None)

roads["geom_3d"] = roads_3d

print("3D lines created:", roads["geom_3d"].notna().sum(), "/", len(roads)) 

valid_3d = roads["geom_3d"].dropna() 
print("3D geometries created:", len(valid_3d), "/", len(roads)) 

# Verify Z exists (third coord) 

first = valid_3d.iloc[3] 
print("First 3D coord sample:", list(first.coords)[0]) 