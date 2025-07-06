package cl.tech.pagarms.service;

import cl.tech.pagarms.model.Deuda;
import cl.tech.pagarms.repository.DeudaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class DeudaService {

    @Autowired
    private DeudaRepository deudaRepository;

    public Deuda crearDeuda(Long usuarioId, String descripcion, Double monto) {
        Deuda d = new Deuda(usuarioId, descripcion, monto);
        return deudaRepository.save(d);
    }

    public List<Deuda> listarDeudas(Long usuarioId) {
        return deudaRepository.findAll().stream()
                .filter(d -> d.getUsuarioId().equals(usuarioId))
                .toList();
    }

    public Map<String, Object> abonarDeuda(Long usuarioId, Long deudaId, Double monto, Double porcentaje) {
    Optional<Deuda> opt = deudaRepository.findById(deudaId);
    if (opt.isEmpty()) return null;

    Deuda d = opt.get();
    if (!d.getUsuarioId().equals(usuarioId) || d.getEstado() == Deuda.Estado.PAGADA) return null;

    Double saldo = d.getSaldoPendiente();
    if (saldo == null) saldo = d.getMonto();  // fallback defensivo

    if (monto == null && porcentaje == null) {
        porcentaje = Math.random() * 0.4 + 0.1; // entre 10% y 50%
    }
    if (monto == null && porcentaje != null) {
        monto = saldo * porcentaje;
    }

    if (monto == null || monto <= 0 || monto > saldo) {
        return Map.of("error", "Monto inválido");
    }

    saldo -= monto;
    d.setSaldoPendiente(Math.max(saldo, 0.0));

    if (saldo <= 0.0) {
        d.setEstado(Deuda.Estado.PAGADA);
    }

    deudaRepository.save(d);

    return Map.of(
            "deuda_id", d.getId(),
            "saldo_pendiente", d.getSaldoPendiente(),
            "estado", d.getEstado()
    );
}

    public Optional<Deuda> pagarDeudaPorId(Long usuarioId, Long deudaId, Double monto) {
        Optional<Deuda> opt = deudaRepository.findById(deudaId);
        if (opt.isEmpty()) return Optional.empty();

        Deuda d = opt.get();
        if (!d.getUsuarioId().equals(usuarioId) || d.getEstado() == Deuda.Estado.PAGADA) {
            return Optional.empty();
        }

        if (monto == null || monto >= d.getSaldoPendiente()) {
            d.setSaldoPendiente(0.0);
            d.setEstado(Deuda.Estado.PAGADA);
        } else {
            d.setSaldoPendiente(d.getSaldoPendiente() - monto);
        }

        return Optional.of(deudaRepository.save(d));
    }
}