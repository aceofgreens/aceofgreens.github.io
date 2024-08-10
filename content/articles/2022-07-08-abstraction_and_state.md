---
title: Abstraction and State
date: 2022-07-08 16:00:00 +0200
tags: cs
slug: abstraction_and_state
---

This post is a short summary of the first three chapters of Hal Abelson and Gerald Jay Sussman's wizard book, [Structure and Interpretation of Computer Programs](https://en.wikipedia.org/wiki/Structure_and_Interpretation_of_Computer_Programs) (SICP), which I read, much to my embarassment, only recently. Some of the code snippets are taken from the [adapted Python version](https://wizardforcel.gitbooks.io/sicp-in-python/content/index.html).

### Building Abstractions with Procedures

Programming is about decomposing problems into smaller more manageable subproblems. You then "compose" the solutions of these subproblems to obtain a solution for the real problem. In a way, composition is the essence of programming (ask Bartosz Milewski). A good programming language then has 3 main mechanisms which facilitate composition:

1. **Primitive expressions**, which represent the simplest entities the language is concerned with
2. **Means of combination**, by which compound elements are built from simpler ones,
3. **Means of abstraction**, by which compound elements can be named and manipulated as units.

The primitive expressions consist of primitive values and their types - integers, strings, floats - as well as any built-in operators. The means of combination are for example generic types like tuple and list, and the means of abstraction are features like custom procedures, classes, iterators, context managers, and so on.

These 3 mechanisms are conceptual, they define how the language will work in principle. But to actually implement a program and run it, an **interpreter** is needed. An interpreter is a program that carries out the computational processes defined in a given programming language. A program without an interpreter is just a mathematical description of objects and relationships. An interpreter allows us to evaluate this description to produce results.

Central to composition is the ability to name objects, which greatly facilitates programming and is a handy tool in managing the complexity of programs. Naming is simply a binding between names as keys, and objects as values. This association requires the interpreter to have an **environment** - a memory storing these bindings. Whenever an expression is evaluated, its variables are replaced with their values using the proper name-to-value binding.

Along with naming, procedures are the basis of abstraction. They allow us to name a set of statements and execute them repeatedly. If a procedure does not have assignment statements, it can be evaluated easily using a substitution model, either *normal order* (fully expand and then reduce) or *applicative order* (evaluate the arguments and then apply). Procedures with assignment statements cannot be handled using simple substitution and require the more powerful *environment* model, which is discussed later in this post.

*Higher order procedures* are those procedures that take in or output other procedures. Some use-cases are:

- In mathematics, to implement partial application, composition, fixed point finders, root finders, iterative improvement solvers;
- With decorators (with or without arguments, stacked or not), to modify an input procedure by adjusting its input/output before or after its execution;
- In currying, to convert a function taking multiple arguments into a sequence of functions each taking one argument;
- To speed up recursive functions using memoization;
- To trace the function calls of recursive functions.

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

We can also define procedures within procedures. Inner procedures are useful because they can provide **procedural abstraction**, where the details of how a procedure is implemented are suppressed, and the particular procedure itself can be replaced by any other procedure with the same overall behavior. In other words, inner procedures allow us to build abstractions that separate the way the procedure is used from the details of how it's implemented, this being the backbone principle of modularity.

Inner and outer procedures have a close resemblance to the lambda calculus. Those variables appearing in the body of the procedure that can be consistently renamed without changing the procedure definition are called *bound* variables. Those which are not bound are *free*. The set of expressions for which a binding defines a name is called the *scope* of that name. As an example from the lambda calculus, consider $(\lambda x. x)(\lambda y.yx)$. In the first expression $x$ is bound. In the second expression $y$ is bound and $x$ is free, since its value depends on the context. The scope of $x$ is the first lambda and does not extend to the second one. 

In computer programming, a free variable is a variable in some procedure whose value depends on the context where the function is invoked, called or used. A free variable is determined dynamically at run time searching the name of the variable backwards on the function call stack. A bounded variable evaluation does not depend on the context of the function call. This is the most common variable type. In Python local variables, global variables and parameters are all bounded variables. 

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
Similar to procedural abstraction, the basic idea of data abstraction is to separate the data representation from its actual use. The data representation consists of an abstract interface describing how to use this data and what operations can be performed on it. The usage relates to how we operate with the data, how we use the interface it provides. A good data abstraction allows us to change the data representation, but not its interface, without changing the procedures that operate on that data. 

