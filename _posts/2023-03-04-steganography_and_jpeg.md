---
layout: post
title: Steganography & JPEG
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

This can be proved by noting that since any pixel is changed by at most $1$ in absolute value, the mean squared error is bounded, and hence the PSNR achieves a lower bound of about $48$. The logarithmic scaling is a signal-processing convention and is used often when measuring "power-like" variables like intensity and energy. Just for comparison, the PSNR of the method where we replace the LSBs directly is about $39.1 \text{dB}$.

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

Consider what happens with an odd extended function. We might have $(..., x_{N-1}, x_{N}, -x_{N}, -x_{N-1}, ...)$ or $(..., x_{N}, 0, -x_N, ...)$ where essentially $f(-x) = -f(x)$. If $f(x)$ doesn't change sign within $(x_1, ..., x_N)$, then it surely changes sign at the boundaries $1$ and $N$ and this introduces discontinuities, reducing the rate of convergence of the series. This is why the discrete Fourier transform or the discrete sine transforms are not particularly favourable for compression - because their extended function is odd, which adds discontinuities and increases the number of required terms for any given level of accuracy. Whereas with the DCT-II the extension is always continuous at the boundaries.

The DCT can be trivially extended to two-dimensional signals and it's what we'll use here. We change the notation slightly, letting $f(x, y)$ be the image and $F(u, v)$ be the DCT. $u$ and $v$ are the spatial frequency multiples.

$$
\begin{aligned}
F(x, y) & = e_u e_v \sum_{x=0}^{N-1} \sum_{y=0}^{N-1} f(x, y) \cos \Big[\frac{\pi}{N} \big(x + \frac{1}{2}\big) u \Big]   \cos \Big[\frac{\pi}{N} \big(y + \frac{1}{2}\big) v \Big] \\

f(x, y) & = \frac{2}{N} \sum_{u=0}^{N-1} \sum_{v=0}^{N-1} e_u e_v F(u, v)  \cos \Big[\frac{\pi}{N} \big(x + \frac{1}{2}\big) u \Big] \cos \Big[\frac{\pi}{N} \big(y + \frac{1}{2}\big) v \Big] \\

e_x & = \begin{cases}
\frac{1}{\sqrt{2}}, & x = 0 \\
1, & \text{otherwise.}
\end{cases}

\end{aligned}
$$

