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

Representing a bunch of points simply as a big matrix is a terrible idea for most purposes. We need specialized data structures, and the octree and $k$-d trees come to the rescue. An octree is a tree in which every internal node has up to eight children. It is used to partition the space into 8 octants for easier searching. To build an octree we start with a single giant voxel covering all points. We then split it into 8 non-overlapping octants. Now, we keep subdiving those octants which have more than one point within them, until they have zero or one inside. The larger octants are not subdivided. In such a way a big tree is populated, whose internal nodes can have at most eight children. To insert a new point we start from the root node and progressively navigate down the branches until we find its new place. Searching is handled similarly.

Octrees are the 3D variant of quadtrees. A quadtree divides 2D space into quadrants and subquadrants, representing the points as leaf nodes in a tree whose internal nodes can have at most four children. For both quadtrees and octrees the insertion and deletion of a single element have complexities $O(\log n)$ where $n$ is the number of nodes. 

K-D trees are similar data structures but with some differences. A $k$-d tree is a binary tree and each internal node can have at most two children. At every internal node the points are split according to one coordinate axis - $x$, $y$, or $z$, much like in a decision tree. To create one of these trees we start with the points, choose one axis, e.g. $x$, and split at the median $x$-coordinate of the points we have to insert. Half the points will be to the left of this node, and half to the right. We call the constructor recursively to further split each half until a desired number of points, perhaps one, falls within each subdivision. Search, insertion and deletion are all $O(\log n)$.

One particular strenght of both the octree and the $k$-d tree is the ability to find nearest neighbors efficiently. To find the nearest neighbor of a query point $p$, we follow the branches according to $p$'s location until we reach a leaf node. Its distance to $p$ is the current minimal distance. Then, we start backtracking up the tree. At each of the internal nodes we compare the distance between $p$ and the splitting value. If it is larger than the current minimal distance, there's no point in searching the corresponding branch. If it is smaller, then there may be a leaf node that is closer than our current estimate, in which case we have to search that branch. The search ends once we reach the root.

<figure>
    <img class='small_img' src="/resources/octree.png" alt="Octree spatial representation" width="1200">
    <figcaption>Figure 1: 3D space divided according to an octree. There are only 5 points, shown by the black octants which they occupy. The tree depth is 5 levels. Notice how recursively dividing the octants produces unoccipied regions. </figcaption>
</figure>


Being able to efficiently calculate closest points allows us to calculate the Chamfer distance between two point clouds. It is given by the symmetric average distance between a point from the first cloud and its nearest neighbor in the other one. It is a fundamental metric used when registering or generating point clouds. It has wide applications for example in autonomous vehicles where [generative models predict future Lidar clouds](https://arxiv.org/abs/2311.01017) conditional on vehicle motion.

What else can we do with point clouds? There are various options. One can:
- Downsample the points by bucketing them into regularly-placed voxels and averaging all points within each voxel. This has the effect of filtering out noisy points.
- Estimate vertex normals by looking at the neighborhood of each point and computing a principal axis based on the covariance of the points in that neighborhood.
- Crop the point cloud, calculate a bounding box or a [convex hull](https://en.wikipedia.org/wiki/Convex_hull) around it.
- Cluster the points into semantically meaningful groups or do plane segmentation to find a 3D plane with maximal number of points lying on it. This is commonly done with [RANSAC](https://en.wikipedia.org/wiki/Random_sample_consensus) - that famous absurdly simple, absurdly robust line-fitting algorithm. 

Now consider triangle meshes. They consist of $N$ three-dimensional vertices, perhaps stored in an array of shape $(N, 3)$, and $M$ faces, which connect the vertices into cohesive surfaces. The faces can be stored in a matrix of shape $(M, 3)$ where the $i$-th row contains the indices for the three vertices defining the $i$-th face. What can we do with such a mesh? We can:
- Crop, paint, or visualize it. In practice, visualisation looks nicely only with *shading* enabled, which requires surface normals in order to calculate how much light falls on each surface region, based on its orientation with respect to the light source.
- Filter the surface "roughness" by averaging the vertices in a neighborhood, as given by the connectivity of the mesh. This can make surfaces smoother, but some filters based on this principle, like the Laplacian, can have the problem of thinning the surface too much.
- Sample a point cloud from the mesh. Simple methods like uniform sampling from the vertices may result in some points being clustered. To address this, other methods like Poisson disk sampling can be used.
- Do mesh simplification. This means reducing the number of vertices and faces while keeping the mesh detail quality as high as possible. A simple method here could be just to average the vertices falling in a given voxel.

Figure 2 visualizes various characteristics of the mesh like depth, normals, and different shading settings. Note that a triangle face normal is useful in telling us how the face is oriented in 3D. If the shading uses face normals, then it can either apply a constant shade to the whole face - [flat shading](https://en.wikipedia.org/wiki/Shading#Flat_shading), or it can evaluate the colors in two neighboring face centers or vertices and interpolate colours/shades in between - [Gouraud shading](https://en.wikipedia.org/wiki/Gouraud_shading). The former produces discontinuous colors along continuous viewed surfaces, while the latter may produce unrealistic visual artefacts. A slightly more expensive solution is the [Phong shading](https://en.wikipedia.org/wiki/Phong_shading) where instead of interpolating colours we interpolate vertex normals. This produces excellent visual results. A separate topic is whether one uses specular reflection in the lightning. The combination of using both a diffuse and specular reflection is called the [Phong reflection model](https://en.wikipedia.org/wiki/Phong_reflection_model).

<figure>
    <img class='extra_big_img' src="/resources/mesh.png" alt="Mesh visualisation" width="1200">
    <figcaption>Figure 2: Various mesh renderings. 3D object taken from the <a href="https://objaverse.allenai.org/">Objaverse dataset</a>. Top row, left to right: 1. A seashell, rendered with specular lightning, textures, and smooth shading; 2. Same, but with flat shading; 3. Only diffuse lightning with textures; 4. Triangle mesh overlay. Bottom row, left to right: 1. No shading; 2. Coloring based on the x-coordinate of each point; 3. Normals, visualized as RGB colors; 4. Depth map. </figcaption>
</figure>






 



<!-- The algorithm itself is pretty simple. We are given a volumetric data array of shape $(X, Y, Z)$, with all real numbers.  -->