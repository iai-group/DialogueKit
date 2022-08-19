Natural Language Generation (NLG)
=================================

The NLG components in Dialoguekit are template based.
There are two different versions. :py:class:`dialoguekit.nlg.nlg.NLG` and :py:class:`dialoguekit.nlg.nlg_conditional.ConditionalNLG`. 

These two are used in similar ways. The only difference is that the `ConditionalNLG` can use a conditional in the :py:attr:`dialoguekit.core.annotated_utterance.AnnotatedUtterance.metadata` as long as the conditional value is a number.

To start using these NLG classes a template needs to be generated. 
Two methods for doing this are provided:

    * :py:meth:`dialoguekit.nlg.template_from_training_data.build_template_from_instances`
    * :py:meth:`dialoguekit.nlg.template_from_training_data.extract_utterance_template`

Usage Example
"""""""""""""

.. code:: python

    from dialoguekit.core.annotation import Annotation
    from dialoguekit.core.intent import Intent
    from dialoguekit.nlg.nlg import NLG
    from dialoguekit.nlg.template_from_training_data import (
        extract_utterance_template,
    )

    template = extract_utterance_template(
        annotated_dialogue_file=ANNOTATED_DIALOGUE_FILE_PATH,
    )
    nlg = NLG(response_templates=template)
    
    response = nlg.generate_utterance_text(intent=Intent("COMPLETE"))

ConditionalNLG
""""""""""""""

The ConditionalNLG class contains two additional parameters to the ``generate_utterance_text()`` method.

  * ``conditional: str``
  * ``conditional_value: Number``

These fields are used to find the utterance that has the closest ``conditional_value`` to the utterance metadata field with the key ``conditional``.
Note that this necessitates the need of a larger template with multiple values for the ``conditional``.

Custom NLG
""""""""""

If you want to implement your own NLG component feel free to inherit from :py:class:`dialoguekit.nlg.nlg_abstract.AbstractNLG`.