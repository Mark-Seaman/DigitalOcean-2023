# Playbook Prompts

{% for play in plays %}## {{ play.title }}
* Markdown - [{{ play.title }}]({{ play.md }})
* AI Prompt - [{{ play.title }}]({{ play.ai }})

PROMPT: 

    {{ play.prompt }}
{% endfor %}