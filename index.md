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
      <span class="dates_and_tags">{{post.date | date_to_string}}</span> <a class="enum_title" href="{{ post.url }}"><b>{{ post.title }}</b></a>
      {{ post.excerpt }}
      <br>
    </li>


  {% endfor %}
</ul>