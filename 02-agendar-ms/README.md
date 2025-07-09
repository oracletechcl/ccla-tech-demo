To test locally: 


```shell
fn invoke agendar-ms-fn crear-reserva <<EOF
{
  "sucursal": "Santiago",
  "fecha": "2025-07-10",
  "hora": "10:00:00"
}
EOF
```

another example

```shell
export TOKEN="FFSDKJDSLJDS"
fn invoke agendar-ms-fn obtener-reservas-usuario \
  --headers "Authorization: Bearer $TOKEN"
```