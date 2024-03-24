---
layout: post
title: Marching Cubes and Co
date: 2024-03-12 07:00:00 +0200
tags: [cs]
# excerpt_separator: <!--more-->
---

The field of computer graphics contains some very nice and insightful algorithms. I wish I had explored them earlier, but it's still not that late. This post describes *marching cubes* - a ultra-simple algorithm for the extraction of a triangular mesh from a 3D field. This algorithm is widely applicable in all kinds of graphics applications, whether it is volumetric rendering of CT scans in healthcare, or tunnel/cave mapping in an industrial setting. It also combines well with the growingly-popular deep learning NeRF models. There it can be used to render a mesh from the 3D reconstruction.

Marching cubes is not the only clever algorithm worth knowing. We'll start with some basic 3D structures and then move to the volumetric stuff, where marching cube reigns.

Consider point clouds as a relatively simple 3D data structure. A point cloud can be represented as a matrix of shape $(N, 3)$ - $N$ 3-dimensional points, each representing particular $(x, y, z)$ location. Just by looking at these numbers we can get a pretty good sense of the geometry of the scene, especially if the number of points is sufficiently large. Apart from the location, we can also have additional per-point parameters, like color, opacity, or a normal vector. These are stored into specialized file formats such as `.pcd` or `.ply`.

Representing a bunch of points simply as a big matrix is a terrible idea for most purposes. We need specialized data structures, and the octree and k-d trees come to the rescue. An octree is a tree in which every internal node has exactly eight children. It is used to partition the space into 8 octants for easier searching. To build an octree we start with a single giant voxel covering all points. We then split it into 8 non-overlapping octants. Now, we keep subdiving those octants which have more than one point within them, until they have zero or one inside. The larger octants are not subdivided. In such a way a big tree is populated, whose internal nodes can have at most eight children. To insert a new point we start from the root node and progressively navigate down the branches until we find its new place. Searching is handled similarly.
 



<!-- The algorithm itself is pretty simple. We are given a volumetric data array of shape $(X, Y, Z)$, with all real numbers.  -->