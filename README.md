# Laboratory Exercise 3: 3D Computational Modeling: DEM-Vector Integration and GeoJSON Service Delivery

This laboratory extends Laboratory 2 from planar (2D) spatial analysis to true three-dimensional computational modeling. 

Unlike simple extrusion, this exercise constructs `LineString` geometries whose coordinates 
include a Z value ``(x, y, z)``. Z is derived by sampling elevation values from a DEM raster. 

## How to Run analysis.py

## Outputs expected in output/

## Commit Milestones and Reflections

### Reflection - Hybrid IO Milestone Reflection

*1. Why are roads retrieved from PostGIS instead of file?*

Because the roads dataset is in vector format and have a LineString geometry and can be natively stored in and retrieved from PostGIS.

*2. Why is the DEM loaded directly from a raster file?*

Because the DEM contains continuous elevation data within the pixels of the raster file.

*3. How does hybrid IO reflect real-world GIS architecture?*

It shows the reality of real-world GIS datasets generated and utilized in various sectors (public, private, and academe), wherein they are not produced using the same standards and formats making them non-uniform that requires a workaround for interoperability.

*4. Is spatial analysis occuring at this stage?*

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
Densification is necessary to create evenly spaced points at a specified sampling interval of a line segment from the road dataset to be used for sampling the elevation values. Ideally, the sampling interval should match the resolution of the reference raster so that no terrain variation will be missed. For the given case, the DEM has a resolution of 5m (may have been sourced from NAMRIA's IfSAR DEm) but the *SAMPLE_STEP* variable is set to 10m, which may have been set to limit the computational requirement of the exercise.

CRS alignment must be performed before sampling to ensure that the generated sampling points correspond exactly to the raster’s pixel coordinates. The function `sample_dem_z(x, y)` requires x and y coordinates that represent the spatial location of a raster pixel. These coordinates are derived from the raster’s row and column indices and are expressed in the raster’s coordinate reference system (CRS), whether geographic or projected. Therefore, the sampled road points must share the same CRS as the raster prior to sampling. If the CRS is not aligned, the x, y coordinates of the road points will not match the raster’s pixel grid, leading to incorrect elevation extraction.

Now that the road geometries contain Z values, they represent a true three-dimensional dataset rather than a purely visual 3D effect. The Z values are not arbitrary, they are directly extracted from the DEM and correspond to the actual elevation at each sampled location. These elevation values are then embedded into the geometry of each road segment, effectively linking the horizontal alignment (X, Y) with its vertical profile (Z). 