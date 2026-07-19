# LLM Application Basics

LLM applications are software systems that place a model inside a product workflow. A production LLM app usually has:

- input validation
- task routing
- context construction
- model call
- output validation
- logging and evaluation

The important engineering question is not "can the model answer". It is whether the system can reliably decide what context is needed, whether the context is enough, and what to do when the answer should be refused.

In StuckToShip, a learner asking "what should I build first" should be routed to course or learning path evidence. A learner pasting a stack trace should be routed to error recipes. A learner asking where a function is defined should be routed to code retrieval.
