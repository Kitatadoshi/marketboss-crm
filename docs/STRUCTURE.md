# Target Project Structure (Clean Architecture + DDD)

```text
src/
  domain/
    lead/
      entities/
      value-objects/
      events/
      repositories/
      services/
    deal/
    task/
    metric/

  application/
    lead/
      use-cases/
      dto/
    deal/
    task/
    metric/

  infrastructure/
    persistence/
      sqlite/
      json/
    eventbus/
    messaging/

  interfaces/
    http/
      controllers/
      routes/
      views/
        bootstrap/
    cli/

  shared/
    kernel/
    types/
```

## Dependency rule
`interfaces -> application -> domain`

`infrastructure` реализует интерфейсы из `domain/application`, но не проталкивает зависимости в домен.
