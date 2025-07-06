package cl.tech.pagarms.repository;

import cl.tech.pagarms.model.Deuda;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

public interface DeudaRepository extends JpaRepository<Deuda, Long> {
    List<Deuda> findByUsuarioId(Long usuarioId);

    List<Deuda> findByUsuarioIdAndEstado(Long usuarioId, Deuda.Estado estado);

    Optional<Deuda> findByIdAndUsuarioIdAndEstado(Long id, Long usuarioId, Deuda.Estado estado);
}