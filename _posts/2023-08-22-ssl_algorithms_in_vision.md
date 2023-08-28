---
layout: post
title: SSL Algorithms in Vision
date: 2023-08-22 07:00:00 +0200
tags: [ai]
# excerpt_separator: <!--more-->
---

Self-supervised learning (SSL) has emerged as the cornerstone behind the surge of large-scale models permeating the mainstream. In this post, we'll delve into the main families of SSL algorithms, primarily with a focus on those in the realm of computer vision.

SSL is one of the most important developments in machine learning. It's the idea that by modeling the structure of the data, even without the use of any target labels, one can still learn incredibly useful features for downstream applications. This has been verified experimentally to be true for many different tasks and datasets. In fact, the concept of *linear probing*, where one uses a single linear output layer on top of the SSL features, shows that the model trained with SSL learns sophisticated representations in a space where the targets are linearly separable. Why this happens is, as of now, unknown.

SSL is not a novel topic. There are many methods prior to 2020, when modern SSL took off, that go in the direction of learning structural information from the data itself. The most popular examples are:
1. **Information restoration** - this includes colorization from grayscale or methods like masked inpainting, which later evolved into the extremely popular and successful masked autoencoders approach.
2. Using **temporal relationships in video** - here one can do a lot of things - remove audio and predict it from the video, use triplet losses to make the representations of similar objects from two different frames be similar, predict the next frame from the past and so on.
3. Learning **spatial context**. This boils down to learning spatial relations between objects. One can apply random rotations to the objects and have the model predict the rotations, or simply predict the relative location of two patches from the image. The similar, but harder task of creating a "jigsaw" puzzle by permuting patches of the image and then trying to put them back into place is also very popular.
4. **Grouping similar images together** - here the idea is to learn good features by grouping similar images together. One successful method clusters images using K-means and forces the neural image embeddings to be similar if the underlying images belong to the same cluster, and different otherwise. 
5. **Generative models** - GANs have been found to be useful for transfer learning and there have been successful attempts to borrow ideas from their adversarial nature into more complicated systems.
6. **Multi-view invariance**. Here the idea is to be invariant with respect to different random augmentations of the image. One of the first successful approaches maximized the mutual information between different representations. Other methods have tried to use weakly-trained predictors to obtain pseudolabels, which are then used to force similarity between the different augmentations.

### The Deep Metric Learning Family

This is the first family of modern top-performing SSL methods. The idea here is to learn similar representations for similar images according to some criteria like labels, distance between labels, or fixed transformations. Positive samples are those whose representations should be similar, while negative ones are opposite. Since some samples are so different that their representations are trivially very different, it's important to find negative samples which are sufficiently similar and challenge the model. This aspect is called *hard negative mining*. One way to insure that enough hard negatives are observed is to have very large batch sizes when training.

The most basic objective is given by the margin loss 

$$
\mathcal{L}(x_1, x_2, y) = \max(0, -y {\lVert x_1 - x_2 \rVert}_p + m).
$$

Here, $x_1$ and $x_2$ are the two representations, typically projected to a smaller dimension, ${\lVert \cdot \rVert}_p$ is the $p$-norm, $y \in \\{ -1, 1 \\}$ shows whether they should be the same or not, and $m$ is a tolerable margin between the distance. If $y = 1$, then the loss is $0$ if the difference between the two representations is smaller than $m$. If $y=-1$, the loss is $0$ if the difference is larger than $m$.

The similar triplet loss compares an anchor point $x_0$ with a positive point $x_p$ of the same class, and a negative point $x_-$ of a different class and enforces the distances to be sufficiently different:

$$ \mathcal{L}(x_0, x_+, x_-) = \max ({\lVert x_a - x_+ \rVert}_p - {\lVert x_0 - x_- \rVert}_p + m, 0).$$

Ideally, a model trained with the triplet loss is able to minimize the distance between the anchor and the positive while maximizing the distance between the anchor and the negative. The model FaceNet uses a triplet loss to learn feature spaces where the distance between features directly corresponds to how similar any two human faces are.

