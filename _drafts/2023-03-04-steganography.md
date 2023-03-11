---
layout: post
title: Steganography
date: 2023-03-04 07:00:00 +0200
tags: [cs]
# excerpt_separator: <!--more-->
---

In cryptography the phrase "security through obscurity" refers to any approach in the design of a communication system which tries to enforce the security of a message by hiding the system's implementation. Nowadays this is generally discouraged in favour of "security by design", i.e. security obtained by virtue of the underlying system's fundamental properties. Nonetheless, the obscurity approach is not entirely forgotten. In fact, it's alive and kicking in a small cryptography-related field called *steganography*. Here the whole idea is to hide the existence of a message in some kind of carrier medium. This post explores the specific case of digital image steganography, which tries to hide one image in another as well as detect the embedding of multiple images.

In image steganography the carrier medium in which we hide information is the digital image. Theoretically, the setup closely resembles that of encryption [1, 2]. We have an original image $a$, a hidden image $c$, and an optional key $k$, shared or otherwise. Let's say Alice wants to send a hidden image to Bob. She can compute a *stego-image* (basically the equivalent of a ciphertext) using an embedding function $\text{Em}$ with signature:

$$
\text{Em}: \mathcal{C} \times \mathcal{A} \times \mathcal{K} \rightarrow \mathcal{C'} \\
\text{Em}(c, a, k) \mapsto c' \\
c \in \mathcal{C}, a \in \mathcal{A}, k \in \mathcal{K}, c' \in \mathcal{C'}.
$$

