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
int compute_length(string s) {
    return s.length();
}

int compute_mid_index(string s) {
    return s.length()/2;
}
```


A most basic object in the category of types is the $\textbf{Void}$ type, representing a collection with no values. Note that this is not C++'s ```void``` type. To describe it this object, we specify its incoming and outgoing arrows. The incoming arrows are constructors because they represent functions with return type $\textbf{Void}$. The outgoing arrows are destructors, or transformers, because they represent functions which output any other type $\textbf{A}$ from $\textbf{Void}$.

$$
f: \textbf{A} \rightarrow \textbf{Void}
$$

Type $\textbf{Void}$ cannot be constructed because it has no values, so there are no incoming arrows (apart from the identity one).

$$
g: \textbf{Void} \rightarrow A
$$

The $\textbf{Void}$ object has arrows going to all other objects, because it can be transformed into any other type $\textbf{A}$. This function can be defined but never called, because to call it, we need to provide it with a value of type $\textbf{Void}$, of which there are none.

The unit type $()$ is the opposite of $\textbf{Void}$. It has only one possible value, a dummy variable that can be renamed, replaced with a placeholder or even elided. This is the C++ type ```void``` or Python's `None`. The unit type has a single incoming arrow from all other types. Here is the unique constructor from $\textbf{Int}$:

```c++
void construct_void(int n) {
    return;
}
```

It has many transformers. Here is one from $()$ to $\textbf{Int}$.
```c++
int generate_int(void) {
    return 42;
}
```

Another important type is the product type, represented as pairs and tuples. The constructor morphisms take elements of two possibly different types and return an element of the corresponding pair type. The transformer elements are called projections and simply return the first or second elements.
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

An analogy to product types are sum types. The sum type of ```string``` and ```int``` is the collection of values of all strings and integers. In Python's type annotations this would be ```Union[str, int]``` or ```str|int```. To construct a value of type ```str|int``` we need to be given a value of either ```str``` or ```int```. To transform a value of ```str|int``` into, say, ```bool```, we need to do case matching and use a morphism from ```str``` to ```bool``` or one from ```int``` to ```bool```.

The product and sum types discussed so far are extra useful because they allow us to combine types together. If we look at the product type as an operation taking in two types and outputting a third one, this operation behaves a lot like multiplication:
- It is associative, up to an isomorphism. If $(\textbf{A}, (\textbf{B}, \textbf{C})) \cong ((\textbf{A}, \textbf{B}), \textbf{C})$, this means that there is a pair of mutually-inverse morphisms that rearrange these tuples.
- The unit type $()$ acts as a multiplicative unit, i.e. $(\text{Unit}, \text{A}) \cong \text{A} \cong (\text{A}, \text{Unit})$.

These properties are satisfied also with respect to the operation of constructing sum types:
- Constructing sum types is an associative operation, $\text{Union}[\text{A}, \text{Union}[\text{B}, \text{C}]] \cong \text{Union}[\text{Union}[\text{A}, \text{B}], \text{C}]$.
- The $\textbf{Void}$ type acts as an additive zero, $\text{Union}[\textbf{Void}, \text{A}] \cong \text{A} \cong \text{Union}[\text{A}, \textbf{Void}]$.

What this implies is that we can define an algebra of types where types can be summed and multiplied to yield new types. For example, the polymorphic type $\text{Option}[\text{A}]$ can be defined as $\text{Union}[(), \text{A}]$. Similarly, the list type can be defined recursively as $\text{List}[\text{A}] = \text{Union}[(), (\text{A}, \text{List}[\text{A}])]$, and so on. In this way one can add all kinds of trees, maps, and structures. I find it amazing how we can obtain an incredible abundance of types from only a small set of initial building blocks.

But there's still something missing - function types. To get to them, we need to first explore what functors are. A *functor* is a mapping that takes in a given category and outputs a new category, but with the same structure, up to an isomorphism. 

$$
F: \mathcal{C}_1 \rightarrow \mathcal{C}_2 \\
$$

Since a category consists of objects and morphisms, the functor takes in objects in the first category and outputs objects in the second one. Similarly, it takes in morphisms in the first category and outputs morphisms in the second one. If $f: \textbf{A} \rightarrow \textbf{B}$ is a morphism, then it is mapped to $F[f]: F[\textbf{A}] \rightarrow F[\textbf{B}], \forall \textbf{A}, \textbf{B} \in \mathcal{C}_1$.

Functors are very useful because they allow us to translate one category to another in a meaningful way. In the context of types, however, what we're more concerned is endofunctors, which are simply mappings between the same category. Note that while a morphism $f:\textbf{A} \rightarrow \textbf{B}$ is a function taking in a value of type $\textbf{A}$ and outputting one with type $\textbf{B}$, functors take in entire types as input and produce entire types as output.

Parametrically polymorphic type definitions are candidates for being functors. Take for example the option type, defined as $\text{Option}[\textbf{A}] = \text{Union}[(), \text{A}]$. This is not a type, but rather a type constructor because $\textbf{A}$ represents any type. Only when we specify an $\textbf{A}$, like $\textbf{Int}$, we get a concrete type, like $\text{Option}[\textbf{Int}]$. That's how it maps objects to objects. But how does it map morphisms to morphisms?

If $f$ is a morphism between types $A$ and $B$, then $F[f]$ is a mapped morphism between types $F[a]$ and $F[b]$, which is a function taking a value $x$ of type $Option[A]$ and outputting a value $y$ of type $Option[B]$. This function is defined, intuitively, as follows: if $x$ is $()$, return $()$, otherwise return $f(x)$. You can check that this definition of $F[f]$ preserves composition and identity. Therefore, the type constructor $\text{Option}[A]$ together with $F[f]$ form a functor.