# Laboratory Exercise 3: 3D Computational Modeling: DEM-Vector Integration and GeoJSON Service Delivery

This laboratory extends Laboratory 2 from planar (2D) spatial analysis to true three-dimensional computational modeling. 

Unlike simple extrusion, this exercise constructs `LineString` geometries whose coordinates 
include a Z value ``(x, y, z)``. Z is derived by sampling elevation values from a DEM raster. 

## How to Run analysis.py

## Outputs expected in output/

## Commit Milestones and Reflections

### C.4. Reflection - Hybrid IO Milestone Reflection

*1. Why are roads retrieved from PostGIS instead of file?*

Because the roads dataset is in vector format and have a LineString geometry and can be natively stored in and retrieved from PostGIS.

*2. Why is the DEM loaded directly from a raster file?*

Because the DEM contains continuous elevation data within the pixels of the raster file.

*3. How does hybrid IO reflect real-world GIS architecture?*

It shows the reality of real-world GIS datasets generated and utilized in various sectors (public, private, and academe), wherein they are not produced using the same standards and formats making them non-uniform that requires a workaround for interoperability.

*4. Is spatial analysis occuring at this stage?*

Not yet. This is the preliminary phase before performing any spatial analysis by ensuring that the datasets are loaded into objects in-memory through Python so that they can be interoperable and analyzed consistently.