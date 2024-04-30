

## GPTs

[my gpts store](https://gptstore.ai/creators/user-eUjRFH97y4YdV3EhRPqln3NB)



### General Tools
{% assign category_pages = site.pages | where_exp: "item", "item.categories contains 'tools'" %}
{% for page in category_pages%}
* <img src="/Agents/{{ page.url }}/image.webp" Height="32" style="border-radius: 50%; overflow: hidden;" />  <a href= "/Agents{{ page.url }}">{{ page.title }}</a>
{% endfor %}

### Story, Game Design helper
{% assign category_pages = site.pages | where_exp: "item", "item.categories contains 'design'" %}
{% for page in category_pages%}
* <img src="/Agents/{{ page.url }}/image.webp" Height="32" style="border-radius: 50%; overflow: hidden;" />  <a href= "/Agents{{ page.url }}">{{ page.title }}</a>
{% endfor %}

### just for fun
{% assign category_pages = site.pages | where_exp: "item", "item.categories contains 'funny'" %}
{% for page in category_pages%}
* <img src="/Agents/{{ page.url }}/image.webp" Height="32" style="border-radius: 50%; overflow: hidden;" />  <a href= "/Agents{{ page.url }}">{{ page.title }}</a>
{% endfor %}