# Evaluator module

The evaluator module in DialogueKit aims to allow for 
evaluation of conversational agents by supporting standard metrics.

## Overview
| Category      | Metric    | Explanation
|---------------|-----------|------------
| Task-oriented | AvgTurns  | Average number of turns across conversations.
| Task-oriented | Reward    | A scoring function that measures success based on task completion and duration.
| Task-oriented | AvgSatisfaction  | Average overall satisfaction score across conversations.

## Reward config
The reward config should be in the following form:
```yaml
REWARD:
  full_set_points: int (max score to start with)
  missing_intent_penalties:
    - intent: penalty (penalty associated with intent)
    - ...
  repeat_penalty: int (penalty for consecutive repeated intents)
  cost: int (cost for each turn)
```