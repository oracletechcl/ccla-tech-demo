package cl.tech.pagarms.dto;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "Payload para abonar a una deuda")
public class AbonoRequest {

    @Schema(description = "Monto a abonar directamente (opcional)", example = "5000")
    private Double monto;

    @Schema(description = "Porcentaje del saldo pendiente a abonar (entre 0.1 y 0.5, opcional)", example = "0.25")
    private Double porcentaje;

    public Double getMonto() {
        return monto;
    }

    public void setMonto(Double monto) {
        this.monto = monto;
    }

    public Double getPorcentaje() {
        return porcentaje;
    }

    public void setPorcentaje(Double porcentaje) {
        this.porcentaje = porcentaje;
    }
}