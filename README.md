# Laboratory Exercise 3: 3D Computational Modeling: DEM-Vector Integration and GeoJSON Service Delivery

This laboratory extends Laboratory 2 from planar (2D) spatial analysis to true three-dimensional computational modeling. 

Unlike simple extrusion, this exercise constructs `LineString` geometries whose coordinates 
include a Z value ``(x, y, z)``. Z is derived by sampling elevation values from a DEM raster. 

## How to Run analysis.py

1. Install `requirements.txt`
2. Activate virtual environment
3. Run analysis.py in terminal to implement the sampling, elevation embedding, and write output in ***output/*** folder

```bash
python server/analysis.py
```

4. Inspect outputs and interpret

## Outputs expected in output/
- road_sample_points.shp (with extensions)
- roads_3d.geojson (road dataset with elevation values)
- 3D_Roads.html (with dependencies)

## Commit Milestones and Reflections

### Reflection - Hybrid IO Milestone Reflection

**1. Why are roads retrieved from PostGIS instead of file?**

Because the roads dataset is in vector format and have a LineString geometry and can be natively stored in and retrieved from PostGIS.

**2. Why is the DEM loaded directly from a raster file?**

Because a DEM is a raster dataset containing continuous elevation values stored in pixels. It is typically distributed and processed as a raster file, where each cell represents a measured elevation value.

**3. How does hybrid IO reflect real-world GIS architecture?**

It reflects real-world GIS environments where datasets come from different sources, sectors, formats, and standards. Vector data may reside in databases, while raster data may exist as files. This mixed setup requires interoperability strategies to integrate them into a unified workflow (such as using Python for transforming them to uniform objects).

**4. Is spatial analysis occuring at this stage?**

Not yet. This is the preliminary phase before performing any spatial analysis by ensuring that the datasets are loaded into objects in-memory through Python so that they can be interoperable and analyzed consistently.

### Checkpoint - Densification Validity
The quick test of the sampling function printed out the output below.

```bash
Sample points: 8 Line length: 66.12778958136872
```

This means that there were 8 points sampled from the test line segement with a length of appx. 66.13 meters at 10m interval.

### Optional Verification Step - Visualizing Densified Vertices in QGIS

The sampling of the entire road dataset yielded a total of 32,967 points. These points overlaps with the given DEM file. The generation of these points is in preparation of sampling of the elevation values from the DEM.

### Reflection - 3D Geometry Construction Milestone
Densification is necessary to create evenly spaced points at a specified sampling interval of a line segment from the road dataset to be used for sampling the elevation values. Ideally, the sampling interval should match the resolution of the reference raster so that no terrain variation will be missed. For the given case, the DEM has a resolution of 5m (may have been sourced from NAMRIA's IfSAR DEm) but the *SAMPLE_STEP* variable is set to 10m, which may have been set to limit the computational requirement of this exercise.

CRS alignment must be performed before sampling to ensure that the generated sampling points correspond exactly to the raster’s pixel coordinates. The function `sample_dem_z(x, y)` requires x and y coordinates that represent the spatial location of a raster pixel. These coordinates are derived from the raster’s row and column indices and are expressed in the raster’s coordinate reference system (CRS), whether geographic or projected. Therefore, the sampled road points must share the same CRS as the raster prior to sampling. If the CRS is not aligned, the x, y coordinates of the road points will not match the raster’s pixel grid, leading to incorrect elevation extraction.

Now that the road geometries contain Z values, they represent a true three-dimensional dataset rather than a purely visual 3D effect. The Z values are not arbitrary, they are directly extracted from the DEM and correspond to the actual elevation at each sampled location. These elevation values are then embedded into the geometry of each road segment, effectively linking the horizontal alignment (X, Y) with its vertical profile (Z). 

### Required questions
**1. What is preserved when you export 3D geometry to GeoJSON?"**
The coordinate structure of the LineString with a Z value is preserved. As seen in the sample feature below.

```bash
{ "type": "Feature", "properties": { "gid": 1 }, "geometry": { "type": "LineString", "coordinates": [ [ 514943.255081939219963, 1632663.7, 49.0 ], [ 514941.525835616339464, 1632653.850649404339492, 48.0 ], [ 514939.885091927368194, 1632643.98762452439405, 47.414176918570597 ], [ 514938.713218622142449, 1632634.061530400067568, 47.333333333333336 ], [ 514938.475325483130291, 1632624.071113689802587, 47.0 ], [ 514938.958810571697541, 1632614.086963248904794, 46.828353837141186 ], [ 514940.057878021034412, 1632604.151088275713846, 47.0 ], [ 514940.881107475375757, 1632598.078848292119801, 46.906207521522433 ] ] } }
```

**2. What is lost or not formally expressed?**

The Coordinate Reference System (CRS) is not formally preserved in standard GeoJSON. GeoJSON assumes WGS84 by default and does not explicitly store CRS metadata, so projection information may be lost if not documented separately.

**3. Why does GeoJSON still label the geometry as "LineString" even when Z exists? What does this tell you about the difference between data content and data standard?**

GeoJSON still labels the geometry as "LineString" because the geometry type refers to its structure (a connected set of points forming a line), not the number of coordinate dimensions.

Even though we Z values were added using the script below:
```bash
roads_3d = []
for geom in roads.geometry:
    ...
    roads_3d.append(LineString(coords_3d) if len(coords_3d) >= 2 else None)
```

This means geometry is still a line, just with 3D coordinates (x, y, z) instead of (x, y). Data content refers to the actual values stored, in this case, the presence of Z values representing elevation. Data standard, on the other hand, refers to how the data is formally structured and labelled according to a specification (e.g., OGC Standards)


**4. How does this affect visualization in QGIS 3D View? Does QGIS treat this as true 3D geometry or as 2.5D visualization?**

In the normal 2D map canvas, the original roads and the 3D roads look identical because QGIS only renders the X and Y coordinates in plan view. The Z values are stored in the geometry but are not visually expressed in 2D. However, in the 3D environment (such as Qgis2threejs), QGIS reads and uses the embedded Z values. This means the roads are rendered using their actual elevation coordinates, not just draped over a surface.

The original roads dataset (without Z) would be displayed as 2.5D since the elevation is derived from a DEM during visualization.

The updated roads dataset (with Z values embedded) is treated as true 3D geometry, since it is displays the topographic variation when compared to the 2d road data.

**5. If you had to preserve 3D semantics more explicitly, what alternative outputs would you consider?**

To preserve 3D semantics more explicitly, I would consider all the given options depending on my application. GeoPackage supports 3D geometries and is portable, but it remains file-based and limited for multi-user workflows. PostGIS supports true 3D geometry types (e.g., LINESTRING Z, POLYGON Z), spatial indexing, and advanced 3D functions, though it requires database management. 3D Tiles and glTF are optimized for high-performance 3D visualization and for web visualization, but they are not designed for spatial analysis.

Overall, I prefer PostGIS storage because it preserves true 3D geometry while supporting robust spatial analysis and scalable, enterprise-level data management.