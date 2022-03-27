---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: page
title: Posts
permalink: /posts
---

<ul>
  {% for post in site.posts %}
    <li>
      <span class='dates_and_tags'>{{post.date | date_to_string}}</span>
      <a class="enum_title" href="{{ post.url }}"><b>{{ post.title }}</b></a>
    </li>
  {% endfor %}
</ul>