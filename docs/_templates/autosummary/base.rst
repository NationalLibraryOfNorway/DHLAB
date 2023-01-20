
{% block navigation %}
{% if module == 'dhlab' or module == fullname %}
:doc:`home </index>` << :ref:`dhlab`
{% else %}
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

.. currentmodule:: {{ module }}

{% block autoobj %}
{% if objtype == 'class' and members %}
.. autoclass:: {{ objname }}
   :members:
   :undoc-members:
{% else %}
.. auto{{ objtype }}:: {{ objname }}
{% endif %}
{% endblock %}