One of the biggest applications of the DCT is in [JPEG](https://en.wikipedia.org/wiki/JPEG#), the famous algorithm for lossy compression of digital images. It was introduced in 1992 and to this day it's the most popular image compression method in the world. The image format JPEG along with other formats like JFIF are based on it. Let's take a look at how it works:
1.  The image is converted from RGB to [Y'CbCr](https://en.wikipedia.org/wiki/YCbCr#). This colour space disentangles the three channels into one luma channel - how bright a pixel is - and two chroma channels - what colour the pixel has. The luma channel Y' is more or less a gray-scaled version of the image and encodes the light intensity non-linearly using [gamma-corrected](https://en.wikipedia.org/wiki/Gamma_correction) RGB primaries. The Cb is a "difference-blue" chroma channel which measures the difference between blue and the luminance. Similarly, Cr is "difference-red".
2. In the Y'CbCr space, [chroma subsampling](https://en.wikipedia.org/wiki/Chroma_subsampling) is performed. This downsamples the Cb and Cr channels typically by a factor of 2 in both horizontal and vertical directions. What justifies the downsampling is the fact that the human visual system is more sensitive to luma changes than to chroma changes and there's no point in carrying around information which is almost imperceptible.
3. The Y', Cb, and Cr channels are further split into multiple blocks of size $8 \times 8$. Each block is normalized into the range $[-128, 127]$ and then for each channel in that block, the DCT is calculated. At this point each block contains its DCT coefficients. Storing them may temporarily require more than 8 bits, but this is alleviated in the next step.
4. Human vision is such that it's easier to differentiate between two similar brightness settings over a large region, than over a small high-frequency one. We cannot distinguish between $256$ different brightness levels for a small path of pixels, but perhaps just $8$. For that reason, the next step is to quantize the DCT coefficients. Each coefficient from the $8 \times 8$ block is divided by a positive number which depends on the desired quality, and is then rounded to the nearest integer. The divisors are typically larger for those DCT coefficients corresponding to higher frequencies. *Many* of the coefficients may be $0$ after rounding. This is the main step of information loss in the algorithm.
5. Finally, the quantized DCT coefficients are stored as a sequence of bits. How exactly does this happen? For the current block, we iterate over all the coefficients in a zig-zag manner (similar to how the rational numbers can be enumerated). This essentially creates a sequence of 64 numbers with only some of them being non-zero. The zig-zaggy ordering ensures that long subsequences of zeros are created. Then this entire sequence is transformed using a run-length coding scheme. As an example, a sequence "AAAABBCCCCCC" can be encoded as "4A2B6C" saving up 6 symbols. After this step we end up with a shorter sequence of tuples containing information like how many zeros are before a given non-zero coefficient, how many bits are needed to express the coefficient and its actual value. Finally, [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding) is used to shorten this even more. This is a variable-length scheme which further encodes more frequent elements with shorter codewords. This coding is what constitutes the JPEG file.

<figure>
    <img class='extra_big_img' src="/resources/jpeg_compression.png" alt="JPEG compression" width="1200">
    <figcaption>Figure 2: JPEG compression. For each level of the desired quality a separate quantization table is used. The compression ratios typically vary around 10:1. </figcaption>
</figure>

The decoding is basically the reverse process above, where we are able to reconstruct all data except that lost in the quantization step which is forever lost.

Finally, getting back to steganography, a clever way is to insert our hidden data into the LSBs of the non-zero quantized DCT coefficients after step 4. They will then be run-length and Huffman encoded together with the cover image bits into a proper JPEG file. This is what the JSteg algorithm does.

Beyond JSteg, there are many other algorithms which improve the various aspects of the steganographic process. Some algorithms select the DCT coefficients in which to embed the data randomly [6], others use the discrete wavelet transform (DWT) instead of the DCT. A third group use encryption of the hidden data to add an extra layer of security. In general, there is an abundance of methods which compete and improve upon each other.

### References
[1] Provos, N. and Honeyman, P. [Hide and seek: an introduction to steganography](https://ieeexplore.ieee.org/abstract/document/1203220) *IEEE Security & Privacy*, vol. 1, no. 3, pp. 32-44 (2003).   
[2] Cheddad, A., Condell, J., Curran, K. and Kevitt, P. [Digital image steganography: Survey and analysis of current methods](https://www.sciencedirect.com/science/article/abs/pii/S0165168409003648) *Signal Processing*, vol. 90, issue 3, pp. 727-752 (2010).   
[3] Ni, Z., Shi, Y. Q., Ansari, N., Su, W. [Reversible Data Hiding](https://web.njit.edu/~ansari/papers/06TCAS.pdf) *IEEE Trans. Circuits and Systems for Video Technology*, 16(3) 354-362, (2006).   
[4] Li, Z., Chen, X., Pan, X. and Zeng, X. [Lossless Data Hiding Scheme Based on Adjacent Pixel Difference](https://ieeexplore.ieee.org/document/4769535) *International Conference on Computer Engineering and Technology*, Singapore, 2009, pp. 588-592 (2009).   
[5] Subhedar, M. S., Mankar, V. H. [Current status and key issues in image steganography: A survey](https://www.sciencedirect.com/science/article/abs/pii/S1574013714000136) *Computer Science Review*, vol. 13–14, pp. 95-113 (2014).   
[6] Westfeld, A. [F5 - a steganographic algorithm: High capacity despite better steganalysis](https://link.springer.com/chapter/10.1007/3-540-45496-9_21) *Proc. of the 4th Information Hiding Workshop*, vols. 21–37, pp. 289–302 (2001).   
