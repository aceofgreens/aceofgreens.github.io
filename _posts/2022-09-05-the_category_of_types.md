---
layout: post
title: The Category of Types
date: 2022-09-05 16:00:00 +0200
tags: [cs]
---

One of the most important problems in computer science is that of program verification - proving the correctness of the algorithm in a formal, mathematical way. In order to be sure that our solution is implemented correctly, we need to have mathematical guarantees of its properties. Thus, it's common to represent programs using mathematical objects. Some of these are very high-level, like finite state machines. Others are more concerned with the interpretation of the individual statements in the programming language. This post explores the curious and absurdly abstract theory of categories and its use cases when considering programming types.

Viewing programming types as a category is a perspective-changing warp and requires knowing some category theory, so we begin with that. The ingredients of a *category* are:
- Objects, or points, these are the objects we'll consider. Let's denote them with $A$, $B$, $C$, ...
- Morphisms, or arrows between points, these are the relationships between the objects. We denote the morphism $f$ between $A$ and $B$ as $f: A \rightarrow B$.

Right, but a collection of objects with arbitrary morphisms between them is far too general and can represent literally anything. A category has more structure coming from the following restrictions on the morphisms:
- Every object has an identity morphism, relating it to itself. For example, the identity morphism of ofject $C$ is $1_C$ - an arrow from object $C$ to $C$ itself.
- Morphisms compose. If $f: A \rightarrow B$ and $g: B \rightarrow C$, then there exists a morphism $h$ such that $h: A \rightarrow C$. We denote $h$ as $g \circ f$.
- Morphisms satisfy the identity law - if $f: A \rightarrow B$, then $f \circ 1_A = f $ and $1_B \circ f = f $.
- Composition is associative, i.e. $f \circ (g \circ h) = (f \circ g) \circ h$.

With these requirements in place, we can now mention the most useful category, $\textbf{Set}$, the category of sets. Here, the objects are standard sets and the morphisms are functions from one set to another. The composition of morphisms is the standard composition of functions, which is associative and satisfies the identity law. For example, let's look at two objects, $\mathcal{S}_1 = \\{1, 2, 3\\}$ and $\mathcal{S}_2 = \\{4, 5, 6 \\}$. One morphism between them is $f_1: \mathcal{S}_1 \rightarrow \mathcal{S}_2$ such that $f_1(x) = 4, \forall x \in \mathcal{S}_1$. Another one is $f_2(x) = 5, \forall x \in \mathcal{S}_1$. Obviously, there can be multiple morphisms between any two objects.

In the context of programming, we can form the category of data types, whose objects are the individual types, and whose morphisms are functions between types. A type is, intuitively, a collection of values. The type $\textbf{Bool}$ contains the values $\text{true}$ and $\text{false}$. In reality, all types contain also the special value $\perp$, indicating that the function may not return due to runtime errors, exceptions, unbounded loops or infinite recursion, but we'll ignore this. As an example, take the types ```string``` and ```int``` from C++. Two particular morphisms from ```string``` to ```int``` are: 

```c
// Morphisms from type string to type int
int compute_length(string s) {
    return s.length();
}

int compute_mid_index(string s) {
    return s.length()/2;
}
```


A most basic object in the category of types is the $\textbf{Void}$ type, representing a collection with no values. Note that this is not C++'s ```void``` type. To describe this object, we specify its incoming and outgoing arrows. The incoming arrows are constructors because they represent functions with return type $\textbf{Void}$. The outgoing arrows are destructors, or transformers, because they represent functions which output any other type $\textbf{A}$ from $\textbf{Void}$.

Type $\textbf{Void}$ cannot be constructed because it has no values. As a result, no function returning a value of type $\textbf{Void}$ can be defined, so there are no incoming arrows (apart from the identity one). It has outgoing arrows going to all other objects, because it can be transformed into any other type $\textbf{A}$. These function can be defined but never called, because to call it, we need to provide it with a value of type $\textbf{Void}$, of which there are none. It also resembles the fact that any conditional statement is true, if what you condition on is false (sometimes called a vacuous statement).

