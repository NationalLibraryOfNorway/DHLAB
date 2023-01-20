:ref:`dhlab` << :py:obj:`{{ module }}`

{{ name | escape | underline}}


{% block import %}
{% if module %}
..  code-block:: python

    from {{ module }} import {{ name }}
{% endif %}
{% endblock %}


.. automodule:: {{ fullname }}

   {% block attributes %}
   {% if attributes %}
   {{ _('Module Attributes') }}
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. autosummary::
   {% for item in attributes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block functions %}
   {% if functions %}
   {{ _('Functions') }}
   ~~~~~~~~~~~~~~~~~~~~~

   .. autosummary::
   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   {{ _('Exceptions')}}
   ~~~~~~~~~~~~~~~~~~~~

   .. autosummary::
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   {{ _('Classes') }}
   ~~~~~~~~~~~~~~~~~~

   .. autosummary::
      :recursive:
      :toctree:
      :template: autosummary/class.rst
   {% for item in classes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}



{% block modules %}
{% if modules %}
Modules
~~~~~~~~

.. autosummary::
   :toctree:
   :nosignatures:
   :recursive:
{% for item in modules %}
   {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


