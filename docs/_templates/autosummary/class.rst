
{% block navigation %}
{% if module == 'dhlab' %}
<< :ref:`dhlab`
{% else %}
<< :ref:`dhlab` << :py:obj:`{{ module }}`
{% endif %}
{% endblock %}

{{ name | escape | underline}}


{% block import %}
{% if module %}
..  code-block:: python

    from {{ module }} import {{ name }}
{% endif %}
{% endblock %}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% block methods %}
   {% if methods %}
   .. rubric:: {{ _('Methods') }}

   .. autosummary::
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
