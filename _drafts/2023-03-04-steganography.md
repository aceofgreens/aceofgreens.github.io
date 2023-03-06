---
layout: post
title: Steganography
date: 2023-03-04 07:00:00 +0200
tags: [cs]
# excerpt_separator: <!--more-->
---

In cryptography the phrase "security through obscurity" refers to any approach in the design of a communication system which tries to enforce the security of a message by hiding the system's implementation. Nowadays this is generally discouraged in favour of "security by design", i.e. security obtained by virtue of the underlying system's fundamental properties. Nonetheless, the obscurity approach is not entirely forgotten. In fact, it's alive and kicking in a small cryptography-related field called *steganography*. Here the whole idea is to hide the existence of a message in some kind of carrier medium. This post explores the specific case of digital image steganography, which tries to hide one image in another as well as detect the embedding of multiple images.

In image steganography the carrier medium in which we hide information is the digital image. Theoretically, the setup closely resembles that of encryption. We have an original image $a$, a hidden image $c$, and an optional key $k$, shared or otherwise. Let's say Alice wants to send a hidden image to Bob. She can compute a *stego-image* (basically the equivalent of a ciphertext) using an embedding function $\text{Em}$ with signature:

$$
\text{Em}: \mathcal{C} \times \mathcal{A} \times \mathcal{K} \rightarrow \mathcal{C'} \\
\text{Em}(c, a, k) \mapsto c' \\
c \in \mathcal{C}, a \in \mathcal{A}, k \in \mathcal{K}, c' \in \mathcal{C'}.
$$

$\mathcal{C}$ is the space of all images, from which the original image $c$ is taken. $\mathcal{A}$ are all hidden images from which $a$ is taken, $\mathcal{K}$ are the optional keys to use, and $\mathcal{C'}$ are the stego-images - carrier images in which a hidden has been embedded. One wants $\mathcal{C} = \mathcal{C}'$ so that the stego-image does not leak anything.

Once Bob receives the stego-image, he needs a way to extract the hidden information. Depending on the actual setup he may use a key $K$ when extracting:

$$
\text{Ex}: \mathcal{C}' \times \mathcal{K} \rightarrow \mathcal{A} \\
\text{Ex}(c', k) \mapsto a \\
a \in \mathcal{A}, c' \in \mathcal{C}', k \in \mathcal{K}.
$$

Three main aspects define the steganography setup:
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

### The Frequency Domain



### References
Provos, N. and Honeyman, P. [Hide and seek: an introduction to steganography](https://ieeexplore.ieee.org/abstract/document/1203220) *IEEE Security & Privacy*, vol. 1, no. 3, pp. 32-44 (2003).   
Li, Z., Chen, X., Pan, X. and Zeng, X. [Lossless Data Hiding Scheme Based on Adjacent Pixel Difference](https://ieeexplore.ieee.org/document/4769535) *International Conference on Computer Engineering and Technology*, Singapore, 2009, pp. 588-592 (2009).   
Cheddad, A., Condell, J., Curran, K. and Kevitt, P. [Digital image steganography: Survey and analysis of current methods](https://www.sciencedirect.com/science/article/abs/pii/S0165168409003648) *Signal Processing*, vol. 90, issue 3, pp. 727-752 (2010).   

