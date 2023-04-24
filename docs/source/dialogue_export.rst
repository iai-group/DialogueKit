DialogueKit Dialogue Export Format
=====================================

DialogueKit follows a specific format when exporting dialogues to JSON.
Dialogues are stored in separate files for each user-agent pair.

Format
------

.. code-block:: json

  {
    "agent": {
      "id": "MovieAgent",
      "type": "BOT"
    },
    "user": {
      "id": "13",
      "type": "SIMULATOR"
    },
    "dialogues": [
      {
        "conversation_id": "123456790",
        "conversation": [
          {
            "participant": "AGENT",
            "utterance": "Hi",
            "intent": DISCLOSE.NON-DISCLOSE,
            "metadata": {
              "field1": value1,
              "field2": value2,
              ...
            }
          },
          ...
        ],
      },
      ...
    ]
  }
