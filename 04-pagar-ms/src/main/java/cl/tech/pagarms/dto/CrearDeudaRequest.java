package cl.tech.pagarms.dto;

import io.swagger.v3.oas.annotations.media.Schema;

public class CrearDeudaRequest {

    @Schema(description = "Descripción de la deuda", example = "Pago crédito consumo")
    private String descripcion;

    @Schema(description = "Monto de la deuda", example = "15000")
    private Double monto;

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public Double getMonto() {
        return monto;
    }

    public void setMonto(Double monto) {
        this.monto = monto;
    }
}