The unit type $()$, or $\textbf{Unit}$, represents a collection with only one possible value - a dummy variable that can be renamed, replaced with a placeholder or even elided. This is the C++ type ```void``` or Python's `None`. The unit type has exactly one incoming arrow from all other types because there is only one value of type $\textbf{Unit}$. To produce a unit from an integer, we just discard the integer and returning the only possible unit value. Type $\textbf{Unit}$ has many outgoing morphisms. The number of morphisms from unit to integer is equal to the number of different integers. Note that this allows us to identify each integer according to its morphism from the unit type.

The properties of the $\textbf{Unit}$ and $\textbf{Void}$ types are captured in the following graph.
<figure>
    <img class='small_img' src="/resources/basic_types.svg" alt="Basic types" width="1200">
    <figcaption>Figure 1: The types $\textbf{Void}$ and $\textbf{Unit}$. Arrows indicate individual morphisms. $\textbf{Void}$ doesnt' have any incoming morphisms because no function can return a value from the empty set. It has many outgoing morphisms representing functions which cannot be implemented in practice. Type $\textbf{Unit}$ has a single incoming morphism from all other types and multiple outgoing morphisms to all other types, except $\textbf{Void}$. </figcaption>
</figure>


Another important type is the product type, represented as pairs and tuples. Technically, there are many product types because there are many possible pairs and tuples. The incoming morphisms take elements of two possibly different types and return an element of the corresponding pair type. The transformer elements are called projections and simply return the first or second element. Product types have a natural correspondence with the $\text{AND}$ logical operator. 

```c++
std::pair<int, string> create_pair(int n, string s) {
    return std::pair<int, string> p {5, "abc"};
}

int return_first(std::pair<int, string> p) {
    return p.second;
}

string return_second(std::pair<int, string> p) {
    return p.second;
}
```

An analogy to product types are sum types. The sum type of $\textbf{String}$ and $\textbf{Int}$ is $\text{Union}[\textbf{String}, \textbf{Int}]$ - the collection of values of all strings and integers. In Python's type annotations a sum type would be represented as ```Union[str, int]``` or ```str|int```. To construct a value of type ```str|int``` we need to be given a value of either ```str``` or ```int```. To transform a value of ```str|int``` into, say, ```bool```, we need to do case matching and use a morphism from ```str``` to ```bool``` or one from ```int``` to ```bool```. Lastly, sum types correspond to the logical operator $\text{OR}$. There is a deep and beautiful correspondence between types and logical proposition called the Curry-Howard isomorphism but this is a separate topic.

The concept of a monoid plays a significant role in category theory. A monoid is a set of elements $S$, with an operation $\bullet: S \times S \rightarrow S$ such that:
- $\bullet$ is associative, $a \bullet (b \bullet c) = (a \bullet b) \bullet c, \forall a, b, c \in S$ 
- there exists an element $e$ in $S$ for which $e \bullet a = a \bullet e = a, \forall a \in S$.

As an example, the real numbers with $\bullet$ being multiplication form a monoid where $1$ is the multiplicative unit. They also form a separate monoid under summation where the unit is 0. This is valid also for integers, rational, and complex numbers.

The product and sum types discussed so far are extra useful because they allow us to combine types together. If we look at the product type as an operation taking in two types and outputting a third one, this operation behaves a lot like multiplication:
- It is associative, up to an isomorphism - $(\textbf{A}, (\textbf{B}, \textbf{C})) \cong ((\textbf{A}, \textbf{B}), \textbf{C})$. This means that while these two types are different, they contain the same information, and there is a pair of mutually-inverse morphisms that can rearrange these tuples.
- The unit type $()$ acts as a multiplicative unit, i.e. $(\text{Unit}, \text{A}) \cong \text{A} \cong (\text{A}, \text{Unit})$.

