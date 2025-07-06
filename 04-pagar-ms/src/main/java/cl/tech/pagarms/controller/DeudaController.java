package cl.tech.pagarms.controller;

import cl.tech.pagarms.model.Deuda;
import cl.tech.pagarms.service.DeudaService;
import cl.tech.pagarms.dto.CrearDeudaRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpServletRequest;
import java.util.*;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;

@RestController
@RequestMapping("/api/v1/deudas")
public class DeudaController {

    @Autowired
    private DeudaService service;

    @PostMapping("/")
    public ResponseEntity<Deuda> crearDeuda(@RequestBody CrearDeudaRequest body, HttpServletRequest req) {
        Long usuarioId = getUsuarioId(req);
        String descripcion = body.getDescripcion();
        Double monto = body.getMonto();
        Deuda d = service.crearDeuda(usuarioId, descripcion, monto);
        return ResponseEntity.ok(d);
    }

    @GetMapping("/")
    public ResponseEntity<List<Deuda>> listarDeudas(HttpServletRequest req) {
        Long usuarioId = getUsuarioId(req);
        return ResponseEntity.ok(service.listarDeudas(usuarioId));
    }

    @Operation(
        summary = "Abona a una deuda específica (por ID)",
        description = """
            Permite abonar a una deuda específica.
            Si no se especifica monto ni porcentaje, se abona entre 10% y 50% random del saldo pendiente.
            Si se especifica 'monto' en el body, se abona ese monto.
            Si se especifica 'porcentaje', se abona ese porcentaje del saldo pendiente.
            """
    )
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Abono realizado exitosamente"),
        @ApiResponse(responseCode = "404", description = "Deuda no encontrada"),
        @ApiResponse(responseCode = "400", description = "Monto o porcentaje inválido")
    })
    @PostMapping("/{id}/pagar")
    public ResponseEntity<?> abonarDeuda(
            @Parameter(description = "ID de la deuda a abonar") @PathVariable Long id,
            @RequestBody(required = false) Map<String, Object> body,
            HttpServletRequest req
    ) {
        Double monto = null;
        Double porcentaje = null;
        if (body != null) {
            if (body.containsKey("monto")) {
                monto = Double.valueOf(body.get("monto").toString());
            }
            if (body.containsKey("porcentaje")) {
                porcentaje = Double.valueOf(body.get("porcentaje").toString());
            }
        }
        Long usuarioId = getUsuarioId(req);
        Map<String, Object> resp = service.abonarDeuda(usuarioId, id, monto, porcentaje);
        if (resp == null) {
            return ResponseEntity.status(404).body(Map.of("error", "Deuda no encontrada o no pertenece al usuario."));
        }
        if (resp.containsKey("error")) {
            return ResponseEntity.badRequest().body(resp);
        }
        return ResponseEntity.ok(resp);
    }

    @Operation(
        summary = "Paga una deuda específica (por ID), en cuotas o monto definido",
        description = "Permite abonar a una deuda específica. Si no se especifica monto, se abona entre 10% y 50% random. Si se especifica 'monto' en el body, se abona ese monto.",
        responses = {
            @ApiResponse(responseCode = "200", description = "Pago realizado o deuda pagada"),
            @ApiResponse(responseCode = "404", description = "Deuda no encontrada o no pendiente"),
            @ApiResponse(responseCode = "400", description = "El monto enviado no es válido")
        }
    )

    @PostMapping("/{id}/pagar")
public ResponseEntity<?> pagarDeudaPorId(@PathVariable("id") Long deudaId, @RequestBody(required = false) Map<String, Object> body, HttpServletRequest req) {
    Long usuarioId = getUsuarioId(req);

    // Permite un monto específico opcional (si se quiere abonar un valor definido, sino será random)
    Double monto = null;
    if (body != null && body.get("monto") != null) {
        try {
            monto = Double.valueOf(body.get("monto").toString());
        } catch (Exception ex) {
            return ResponseEntity.badRequest().body(Map.of("error", "El campo monto debe ser numérico"));
        }
    }

    Optional<Deuda> pagada = service.pagarDeudaPorId(usuarioId, deudaId, monto);
    if (pagada.isPresent()) {
        Map<String, Object> resp = new HashMap<>();
        resp.put("deuda_id", pagada.get().getId());
        resp.put("saldo_pendiente", pagada.get().getSaldoPendiente());
        resp.put("estado", pagada.get().getEstado());
        resp.put("mensaje", pagada.get().getEstado() == Deuda.Estado.PAGADA
            ? "¡Deuda completamente pagada!"
            : "Cuota abonada a la deuda.");
        return ResponseEntity.ok(resp);
    } else {
        return ResponseEntity.status(404).body(Map.of("error", "Deuda no encontrada o no pendiente."));
         }
    }

    private Long getUsuarioId(HttpServletRequest req) {
        Object id = req.getAttribute("usuarioId");
        if (id instanceof Integer) return ((Integer) id).longValue();
        if (id instanceof Long) return (Long) id;
        throw new RuntimeException("No se pudo obtener usuarioId desde JWT");
    }
}