
{% block navigation %}
:doc:`home </index>` << :ref:`dhlab`
{% endblock %}

{{ name | escape | underline}}


{% block import %}

..  code-block:: python

    from dhlab import {{ name }}

{% endblock %}

.. currentmodule:: {{ module }}

{% block autoobj %}
.. autoclass:: {{ objname }}
   :members:
{% endblock %}