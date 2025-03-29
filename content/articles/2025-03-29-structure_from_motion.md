---
Title: Data-Driven Structure From Motion
Date: 2025-03-29 07:00:00 +0200
Tags: ai
slug: data_driven_structure_from_motion
---

Structure from motion (SFM) has come a long way. It started back in the 1950s when researchers painstakingly derived 3D structures from pairs of aerial photographs through precise geometric reasoning. The [eight-point algorithm](https://en.wikipedia.org/wiki/Eight-point_algorithm) in 1981 was one of the first applications of mathematical rigour to the problem. In the late 1990s [RANSAC](https://en.wikipedia.org/wiki/Random_sample_consensus) enabled robust estimation in the presence of noise, while [bundle adjustment](https://en.wikipedia.org/wiki/Bundle_adjustment) greatly improved the reconstruction precision by jointly updating both the camera parameters and the scene geometry. In the next 10 years these solutions were scaled up and turned into products. Since then, deep learning has become the norm, with more of a focus on data-driven learning instead of explicit geometry modeling.

SFM is a huge topic and we cannot cover all the major developments in details. Instead, we'll only explore 5 particular papers from the [Visual Geometry Group](https://www.robots.ox.ac.uk/~vgg/) in Oxford, leading up to the VGGT. 

We begin with *two*-view SFM. The classic approach for recovering camera motion (rotation and translation) and 3D geometry (sparse point cloud) is as follows:

1. Detect keypoints and extract features for them using e.g. [SIFT](https://en.wikipedia.org/wiki/Scale-invariant_feature_transform). Match keypoints from one image $\mathbf{x}_i$ to keypoints in the other image $\mathbf{x}_i'$, forming sparse matching points $(\mathbf{x}_i, \mathbf{x}_i')$.
2. Use RANSAC to filter the matching points. Concretely, randomly select 5 matching pairs (assuming known camera instrinsics $\mathbf{K}$) and estimate the intrinsic matrix $\mathbf{E}$. Then compute the errors (epipolar constraint residuals) for all matched pairs using that essential matrix. Count the number of *inliers* - pairs with an error below a specified threshold. Repeat this whole random process of sampling pairs and estimating their essential matrix for a number of iterations, finally obtaining the essential matrix with most inliers.
3. Decompose the essential matrix into a rotation matrix and a translation vector, $\mathbf{E} = [\mathbf{t}]_\times \mathbf{R}$. There are 4 possible $(\mathbf{R}, \mathbf{t})$ solutions. Select the physically appropriate one based on the *cheirality* constraint, ensuring reconstructed points lie in front of both cameras. The essential matrix constraint $\mathbf{x}_i'^\mathsf{T} \mathbf{E} \mathbf{x}_i = 0$ is satisfied for any scaling factor $\alpha$ in the translation, $[\alpha \mathbf{t}]_\times \mathbf{R} = \alpha [\mathbf{t}]_\times \mathbf{R} = \alpha \mathbf{E}$, hence the retrieved translation is only up to a multiplicative constant (scale ambiguity).
4. Use triangulation to estimate the 3D points. The 3D point $X_i$ is chosen to be the one that minimizes the distance between the two rays - one from camera center $C_1$ through $\mathbf{x}_i$ and the other from camera center $C_2$ through $\mathbf{x}_i'$.

This classic approach is well-posed but produces relative camera motion and relative scene geometry, i.e. up to an unknown scale factor. With deep learning nothing prevents us from trying to predict absolute depth from a single image and absolute camera motion from both images. Yet, this is ill-posed and performance depends on how close the test image pair is to the training pairs, so that whatever priors are learned from the training set are still reasonable in the new images.

In 2021 an interesting approach was proposed that is both accurate, due to deep learning, and well-posed, due to incorporating classic SFM elements [1]. What they do is the following:

1. Estimate the [optical flow](https://en.wikipedia.org/wiki/Optical_flow) between the two images. This produces dense matching points which need to be heavily filtered. To do so, use SIFT just for keypoint detection (not matching). The optical flow is more accurate in high-textured regions found by SIFT.
2. Apply RANSAC on the filtered pairs obtaining $\mathbf{E}$ and therefore $(\mathbf{R}, \mathbf{t})$ after decomposition.
3. For depth, however it is obtained, it should not be supervised with GT metric depth because this will introduce a mismatch between the relative translation $\mathbf{t}$ and the predicted depth $d_i$.
4. Instead, use something similar to *plane sweep stereo*. For point $\mathbf{x}_i$, its matching point $\mathbf{x}_i'$ lies somewhere along the corresponding epipolar line. If you knew the depth $d_i$, you can get the point as $\mathbf{x}_i' = \mathbf{K}[\mathbf{R} | \mathbf{t}] [(\mathbf{K}^{-1}\mathbf{x}_i) d_i, \ 1 ]^\mathsf{T}$. But the translation $\mathbf{t}$ obtained previously is only relative. So we do two things: first we normalize $\mathbf{t}$ to unit norm, and second, we prepare multiple depth planes $d_1, d_2, ..., d_D$. The plane sweep algorithm generates a cost volume of shape $(H, W, D)$ from which it retrieves the estimated depth of that pixel, $\hat{d}_i$. It is then scaled according to the GT scale, $\alpha_\text{GT} \hat{d}_i$ and is supervised with the GT metric depth. This is called *scale-invariant matching* and is well-posed. Phew...



### References
[1] Wang, Jianyuan, et al. [Deep two-view structure-from-motion revisited.](https://openaccess.thecvf.com/content/CVPR2021/html/Wang_Deep_Two-View_Structure-From-Motion_Revisited_CVPR_2021_paper.html?ref=https://githubhelp.com) Proceedings of the IEEE/CVF conference on Computer Vision and Pattern Recognition. 2021.   
[2] 
