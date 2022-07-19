---
layout: post
title: Structure and Interpretation of Computer Programs
date: 2022-07-08 16:00:00 +0200
tags: [cs]
---

This post is a short summary of the first three chapters of Hal Abelson and Gerald Jay Sussman's wizard book, [Structure and Interpretation of Computer Programs](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs), which I read, much to my embarassment, only recently.

### Building Abstractions with Procedures

Programming is about decomposing problems into smaller more manageable subproblems. You then "compose" the solutions of these subproblems to obtain a solution for the real problem. In a way, composition is the essence of programming (ask Bartosz Milewski). A good programming language then has 3 main mechanisms which facilitate composition:
1. **Primitive expressions**, which represent the simplest entities the language is concerned with
2. **Means of combination**, by which compound elements are built from simpler ones,
3. **Means of abstraction**, by which compound elements can be named and manipulated as units.

The primitive expressions consist of primitive values and their types - integers, strings, floats - as well as any built-in operators. The means of combination are for example generic types like tuple and list, and the means of abstraction are features like being able to write custom procedures, classes, iterators, context managerts, and so on.

These 3 mechanisms are conceptual, they define how the language will work in principle. But to actually implement a program and run it, an interpreter is needed. An interpreter is a program that carries out the computational processes defined in a given programming language. A program without an interpreter is just a mathematical description of objects and relationships. An interpreter allows us to evaluate this description to produce results.

Central to composition is the ability to name objects, which greatly facilitates programming and is a handy tool in managing the complexity of programs. Naming is simply a mapping between names as keys, and objects as values. This association requires the interpreter to have an **environment** - a memory storing these mappings. Whenever an expression is evaluated, its variables are replaced with their values using the current name-to-value mapping.

Along with naming, procedures are the basis of abstraction. They allow us to name a set of statements, possibly depending on any arguments, and execute them repeatedly. If a procedure does not have assignment statements, it can be evaluated easily using a substitution model, either *normal order* (fully expand and then reduce) or *applicative order* (evaluate the arguments and then apply). Procedures with assignment statements cannot be handled using simple substitution and require the more powerful *environment* model.

*Higher order procedures* are those procedures that take in or output other procedures. Some use-cases are:
- In mathematics, to implement partial application, composition, fixed point finders, root finders, iterative improvement solvers,
- In decorators, to modify an input procedure by adjusting its input or output before or after its execution,
- In currying, to convert a function taking multiple arguments into a sequence of functions each taking one argument.

We can implement currying in Python 3 as follows:
```python
from inspect import signature
from typing import Callable

# An example function with 4 inputs
def f(x1: float, x2: float, x3: float, x4: float) -> float:
    if x4 != 0:
        return x1 * x2 + x3 / x4
    else:
        return x1 + x2 + x3

# First way to do currying is to hardcode the number of arguments
g = lambda w: (lambda x: (lambda y: (lambda z: f(w, x, y, z))))

# Second better way that can accomodate variable number of arguments
def curry(f: Callable):
    n_params = len(signature(f).parameters)

    def __curry(f, num_args, args):
        if num_args == 0:
            return f(*args)
        return lambda x: __curry(f, num_args - 1, args + [x])
    
    return __curry(f, n_params, [])

result1 = g(1)(2)(3)(4) # 2.75
result2 = curry(f)(1)(2)(3)(4) # 2.75
```
<!-- Discuss bound and free variables -->

We can also define procedures within procedures. Inner procedures are useful because they can provide **functional abstraction**, where the details of how a function is implemented are suppressed, and the particular function itself can be replaced by any other function with the same overall behavior. In other words, inner procedures allow us to build abstractions that separate the way the procedure is used from the details of how the procedure is implemented, this being the backbone principle of modularity.

Inner and outer procedures have a close resemblance to lambda calculus. Those variables appearing in the body of the procedure that can be consistently renamed without changing the procedure definition are called *bound* variables. Those which are not bound are *free*. The set of expressions for which a binding defines a name is called the *scope* of that name. As an example from the lambda calculus, consider $(\lambda x. x)(\lambda y.yx)$. In the first expression $x$ is bound. In the second expression $y$ is bound and $x$ is free, since its value depends on the context. The scope of $x$ is the first lambda and does not extend to the second one. 

In computer programming, a free variable is a variable in some procedure whose value depends on the context where the function is invoked, called or used. A free variable is determined dynamically at run time searching the name of the variable backwards on the function call stack. A bounded variable evaluation does not depend on the context of the function call. This is the most common modern programming languages variable type. In Python local variables, global variables and parameters are all bounded variables. 

