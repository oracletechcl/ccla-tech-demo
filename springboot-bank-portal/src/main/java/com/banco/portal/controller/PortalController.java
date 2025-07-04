package com.banco.portal.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PortalController {

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("username", "Denny");
        model.addAttribute("saldo", "$4,200.00");
        model.addAttribute("ultimasTransacciones", new String[]{
            "Compra Supermercado -$45.00",
            "Transferencia Recibida +$1,000.00",
            "Pago Tarjeta -$300.00"
        });
        model.addAttribute("noticias", new String[]{
            "La tasa de interés se mantiene estable.",
            "Nuevo producto de inversión disponible.",
            "Horario especial durante feriados."
        });
        return "home";
    }
}
