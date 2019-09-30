# Mesopotamian Knowledge Graph 

## About the project

This project is a place to use different NLP tools and LinkedData techniques to explore the way ancient Mesopotamians organized information. 

## List of Blog Posts 

<ul>
    {% for post in site.posts %}
    <li>
    <a href="{{ post.url }}">{{post.date | date: "%A, %b %-d, %Y" }}: {{ post.title }} </a> 
    </li>
    {% endfor %}
</ul>
