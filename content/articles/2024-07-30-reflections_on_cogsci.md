---
Title: Reflections on CogSci
Date: 2024-07-30 07:00:00 +0200
Tags: rl
slug: reflections_on_cogsci
---

[CogSci2024](https://cognitivesciencesociety.org/cogsci-2024/) was a blast. Lots of interesting talks and posters. It was particularly nice to see how the cogsci community approaches certain questions differently from the ML people and yes, it's *quite* different, even the methodology seems to be different. From what I saw cogsci people tend to engage more in the classic scientific method - hypothesis creation, implementation, and experiments, conlusions. With ML, deep learning specifically, it's more of an engineering approach, where the emphasis is on practical results and proper benchmarking. This is what we'll discuss here. All in all, the conference was great. I presented some ideas, made new friends, learned some things, disagreed on others, explored Rotterdam (the host city) and left excited and with new ideas.

My strategy here is to briefly cover multiple topics at a relatively superficial level. This still has the benefit that one learns what are the main questions and approaches, and can therefore look up the details later on. 

### Workshops

First, an interesting workshop was [CogGraph](https://coggraph.github.io/) - a mixture of cognitive science and computer graphics. There are many graphics programs which are meant to be "consumed" by people, and in that case what is rendered has to go through our perception, which has peculiar biases and heuristics. Therefore, a question arises: how do we adapt the graphics pipelines or the visual parts in an application so as to maximize some effect on the user? For example, it matters how you present visual results, as some graphs have naturally salient visual features which are quickly picked up by us. And in those cases it matters whether the salient features (trendlines, clusters, spatial distributions) in your presentation are aligned to highlight accurately the underlying data or not. This can be used to produce intuitive memorable plots or to intentionally confuse others.

Another example is with graphics simulations. Modern renderers are becoming quite sophisticated - they are [modular](https://github.com/NVlabs/nvdiffrast), efficient, and often [differentiable](https://github.com/mitsuba-renderer/mitsuba3), so you can take derivatives of the entire simulation with respect to camera poses, geometry, [BSDFs](https://en.wikipedia.org/wiki/Bidirectional_scattering_distribution_function), and volumes. And the question of interest is basically how do humans reconstruct the world around us, that is, how do we estimate positional relationships, material properties, physically-realistic object interactions? This is sometimes called "inverse graphics" - given an image, how do we estimate the scene object properties that upon rendering give rise to that image?

Note that modern computer graphics have more or less achieved their longstanding dream of complete photorealism. In some tasks they are becoming superhuman, as we can simulate things which humans cannot even imagine (in sufficient details) - objects breaking into many pieces, particles interacting, knots twisting, nonlinear elastic deformations [1], objects warping [2]. But humans have other abilities which are still missing from software approaches, e.g. the ability to infer object stiffness from shape and motion cues [3], or the ability to "see" liquids from static snapshots [4]. A useful approach to bridging the gap between photorealistic graphics and intuitive humanlike inverse graphics has been to use 3D physics engines where inference of object properties is achieved using MCMC sampling [5]. All in all, this type of vision mixed with cognitive science has *many* interesting questions and is a joy to explore.

There was also a nice [workshop on in-context learning](https://jacquespesnot.github.io/2024_CogSci_Workshop/). This refers to learning from multiple input-output examples at test time. Instruction-tuned LLMs have shown the incredible value of such a capability. Note that when the prompt already contains a few examples for the task at hand the important information mixing happens at the level of individual tokens, not at the level of the weights. In various personal experiments I've found improved performance because of this. Another thing I realized is that with in-context learning, the fact that we have a few ready examples allows us to learn a small dynamics model and a critic over them. Once we have the dynamics and a critic we can do planning. This raises the question of whether the critic or the responder can be extracted in an implicit form, or if we can build actual planning on top of the network.

Humans have an extraordinary ability for in-context learning. Consider a sequence problem where we are given relations and letters.

$$
L \rightarrow B \downarrow M \rightarrow M \downarrow T \leftarrow C \leftarrow E \uparrow F \uparrow \ ?
$$

It's difficult to say what symbol stands at the location of the $?$. Yet, if we picture a two-dimensional grid where we start at $(0, 0)$ and move according to the arrows, encountering the letters as we go, it becomes clear that the answer is $L$, as we have returned to the starting point.

The hippocampus and the prefrontal cortex are engaged with such spatial reasoning. Moreover, spatial is meant in an abstract sense, as we can compare different things semantically, which also involves an abstract "spatial" comparison. The neurons in the hippocampus represent your current location, as evidenced by the fact that they light up when encountering particular locations. This results in well-defined "grid", "place", or "border" cells. The prefrontal cortex also encodes positional information but differently, displaying joint past, present, and future sequence features, to be explained shortly. 
 
To solve a task like the one above, one needs to have an abstract relational schema, which represents the structure of the problem, and memory, which stores sensory observations (the letters) associated with the spatial locations. To predict the next sensory observation, one has to do *path integration* to trace the observed sequence onto the structural graph. Now, an RNN with external memory, some (key, value) store implemented as a Hopfield network, can solve this task. In its hidden state it learns to represent positional features in a manner that generalizes across tasks. The association between current position and sensory observation is stored in the (key, value) episodic memory. Based on this there is an argument that the hippocampus works like a RNN with external memory.

The case with the prefrontal cortex (PFC) is trickier. It is generally thought that unlike episodic memories in the hippocampus, the PFC stores sequence memories in the dynamics of neural activity (the exact patterns in neuronal firings). Can we model this setup using a RNN without external memory? Yes. First, we can think of total neural activity as a bunch of *slots*. And to predict the next observation we have to read-out from one of these slots, one which is fixed. Therefore, to predict a different observation we need to swap the content from a different slot into this fixed readout slot. The RNN thus learns to dynamically copy and shifts slot contents across different slots. Intuitively, the hidden state and the transition matrix are bigger because we are now tracking the relative position *to* each observation, rather than abstract task position. This is a theory of how PFC spatial reasoning works [6]. There are ways to compare RNN and human PFC activations.

There was also a cool workshop on compositionality in brains and machines. Compositionality refers to the ability to hierarchically compose concepts, obtaining newer concepts with altered meaning - obviously a crucial aspect of intelligence. In LLMs for example compositionality is achieved by mixing token features using self-attention. This kind of mixing can happen either step by step at generation time, or with many tokens in parallel, such as when processing the prompt. In humans I'd say it's still unclear. It's common to study how brain activity changes when we process a sentence slowly word by word vs when we process it in parallel, such as when a short sentence is shown only for a split second before it disappears. But not only word meanings compose, visual patterns and action sequences also compose.

### Talks

There were multiple interesting talks, but my favourite was probably Alison Gopnik's talk. According to her, there are three different cognitive capacities that trade-off against each other - exploration, exploitation, and care. Exploitation is dominant during adulthood, when we strive to achieve goals and maximize utilities. Exploration is dominant in our infancy and child years. Here our intelligence is directed towards trying and figuring out things. Common strategies are trial-and-error, and learning by doing. This is the area of intrinsic motivation, open-ended learning, even developmental robotics. But we're not really interested in learning *everything* about the world - just that which can be affected by our own actions.

This idea is quite profound. Our early-years curiosity is guided toward learning causal models of the world. To learn such models we need *interventions* (the `do` operator) and that's precisely why infants are hardcoded to act almost randomly, moving all the time, trying out stuff, in other words physically acting. All these interventions allow us to learn how the world changes following our actions and is precisely the idea of *empowerment* in RL - the behavioural bias which leads us to select actions likely to have larger rather than smaller impact on the environment.

However, exploration is costly. By definition it means not optimizing and not providing. You need somebody to take care of you while you explore. That's why there's the third type of cognitive drive - care, predominantly in the elderly. Evolution has developed this drive for obvious reasons. And while the talk was cheerful and engaging, my thoughts on this subject are much more depressing. The fact is that as we age, we become less curious, less creative, less open-minded. Our brains become less malleable. Our world models become more crystalized and less fluid. We stop recognizing new patterns. Learning stops and inference settles in. That's why even though the life expectancy increases, our *effective* lifespan is *much much* shorter.

There were other interesting talks on various topics like deep learning as a basis of cognition, lots of stuff on LLMs, predictive coding, autotelic goal-generating agents, etc. I realized that humans are not *fully*-autotelic. We can choose short- and long-term goals but we can't really choose what gives us biochemical rewards (almost impossible to rewire your dopaminergic circuits). Similarly, the brain, I think, does not do anything more than pattern matching. In that sense I think I am a "pattern purist". Sometimes I hear claims about the brain doing "combinatorial" reasoning, but what does that even look like? I am skeptical because I can't picture how anything other than pattern matching can be implemented in the substrate of our neurons.

In general, there were a lot of talks that place LLMs in a cognitive context and try to compare with humans. The general approach is: you run some carefully-designed cognitive experiment on human subjects and analyse their results, then you run it on a LLM. If its results have similar patterns to those of the human subjects, we can conclude that the LLM has similar biases, judgements, risk profiles, and whatnot. Naturally, this treats the LLM as a black box, only looking at its inputs and outputs. It does not utilize the fact that we can actually build these complicated systems to test our hypotheses. After all, AI is the only playground that allows us to build models of human cognition and test them out. Thus, I don't find this approach particularly interesting because it has the same empirical methodology as social science studies, except that the problem setting is not social, but rather has at least something to do with human reasoning.

ML and cogsci seem to have different methodologies. Cogsci is based on the scientific method - design experiments, collect results, fit a theory around them. Such theories offer mostly theoretical explanations about human behaviour and reasoning. ML, at least fields like NLP or vision, has more of an engineering approach - invent new algorithms, build models, benchmark. It emphasizes not understanding per se, but practical results. And it's easier to extract value from practical results as opposed to theoretical ones. This is where the free market comes in - it takes the research output and adapts it for value extraction by productizing it.

### My Project

I presented a poster on how to build RL agents that support a subjective virtual narrative about themselves. This is what we refer to as consciousness in humans. It's obviously a very reductionist approach. Even though I've had very good discussions with people who are non-reductionists as time passes I'm becoming more and more reductionist. After all, this *is* the way to understand things - you break them apart into primitives and learn how they compose. If something meaningful is missing from the model, you add it, and you still have *a model*. There is no reason to believe that the concept in question is anything other than the explanation offered by your model. If you claim so without scientific evidence, I can disprove it without scientific envidence. No one I've spoken with has been able to refute this logic so far.

I had very nice discussion at the poster session. People were genuinely curious and interested. They found it novel and I was happy explaining it. One person said *"But it's still missing phenomenological experiences"* and I was like *"What does that mean? You know that's not a healthy scientific term, right?"*. I also found out who my meta-reviewer was. In general, I wish some of the legendary scientists who were there (like Josh T.) saw my poster but, alas, they were busy.

In terms of how my interests evolve, I feel that learning about neuroscience and cognitive science, while definitely interesting, has only increased my appreciation towards computer science and engineering as a whole. AI is what I want to do right now and I'd be more than happy to devote a large part of my life to it. You see, cogsci has a fundametal limit, that of the capability of the human brain, whereas AI is limitless. You can go beyond what's biologically possible... to incredible results.

### The Trip

Finally, some observations on Rotterdam. It's a great city, very modern, with a beautiful skyline and a strong maritime feel. The arrival was tough - two flights and a train from Schiphol to Rotterdam. But the remaining free time that day was worth it. The maritime museum was pretty good. It had one section decorated like an offshore drilling rig. You put on a safety vest and climb up some stairs, reaching a closed room with guardrails and huge video walls playing animations of a thunderous grey sky and a stormy sea. There were lots of miniature models of specialized drilling and support ships and it was great to learn above how wind turbines are installed, how oil is extracted, or how a [remotely operated underwater vehicle](https://en.wikipedia.org/wiki/Remotely_operated_underwater_vehicle) (ROUV) is handled.

Outside there's a great harbour and you can climb onto some of the ships. Further down there's a place with artificial waves in one of the canals where people can surf. I saw a goose casually walking on the street there and crossing like a human. In general the city is quite nice, there are lots of canals with clear green water and kelp sticking out of the seafloor. The architecture is modern because the city was rebuilt after all the WW2 bombing. The [Erasmusbrug](https://en.wikipedia.org/wiki/Erasmusbrug) and the [Depot Boijmans Van Beuningen](https://en.wikipedia.org/wiki/Depot_Museum_Boijmans_Van_Beuningen) were great to explore. But the absolute highlight was the [Euromast](https://en.wikipedia.org/wiki/Euromast) tower with its gorgeous view and nice club beats. From the top one can see both the downtown and the docklands. Foodwise, one cannot complain. There are Dutch restaurants, English pubs, Asian places. We ate a 6-plate meal in a chic Asian-fusion restaurant and paid only 45 euro ppax. In the closing day of the conference there was some strange summer carnival and the streets were busy. But my plan was to go to Amsterdam.

Amsterdam is a crazy city. Very beautiful but also crushingly crowded with people of all backgrounds and nationalities. I only spent around 24 hours there but I got a good sense of the ambience. It has stunning picturesque canals and great museums (e.g. Van Gogh, [Rijksmuseum](https://en.wikipedia.org/wiki/Rijksmuseum)). My hotel was far enough from the city center to allow for a good amount of walking, while still being close enough to see attractions like the [Royal Palace](https://en.wikipedia.org/wiki/Royal_Palace_of_Amsterdam) along the way. Some of the other attractions are not for blogging$^*$. All in all, the place definitely has a very unique feel to it. I like it. And it was a worthy conclusion to the trip.

<figure>
    <img class='extra_big_img' src="/images/euromast.jfif" alt="View from Euromast" width="1200">
    <figcaption>Figure 1: The view from Euromast. </figcaption>
</figure>

### References
[1] Li, Minchen, et al. Incremental potential contact: intersection-and inversion-free, large-deformation dynamics. ACM Trans. Graph. 39.4 (2020): 49.   
[2] Mehta, Ishit, Manmohan Chandraker, and Ravi Ramamoorthi. A level set theory for neural implicit evolution under explicit flows. European Conference on Computer Vision. Cham: Springer Nature Switzerland, 2022.  
[3] Paulun, Vivian C., et al. Shape, motion, and optical cues to stiffness of elastic objects. Journal of vision 17.1 (2017): 20-20.   
[4] Paulun, Vivian C., et al. Seeing liquids from static snapshots. Vision research 115 (2015): 163-174.    
[5] Wu, Jiajun, et al. [Galileo: Perceiving physical object properties by integrating a physics engine with deep learning.](https://proceedings.neurips.cc/paper/2015/hash/d09bf41544a3365a46c9077ebb5e35c3-Abstract.html) Advances in neural information processing systems 28 (2015).   
[6] Whittington, James CR, et al. [On prefrontal working memory and hippocampal episodic memory: Unifying memories stored in weights and activity slots.](https://www.biorxiv.org/content/biorxiv/early/2024/03/04/2023.11.05.565662.full.pdf) bioRxiv (2023): 2023-11.
