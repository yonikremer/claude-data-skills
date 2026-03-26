# Shapely Common Operations Reference

## 1. Geometry Creation
- **Point**: `Point(0, 0)`
- **LineString**: `LineString([(0, 0), (1, 1)])`
- **Polygon**: `Polygon([(0, 0), (1, 1), (1, 0)])`
- **MultiPoint**: `MultiPoint([(0, 0), (1, 1)])`
- **MultiLineString**: `MultiLineString([[(0, 0), (1, 1)], [(2, 2), (3, 3)]])`
- **MultiPolygon**: `MultiPolygon([Polygon([(0, 0), (1, 1), (1, 0)]), ...])`

## 2. Geometric Relationships (Predicates)
- `geom1.intersects(geom2)`: True if the two geometries have any point in common.
- `geom1.contains(geom2)`: True if geom2 is completely inside geom1.
- `geom1.within(geom2)`: True if geom1 is completely inside geom2.
- `geom1.touches(geom2)`: True if the two geometries have at least one point in common, but their interiors do not intersect.
- `geom1.crosses(geom2)`: True if the two geometries have some, but not all, interior points in common.
- `geom1.disjoint(geom2)`: True if the two geometries have no points in common.

## 3. Geometric Analysis (Constructors)
- `geom.buffer(distance)`: Returns a representation of all points within a given distance of the geometric object.
- `geom1.intersection(geom2)`: Returns the intersection of two geometries.
- `geom1.union(geom2)`: Returns the union of two geometries.
- `geom1.difference(geom2)`: Returns the difference of two geometries.
- `geom1.symmetric_difference(geom2)`: Returns the symmetric difference of two geometries.
- `geom.centroid`: Returns the geometric center of the object.
- `geom.representative_point()`: Returns a point that is guaranteed to be inside the geometry.

## 4. Measurement
- `geom.area`: Returns the area of the geometry.
- `geom.length`: Returns the length of the geometry.
- `geom.bounds`: Returns the bounding box (minx, miny, maxx, maxy).
- `geom.distance(other_geom)`: Returns the shortest distance between two geometries.
