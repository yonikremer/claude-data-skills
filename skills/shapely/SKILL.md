---
name: shapely
description: Planar geometric manipulation and analysis using Shapely. Use for buffering, intersections, area/length calculations, and spatial predicates (contains, within, intersects).
---

# Shapely (Geometric Analysis)

Shapely is a Python library for manipulation and analysis of planar geometric objects. It's built on GEOS and is widely used for spatial analysis.

## Core Concepts

- **Geometries**: Point, LineString, Polygon, and their Multi- variants.
- **Predicates**: Boolean operations that test relationships between geometries (e.g., `intersects`, `contains`, `within`).
- **Constructors**: Methods that create new geometries from existing ones (e.g., `buffer`, `intersection`, `union`).

## Quick Start: Common Workflows

### 1. Geometry Creation
```python
from shapely.geometry import Point, LineString, Polygon

# Create geometries
p = Point(0, 0)
line = LineString([(0, 0), (1, 1)])
poly = Polygon([(0, 0), (1, 1), (1, 0)])
```

### 2. Spatial Relationships (Predicates)
```python
# Check if point is within polygon
if p.within(poly):
    print("Point is inside polygon")

# Check if two geometries intersect
if line.intersects(poly):
    print("Line and polygon have common points")
```

### 3. Buffering and Unions
```python
# Create a buffer around a line
buffered_line = line.buffer(0.5)

# Calculate union of two polygons
unified_poly = poly.union(other_poly)
```

## Strict Idioms

- **Check Validity**: Always check if a geometry is valid: `geom.is_valid`.
- **Coordinate Order**: Shapely uses (x, y) or (long, lat) order. Ensure consistency.
- **Floating Point Precision**: Be aware of precision issues with spatial operations.

## Advanced Operations

- **Spatial Analysis Reference**: See [shapely-common-ops.md](references/shapely-common-ops.md) for a comprehensive list of predicates, constructors, and measurements.

## Common Pitfalls

- **Incorrect Order**: Using (lat, long) instead of (long, lat).
- **Self-Intersecting Polygons**: Polygons must be simple and valid. Use `geom.is_valid` and `make_valid()` if needed.
- **Ignoring Units**: Buffer distance units depend on the coordinate system.