Data abstraction can be achieved by building abstraction barriers. For example, if we have to represent rational numbers, the methods for arithmetic - `add`, `subtract`, `multiply` - should be oblivious to how rational numbers are represented. On a lower level, rational numbers can be represented using selectors `numerator` and `denominator`. On a yet lower level, rational numbers might be represented as pairs, which should be hidden from the higher levels. In such cases, changing the representation from pairs to lists will not require us to modify the code that does arithmetic calculations. This would be well-abstracted data. In general, an abstraction barrier violation occurs whenever a part of the program that can use a higher level function instead uses a function from a lower level.

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
The code above uses an inner procedure to create the pair type. Similarly, one can use nested pairs where the second element points to another pair. It is precisely this closure property, pairs of pointers being able to point to other pairs of pointers, which allows us to use pairs as building blocks in other compound data structures such as sequences - any compound data type supporting length and item selection functionality. 

Working with sequences is one of the most common cases exhibiting *conventional interfaces* - a design principle encouraging data formats shared across many modular components, which can be combined, composed, or otherwise mixed, in a succinct and natural way. For example, if we are working with sequences, a common interface for many of our functions might be that they take in a sequence and output a sequence. Since this format is shared among the various functions, they can be composed arbitrarily, much like in a pipeline. This is the main idea behind the `map`/`filter`/`reduce` higher-order procedures - starting with a sequence, we can apply various selection and transformation operations to process the lists.

There is a close resemblance between the map-reduce flow and signal processing. In signal processing, we begin with an enumerator which generates the signal. It may go next into a filter which discards some samples, or into a transducer which transforms the samples. The signals may also be accumulated in a reduce (or *fold*) step, yielding aggregated values. All these opportunities are provided using the map, filter, and reduce procedures.

So... procedures can be used to define pairs and sequences. But they can also be used to define mutable data, for example dictionary-like objects. Below, we have a badly performing, but easy to understand dictionary defined using inner procedures. Upon calling `make_dict()`, various inner procedures are defined, along with a list for the dictionary contents, which are represented as a list of key-value tuples. What `make_dict` returns is a function called `dispatch`, which takes in an operation to perform, and optional key and value. This style is called [message passing](https://en.wikipedia.org/wiki/Message_passing) because along with the actual arguments, you pass in a message saying what kind of functionality you want, and the `dispatch` function figures out itself what inner function to call.

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

### Modularity and state
To keep programs modular, it's useful to represent real world entities as durable objects that change through the program execution. Having a state can be achieved either through object-oriented programming (OOP), where each class instance has a state, or through procedural abstractions. 

```python
def make_withdraw(balance: int):
    def withdraw(amount: int):
        nonlocal balance
        if amount > balance:
            return "Insufficient funds"
        balance = balance - amount
        return balance
    return withdraw
```

A classic example of a stateful procedure is an ATM where we set the initial balance and return an inner procedure, modifying that balance. If a given function only ever reads a variable, then its value can easily be substituted inside the function.

But with assignment introduced, the substitution model is no longer an adequate model of procedure application. It is now important to know at what time a variable was bound to a given value. This can be achieved using the environment model.

The environment model consists of a sequence of frames. Each frame has

- a table of bindings between names and values
- a pointer to the enclosing environment.

To compute an expression in a given environment, we (i.e., the interpreter) look up if the variable name is bound in the current frame (to one to which the environment points). If it is, we substitute it with its corresponding value, otherwise we looks in the table of bindings of the enclosing environment, and so on, until a binding is found, or we reach the global environment.

To evaluate a procedure that in turn calls other procedures, we create a new frame for each procedure call.  The binding table of the new frame contains the formal parameter names bound to the arguments, and the pointer references the environment in which the function was defined (not called). This allows us to efficiently resolve naming conflicts between local and global variables.

It is important that the enclosing environment is the one where the procedure is defined, not invoked. This is called *lexical scoping*. The alternative is to have dynamic scoping, which is fairly rare. Python has lexical scoping, as seen from the following example.
```python
def print_x():
    print("x =", x)

def outer():
    x = 20
    print_x()
    print("x =", x)

x = 3
outer()
# Output:
# 3
# 20
```
The frame for `print_x` points to the global frame, where `print_x` is defined, not the `outer` frame, where `print_x` is called.
That is why irrespective of where we call `print_x` from, it prints 3, not 20.

So long as we do not use assignments, two evaluations of the same procedure with the same arguments will produce the same result. Such procedures can be viewed as computing mathematical functions. Programming without any use of assignments is accordingly known as **functional programming**.

In contrast to functional programming, programming that makes extensive use of assignment is known as **imperative programming**. Programs written in imperative style are additionally susceptible to bugs related to the ordering of statements around the assignment, as well as concurrency issues. Nonetheless, modelling entities as objects, each with its own state, is very convenient and natural.

In conclusion, we have seen that procedures can be used to define data, they can process data, or even be passed as data to other procedures. The distinction between procedures and data is murky. In theoretical computer science, we often rely on statements like $U(f, x) = f(x)$ where $f$ is passed both as data and as an executable. In that regard, I believe SICP offers a nice connection between the theory and the real-life use cases.




