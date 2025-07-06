package cl.tech.pagarms.controller;

import cl.tech.pagarms.model.Deuda;
import cl.tech.pagarms.service.DeudaService;
import cl.tech.pagarms.dto.CrearDeudaRequest;
import cl.tech.pagarms.dto.AbonoRequest;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RestController
@RequestMapping("/api/v1/deudas")
public class DeudaController {

    @Autowired
    private DeudaService service;

    @PostMapping("/")
    public ResponseEntity<Deuda> crearDeuda(@RequestBody CrearDeudaRequest body, HttpServletRequest req) {
        Long usuarioId = getUsuarioId(req);
        Deuda deuda = service.crearDeuda(usuarioId, body.getDescripcion(), body.getMonto());
        return ResponseEntity.ok(deuda);
    }

    @GetMapping("/")
    public ResponseEntity<List<Deuda>> listarDeudas(HttpServletRequest req) {
        Long usuarioId = getUsuarioId(req);
        return ResponseEntity.ok(service.listarDeudas(usuarioId));
    }

    @Operation(
        summary = "Abona a una deuda",
        description = "Permite abonar a una deuda por monto o porcentaje.",
        responses = {
            @ApiResponse(responseCode = "200", description = "Abono realizado"),
            @ApiResponse(responseCode = "404", description = "Deuda no encontrada"),
            @ApiResponse(responseCode = "400", description = "Monto o porcentaje inválido")
        }
    )
    @PostMapping("/{id}/abonar")
    public ResponseEntity<?> abonarDeuda(
            @PathVariable("id") Long id,
            @RequestBody(required = false) AbonoRequest body,
            HttpServletRequest req) {

        Double monto = body != null ? body.getMonto() : null;
        Double porcentaje = body != null ? body.getPorcentaje() : null;

        Long usuarioId = getUsuarioId(req);
        Map<String, Object> respuesta = service.abonarDeuda(usuarioId, id, monto, porcentaje);

        if (respuesta == null) {
            return ResponseEntity.status(404).body(Map.of("error", "Deuda no encontrada o no pertenece al usuario."));
        }
        if (respuesta.containsKey("error")) {
            return ResponseEntity.badRequest().body(respuesta);
        }
        return ResponseEntity.ok(respuesta);
    }

    @Operation(
        summary = "Cancela una deuda",
        description = "Permite cancelar una deuda completamente o con un abono específico.",
        responses = {
            @ApiResponse(responseCode = "200", description = "Pago realizado"),
            @ApiResponse(responseCode = "404", description = "Deuda no encontrada"),
            @ApiResponse(responseCode = "400", description = "Monto inválido")
        }
    )
    @PostMapping("/{id}/cancelar")
    public ResponseEntity<?> cancelarDeudaPorId(
            @PathVariable("id") Long deudaId,
            @RequestBody(required = false) Map<String, Object> body,
            HttpServletRequest req) {

        Long usuarioId = getUsuarioId(req);
        Double monto = null;

        if (body != null && body.containsKey("monto")) {
            monto = toDouble(body.get("monto"));
            if (monto == null) {
                return ResponseEntity.badRequest().body(Map.of("error", "El campo monto debe ser numérico"));
            }
        }

        Optional<Deuda> pagada = service.pagarDeudaPorId(usuarioId, deudaId, monto);
        if (pagada.isEmpty()) {
            return ResponseEntity.status(404).body(Map.of("error", "Deuda no encontrada o no pendiente."));
        }

        Deuda d = pagada.get();
        Map<String, Object> resp = new HashMap<>();
        resp.put("deuda_id", d.getId());
        resp.put("saldo_pendiente", d.getSaldoPendiente());
        resp.put("estado", d.getEstado());
        resp.put("mensaje", d.getEstado() == Deuda.Estado.PAGADA
                ? "¡Deuda completamente pagada!" : "Cuota abonada.");
        return ResponseEntity.ok(resp);
    }

    // --- Helpers ---

    private Long getUsuarioId(HttpServletRequest req) {
        Object id = req.getAttribute("usuarioId");
        if (id instanceof Integer) return ((Integer) id).longValue();
        if (id instanceof Long) return (Long) id;
        throw new RuntimeException("No se pudo obtener usuarioId desde JWT");
    }

    private Double toDouble(Object value) {
        try {
            return Double.valueOf(value.toString());
        } catch (Exception e) {
            return null;
        }
    }
}