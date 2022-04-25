---
layout: page
permalink: /
---




Recent posts:
<ul>
  {% for post in site.posts %}

    {% if forloop.index > 5 %}
        {% break %}
    {% endif %}
    
    <li>
      <span class="dates_and_tags">{{post.date | date_to_string}} </span> <a class="enum_title" href="{{ post.url }}"><b>{{ post.title }}</b></a>
      {{ post.excerpt }}
      <br>
    </li>

  {% endfor %}
</ul>


<figure>
    <img src = "margulis_graph3.svg" alt="Expander Graph" width="1000">
    <figcaption>Figure 1: An expander - a most curious sparse graph with strong connectivity properties.<br>Every subset of less than half the total number of vertices has a proportionally large boundary of edges.</figcaption>
</figure>