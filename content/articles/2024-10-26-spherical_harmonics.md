---
Title: Spherical Harmonics
Date: 2024-10-26 07:00:00 +0200
Tags: cs
slug: spherical_harmonics
---

Spherical harmonics are a nice little mathematical tool that has found big applications in computer vision for modeling view-dependent light. The first time I encountered them was in the [Plenoxels](https://arxiv.org/abs/2112.05131) paper and I've been meaning to explore them ever since. Apart from the mathematics, there's not much to worry about, it's actually quite pleasant.

We start with some motivation from computer graphics. Consider that, due to light being directional, in 3D we can think of the incoming and outgoing light directions as points on a unit sphere. The rendering equation defines the radiance at a surface point $\mathbf{p}$ that goes out in direction $\mathbf{v}$. It consists of the emitted light from point $\mathbf{p}$ in that direction, summed with the reflected light towards $\mathbf{v}$ from all incoming directions:

$$
L_{\text{out}}(\mathbf{p}, \mathbf{v}, \lambda) = L_{\text{emit}}(\mathbf{p}, \mathbf{v}, \lambda) + \int_\Omega \text{BRDF}(\mathbf{p}, \mathbf{s}, \mathbf{v}, \lambda) L_{\text{in}}(\mathbf{p}, \mathbf{s}, \lambda) (\mathbf{n}^T \mathbf{s}) d\mathbf{s}.
$$

Here $\lambda$ is the wavelength, $\Omega$ is the hemisphere of all incoming directions $\mathbf{s}$, $\mathbf{n}$ is the surface normal at point $\mathbf{p}$, and the BRDF controls the precise way in which light is reflected. Diffuse surfaces reflect light uniformly in all directions, while specular surfaces reflect in a mirror-like way. Most natural surfaces have both a specular and a diffuse component.

In radiometry, the [radiance](https://en.wikipedia.org/wiki/Radiometry), or the emitted electromagnetic energy, is also measured in a directional way. The total power of light emittance by a physical object is called *radiant flux*. If we differentiate it with respect to direction, we get *radiant intensity*. If we further differentiate it by its surface area, we get radiance. Thus, when it comes to waves, it is important to be able to model directionally-dependent quantities.

In vision, when reconstructing 3D scenes, for example using [neural radiance fields](https://en.wikipedia.org/wiki/Neural_radiance_field), it is common to have the network model a function like $(\mathbf{p}, \theta, \phi) \mapsto \mathbf{c}$. If we only predict the RGB color $\mathbf{c}$ from the point coordinates $\mathbf{p}$, without consider the viewing direction $(\theta, \phi)$, then the point will look the same from all directions, which may be unrealistic. Thus, usually we condition the generated color to depend on the viewing direction. Spherical harmonics are a different way to achieve this.

The Laplacian of a function $f(x, y)$ is given by $\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$. Any function $f$ for which $\nabla^2 f = 0$ is called a harmonic. This property entails a certain smoothness to the function. To see why, consider the Laplacian operator applied on images, in which case it's called the Laplacian filter. It looks like the following convolution kernel.

$$
\begin{pmatrix}
0 & -1 & 0 \\
-1 & 4 & -1 \\
0 & -1 & 0
\end{pmatrix} \text{ or } 
\begin{pmatrix}
-1 & -1 & -1 \\
-1 & 8 & -1 \\
-1 & -1 & -1
\end{pmatrix}
$$

It takes the difference between the value at the central point and the average value of the surrounding points. When scanning it along an image, it produces a peak whenever a change in intensity is detected. Intuitively, this Laplacian is equal to zero whenever the central value is exactly equal to the average of the surrounding values. In that regard, the function is smooth.

Spherical harmonics are harmonic functions defined on the surface of a sphere. Naturally, they are smooth. They do not have any isolated local maxima (or similarly minima). This means that there is no point $x^*$ on the sphere where the harmonic has a local maximum (there exists a small neighborhood around $x^*$ where the values are all smaller than the value at $x^*$) that is also unique in attaining this value across the whole domain. For example, the function $sin(x)$ has a local maximum at $\pi/2$ but it is not isolated, because there are other local maxima at $\frac{5\pi}{2}, \frac{9\pi}{2}, ...$ which attain the same value.

With spherical harmonics there are no isolated local extema. There may be local maxima and minima, but they are not isolated. Any increase in the function needs to be offset by a decrease somewhere else. An intuitive way to think about this is through the Laplacan filter kernel for 2D images. The versions presented above are $3\times3$, but we can extend them to $5\times5$ and beyond:

$$
\begin{pmatrix}
0 &	0	&	-1	&	0	&	0 \\
0	&	-1	&	-2	&	-1	&	0 \\
-1	&	-2 & 16	&	-2	&	-1 \\
0	&	-1	&	-2	&	-1	&	0 \\
0	&	0	&	-1	&	0	&	0 \\
\end{pmatrix}.
$$

This filter is just a better approximation of the Laplacian compared to the $3\times3$ one. If we imagine an even bigger one, it becomes clear that it is entirely possible to have a high-value region within the neighborhood, as long as there are also points somewhere in it that are sufficiently negative so as to balance it out.

Figure 1 shows a few spherical harmonics (only their real part really). Each of them has specific *degree* and *order* parameters. The order, called $m$, represents the number of waves we can count if we trace the sphere horizontally along a constant latitude. If $m=0$, the harmonic has no variation along the longitude and is symmetric around the polar axis. The degree, typically called $\ell$, represents the number of latitude (horizontal) variations or bands that the function will have. If we trace the values on a line from one pole to the other, it will have $\ell - |m|$ zero-crossings. A particular harmonic is written as $Y_l^m$.


<figure>
    <img class='big_img' src="/images/sh1.png" alt="Spherical harmonics" width="1200">
    <figcaption>Figure 1: Spherical harmonics from degree one to degree three. Only the real part is shown. Red regions are positive, blue are negative, white is close to zero. Colors are normalized independently for each harmonic and cannot be compared between different harmonics.</figcaption>
</figure>