With time, deep metric learning has gradually evolved into *contrastive predictive coding*, also called contrastive SSL. This change has led to the usage of bigger datasets, deeper networks, and the use of *projectors* which map the representation into a lower-dimensional space where the loss is calculated, and are otherwise discarded at test time. The hard negative sampling has given way to random sampling of augmentations where the positives are those views which come from the same sample, and the nagatives are all other samples.

The most popular loss of this kind is the infoNCE loss [1]:

$$
\mathcal{L} = - \sum_{(i, j) \in \mathbb{P}} \log \Big( \frac{e^{\text{CoSim}(z_i, z_j)/\tau}}{\sum_{k = 1}^N e^{\text{CoSim}(z_i, z_k)/\tau}}  \Big),
$$

where we try to identify a single positive sample from the set of $N-1$ other noise samples. It's a form of cross-entropy. In general, entropy gives you the amount of information contained in a probabilistic event. Consequently, a perfect encoding of the underlying probability distribution will require exactly that many bits of information to encode that event. Cross-entropy instead gives us the amount of information needed to encode (or identify) that event if our coding is inefficient. It is lower-bounded by the entropy. Hence, if the underlying random variable is degenerate and is deterministic (e.g. when classifying cats and dogs, where the labels are $0$ and $1$) the lower bound of the cross-entropy is $0$.

**SimCLR** [2] is a very successful SSL model that uses the infoNCE loss. It works by sampling a batch of $N$ images, $\\\{x_k \\\}_{k = 1}^N$, applying two sets of random augmentations like cropping, scaling, colour jittering to each image, pushing each view through the encoder, and then computing the infoNCE loss on the resulting representations. In particular, of the $2N$ total image views, we can calculate the loss on a single positive pair, defined as that tuple of views which originate from the same sample, as 

$$ \ell(i, j) = - \log \Big ( \frac{\exp(s_{i, j} /\tau  )} {\sum_{k = 1}^{2N} \mathbb{I}_{[k \ne i]} \exp (s_{i, k} \tau)} \Big ). $$

Here $s_{i, j}$ is some similarity metric like a cosine similarity or a simple dot product and $\tau$ is a temperature parameter which increases or decreases the sharpness of events in predictions. Note that in the denominator the sum runs across all other $2N - 1$ views different from $i$. Therefore, if we order them such that those views from the same sample have subsequent indices, the model learns that views $2i - 1$ and $2i$ are positive pairs, but $2i - 1$ and any other view from $\\\{1, ..., 2i-2, 2i + 1, ... 2N\\\}$ are negative. The end result is the ability to recognize when two augmentations come from the same sample (a form of augmentation invariance) which turns out to produce very useful features for downstream tasks.

The total loss is given by $\mathcal{L} = \frac{1}{2N} \sum_{k=1}^N (\ell(2k - 1, 2k) + \ell(2k, 2k-1))$ which simply aggregates across all positive samples and handles the asymmetric nature of the infoNCE loss.

The **NNCLR** model [3] is similar to SimCLR except that it learns similarity not within a single instance, but across different instances in the dataset. This yields more diverse semantic variations than only using pre-defined transformations. Essentially, given a minibatch of images, NNCLR starts by applying two sets of random transformations to each image like in SimCLR, obtaining two sets of views. Now for each view in the first set, it finds the nearest neighbor latent embedding from a support set of *other instances* from the dataset. This support set is implemented as a simple FIFO queue which stores running latent representations across instances. Then the infoNCE is applied on the set of nearest neighbors and the set of random augmentations.

**MeanShift** [4] is another popular SSL method that works in a similar way. From a single image, two random views are extracted. One is fed to a online encoder updated with gradient descent, the other is fed to a target encoder updated using slow moving average on the weights of the online one. The latent from the target encoder goes into a memory bank, from which a set of nearest neighbors (more than one) are retrieved. The latent from the online decoder is pushed towards the mean of the nearest neighbors.

