---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: page
title: Tags
permalink: /tags
---

{% for tag in site.tags %}
  <h3>{{ tag[0] }}</h3>
  <ul>
    {% for post in tag[1] %}
      <li>
        <span class='dates_and_tags'>{{post.date | date_to_string}}</span>  
        <a class="enum_title" href="{{ post.url }}">
          <b>{{ post.title }}</b>
        </a>
      </li>
    {% endfor %}
  </ul>
{% endfor %}