---
title: Rationality Is Scarce
date: 2022-11-26 07:00:00 +0200
tags: ultra-rationalism
excerpt_separator: <!--more-->
slug: rationality_is_scarce
---

I open up Dostoevsky's *Notes From the Underground*. I start reading the first paragraph.
> I am a sick man... I am a spiteful man. I am an unattractive man. I believe my liver is diseased. However, I know nothing at all about my disease, and do not know for certain what ails me. I don’t consult a doctor for it, and never have, though I have a respect for medicine and doctors. Besides, I am extremely superstitious, sufficiently so to respect medicine, anyway (I am well-educated enough not to be superstitious, but I am superstitious). No, I refuse to consult a doctor from spite. That you probably will not understand. Well, I understand it, though. Of course, I can’t explain who it is precisely that I am mortifying in this case by my spite: I am perfectly well aware that I cannot “pay out” the doctors by not consulting them; I know better than anyone that by all this I am only injuring myself and no one else. But still, if I don’t consult a doctor it is from spite. My liver is bad, well—let it get worse!

I get immediately triggered. I close the book.
<!--more-->

How is it that people like that, who apparently know what's best for them, still purposefully do the exact opposite? What's the driving force behind their decisions? What motivates them to go against the best known rational action?

I have gradually come to realize that in our modern lives, in the Western societies at least (though I suppose this holds also in other parts of the world) there is a huge difference between knowing the truth and acting on it. 

Finding the truth is a problem within the space of competing ideas. It requires evaluating the merits of multiple competing explanations of the world and ordering them by their validity. The ordering is subjective from person to person and depends on the mental scheme that each one of us uses to inductively build knowledge of the surrounding world. 

Acting on the truth is much more important because it leads to realizations in the space of the real world and is what brings change to it. Acting on the truth is directly related to how much you value truth. What good is a well thought out plan if you don't follow it? 

If I have to oversimplify and speak with RL terminology, finding truth is about having accurate Q-values $Q(s, a_1), ..., Q(s, a_n)$, for all available actions $a_i$ and being rational is about executing the best action $
\underset{a}{\mathrm{argmax}} \ Q(s, a).
$

You can be very intelligent and understand how the world works, but at the same time be irrational and not take the most optimal action. As a consequence, you may squander your gift. Does it matter if you're smart enough to identify the best action, but are unwilling to execute it, or you are not able to find it in the first place? From a pragmatic outsider perspective, it doesn't matter - the optimal action is not executed regardless.

[Verificationism](https://en.wikipedia.org/wiki/Verificationism) is the principle that only statements that are empirically verifiable (through senses, mathematical proofs, etc.) are cognitively meaningful. Anything else is tautological - it may provoke an emotional reaction, but it does not convey any truth value, information or factual content. In that sense fields like theology, ethics, and aesthetics are in essense meaningless.

If we extend the verificationism principle to control settings, we get that only actionable situations - those in which our actions can make a difference - are meaningful, as they are the ones amenable to improvement by our actions. Anything else is attention clutter. A concrete example of this rule is that you should not compete with others too much, because you cannot change them. But you should compete always with lagged version of yourself and improve over your expectations. In reinforcement learning this is called *self-play* and is incredibly powerful. Competition should not be spatial - with other agents - but rather temporal - with past versions of you.

In the real world there are many explanations for not taking the optimal greedy action:

- People have to **balance multiple tasks** and it may happen that the greedy action to one task is a suboptimal action for another, more important task. This is very common setting in economics, where households have to decide between consuming today or saving so as to consume more tomorrow. Firms have to decide between distributing profits as dividends or inversting them in long-term capital. Governments have to decide whether to borrow at the expense of future generations so they can spend now.
- The greedy action may be outside of the **law**. Obviously, it may be beneficial to acquire resources by violence and plunder. But laws and law enforcement raise the costs of engaging in similar reprehensible behaviour and if the cost of doing so is too high to you, you obviously should not do it, morals aside.
- **Dogmatic beliefs** can block entire topics from your consideration. Whether it's organized religion, folk traditions, political beliefs, or scientific theories of everything, believing without questioning will only make your world model more fragile.

That last one is what really makes my blood boil. Because beliefs are a type of actions. We often act based on our beliefs and hence the choice over beliefs affects our behaviour. Here are some examples of irrational mistakes I typically notice:

- Judging an argument by its meta-content, instead of its actual content. Does the speaker's outfit, demeanor, nationality, or past history matter when judging the validity of their argument? No, it shouldn't. What determines the validity is the logical content of the argument alone. In an ideal world, persuasion does not contain *ethos* and *pathos*, only *logos*.
- Disapproving of a political argument just because the proposal seems extreme. Yes, most bad proposals are extreme in nature, but that does not mean that any extreme proposal is bad. Invert the reasoning, use Bayes.
- Continuing to keep up with past traditions while at the same time agreeing that they're silly. If you are not religious and agree that lighting a candle will not improve your life in any way, then stop doing it. The only exception here is if you're doing it to appease others, i.e. due to expectation.
- Attributing rare events to fate, destiny, God, or any supra-natural entity. Things happen due to either causal reasons, or pure randomness. Adopting a scientific and natural explanation for the world produces models with absurdly better predictive power and considerably shorter descriptions than any supra-natural proofless argument.

I find the principles above very useful also because they tend to simplify the way we look at the world. The modern world is constantly becoming more and more complicated - there are more diverse opinions, more interdependencies and relationships to take into account. One way to deal with that complexity is by having simpler, shorter, and more concrete views on the various topics.

And about religion in general. Many people do not believe in God, an almighty white-bearded person micromanaging our daily lives, but claim to believe, in one form or another, in an "vast and infinite energy" guiding us. They call it the cosmos, the universe, or it might be any other bland term, but it's always a high-level type of entity that is responsible for our hardships. Do I need to state how preposterous this is? It's the same with the multiverse, just a big unprovable fad.

Let's see some quotes by the Underground man. He claims that

> In despair there are the most intense enjoyments, especially when one is very acutely conscious of the hopelessness of one's position.

and similarly asks

> How can a man of consciousness have the slightest respect for himself?

It would seem that acute consciousness is, presumably, the highest form of understanding of the world and attaining it brings about this inertia which incapacitates you, and prevents you from doing anything and becoming anyone, thus the ongoing self-loathing. But consciousness is not the "end". What I'm pushing for is the realization that our consciousness is a physical phenomenon. It's bounded by the same laws of physics and the same limits of computation as everything else. We are not outside of the system, we are parts of it.

>I tell you solemnly, that I have many times tried to become an insect. But I was not equal even to that. I swear, gentlemen, that to be too conscious is an illness- a real thorough-going illness.

This reasoning seems quite limited. The human consciousness is a modelling mechanism - a virtual reality where we attribute meaning to various objects and actions. It's purpose is to make our behaviour more guided and cohesive. The realization of our inadequacies and limitations should not lead to nihilism and angst, but rather to humility and awe. We are born with already defined reward functions which we just need to maximize. And in that sense, rationality is a virtue. Take pride in it.