As an example, consider the following in Python.

```python
def f() -> None:
    x = 1
    def g() -> None:
        y = 2
        print(locals())
    return g()
```
Upon running `f()` we can see that the local variables of `g` are only `{'y': 2}`. `{'x': 1}` is not included, because `x` is a `nonlocal` variable in `g` or in other terms, free.

### Building abstractions with data
The basic idea of data abstraction is to structure programs so that they operate on abstract data. That is, programs should use data in such a way as to make as few assumptions about it as possible. At the same time, a concrete data representation is defined as an independent part of the program. These two parts of a program - the one that operates on abstract data and the one that defines a concrete representation - are connected by a small set of procedures that implement abstract data in terms of the concrete representation.

Data abstraction can be achieved by building abstraction barriers. For example, if we have to represent rational numbers, the methods which use rational numbers - `add`, `subtract` - should be oblivious to how rational numbers are represented. On a lower level, rational numbers are represented using selectors `numerator` and `denominator` which return the main properties of every rational number. On a yet lower level, rational numbers might be represented as pairs, which should be hidden from the higher levels. An abstraction barrier violation occurs whenever a part of the program that can use a higher level function instead uses a function in a lower level.

Now, the distinction between data and procedures is fuzzy, because we can pass procedures as inputs, as if they were data. The other way is also possible, creating novel data types using procedures. 

```python
from typing import Callable

def create_pair(x, y) -> Callable:
    def get(index: int):
        if index == 0:
            return x
        else:
            return y
    return get
```
The code above uses an inner procedure to create the pair type. Similarly, one can use nested pairs where the second element points to another pair, to represent sequences - any compound data type supporting length and item selection functionality. 

Working with sequences is one of the most common cases exhibiting *conventional interfaces* - a design principle encouraging data formats shared across many modular components, which can be combined, composed, or otherwise mixed, in a succinct and natural way. For example, if we are working with sequences, a common interface for many of our functions might be that they take in a sequence and output a sequence. Since this format is shared among the various functions, they can be composed arbitrarily, much like in a pipeline. This is the main idea behind the `map`/`filter`/`reduce` higher-order procedures - starting with a sequence, we can apply various selection and transformation operations to process the lists.

There is a close resemblance between the map-reduce flow and signal processing. In signal processing, we begin with an enumerator which generates the signal. It may go next into a filter which discards some samples, or into a transducer which transforms the samples. Periodically, the signals may be accumulated in a reduce (or *fold*) step, yielding aggregated values.

So... procedures can be used to define pairs and sequences. But they can also be used to define mutable data, for example dictionary-like objects. Here, we have a badly performing, but easy to understand dictionary defined using inner procedures. Upon calling `make_dict()`, various inner procedures are defined, along with a list for the dictionary contents, which are represented as a list of key-value tuples. What `make_dict` returns is a function called `dispatch`, which takes in an operation to perform, and optional key and value. This style is called [message passing](https://en.wikipedia.org/wiki/Message_passing) because along with the actual arguments, you pass in a message saying what kind of functionality you want, and the internal function figures out itself what inner function to call.

```python
from typing import Callable

def make_dict() -> Callable:
    records: list[tuple] = []
    
    def getitem(key):
        for k, v in records:
            if k == key:
                return v
    
    def setitem(key, value) -> None:
        for item in records:
            if item[0] == key:
                item[1] = value
                return
        records.append((key, value))
    
    def dispatch(message: str, key=None, value=None):
        if message == 'getitem':
            return getitem(key)
        elif message == 'setitem':
            setitem(key, value)
        elif message == 'keys':
            return tuple(k for k, _ in records)
        elif message == 'values':
            return tuple(v for _, v in records)
    
    return dispatch
```
The function `dispatch` goes through each possible message to see which procedure to call. With many available procedures (imagine in the order of 100s), this may become unnecessarily slow. In that case, **data-directed programming** can be used. In a more general case where also the input type is variable, if we have $n$ procedures and $m$ different data types, we can have up to $nm$ if-else checks for finding the right procedure to call. To add the $m+1$-th type, we'll have to modify all $n$ procedures and add one new check to their code, which is tedious and error-prone. Data-directed programming solves this by having a table where the rows indicate the procedures and the columns the types. Each entry in the table shows the procedure to call for that input type. When we want to add a new type, we just add some new entries to the table. This means that functionality for new types can be designed in isolation and then combined additively (without modification).



<!-- The major implementation cost of first-class procedures is that allowing procedures
to be returned as values requires reserving storage for a procedure’s free variables even
while the procedure is not executing. -->
