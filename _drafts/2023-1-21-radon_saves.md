---
layout: post
title: Radon Saves
date: 2023-01-21 07:00:00 +0200
tags: [cs]
# excerpt_separator: <!--more-->
---

Have you ever wondered how computed tomography (CT) scans work? How is it possible that by blasting some "lasers" in the direction of a person's head we can determine with impressive accuracy the intricate geometry and shape of the person's brain? CT scans offer a unique curious mathematical problem and represent, in my opinion, one of the most interesting topics in applied math. This post explores the main mathematical contraption involved - the Radon transform - and how it's used to recover distinct 2D images from aggregated signals.

Tomography is the process of obtaining a visual representation of an object from multiple individual slices from it. It allows for the construction of realistic 3D models whose individual components have the correct proportions and high resolution of details. It is used extensively in healthcare and medical applications where it's able to provide invaluable information about the state and shape of the patient's internal organs.

Computed tomography, also called computerized tomography is a technique to do tomography from X-ray slices. The CT scanner consists of the following main components:
- An X-ray tube which converts electricity into X-ray waves. It shoots out X-rays into a fairly wide sector and is able to rotate around the object of interest, so that the waves can penetrate the object from all directions.
- Multiple X-ray detectors located on the other side of the X-ray generators. They are able to capture the X-rays and measure how attenuated they are. As the X-rays travel through tissue they gradually lose their intensity (calculated as the flux of the wave divided by the period), depending on the type of materials they pass through. The X-rays start with high intensity, travel through the medium and go through it with significantly less energy. The detectors measure the difference in energy - how attenuated the rays are. This gives some information on the density of the material that the rays have gone through.
- A gantry which holds the X-ray generator and the detectors. This is typically a moving and rotating frame where the components are attached. By rotation and moving different axial (horizontal), sagittal (longitudinal) or coronal (frontal) slices can be obtained.

The main aspect of theoretical interest is that, for each X-ray, the detector in which it falls, captures the total loss of energy of the ray. Thus from a single measurement we cannot determine where exactly the energy decreased most, how many different types of tissues it went through, and what they different densities were. In a sense, what we only see is the sum aggregated from many interactions. The question is how we can reconstruct the inner geometry of the medium from these aggregates - a difficult inverse problem.

For the sake of discussion, suppose the real image of the given slice is given by the function $f(\textbf{x}) = f(x, y)$, where $x$ and $y$ are the spatial coordinates. A single X-ray travels as a line $L$ and, simplifying a bit, we observe the integral of the function across that line

$$
Rf(L) = \int_L f(\textbf{x}) |d\textbf{x}|
$$

This is actually a transform - a higher order object that takes in functions in one domain and maps them to functions in another. Here the input is a function $f(x, y)$ taking in spatial coordinates $x$ and $y$ and the output is a function from the space of all lines to the reals. More concretely this function takes in a concrete line, and returns the integral of $f(x, y)$ across this line. This transform is called the Radon transform and is central to the topic of computerized tomographies:

$$
R: (f: X \times Y \rightarrow \mathbb{R}) \rightarrow (f': L \rightarrow \mathbb{R})
$$

We can define a line using the equation $x \cos \phi + y \sin \phi = r$. This corresponds to a line that is perpendicular to the one going through the origin at an incline of $\phi$, and has a distance to the origin of $r$. In particular varying the tuple $(\phi, r)$ can produce all lines in the two-dimensional space.

The tuple $(\phi, r)$ also defines a point on the circle with radius $r$. The $x$ and $y$ coordinates of the tangent line at that point can be parameterized as

$$
\begin{bmatrix}
z \sin \phi + r \cos \phi \\
 -z\cos \phi + r \sin \phi
\end{bmatrix}
$$

Here $z$ is the distance from the tangent point with coordinates $(r\cos \phi, r \sin \phi)$. If $z$ is 0, we get the tangent point, if z is not zero we move along the tangent line.

With these parametrizations we can write the Radon transform as

$$
g(\phi, r) = \iint f(x, y) \delta(x \cos \phi + y \sin \phi - r) dx dy.
$$

That is, integrate over all of $x$ and $y$, but null out the value if not on the line defined by $(\phi, r)$.

Similarly, this is equivalent to moving along the line directly and integrating only the points on it

$$
g(\phi, r) = \int_{-\infty}^\infty f(x(z), y(z)) dz = \int_{-\infty}^\infty f(z \sin \phi + r \cos \phi, -z\cos \phi + r \sin \phi) dz.
$$

So how might we compute Radon transform for a given image $f(x, y)$?
1. First, the image has to be padded to a square. This is easily achieved by adding zero rows and columns such that the the non-zero pixels of the actual image stay roughly in the center of the resulting square image.
2. Create an array of $N$ angles for the lines - $(\phi_1, \phi_2, ..., \phi_N)$. These should span the range from 0 to 180 degrees.
3. Initialize an array to store the Radon transform results. This should have as many rows as the padded image and as many columns as the angles.
4. For each of the angles, rotate the image by that amount.
The rotation can be achieved by using a similarity matrix. The translations in the third column ensure that the centre $(c_x, c_y)$ does not change when rotating. Then, sum the pixel intensities across the rows and store the aggregated values in the corresponding column in the Radon array.

$$
\begin{bmatrix}
\cos \phi & -\sin \phi & c_x(1-\cos\phi) + c_y \sin \phi\\
\sin \phi & cos \phi & c_y(1 - \cos \phi) - c_x \sin \phi\\
0 & 0 & 1\\
\end{bmatrix}
$$

At the end we are left with a matrix containing the integrals for the various $(\phi, r)$ lines, where $\phi$ angles has been defined manually and the distances $r$ comes from the pixels along the side of the image.

<!-- Image taken from here https://commons.wikimedia.org/wiki/File:CT_of_a_normal_brain,_axial_17.png -->

<!-- % We start with a circle of radius $r$. If we fix an angle $\phi$, this defines a point $P$ on the circle with coordinates $(r \cos \phi, r \sin \phi)$. Any point in 2D can be defined using a combination of $(r, \phi)$, where $r$ is the distance of the point to the origin and $\phi$ is the angle between the vector $(r \cos \phi, r \sin \phi)$ and the $x$-axis. -->
