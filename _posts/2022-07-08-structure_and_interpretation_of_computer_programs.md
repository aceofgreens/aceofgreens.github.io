---
layout: post
title: Structure and Interpretation of Computer Programs
date: 2022-07-08 16:00:00 +0200
tags: [cs]
---

This post is a short summary of the content of Hal Abelson and Gerald Jay Sussman's wizard book, [Structure and Interpretation of Computer Programs](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs), which I read, much to my embarassment, only recently.

### Building Abstractions with Procedures

Programming is about decomposing problems into smaller more manageable subproblems. You then "compose" the solutions of these subproblems to obtain a solution for the real problem. In a way, composition is the essence of programming (ask Bartosz Milewski). A good programming language then has 3 main mechanisms which facilitate composition:
1. **Primitive expressions**, which represent the simplest entities the language is concerned with
2. **Means of combination**, by which compound elements are built from simpler ones,
3. **Means of abstraction**, by which compound elements can be named and manipulated as units.

The primitive expressions consist of primitive values and their types - integers, strings, floats - as well as any built-in operators. The means of combination are for example generic types like tuple and list, and the means of abstraction are features like being able to write custom procedures, classes, iterators, context managerts, and so on.

These 3 mechanisms are conceptual, they define how the language will work in principle. But to actually implement a program and run it, an interpreter is needed. An interpreter is a program that carries out the computational processes defined in a given programming language. A program without an interpreter is just a mathematical description of objects and relationships. An interpreter allows us to evaluate this description to produce results.

Central to composition is the ability to name objects, which greatly facilitates programming and is a handy tool in managing the complexity of programs. Naming is simply a mapping between names as keys, and objects as values. This association requires the interpreter to have an **environment** - a memory storing these mappings. Whenever an expression is evaluated, its variables are replaced with their values using the current name-to-value mapping.

Along with naming, procedures are the basis of abstraction. They allow us to name a set of statements, possibly depending on any arguments, and execute them repeatedly. If a procedure does not have assignment statements, it can be evaluated easily using a substitution model, either a *normal order* (fully expand and then reduce) or *applicative order* (evaluate the arguments and then apply). Procedures with assignment statements cannot be handled using simple substitution and require the more powerful *environment* model.

*Higher order procedures* are those procedures that take in or output other procedures. Some use-cases are:
- In mathematics, to implement partial application, composition, fixed point finders, root finders, iterative improvement solvers,
- In decorators, to modify an input procedure by adjusting its input or output before or after its execution,
- In currying, to convert a function taking multiple arguments into a sequence of functions each taking one argument.

We can implement currying in Python 3 as follows:
```python
from inspect import signature

# An example function with 4 inputs
def f(x1, x2, x3, x4):
    if x4 != 0:
        return x1 * x2 + x3 / x4
    else:
        return x1 + x2 + x3

# First way to do currying is to hardcode the number of arguments
g = lambda w: (lambda x: (lambda y: (lambda z: f(w, x, y, z))))

# Second better way that can accomodate variable number of arguments
def curry(f):
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

Inner and outer procedures have a close resemblance to lambda calculus. Those variables appearing in the body of the procedure that can be consistently renamed without changing the procedure definition are called *bound* variables. Those which are not bound are *free*. The set of expressions for which a binding defines a name is called the *scope* of that name. As an example from lambda calculus, consider $(\lambda x. x)(\lambda y.yx)$. In the first expression $x$ is bound. In the second expression $y$ is bound and $x$ is free, since its value depends on the context. The scope of $x$ is the first lambda and does not extend to the second one. 

In computer programming, a free variable is a variable in some procedure whose value depends on the context where the function is invoked, called or used. A free variable is determined dynamically at run time searching the name of the variable backwards on the function call stack. A bounded variable evaluation does not depend on the context of the function call. This is the most common modern programming languages variable type. Local variables, global variables and parameters are all bounded variables. 

As an example, consider the following in Python.

```python
def f():
    x = 1
    def g():
        y = 2
        print(locals())
    return g()
```
Upon running `f()` we can see that the local variables of `g` are only `{'y': 2}`. `{'x': 1}` is not included, because `x` is a `nonlocal` variable in `g` or in other terms, free.


<!-- The major implementation cost of first-class procedures is that allowing procedures
to be returned as values requires reserving storage for a procedure’s free variables even
while the procedure is not executing. -->