Thus, the category of types is a monoidal category because we have a monoid in types, under the product operation. This is also the case with regard to constructing sum types:
- Constructing sum types is an associative operation up to an isomorphism, $\text{Union}[\text{A}, \text{Union}[\text{B}, \text{C}]] \cong \text{Union}[\text{Union}[\text{A}, \text{B}], \text{C}]$.
- The $\textbf{Void}$ type acts as an additive zero, $\text{Union}[\textbf{Void}, \text{A}] \cong \text{A} \cong \text{Union}[\text{A}, \textbf{Void}]$.

What this implies is that we can define an algebra of types where types can be summed and multiplied to yield new types. For example, the polymorphic type $\text{Option}[\text{A}]$ can be defined as $\text{Union}[(), \text{A}]$. Similarly, the list type can be defined recursively as $\text{List}[\text{A}] = \text{Union}[(), (\text{A}, \text{List}[\text{A}])]$, and so on. In this way one can add all kinds of trees, maps, and structures. One can even compute identities like $x^2 - y^2 = (x-y)(x+y)$ on types. I find it amazing how we can obtain an incredible abundance of types from only a small set of initial building blocks.

But there's still something missing - function types. Let's pick two types $\mathbf{A}$ and $\mathbf{B}$. It can be proven than the collection of morphisms between $\mathbf{A}$ and $\mathbf{B}$ is itself an object in our category of types. This object represents the function type of all functions from $\textbf{A}$ to $\textbf{B}$. Its incoming arrows, or constructors, are ```lambda``` expressions. Its outgoing arrows are ```eval``` statements. We can also mention that function types correspond to $\Rightarrow$, implication in logic.

From here, unfortunately, the theory about our type system only goes deeper. A *functor* is a mapping between entire categories. It takes in one category and outputs another one, while preserving the structure of the first.

$$
F: \mathcal{C}_1 \rightarrow \mathcal{C}_2 \\
F[X] = Y, \  X\in \mathcal{C}_1, Y \in \mathcal{C}_2 \\
F[f] = f', \  f \in \mathcal{C}_1, f' \in \mathcal{C}_2\\
$$

Since a category consists of objects and morphisms, the functor takes in objects in the first category and outputs objects in the second one. Similarly, it takes in morphisms in the first category and outputs morphisms in the second one. If $f: \textbf{A} \rightarrow \textbf{B}$ is a morphism, then it is mapped to $F[f]: F[\textbf{A}] \rightarrow F[\textbf{B}], \forall \textbf{A}, \textbf{B} \in \mathcal{C}_1$.

Functors are very useful because they allow us to translate one category to another in a meaningful way. In the context of types, however, what we're more concerned is endofunctors, which are simply mappings between the same category. Note that while a morphism $f:\textbf{A} \rightarrow \textbf{B}$ is a function taking in a value of type $\textbf{A}$ and outputting one with type $\textbf{B}$, functors take in entire types as input and produce entire types as output.

Parametrically polymorphic type definitions are candidates for being functors. Take for example the option type, defined as $\text{Option}[\textbf{A}] = \text{Union}[(), \textbf{A}]$. This is not a type, but rather a type constructor because $\textbf{A}$ represents any type. Only when we specify an $\textbf{A}$, like $\textbf{Int}$, we get a concrete type, like $\text{Option}[\textbf{Int}]$. That's how it maps objects to objects. But how does it map morphisms to morphisms?

If $f$ is a morphism between types $A$ and $B$, then $F[f]$ is a mapped morphism between types $F[a]$ and $F[b]$, which is a function taking a value $x$ of type $\text{Option}[\textbf{A}]$ and outputting a value $y$ of type $\text{Option}[\textbf{B}]$. This function is defined, intuitively, as follows: if $x$ is $()$, return $()$, otherwise return $f(x)$. You can check that this definition of $F[f]$ preserves composition and identity. Therefore, the type constructor $\text{Option}[\textbf{A}]$ together with $F[f]$ form a functor.

