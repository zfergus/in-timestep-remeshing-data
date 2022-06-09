---
tags: SIGGRAPH 2023
---

# Plasticity Project Progress

## June 08, 2022

### Problem setup

Take a square in 2D and squash it using DBC. On the left the square gets squashed to 1% its original height. On the right it is squashed to 90% its original height.

### Isotropic Meshing

* $n$ is the number of points on each side

| $n=10$                               | $n=20$                               | $n=50$                               |
| ------------------------------------ | ------------------------------------ | ------------------------------------ |
| ![](https://i.imgur.com/hPbDPs1.png) | ![](https://i.imgur.com/TipbwjO.png) | ![](https://i.imgur.com/EkQqZd3.png) |

We can clearly see some really bad sliver elements in the fold. We also see some geometric locking bottom at the bottom right preventing it from bulging out 

### Anisotropic Meshing

| Rest                                 | Deformed                             |
| ------------------------------------ | ------------------------------------ |
| ![](https://i.imgur.com/FXankuT.png) | ![](https://i.imgur.com/7wwCOCN.png) |

This is a manually graded mesh with more resolution on the left. It folds earlier than the highest resolution isotropic mesh, but it still has sever locking on the right.

### Anisotropic $p$-refinement

| Rest                                 | Deformed                             |
| ------------------------------------ | ------------------------------------ |
| ![](https://i.imgur.com/E7pcU8n.png) | ![](https://i.imgur.com/xhhFx3f.png) |

An anisotropic higher-order mesh (P4 to P1). P4 helps with the folding but we need at least P2 on the right. 

### Comments

* This set of experiments makes me worried about adaptive $p$-refinement because there are some clearly highly curved element.

## June 09, 2022

**Isotropic $p=1$ w/ $n=1$ time:** 10.38s

### Isotropic $p=2$ (178.1s)

![](https://i.imgur.com/MGshSoa.png)

### Isotropic $p=4$ (477.6s)

![](https://i.imgur.com/rpFbMLh.png)

### Without Contact


## ToDo

* [ ] oracle mesh (run simulation then use deformed mesh as a quality metric for remeshing)
* [ ] try w/o no contact to disambiguate contact and elasticity locking
* [ ] $L2$ Projection
    * [ ] plot elasticity potential of quasi-static sim (zero-out velocities)
    * [ ] plot kinetic energy in dynamic sim
* [ ] More Scenes
    * [ ] "masticator"
    * [ ] high-impact ball against wall
    * [ ] compress and release sphere using square w/ contact



