# c14garden
off grid garden automation

WIP

## mqtt commands (use QoS 1)

### channel /system_name/actuators/set

```
{
  "pump": "schedule",
  "wednesday": "18:00",
  "duration": 5,
  "amount": 20
}
```

```
{
  "pump": "deschedule",
  "wednesday": "18:00",
  "duration": 5,
  "amount": 20
}
```

```
{
  "pump": "deschedule_all"
}
```

```
{
  "pump": true,
}
```

```
{
  "pump": false,
}
```

### channel /system_name/system/set

```
{
  "system": "kill",
}
```

```
{
  "system": "halt",
}
```

```
{
  "system": "reboot",
}
```
