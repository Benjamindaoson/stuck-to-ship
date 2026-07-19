# Code RAG And Debugging

Code RAG is different from document RAG. Code questions often require exact symbols, file paths, imports, configuration, and call flow.

A learner may ask:

- where a function is defined
- which file starts the app
- why an import fails
- how an environment variable is read
- which route calls a service

Plain text chunks are not enough for these questions. The first useful step is AST symbol extraction for classes and functions. A stronger version adds imports, call edges, config references, tests, and README links.

Good code answers should cite file paths and line numbers. If the codebase evidence is missing, the assistant should ask for the repository path instead of guessing.
