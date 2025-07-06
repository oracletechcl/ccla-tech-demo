package cl.tech.pagarms.auth;

import org.springframework.stereotype.Component;
import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

// Simple filter that simulates extracting usuarioId from JWT
@Component
public class JwtAuthFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;
        // Simular usuarioId. Aquí iría la lógica real de JWT.
        req.setAttribute("usuarioId", 1L); // Valor fijo para pruebas
        chain.doFilter(request, response);
    }
}