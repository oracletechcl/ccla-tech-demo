package cl.tech.pagarms.model;

import jakarta.persistence.*;

@Entity
public class Deuda {

    public enum Estado {
        PENDIENTE,
        PAGADA
    }

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Long usuarioId;

    private String descripcion;

    private Double monto;

    // Nuevo: saldo pendiente para cuotas
    private Double saldoPendiente;

    @Enumerated(EnumType.STRING)
    private Estado estado;

    // ----- Constructores -----

    public Deuda() {
    }

    public Deuda(Long usuarioId, String descripcion, Double monto) {
        this.usuarioId = usuarioId;
        this.descripcion = descripcion;
        this.monto = monto;
        this.saldoPendiente = monto;
        this.estado = Estado.PENDIENTE;
    }

    // ----- Getters y Setters -----

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getUsuarioId() {
        return usuarioId;
    }

    public void setUsuarioId(Long usuarioId) {
        this.usuarioId = usuarioId;
    }

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

    public Double getSaldoPendiente() {
        return saldoPendiente;
    }

    public void setSaldoPendiente(Double saldoPendiente) {
        this.saldoPendiente = saldoPendiente;
    }

    public Estado getEstado() {
        return estado;
    }

    public void setEstado(Estado estado) {
        this.estado = estado;
    }
}