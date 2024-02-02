
[my gpts store](https://gptstore.ai/creators/user-eUjRFH97y4YdV3EhRPqln3NB)

* GPTs:
{% assign sorted_pages = site.pages | sort: 'date' | reverse %}
{% for page in sorted_pages limit:10 %}
<entry>
<title>{{ page.title }}</title>
<link href="{{ site.url | prepend: site.baseurl }}{{ page.url }}"/>
<updated>{{ page.date | date_to_xmlschema }}</updated>
  * <id>{{ site.url | prepend: site.baseurl }}{{ page.url }}</id>
</entry>
{% endfor %}