Just like a functor is a mapping between categories, we can define a mapping between functors. This is called a *natural transformation*. If we fix two functors $F_1$ and $F_2$ from category $\mathcal{C}_1$ to category $\mathcal{C}_2$ and fix object $\textbf{A} \in \mathcal{C}_1$, then after applying the two functors we get two objects $F_1(\textbf{A})$ and $F_2(\textbf{A})$ in category $\mathcal{C}_2$. The natural transformation between $F_1$ and $F_2$ maps $F_1(\textbf{A})$ to $F_2(\textbf{A})$, but this is an existing morphism in $\mathcal{C}_2$. So the natural transformation between $F_1$ and $F_2$ takes an object $\textbf{A}$ in $\mathcal{C}_1$ and returns a morphism in $\mathcal{C}_2$.

As an example, fix two functors, $F_1[\textbf{A}] = \text{List}[\textbf{A}]$ and $F_2[\textbf{A}] = \text{Tuple}[\textbf{A}]$, which in the category of types are type constructors. If we set $\textbf{A}$ to $\textbf{Int}$, the natural transformation between them returns a function taking in a value of type $\text{List}[\textbf{Int}]$ and outputting a value of type $\text{Tuple}[\textbf{Int}]$. If $\textbf{A}$ is $\textbf{Bool}$, we get a function with signature $\text{List}[\textbf{Bool}] \rightarrow \text{Tuple}[\textbf{Bool}]$. This shows that the natural transformation between these two functors is a polymorphic function with signature $\text{List}[\textbf{A}] \rightarrow \text{Tuple}[\textbf{A}]$. This is the power of natural transformations, they represent polymorphic functions.

We said above that functors mapping objects and morphisms from one category to itself are called endofunctors. Interestingly, the collection of all endofuctors in category $\mathcal{C}$ forms another category $\mathcal{C}'$. The objects of $\mathcal{C}'$ are the endofunctors in $\mathcal{C}$ and the morphisms of $\mathcal{C}'$ are the corresponding natural transformations in $\mathcal{C}$.

In this magical category, consider the binary operation of composing two endofunctors. This is always possible since endofunctors map categories to themselves. Now, within this category $\mathcal{C}'$ where objects are endofunctors, there exist particular objects which together with particular morphisms form a monoid under the operation of endofunctor composition. Such objects are *monads* in the original category $\mathcal{C}$.

A monad in $\mathcal{C}$ is an endofunctor $T$ of $\mathcal{C}$ together with two natural transformations $\eta: 1_C \rightarrow T$ and $\mu: T \times T \rightarrow T$ such that:
- $\eta$ acts as a unit under composition, $\mu \circ T \eta = \mu \circ \eta T = 1_T$
- $\mu$ acts as a binary operator for composition, $\mu \circ T\mu = \mu \circ \mu T$.

The conditions on $\eta$ and $\mu$ ensure that the resulting structure is a monoid.

Let's see what these concepts in practice by examining the $\text{Option}$ monad.
The $\text{Option}$ monad consists of:
- A type constructor (endofunctor) $\textbf{A} \rightarrow \text{Option}[\textbf{A}]$ which takes in and outputs entire types
- A polymorphic function ```unit``` (natural transformation $\eta$) with signature $\textbf{A} \rightarrow \text{Option}[\textbf{A}]$ which takes in and outputs values of type $\text{A}$ and $\text{Option}[\textbf{A}]$, respectively.
- A polymorphic function ```bind``` (natural transformation $\mu$) with signature $(\text{Option}[\textbf{A}], \textbf{A} \rightarrow \text{Option}[\textbf{B}])\rightarrow \text{Option}[\textbf{B}]$

The function `unit` takes in a value and wraps it in the new type $\textbf{Option}$. It acts as a left identity for `bind`, meaning that `bind(unit(x), f) = f(x)`. It is also a right identity for `bind`, meaning that `bind(ma, unit) = ma`, where `ma` is an instance of the $\text{Option}[\textbf{A}]$ type, for some concrete $\textbf{A}$. The function `bind` takes in an option instance and a function $f$. It then extracts the inner value from the option instance, applies $f$ to it, and re-wraps the result in another option.

In essence, monads allow us to capture function composition and decorate it with additional functionality. Some of the functions we care about may have side effects like writing to a file or may even contain runtime errors.



<!-- Add that some things are purposefully left out, definitions of natural transformations, sum types, product types, function types. -->