### The Self-Distillation Family
*Model distillation* is a technique where knowledge from a large, complex model (often referred to as the "teacher" model) is transferred to a smaller, simpler model (known as the "student" model). The goal is to get the student model to perform as closely as possible to the teacher model, but with the benefits of reduced size, faster inference times, and possibly fewer computational resources for deployment. *Self-distillation* instead refers to a process where a trained model (the teacher) is used to generate pseudo-labels or soft targets for the training data, and then the same model (the student) is trained on these pseudo-labels or soft targets to improve its performance.

**BYOL** (bootstrap your own latent) [5] is the canonical model here. It samples two augmentations of the image and feeds them to two encoders - one is the student, $f_{\theta_s}$, the other is the teacher, $f_{\theta_t}$. Then a predictor network $p_\gamma$ maps the latent from student into a prediction which gets compared with the latent from the teacher. The student is updated using gradient descent. The teacher is updated using an exponential moving average parameterized by $\xi$ on the weights of the student, which prevents collapse.

$$
\begin{align}
\mathcal{L} &= \mathbb{E}_{x, t_1, t_2 \sim (X, T_1, T_2)}  \Big[ { \big\lVert h\big(p_\gamma(f_{\theta_s}(t_1(x))) \big) - h \big(f_{\theta_t} (t_2(x)) \big) \big\rVert}_2^2 \Big] \\
h(v) &= \frac{v}{\max( {\lVert v \rVert}_2 + \epsilon)} \\
\theta_t &= \xi \theta_t + (1 - \xi)\theta_s 
\end{align}
$$

Here, $h$ is a $\ell_2$ normalization on the latents and $t_1$, $t_2$ are the random augmentations. Notice that the MeanShift method is exactly equal to BYOL when the number of neighbors is one.

**SimSiam** [6] simplifies the objective by not using EMA updates on the target network, but simply detaching the tensors at the right place in the computational graph. **DINO** [7] centers the outputs of the encoder using a running mean across the batch, applies a temperature-conditioned softmax, in effect discretizing the representations, normalizes, and finally minimizes the cross entropy between the student output and the detached teacher output.

Compared to BYOL which contrasts between two augmentations of the same image but processed through slightly different networks, **MoCo** relies on contrastive learning with the infoNCE loss [8]. It introduces a momentum encoder, a moving average of the main encoder, which further stores representations from previous batches into a queue. When training, we sample two sets of augmentations, called the *queries* and the *keys*, from the current batch. Now their pairs are considered positive samples, while the pairs between the queries and the latents in the queue are considered negatives. The infoNCE loss is applied on all positive and negative pairs.


### The Canonical Correlation Analysis Family

