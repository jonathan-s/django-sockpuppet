---
description: How to use custom template tags
---

# Template Tags

Multiple custom template tags are provided by the library to make it easier to generate HTML attributes that interact with reflex.
These are `stimulus_controller`, `reflex` and `*_reflex` where `*` describes valid stimulus actions like _click_, _submit_, ...

## The *_reflex tags

The `*_reflex` tags can be used to connect a HTML attibute like the `<a>` Tag to a reflex. Some syntax examples are

```
<a href="#" {% click_reflex 'example_reflex' 'increment' parameter=parameter %}>click me</a>
<a href="#" {% submit_reflex 'example_reflex' 'increment' parameter=parameter %}>click me</a>
<input type="text" {% input_reflex 'example_reflex' 'increment' parameter=parameter %}/>
```

where different tags are used for different _actions_.

## The Syntax of the *_reflex tags

There are three ways to pass data to the *_reflex tags:
1. Pass `controller` and `reflex` as list attributes and all parameters (`data-` attributes) as kvargs
2. Use the `*_reflex` tag inside a `stimulus_controlle` Block and only pass `reflex` (controller will be taken automatically from the `stimulus_controller`). Parameters work the same as above.
3. Use a `dict` as sole list argument which has to contain the keys `controller` and `reflex`. All other dict entries as well as all given kvargs are used as `data-` attributes.

