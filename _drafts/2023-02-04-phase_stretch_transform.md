---
layout: post
title: The Phase Stretch Transform
date: 2023-02-04 07:00:00 +0200
tags: [cs]
# excerpt_separator: <!--more-->
---

I have recently discovered [PhyCV](https://github.com/JalaliLabUCLA/phycv) - an awesome new physics-inspired computer vision library. It contains refreshing new algorithms for various imaging tasks, all of them with a physical justification. This post explores one of these - the phase stretch transform (PST), which can be used to detect edges and corners, or enhance even the faintest visual features in images from poorly-lit environments. It's a very clever technique and getting to know how it works also yields, as a benefit, some basic knowledge in topics like Fourier optics and wave propagation.

In general, the phase stretch transform builds on top of other ideas which one should understand. The most basic of these is the notion of a wave - a disturbance that is being propagated through space and time in a given medium. There are many types of waves - acoustic waves, mechanical waves and electromagnetic waves being a few of them. One of the simplest waves is the sine wave, modelled as

$$
\Psi(x, t) = A \sin (k x - \omega t + \phi).
$$

Here $x$ is a spacial one-dimensional variable and $t$ is a temporal variable. $A$ is called the *amplitude* of the wave and shows the magnitude of the wave. In the case of acoustic waves, this would be air pressure. In the case of water waves (a type of mechanical waves) the amplitude may be the current height of the wave, as measured from the average. In general the magnitude may depend on the position $(x, t)$. Everything within the sine function is called the *phase* and affects the spacio-temporal positioning of the wave. The parameter $k$ is the wavenumber - a measure of the spatial frequency - and $\omega$ is the temporal frequency affecting how fast the wave at a fixed space position repeats in time. $\phi$ is called the phase shift because it further shifts the wave without changing its frequencies.

It is useful to represent waves mathematically using complex numbers:

$$
\Psi(x, t) = A e^{i(kx - \omega t + \phi)} = A \cos(kx - \omega t + \phi) + i A \sin(kx - \omega t + \phi).
$$

For a wave with fixed parameters $(k, \omega, \phi)$ evaluating it at a position $(x, t)$ requires two numbers, the amplitude and the phase, and conveniently, these can be represented as a single complex number. As per [Euler's formula](https://en.wikipedia.org/wiki/Euler%27s_formula), the complex exponential form is just a more convenient way to represent the sum of a cosine and a complex sine. Additionally transforming the point $(A\cos(kx - \omega t + \phi), A\sin(kx - \omega t + \phi))$ from Cartesian to polar coordinates yields exactly the amplitude and the phase $(A, kx-\omega t + \phi)$. Note that the real component of the wave value serves to model actual *observable* quantities from the real world and the fact that it comes from a cosine is not problematic because the cosine function is just a phase-shifted sine.

<!-- Verify the above paragraph. -->

Various signals like audio samples or images can be considered as a superposition of many individual waves. And the Fourier transform, a tool that is ubiquitous in signal processing, can be used to disentangle the sum signal into its individual constituents. In that context, it is a very important insight that phases tend to carry more of the "useful" information, compared to amplitudes. This can be visualized easily using the two-dimensional Fourier transform applied on images.

Applying the 2D FFT on images works as follows. If the image is single-channel, with size $(H, W)$, we assume the spatial sampling frequency is 1.0 and therefore by [Nyquist](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem) the maximum spatial frequency we can capture is $0.5$. So the frequency bins for the height are $H$, spread linearly from $-0.5$ to $0.5$. Similarly, those for the width are $W$, spread from $-0.5$ to $0.5$. The FTT shows, for two particular frequencies along the image axes, how much of them is present in the image.

Figure 1 shows a classic experiment where we take the two-dimensional Fourier transform of one image, and reconstruct it with either the magnitude, or the phase, or both. In essence, the Fourier transform outputs a dense matrix of complex numbers. Their magnitudes, $\sqrt{x^2 + y^2}$, and phase angles, $\tan^{-1}(y/x)$, are plotted for visualization. The plot of the magnitudes is commonly called the Fourier *spectrum*. Applying the inverse 2D FFT on the magnitudes only produces an almost entirely dark image, whereas reconstructing from the phases produces the main contours of the objects from the original image.

<figure>
    <img class='big_img' src="/resources/fourier_reconstructions2.png" alt="Fourier reconstructions" width="1200">
    <figcaption>Figure 1: Various outputs from the Fourier transform. The input image is in the top left. The second and third images contains the magnitude and phase from the Fourier transform. The second row contains reconstructions using the inverse Fourier transform. The magnitude images have been log-scaled for visual clarity. When reconstructing from phases only, the absolute value of the real components are plotted for better contrast.</figcaption>
</figure> 

Reconstructing with the actual magnitudes and a set of random phases, or with the actual phases and a set of random magnitudes does not change the output noticeably. Or even mixing the magnitudes and phases of two different images will produce a blurry image with visible contours coming from the image from which the phases were taken. All of this shows that for visual signals, where most of human perception is based on edges, corners and contours, the phases of the waves are more important than the magnitudes.

This is the first hint that **by modifying the phases** we can change the shapes of the objects in the image and potentially **enhance any edges or visually impaired features**.

Additional insights can be gained by exploring how an electromagnetic pulse, like light, propagates in a dispersive medium, like a fiber. This will be useful to showcase how optical dispersion in fiber changes the phases of the waves. Wave propagation is a complicated topic and the cornerstone here is the following fundamental partial differential equation:

$$
i \frac{\partial A }{\partial z} + \frac{i \alpha}{2} A - \frac{\beta_2 }{2} \frac{\partial^2 A}{\partial t^2 } + \gamma |A|^2 A = 0.
$$

This equation is fundamental and deserves some explanation:
- We can imagine a one-dimensional horizontal fiber of length $L$. The variable $z$ is the spatial distance from the start of the fiber, and ranges from $0$ to $L$. The variable $t$ is the time and shows how various quantities change through time.
- Suppose the input signal is $f(t)$. As it travels through the fiber it's modified by various fiber characteristic effects into the output signal $y(t)$. Our main interest is in estimating what is $y(t)$ and how $f(t)$ changes into it.
- $A(z, t)$ is the amplitude of the signal at position $z$ and time $t$
- $\alpha$ is an *attenuation* parameter and is related to how much information is lost in the fiber. The entire term $i \alpha A /2$ represents the loss at the current amplitude,
- $\beta_2$ is called the [*group velocity dispersion* (GVD)](https://en.wikipedia.org/wiki/Group_velocity_dispersion) parameter. It relates to how the pulse travelling through the fiber broadens due to [dispersion](https://en.wikipedia.org/wiki/Dispersion_(optics)). This happens because in a dispersive medium, the refraction index depends on the wavelength and hence, white light, being a combination of many individual monochromatic components, is broken down into its spectral colors. Additionally, with dispersion the [velocity of individual waves](https://en.wikipedia.org/wiki/Phase_velocity) depends on the wavelength and hence the shape of the [pulse](https://en.wikipedia.org/wiki/Wave_packet), itself being a combination of possibly many waves, is broadened as some of the waves start to travel [faster than the pulse itself](https://en.wikipedia.org/wiki/Group_velocity). 
- The $\gamma$ parameter controls the nonlinearity term $\gamma\|A\|^2 A$ and represents many of the nonlinear effects that could arise in optical fibers. These are mainly caused by the fact that the polarization density depends nonlinearly on the electric field of the light.

<!-- 1. Phase and amplitude, Fourier phase of images
2. NLSE for propagation
3. Time stretching 
4. Implementation

Sources: https://commons.wikimedia.org/wiki/File:Soyuz_TMA-5_launch.jpg

 -->

$$
\frac{}{}
$$