[Canonical correlation analysis](https://en.wikipedia.org/wiki/Canonical_correlation) (CCA) is a very general way to learn the relationships between two random vectors $X \in \mathbb{R}^n$ and $Y \in \mathbb{R}^m$ from their [cross-covariance matrix](https://en.wikipedia.org/wiki/Cross-covariance_matrix). CCA seeks two vectors $a$ and $b$ such that the correlation $\text{corr}(a^TX, b^TY)$ is maximal. In that case $a$ and $b$ are called the first pair of canonical variables. One can find the second pair by finding a similar pair of vectors which maximize that correlation but are themselves uncorrelated to the previous pairs of canonical variables.

In the context of deep learning we usually seek nonlinear transformations. If they are $f_x$ and $f_y$, then their outputs are $U = f_x(X)$ and $V = f_y(Y)$. The CCA framework optimizes for $f_x$ and $f_y$ such that $U$ and $V$ have zero-mean, identity covariance, and maximal agreement across the whole dataset:

$$
\mathcal{L} = - \sum_{n = 1}^N \langle U_n, V_n \rangle \\
\text{s.t. } \frac{1}{N}\sum_{n = 1}^N U_n = \frac{1}{N}\sum_{n = 1}^N V_n = \mathbf{0}, \frac{1}{N} \textbf{U}^T\textbf{U} = \frac{1}{N} \textbf{V}^T \textbf{V} = \textbf{I}
$$

**VICReg** (variance, invariance, covariance regularization) [9] samples two sets of augmented views $X$ and $X'$ from the current image batch, and encodes them into representations $Z$ and $Z'$, after which it uses a loss with three regularization terms. The first encourages the variance of the variables within $Z$ and $Z'$ to be above a certain threshold, thus encouraging diversity across the samples in the batch. The second is a covariance term which acts on the individual variables in $Z$ and separately in $Z'$ by forcing them to have zero covariance. The intuition is that the individual elements of $Z$ should capture as much information as possible by being decorrelated. Lastly, an invariance term acts to minimize the mean squared distance between the representations in $Z$ and those in $Z'$. This acts across the two sets of encodings. Obviously, such a term is needed because $X$ and $X'$ come from the same set of underlying images.

Another similar method is **BarlowTwins** [10], where from the representations $Z$ and $Z'$ we directly compute a cross-correlation matrix and push it towards the identity matrix. This itself has two effects: it forces the individual elements of the representation to have unit variance, and also forces the elements to be as diverse as possible (to have zero covariances).  **SwAV** (swapped assignments between views) [11] is a particularly interesting method that does not compare image features directly but rather uses a "swapped" prediction task. First, apart from training the encoder, this method also learns a number of "prototype" vectors, or "codes". They are learned jointly with the other parameters using gradient descent. Then each representation from the two sets of the augmented views is assigned to one of these code vectors. Supose $z$ and $z'$ are the representations and $q$ and $q'$ are the correspondingly assigned code vectors. The loss, at a high level, has the following form $\mathcal{L} = \ell(z, q') + \ell(z', q)$, i.e. it mixes them up. The code vectors can be *roughly* thought of as the canonical variables from CCA.

### The Masked Image Modeling Family
The idea of image inpainting, where a large part of the image is greyed-out and then predicted from the remaining data, has been shown to yield strong results and to produce good features. An important model is **BEiT** (bidirectional encoder representation from image transformers) [12] which introduced the idea of masked image modeling (MIM), similar to how BERT is trained.

BEiT keeps two representations for the image - *image patches* and *visual tokens*. An image patch is simply a small square patch of pixels, flattened and linearly projected. They preserve the raw pixel values. Visual tokens are the equivalent of word tokens from NLP - a fixed number (8192) of discrete visual tokens are learned using a discrete variational autoencoder. The discrete nature makes the model non-differentiable so tricks like the Gumbel-softmax relaxation are used. This is the *pre*-pre-training part. The end result is a *tokenizer* which can take an image and produce a grid of $14 \times 14$ visual tokens.

Then, in the actual pre-training we have a transformer encoder which takes in image patches, of which some are masked. The transformer outputs a hidden representation for these masked patches and a softmax is applied. This corresponds to the probability that the visual token for a given masked patch corresponds to any of the predefined and learned visual tokens. In essence, the model maximizes the log-likelihood of the correct visual tokens. After the pre-training the model can be fine-tuned on downstream tasks.

BEiT is a complex model. **MAE** (masked autoencoders) [13] simplify it by directly reconstructing image patches instead of discrete tokens. MAE randomly selects visible image patches, passes them to an encoder, adds mask tokens and uses a lightweight decoder to reconstruct the whole image. **SimMIM** [14] also goes in the direction of simplifying the pipeline by having a single encoder and a single-layer prediction head.

<figure>
    <img class='extra_big_img' src="/resources/ssl_families.svg" alt="SSL Families" width="1200">
    <figcaption>Figure 1: Simplified schematics of three popular SSL algorithm families. The contrastive learning one (left) learns features invariant to semantically-preserving transformations. The self-distillation family (middle) learns features by distilling information across lagged versions of the same network. The CCA approach (right) learns features by regularizing the learned representations. Green boxes represent data. Yellow boxes are learnable components. Red boxes are operations. The three concrete models depicted are SimCLR, BYOL, and VICReg.</figcaption>
</figure>

### References
[1] Oord, Aaron van den, Yazhe Li, and Oriol Vinyals. [Representation learning with contrastive predictive coding.](https://arxiv.org/abs/1807.03748) *arXiv preprint arXiv:1807.03748* (2018).  
[2] Chen, Ting, et al. [A simple framework for contrastive learning of visual representations.](https://proceedings.mlr.press/v119/chen20j.html) *International conference on machine learning*. PMLR, 2020.  
[3] Dwibedi, Debidatta, et al. [With a little help from my friends: Nearest-neighbor contrastive learning of visual representations.](https://openaccess.thecvf.com/content/ICCV2021/html/Dwibedi_With_a_Little_Help_From_My_Friends_Nearest-Neighbor_Contrastive_Learning_ICCV_2021_paper.html) *Proceedings of the IEEE/CVF International Conference on Computer Vision*. 2021.  
[4] Koohpayegani, Soroush Abbasi, Ajinkya Tejankar, and Hamed Pirsiavash. [Mean shift for self-supervised learning.](https://openaccess.thecvf.com/content/ICCV2021/html/Koohpayegani_Mean_Shift_for_Self-Supervised_Learning_ICCV_2021_paper.html) *Proceedings of the IEEE/CVF International Conference on Computer Vision*. 2021.  
[5] Grill, Jean-Bastien, et al. [Bootstrap your own latent-a new approach to self-supervised learning.](https://proceedings.neurips.cc/paper_files/paper/2020/file/f3ada80d5c4ee70142b17b8192b2958e-Paper.pdf) *Advances in neural information processing systems 33* (2020): 21271-21284.  
[6] Chen, Xinlei, and Kaiming He. [Exploring simple siamese representation learning.](https://openaccess.thecvf.com/content/CVPR2021/html/Chen_Exploring_Simple_Siamese_Representation_Learning_CVPR_2021_paper.html) *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*. 2021.   
[7] Caron, Mathilde, et al. [Emerging properties in self-supervised vision transformers.](https://openaccess.thecvf.com/content/ICCV2021/html/Caron_Emerging_Properties_in_Self-Supervised_Vision_Transformers_ICCV_2021_paper.html) *Proceedings of the IEEE/CVF international conference on computer vision*. 2021.  
[8] He, Kaiming, et al. [Momentum contrast for unsupervised visual representation learning.](https://openaccess.thecvf.com/content_CVPR_2020/html/He_Momentum_Contrast_for_Unsupervised_Visual_Representation_Learning_CVPR_2020_paper.html) *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*. 2020.  
[9] Bardes, Adrien, Jean Ponce, and Yann LeCun. [Vicreg: Variance-invariance-covariance regularization for self-supervised learning.](https://arxiv.org/abs/2105.04906) *arXiv preprint arXiv:2105.04906* (2021).  
[10] Zbontar, Jure, et al. [Barlow twins: Self-supervised learning via redundancy reduction.](https://proceedings.mlr.press/v139/zbontar21a.html) *International Conference on Machine Learning*. PMLR, 2021.  
[11] Caron, Mathilde, et al. [Unsupervised learning of visual features by contrasting cluster assignments.](https://proceedings.neurips.cc/paper/2020/hash/70feb62b69f16e0238f741fab228fec2-Abstract.html) *Advances in neural information processing systems 33* (2020): 9912-9924.
[12] Bao, Hangbo, et al. [Beit: Bert pre-training of image transformers.](https://arxiv.org/abs/2106.08254) *arXiv preprint arXiv:2106.08254* (2021).  
[13] He, Kaiming, et al. [Masked autoencoders are scalable vision learners.](https://openaccess.thecvf.com/content/CVPR2022/html/He_Masked_Autoencoders_Are_Scalable_Vision_Learners_CVPR_2022_paper) *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*. 2022.  
[14] Xie, Zhenda, et al. [Simmim: A simple framework for masked image modeling.](https://openaccess.thecvf.com/content/CVPR2022/html/Xie_SimMIM_A_Simple_Framework_for_Masked_Image_Modeling_CVPR_2022_paper.html) *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*. 2022.  