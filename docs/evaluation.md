# Evaluator module

The evaluator module in DialogueKit aims to allow for the evaluation of conversational agents by implementing established metrics.

## Overview

| Category      | Metric    | Explanation
|---------------|-----------|------------
| Task-oriented | AvgTurns  | Average number of turns across conversations.
| Task-oriented | Reward    | A scoring function that measures success based on task completion and duration.
| Task-oriented | AvgSatisfaction  | Average overall satisfaction score across conversations.

## Reward config

The reward config should be in the following form:
```json
{
  "full_set_points": 20, # int (max score to start with)
  "missing_intent_penalties":
    - "INQUIRE": 4, # penalty (penalty associated with intent if missing)
    - ...,
  "repeat_penalty": 1, # int (penalty for consecutive repeated intents)
  "cost": 1, # int (cost for each turn)
}
```