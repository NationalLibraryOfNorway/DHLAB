
{% block navigation %}
{% if module == 'dhlab' or module == fullname -%}
:doc:`home </index>` << :ref:`dhlab`
{% else -%}
:doc:`home </index>` << :ref:`dhlab` << :py:obj:`{{ module }}`
{% endif %}
{% endblock %}
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
      :template: autosummary/base.rst
      :toctree:
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
      :recursive:
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
      :template: autosummary/base.rst
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
   :template: autosummary/module.rst
{% for item in modules %}
   {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