$\mathcal{C}$ is the space of all images, from which the original image $c$ is taken. This is called a carrier or a *cover* image. $\mathcal{A}$ are all hidden images from which $a$ is taken, $\mathcal{K}$ are the optional keys to use, and $\mathcal{C'}$ are the stego-images - carrier images in which the hidden information has been embedded. One wants $\mathcal{C} = \mathcal{C}'$ so that the stego-image does not leak anything.

Once Bob receives the stego-image, he needs a way to extract the hidden information. Depending on the actual setup he may use a key $K$ when extracting:

$$
\text{Ex}: \mathcal{C}' \times \mathcal{K} \rightarrow \mathcal{A} \\
\text{Ex}(c', k) \mapsto a \\
a \in \mathcal{A}, c' \in \mathcal{C}', k \in \mathcal{K}.
$$

Three main aspects define the steganography setup [1]:
1. **Capacity**, relates to how much information can be hidden in the carrier medium
2. **Security**, relates to how easy it is for an eavesdropper to detect any of the hidden information. Achieving high security, along with high capacity are the main goals in steganography.
3. **Robustness**, relates to how much modification can the stego medium withstand before any hidden information is destroyed. Achieving a high degree of robustness is the goal of watermarking, where removing some information is impossible without severely degrading the quality.

Apart from embedding information in digital images, the other complementary task would be to detect them. This is called *steganalysis*. Most of the methods that we'll discuss next are easily detectable. That being said, here the intent is to provide a general classification of the different methods without delving into *too* much details.

An image can be treated as a spatial signal sampled in a rectangular regular grid of coordinates. We can either insert the hidden information directly in this spatial domain, or in the related frequency domain, which is a different representation of the same information. Here we'll see methods using both approaches.

### The Spatial Domain
Probably the simplest spatial domain method is to hide information in the least significant bits (LSBs) of the carrier image. Suppose the carrier and the hidden information are both images represented as arrays of type ``uint8``. Suppose the carrier image is of shape $(H, W, 3)$. Let's assume for simplicity that the hidden image is also of that shape, otherwise we can pad up to or downsize to that shape.

We have to decide how many of the LSBs in the original image we'll use for the hidden image. From some quick experiments I've decided that 4 bits from every element works best. This supports up to $2^4 = 16$ different color intensities both in the original and the hidden images. To implement this, we just take the 4 most significant bits from each element in the image-to-hide and insert them into the 4 least significant bits of the corresponding elements in the carrier. This can be efficiently computed for vectorized inputs like images using bitwise operations.

```
def embed(x, y):
    """ Embeds image y into image x. """
    carrier = x & 11110000
    hidden_info = (y & 11110000) >> 4
    stego_image = carrier | hidden_info
    return stego_image

def extract(x):
    """ Extracts hidden information from image x. """
    hidden = (x & 00001111) << 4
    original = x & 11110000
    return original, hidden
```

In the pseudocode above the number of hidden bits transferred to the carrier is hardcoded for simplicity to 4 in each element. This means that the stego-image which will be visible to everyone and the hidden image will have the same quality. In reality, it's more common to favour the quality of the stego-image, so it's more difficult to detect that any hidden image is present just by visual inspection. Figure 1 shows a stego-image hiding a completely different image in the 3 last bits of each of its pixel. It is clear as day that this approach deals with an obvious trade-off - we can either have a cover image with high details and a hidden message with low details, or vice versa. Notice how with just 3 bits per element, the hidden image still looks quite reasonable. Using more bits will improve the details and make the dark background more consistent and uniform, but only at the expense of a lower quality cover.

<figure>
    <img class='extra_big_img' src="/resources/stego_3.jpeg" alt="Steganography in the spatial domain" width="1200">
    <figcaption>Figure 1: Steganography in the spatial domain. We hide the first 3 bits of each element of a hidden image in the last 3 bits of each element of a cover image. The image is multi-channel, and the different colour channels do not change the conceptual idea in any way. Since the hidden image has values only between $0$ and $2^3$, making it very dark, just for the visualization we multiply them by $2^5$. </figcaption>
</figure>

A different clever way to do steganography in the spatial domain is through the image intensity histogram [2, 3]. To motivate this method, assume our secret consists of $K$ bits, $B = b_1b_2...b_K$. The image quality won't be decreased too much if we flip the least significant bit of every pixel. So we can do the following: we increase the intensity of all pixels with value greater than $L$ by $1$. After this transformation there will be no pixels with value exactly $L + 1$ and the histogram will have an empty bin. This is where we can fit our message $B$. We scan the image sequentially and whenever we find a pixel with value $L$, we consider the next bit we want to hide. If it's $1$, we increase that pixel by 1. Otherwise, we keep it as is.

The end result is that all pixels with intensity less than $L$ are unchanged. The number of pixels with value $L$ is equal to the number of zeros in $B$, those with value $L+1$ equal the ones in $B$ and all pixels with greater intensity have their intensity increased by $1$. With this method we can insert up to $h(L)$ bits, where $h$ is the image histogram. Hence, to maximize capacity, $L$ should be chosen as the mode of the histogram - the most frequent intensity.

As another benefit, this technique can be entirely reversible... after we make some additional modifications. In the setup presented so far, we change the cover image, although slightly, and this cannot be undone. Consider what happens to the pixels with intensity $255$. When we add $1$ to them, they will overflow. To fix this, we find the *least* frequent intensity value, $L'$, which is assumed greater than $L$ (otherwise the whole algorithm is mirrored). Now, we set all pixels with value $L'$ to zero, but we also save their coordinates, as well as the value $L'$ itself. This is called the *overhead* for later reconstruction.

To make the method entirely reversible we can pass this overhead info into the hidden message payload. As a result, the *effective* capacity is reduced, but we are able to reconstruct the cover image perfectly. This also answers the question of why $L'$ is the least frequent intensity - because any larger intensity would lead to a larger overhead and subsequently reduced capacity. In terms of the quality of the cover image, we can measure it using the peak-signal-to-noise ratio (PSNR) which is fairly high.

$$
\text{PSNR} = 10 \log_{10} \Big(\frac{255 \times 255}{MSE} \Big) = 48.13 \text{dB}.
$$

This can be proved by noting that since any pixel is changed by at most $1$ in absolute value, the mean squared error is bounded, and hence the PSNR achieves a lower bound of about $48$. The logarithmic scaling is a signal-processing convention and is used often we measuring "power-like" variables like intensity and energy. Just for comparison, the PSNR of the method where we replace the LSBs directly is about $39.1 \text{dB}$.

Regarding the extraction, it's very similar to the embedding, but with inverse operations applied in the inverse order. We won't spend much time on it. The point is that this type of histogram-based steganography is reversible and provides an acceptable amount of capacity.

There are multiple improvements to the above method. First, one can use multi-channel images to increase the capacity tremendously. Second, one can use multiple maximal-minimal points $(L, L')$ to increase the capacity even in a single channel. Thirdly, one can consider the histogram of adjacent pixel differences (across either rows or columns) which typically looks like a zero-centered Gaussian. Since adjacent pixels in a homogeneous region have a difference of $0$, the zero bin in the histogram accumulates much more pixels than before, and hence more information can be inserted [4].

### The Frequency Domain
In the frequency domain the image is represented by the amplitude coefficients of multiple sinusoidal waves of varying frequencies which when added together reconstruct our image. It is known that the human visual system is more sensitive to lower frequency variations than to high ones. Additionally, the pixels of finer details like edges and corners which are represented by higher frequency waves are typically uncorrelated with other nearby pixels, unlike those of low-frequency waves. This means that we can potentially hide information in the higher frequencies without reducing the quality of the stego-image perceptibly.

We can use almost any transform to achieve our needs. However, only some have established themselves as a standard due to the various beneficial factors they possess. The most commonly used one is the [discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) (DCT) which is used *ubiquitously* in science and engineering. It represents a function as a sum of cosines and has very nice compression properties which we'll explore now.

Suppose we have a discrete sequence $(x_1, ..., x_N)$. If we fit a sum of sines and cosines to this sequence, we'll be able to evaluate it even outside of its left and right boundaries. That means that any Fourier-like transform operating on a finite domain implies a periodic extension to the original sequence, due to the periodicity of the sines and cosines. The DCT, where we use only cosines, implies an *even* extension.

At this point let's assume two important properties of the extended function:
1. It is even at both the left and right boundaries $x_1$ and $x_N$,
2. The point around which it is even is the midpoint between $x_1$ and the previous extended point.

These two assumptions lead to an extended sequence 

$$
(..., x_N, ..., x_2, x_1, x_1, x_2, ..., x_N, x_N, x_{N-1}, ..., )
$$

where near the endpoints the points are copied, $(..., x_{N-1}, x_N, x_N, x_{N-1}, ...)$. Just for comparison, if our second assumption was that the extended sequence was even around exactly the boundary, then this would create sequences with less duplicated points $(..., x_{N-1}, x_N, x_{N-1}, ...)$. With the specific assumptions as defined above, the most common DCT type, DCT-II, is defined:

$$
\begin{aligned}
X_k & = e_k \sum_{n=0}^{N-1} x_n \cos \Big[\frac{\pi}{N} \big(n + \frac{1}{2}\big) k \Big], \ \text{ for all } k=0, ..., N-1 \\
x_n & = \frac{2}{N} \sum_{k=0}^{N-1} e_k X_k  \cos \Big[\frac{\pi}{N} \big(n + \frac{1}{2}\big) k \Big], \ \text{ for all } n=0, ..., N-1 \\

e_k & = \begin{cases}
\frac{1}{\sqrt{2}}, & k = 0 \\
1, & \text{otherwise.}
\end{cases}

\end{aligned}
$$

Here $x_n$ is the signal in the spatial domain at index $n$ and $X_k$ is the value of the DCT, or the *strength*, at the frequency multiple $k$. The first equation is the forward transform, often called *analysis*, and the second one is the inverse, often called *synthesis*. The various multiplicative constants are more or less a convention and can vary across authors. As a sanity check, consider what the strength of the $0$-th frequency, which is $X_0 = \frac{1}{\sqrt{2}} \sum_{n=0}^{N - 1} x_n$. If we reconstruct the signal using only this frequency, we get $\frac{1}{N} \sum_{n=0}^{N-1} x_n$ -  the mean of the entire signal.

Apart from DCT-II, there are many other variants, depending on whether the function is even/odd on the left/right boundary and around which point exactly. Note that unlike the discrete Fourier transform, here the coefficients are entirely real. There's something deeper going on though. **Functions which can be represented with fewer sinusoidal terms tend to be more compressible than those requiring many terms.** And which functions require many terms? Those that have rapidly changing peaks and discontinuities. And often discontinuities come from the boundaries of the sequence.

Consider what happens with an odd extended function. We might have $(..., x_{N-1}, x_{N}, -x_{N}, -x_{N-1}, ...)$ or $(..., x_{N}, 0, -x_N, ...)$ where essentially $f(-x) = -f(x)$. If $f(x)$ doesn't change sign withing $(x_1, ..., x_N)$ then it surely changes sign at the boundaries $1$ and $N$ and this introduces discontinuities, reducing the rate of convergence of the series. This is why the discrete Fourier transform or the discrete sine transforms are not particularly favourable for compression - because their extended function is odd, which adds discontinuities and increases the number of required terms for any given level of accuracy. Whereas with the DCT-II the extension is always continuous at the boundaries.



### References
Provos, N. and Honeyman, P. [Hide and seek: an introduction to steganography](https://ieeexplore.ieee.org/abstract/document/1203220) *IEEE Security & Privacy*, vol. 1, no. 3, pp. 32-44 (2003).   
Cheddad, A., Condell, J., Curran, K. and Kevitt, P. [Digital image steganography: Survey and analysis of current methods](https://www.sciencedirect.com/science/article/abs/pii/S0165168409003648) *Signal Processing*, vol. 90, issue 3, pp. 727-752 (2010).   
[3] Ni, Z., Shi, Y. Q., Ansari, N., Su, W. [Reversible Data Hiding](https://web.njit.edu/~ansari/papers/06TCAS.pdf) *IEEE Trans. Circuits and Systems for Video Technology*, 16(3) 354-362, (2006).   
[4] Li, Z., Chen, X., Pan, X. and Zeng, X. [Lossless Data Hiding Scheme Based on Adjacent Pixel Difference](https://ieeexplore.ieee.org/document/4769535) *International Conference on Computer Engineering and Technology*, Singapore, 2009, pp. 588-592 (2009).   
[5] Subhedar, M. S., Mankar, V. H. [Current status and key issues in image steganography: A survey]() *Computer Science Review*, vol. 13–14, pp. 95-113 (2014).


